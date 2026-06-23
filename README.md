# render-engine

A script for making one or more compilation videos from source videos.


## 📌 Purpose

When triggered by webhook, this script makes slices from videos in your `/data/src-video/` path and arranges them in one or more compilation videos saved to your `/data/dest-video/` path, according to the instructions you give it using CSV in your `/data/manifest/` path.


## 💎 Features

Why make this and not use an alternative?

I needed a video compilation script that:
* ✅ Makes videos from one or more source videos
* ✅ Fixes video inconsistencies before joining
* ✅ Rotates and resizes videos
* ✅ Simplifies the underlying commands (FFmpeg)

With some more specific needs:
* ✅ Runs in a Dockerised Python environment
* ✅ Runs as non-root user
* ✅ Triggers by webhook and reports HTTP status
* ✅ Only renders a video if input is new or changed


## 🧱 Dependencies

For best results, run this script:
* Within this excellent Docker image ([eswardudi/python-ffmpeg](https://hub.docker.com/r/eswardudi/python-ffmpeg)), which provides the Python and FFmpeg needed for video automation.
* With access to the directories mentioned in the `docker-compose.yml` further down this page.


## ​​🗺️ Getting Started

Check the Installation Steps for detailed setup instructions, but this is a 

1. Create directories on the host machine
2. Copy `process_videos.py` to your `/data/app/` directory
3. Configure and run the `docker-compose.yml`
4. Update your automations to save CSV manifest files to your `/data/manifest/` tree and to trigger the webhook when it makes sense for you
5. Check the `/data/dest-videos/` path to find your automatically compiled videos


## 📦 Installation Steps

This script is designed to run exclusively within a Docker container environment pre-configured with Python and FFmpeg. 

1. Create directories on the host machine

    Using your standard non-root user (UID 1000), create the folders for app, manifests, cache, and videos on your host machine. Creating them *before* launching Docker ensures they inherit correct user permissions for the script to work as intended.

2. Copy `process_videos.py` to your `/data/app/` directory 

3. Configure and run the `docker-compose.yml`

    * Remember to replace the host paths (on the left side of the `:` symbol under the `volumes` key).

   * Importantly, keep the `:ro` attached to the `/data/src-videos` to ensure this script has read only access to your source videos. As a disclaimer, I take no responsibility for any mistakes caused by this script does outside the context of my purposes and you should have a backup-and-restore strategy for you source videos anyway.

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
          - </path/to/your/manifest/dir>:/data/manifest:ro
          - </path/to/your/source/videos>:/data/src-videos:ro
          - </path/to/your/cache/dir>:/data/cache:rw
          - </path/to/your/destination/videos>:/data/dest-videos:rw
        working_dir: /app
        command: python process_videos.py
        restart: always
    ```


## 📋 Usage

1. Name and organise your CSV manifest files

    The file name and relative subfolder path you choose for your CSV dictates the exact path and file name of the finished video. The engine automatically drops the `.csv` extension and replaces it with `.mp4` when saving to the `/data/dest-videos/` tree.
    
    * **Example Input:** `/data/manifest/holidays/bali_trip.csv`
    * **Example Output:** `/data/dest-videos/holidays/bali_trip.mp4`

2. Populate the CSV contents

    You may generate these manually or automatically, but the CSVs must look like this (including the headings):

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

3. Trigger via webhook

    The engine runs as a background service waiting for an HTTP POST request. You do not need to send any video files or manifest data in the request body, the script automatically scans your `/data/manifest/` tree and uses file modification dates to figure out new/changed CSVs that need to be rendered.

    To trigger a full scan and render, send an empty JSON POST request:

    * **Method:** `POST`
    * **URL:** `http://render-engine:5000/render`
    * **Headers:** `Content-Type: application/json`
    * **Payload:**
      ```json
      {}
      ````

4. Video compilation

    The script will keep n8n waiting until the render is complete, and return a 200 OK JSON response upon completion. You will find the final rendered videos in the `/data/dest-videos/` tree once complete.


## ⚙️ How It Works

This script runs a simple video compilation engine inside a Docker container. It stays alive as a background service and processes videos on demand.

1. **Listen:** It waits for a web request sent to `http://render-engine:5000/render`.

2. **Scan:** Once triggered, it looks inside `/data/manifest/` for your CSV manifest files.

3. **Check:** It skips any CSV file if the final video already exists and the CSV hasn't been changed since the last render.

4. **Process:** For new or updated CSVs, it trims, rotates, resizes, and saves the referenced source videos as cached clips in the `/data/cache/` folder.

5. **Combine:** It glues those cached clips together into a finished video. The final file is saved to `/data/dest-videos/` using the ***exact same name and relative subfolder structure*** as your input CSV (e.g., `/data/manifests/holidays/bali_2026.csv` becomes `/data/dest-videos/holidays/bali_2026.mp4`).


## 🔮 Future Work

* 💡 Enable multi-threading
* 💡 Enable hardware acceleration
* 💡 Enable background music additions
* 💡 Logic checks ('start_time > end_time' = error)
* 💡 Error checks (missing files)
* 💡 Rate limiting / stop overlap requests


## 🔎 Key Words

Video Compilation / FFmpeg / Python / Docker / Web Hook / n8n / EDL / Edit Decisions List


## 👍 Related Resources

Before creating this, I reviewed these resources and alternative solutions:

* [AMIA Open Source / ffmprovisr](https://amiaopensource.github.io/ffmprovisr/)
* [pilotpirxie / json-to-ffmpeg](https://github.com/pilotpirxie/json-to-ffmpeg)
* [kcsry / ffmpeg-edl](https://github.com/kcsry/ffmpeg-edl)


## 🎨 License

Usage is provided under the MIT License. See LICENSE for the full details.