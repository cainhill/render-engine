# render-engine

A simple Python-based rendering engine running in Docker that automatically processes and combines one or more source videos into polished destination videos based on instruction lists (CSV manifest files).

## How It Works

This script runs a simple video editing engine inside a Docker container. It stays alive as a background service and processes videos on demand.

1. **Listen:** It waits for a web request sent to `http://render-engine:5000/render`.
2. **Scan:** Once triggered, it looks inside `/data/manifest/` for your CSV manifest files.
3. **Check:** It skips any CSV file if the final video already exists and the CSV hasn't been changed since the last render.
4. **Process:** For new or updated CSVs, it trims, rotates, resizes, and saves the source videos as cached clips in the `/data/cache/` folder.
5. **Combine:** It glues those cached clips together into a finished video, saving it to `/data/dest-videos/` using the exact same name as your CSV.

## Features

I needed a scriptable video rendering solution that:

* ✅ Runs in a Dockerised Python environment
* ✅ Run as non-root user for 'least privilege' policy
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

    Place your CSV manifest files inside the mapped `/data/manifest` path. The CSVs must look like this (including the headings):

    ```
    source,start_time,end_time,rotation
    a.mp4,0.328,4.275,0
    b.mp4,10.374,15.593,90
    c.mp4,0,8.5,180
    d.mp4,22,30,270
    ```
    * **source:** The file path of the video relative to the `/data/src-videos/` directory (e.g., if you list `a.mp4` in the CSV, the script will source `/data/src-videos/a.mp4` for processing).
    * **start_time / end_time:** Cut boundaries in seconds. Aim for a maximum of 3 decimal places (e.g., `15.593` for millisecond-precision cuts). While the script can read longer numbers without crashing, FFmpeg only really uses 3 decimal places for calculating the nearest video frame.
    * **rotation:** May only be set to one of 0, 90, 180, 270. 0 (no change), 90 (clockwise), 180 (upside down), and 270 (counter-clockwise).

## Installation

This script is designed to run exclusively within a Docker container environment pre-configured with Python and FFmpeg.

1. Set up the `docker-compose.yml`

    ```
    version: '3.8'
    services:
      render-engine:
        container_name: render-engine
        image: eswardudi/python-ffmpeg:latest
        user: "1000:1000"
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
* 💡 Error checking ('start_time > end_time')


## Related resources

Before creating this, I reviewed these resources and alternative solutions:

* [AMIA Open Source / ffmprovisr](https://amiaopensource.github.io/ffmprovisr/)
* [pilotpirxie / json-to-ffmpeg](https://github.com/pilotpirxie/json-to-ffmpeg)
* [kcsry / ffmpeg-edl](https://github.com/kcsry/ffmpeg-edl)