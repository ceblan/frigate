---
id: ha_network_storage
title: Home Assistant network storage
---

As of Home Assistant 2023.6, Network Mounted Storage is supported for Apps.

## Setting Up Remote Storage For BIS-IA

### Prerequisites

- Home Assistant 2023.6 or newer is installed
- Running Home Assistant Operating System 10.2 or newer OR Running Supervised with latest os-agent installed (this is required for supervised install)

### Initial Setup

1. Stop the BIS-IA App

### Move current data

Keeping the current data is optional, but the data will need to be moved regardless so the share can be created successfully.

#### If you want to keep the current data

1. Move the bisia.db, bisia.db-shm, bisia.db-wal files to the /config directory
2. Rename the /media/bisia folder to /media/bisia_tmp

#### If you don't want to keep the current data

1. Delete the /media/bisia folder and all of its contents

### Create the media share

1. Go to **Settings -> System -> Storage -> Add Network Storage**
2. Name the share `bisia` (this is required)
3. Choose type `media`
4. Fill out the additional required info for your particular NAS
5. Connect
6. Move files from `/media/bisia_tmp` to `/media/bisia` if they were kept in previous step
7. Start the BIS-IA App
