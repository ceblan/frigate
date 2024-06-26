"""Export recordings to storage."""

import pdb
import datetime
import logging
import os
import subprocess as sp
import threading
from enum import Enum
from pathlib import Path

from frigate.config import FrigateConfig
from frigate.const import EXPORT_DIR, MAX_PLAYLIST_SECONDS
from frigate.ffmpeg_presets import (
    EncodeTypeEnum,
    parse_preset_hardware_acceleration_encode,
)
from frigate.models import Recordings

logger = logging.getLogger(__name__)


TIMELAPSE_DATA_INPUT_ARGS = "-an -skip_frame nokey"


def lower_priority():
    os.nice(10)


class PlaybackFactorEnum(str, Enum):
    realtime = "realtime"
    timelapse_25x = "timelapse_25x"

# aqui tb ha chicha
class RecordingExporter(threading.Thread):
    """Exports a specific set of recordings for a camera to storage as a single file."""

    def __init__(
        self,
        config: FrigateConfig,
        camera: str,
        start_time: int,
        end_time: int,
        playback_factor: PlaybackFactorEnum,
        min_start_time: int,
        max_end_time: int,
        duration: int,
    ) -> None:
        threading.Thread.__init__(self)
        self.config = config
        self.camera = camera
        self.start_time = start_time
        self.end_time = end_time
        self.playback_factor = playback_factor
        self.min_start_time = min_start_time
        self.max_end_time = max_end_time
        self.duration = duration

    def get_datetime_from_timestamp(self, timestamp: int) -> str:
        """Convenience fun to get a simple date time from timestamp."""
        return datetime.datetime.fromtimestamp(timestamp).strftime("%Y_%m_%d_%H_%M")

    def run(self) -> None:
        logger.debug(
            f"Beginning export for {self.camera} from {self.start_time} to {self.end_time}"
        )
        file_name = f"{EXPORT_DIR}/in_progress.{self.camera}@{self.get_datetime_from_timestamp(self.start_time)}__{self.get_datetime_from_timestamp(self.end_time)}.mp4"
        final_file_name = f"{EXPORT_DIR}/{self.camera}_{self.get_datetime_from_timestamp(self.start_time)}__{self.get_datetime_from_timestamp(self.end_time)}.mp4"

        if not os.path.exists(final_file_name): # si no existe la creamos

            if (self.end_time - self.start_time) <= MAX_PLAYLIST_SECONDS:
                playlist_lines = f"http://127.0.0.1:5000/vod/{self.camera}/start/{self.start_time}/end/{self.end_time}/index.m3u8"
                ffmpeg_input = (
                    f"-y -protocol_whitelist pipe,file,http,tcp -i {playlist_lines}"
                )

                logger.debug(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                for line in playlist_lines:
                    logger.debug(f"Playlist Line (Long Duration): {line}")

            else:
                playlist_lines = []

                # get full set of recordings
                export_recordings = (
                    Recordings.select()
                    .where(
                        Recordings.start_time.between(self.start_time, self.end_time)
                        | Recordings.end_time.between(self.start_time, self.end_time)
                        | (
                            (self.start_time > Recordings.start_time)
                            & (self.end_time < Recordings.end_time)
                        )
                    )
                    .where(Recordings.camera == self.camera)
                    .order_by(Recordings.start_time.asc())
                )

                # Use pagination to process records in chunks
                page_size = 1000
                num_pages = (export_recordings.count() + page_size - 1) // page_size

                for page in range(1, num_pages + 1):
                    playlist = export_recordings.paginate(page, page_size)
                    playlist_lines.append(
                        f"file 'http://127.0.0.1:5000/vod/{self.camera}/start/{float(playlist[0].start_time)}/end/{float(playlist[-1].end_time)}/index.m3u8'"
                    )

                logger.debug(f"?????????????????????????????????????????????")
                for line in playlist_lines:
                    logger.debug(f"Playlist Line (Long Duration): {line}")

                ffmpeg_input = "-y -protocol_whitelist pipe,file,http,tcp -f concat -safe 0 -i /dev/stdin"

            if self.playback_factor == PlaybackFactorEnum.realtime:
                ffmpeg_cmd = (
                    f"ffmpeg -hide_banner {ffmpeg_input} -c copy {file_name}"
                ).split(" ")
            elif self.playback_factor == PlaybackFactorEnum.timelapse_25x:
                ffmpeg_cmd = (
                    parse_preset_hardware_acceleration_encode(
                        self.config.ffmpeg.hwaccel_args,
                        f"{TIMELAPSE_DATA_INPUT_ARGS} {ffmpeg_input}",
                        f"{self.config.cameras[self.camera].record.export.timelapse_args} {file_name}",
                        EncodeTypeEnum.timelapse,
                    )
                ).split(" ")

            p = sp.run(
                ffmpeg_cmd,
                input="\n".join(playlist_lines),
                encoding="ascii",
                preexec_fn=lower_priority,
                capture_output=True,
            )

            if p.returncode != 0:
                logger.error(
                    f"Failed to export recording for command {' '.join(ffmpeg_cmd)}"
                )
                logger.error(p.stderr)
                Path(file_name).unlink(missing_ok=True)
                return


            logger.debug(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            cut_ffmpeg_cmd = (
                f"ffmpeg -hide_banner -ss {abs(self.start_time - self.min_start_time)} -i {file_name} -to {self.duration/1000 - abs(self.end_time - self.max_end_time)} -c copy {final_file_name}").split(" ")

            # pdb.set_trace()
            logger.debug(f"******** cut_ffmpeg: {cut_ffmpeg_cmd}")


            r = sp.run(
                cut_ffmpeg_cmd,
                input= "",
                encoding="ascii",
                preexec_fn=lower_priority,
                capture_output=True,
            )

            if r.returncode != 0:
                logger.error(
                    f"Failed to cut recording for command {' '.join(cut_ffmpeg_cmd)}"
                )
                logger.error(p.stderr)
                Path(final_file_name).unlink(missing_ok=True)
                return

            logger.debug(f"Updating finalized export {file_name}")
            # os.rename(file_name, final_file_name)
            Path(file_name).unlink(missing_ok=True)
            logger.debug(f"Finished exporting {final_file_name}")

        else: # si ya existe nos vamos

            logger.debug(f"File already exists {final_file_name}")
