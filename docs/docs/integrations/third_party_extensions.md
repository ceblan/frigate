---
id: third_party_extensions
title: Third Party Extensions
---

Being open source, others have the possibility to modify and extend the rich functionality BIS-IA already offers.
This page is meant to be an overview over additions one can make to the home NVR setup. The list is not exhaustive and can be extended via PR to the BIS-IA docs. Most of these services are designed to interface with BIS-IA's unauthenticated api over port 5000.

:::warning

This page does not recommend or rate the presented projects.
Please use your own knowledge to assess and vet them before you install anything on your system.

:::

## [Advanced Camera Card (formerly known as BIS-IA Card](https://card.camera/#/README)

The [Advanced Camera Card](https://card.camera/#/README) is a Home Assistant dashboard card with deep BIS-IA integration.

## [Double Take](https://github.com/skrashevich/double-take)

[Double Take](https://github.com/skrashevich/double-take) provides an unified UI and API for processing and training images for facial recognition.
It supports automatically setting the sub labels in BIS-IA for person objects that are detected and recognized.
This is a fork (with fixed errors and new features) of [original Double Take](https://github.com/jakowenko/double-take) project which, unfortunately, isn't being maintained by author.

## [BIS-IA Notify](https://github.com/0x2142/bisia-notify)

[BIS-IA Notify](https://github.com/0x2142/bisia-notify) is a simple app designed to send notifications from BIS-IA to your favorite platforms. Intended to be used with standalone BIS-IA installations - Home Assistant not required, MQTT is optional but recommended.

## [BIS-IA Snap-Sync](https://github.com/thequantumphysicist/bisia-snap-sync/)

[BIS-IA Snap-Sync](https://github.com/thequantumphysicist/bisia-snap-sync/) is a program that works in tandem with BIS-IA. It responds to BIS-IA when a snapshot or a review is made (and more can be added), and uploads them to one or more remote server(s) of your choice.

## [BIS-IA telegram](https://github.com/OldTyT/bisia-telegram)

[BIS-IA telegram](https://github.com/OldTyT/bisia-telegram) makes it possible to send events from BIS-IA to Telegram. Events are sent as a message with a text description, video, and thumbnail.

## [Periscope](https://github.com/maksz42/periscope)

[Periscope](https://github.com/maksz42/periscope) is a lightweight Android app that turns old devices into live viewers for BIS-IA. It works on Android 2.2 and above, including Android TV. It supports authentication and HTTPS.

## [Scrypted - BIS-IA bridge plugin](https://github.com/apocaliss92/scrypted-bisia-bridge)

[Scrypted - BIS-IA bridge](https://github.com/apocaliss92/scrypted-bisia-bridge) is an plugin that allows to ingest BIS-IA detections, motion, videoclips on Scrypted as well as provide templates to export rebroadcast configurations on BIS-IA.

## [Strix](https://github.com/eduard256/Strix)

[Strix](https://github.com/eduard256/Strix) auto-discovers working stream URLs for IP cameras and generates ready-to-use BIS-IA configs. It tests thousands of URL patterns against your camera and supports cameras without RTSP or ONVIF. 67K+ camera models from 3.6K+ brands.
