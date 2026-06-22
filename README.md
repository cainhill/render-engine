# render-engine

A simple Python-based rendering engine running in Docker that automatically processes and combines one or more source videos into polished destination videos based on instruction lists (EDL files in CSV format).

## Description

This script runs inside a Docker container to trim, resize, rotate, and combine video files.

At a high-level, this script:

1. Waits for an external request to be made to http://render-engine:5000/render

2. Once received, it scans the `/data/manifest/` tree for any manifest CSV file

3. For each manifest CSV

    1. Skips processing this manifest CSV, if the destination video already exists and there have been no changes to the manifest CSV since the previous render

    2. Otherwise, trims/resizes/rotates/saves to an intermidary `/data/cache/` folder

    3. Then combines the source videos into an output video saved to the `/data/dest-videos/` path (using the same relative path and filename as the manifest CSV)

## Reason for existing

* I needed a programatic video rendering solution
* Written in Python with minimal dependencies
* That could produce many-to-many videos
* Based on one or more manifest CSV inputs
* That could run within a Docker container
* That could handle source videos in different formats
* That n8n could trigger by webhook

## Resources & References

Before creating this, I reviewed these resources and alternative solutions:

* **[AMIA Open Source / ffmprovisr](https://amiaopensource.github.io/ffmprovisr/):** An invaluable repository of FFmpeg command-line scripts and logic blueprints maintained by the Association of Moving Image Archivists, designed to illustrate specific data manipulation techniques.
* **[pilotpirxie / json-to-ffmpeg](https://github.com/pilotpirxie/json-to-ffmpeg):** An experimental Node/TypeScript command-line tool that translates complex multi-track JSON video descriptions (including cross-fades and positional scaling transformations) into standard FFmpeg filtergraphs.
* **[kcsry / ffmpeg-edl](https://github.com/kcsry/ffmpeg-edl):** A Python pipeline wrapper that ingests a tab-separated value (TSV) Edit Decision List to automate segment slicing, tagging, and batch-transcoding chunks via sequential configuration scripts.