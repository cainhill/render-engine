# render-engine

A simple Python-based rendering engine running in Docker that automatically processes and combines one or more source videos into polished destination videos based on instruction lists (CSV manifest files).

## Description

This script runs inside a Docker container to trim, resize, rotate, and combine video files.

At a high-level, this script:

1. Waits for an external request to be made to http://render-engine:5000/render

2. Once received, it scans the `/data/manifest/` tree for any CSV manifest file

3. For each CSV

    1. Skips processing this CSV, if the destination video already exists and there have been no changes to the CSV since the previous render

    2. Otherwise, trims/rotates/resizes the source video into a temporary clip saved to the `/data/cache/` folder

    3. Then combines the cached clips into a destination video saved to the `/data/dest-videos/` path (using the same relative path and filename as the manifest CSV)


## Features

I needed a scriptable video rendering solution that:

* ✅ Runs in a Dockerised Python environment
* ✅ Triggers by n8n request
* ✅ Wraps complicated FFmpeg syntax
* ✅ Processes one or more manifest CSV inputs
* ✅ Handles source videos in different formats
* ✅ Rotates and resizes videos
* ✅ Outputs meaningful progress to Docker logs
* ✅ Produces many-to-many videos
* ✅ Only renders for new or changed manifest CSVs
* ✅ Uses HTTP status to report success/fail to n8n

## Usage

1. Organise your manifests

    Place your CSV manifest files inside the mapped `/data/manifest` path. The CSVs must include headers matching this schema:

    ```
    source,start_time,end_time,rotation
    a.mp4,0.3,4.0,0
    b.mp4,10,15.5,90
    c.mp4,0,8.5,180
    d.mp4,22,30,270
    ```

* **source:** The file name of the video located inside the `/data/src-videos/` directory.

* **start_time:** Cut boundaries in seconds.

* **end_time:** Cut boundaries in seconds.

* **rotation:** May only be set to one of: 0 (no change), 90 (clockwise), 180 (upside down), and 270 (counter-clockwise).

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