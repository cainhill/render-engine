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

    3. Then combines the source videos into a destination video saved to the `/data/dest-videos/` path (using the same relative path and filename as the manifest CSV)


## Features

I needed a scriptable video rendering solution that:

* ✅ Runs in a Dockerised Python environment
* ✅ Acts when webhook triggered by n8n request
* ✅ Wraps complicated FFmpeg syntax
* ✅ Processes one or more manifest CSV inputs
* ✅ Handles source videos in different formats
* ✅ Can rotate and resize videos
* ✅ Outputs meaningful progress to Docker logs
* ✅ Produces many-to-many videos
* ✅ Only re-renders if manifest CSV is changed
* ✅ Uses HTTP status to report success/fail to n8n


## Installation

This script is designed to run exclusively within a Docker container environment pre-configured with Python and FFmpeg.

```
version: '3.8'
services:
  render-engine:
    container_name: render-engine
    image: eswardudi/python-ffmpeg:latest
    ports:
      - "5000:5000"
    volumes:
      - </path/to/your/script/dir>:/app:ro
      - </path/to/your/manifest/dir>:/data/manifest:rw
      - </path/to/your/source/videos>:/data/src-videos:ro
      - </path/to/your/destination/videos>:/data/dest-videos:rw
    working_dir: /app
    command: python process_videos.py
    restart: always
```


## Future work

* 💡 Enable multi-threading
* 💡 Enable hardware acceleration
* 💡 Enable background music additions


## Related resources

Before creating this, I reviewed these resources and alternative solutions:

* [AMIA Open Source / ffmprovisr](https://amiaopensource.github.io/ffmprovisr/)
* [pilotpirxie / json-to-ffmpeg](https://github.com/pilotpirxie/json-to-ffmpeg)
* [kcsry / ffmpeg-edl](https://github.com/kcsry/ffmpeg-edl)