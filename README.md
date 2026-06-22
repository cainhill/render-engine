# render-engine

A simple Python-based rendering engine running in Docker that automatically processes and combines one or more source videos into polished destination videos based on instruction lists (EDL files in CSV format).

## Description

This script runs inside a Docker container to trim, resize, rotate, and combine video files.

At a high-level, this script:

1. Waits for an external request to be made to http://render-engine:5000/render

2. Once received, it scans the `/data/manifest/` tree for any manifest CSV file

3. For each manifest CSV
  * Skips processing this manifest CSV, if the output video already exists and there have been no changes to the manifest CSV since the previous render
  * Otherwise, trims/resizes/rotates/saves to an intermidary `/data/cache/` folder
  * Then combines the source videos into an output video saved to the `/data/dest-videos/` path (using the same relative path and filename as the manifest CSV)

## Reason For Existing

* **Container Compatibility:** Most existing libraries are built for Node.js, TypeScript, or browser environments, whereas this project specifically required a pure Python script configured to run natively inside an isolated Docker container.

* **Minimal Scope:** Existing repositories often include bloat like complex UI layers, cross-fades, and multi-track audio mixing. This script is designed to be exceptionally dumb—doing exactly one job: parsing a CSV manifest to slice, normalise, and combine video clips sequentially.

* **Mismatched Source Handling:** Most lightweight tools crash when input files have mixed frame rates (29.9 vs 30.1 fps) or different orientations. This script embeds those specific fixes directly into a simple, single-pass pipeline.

* **Webhook Automation:** It functions as a lightweight microservice that lets you trigger individual render manifests on demand via a basic HTTP POST request, which matches automation tools like n8n perfectly.


## Resources & References

Before creating this, I reviewed these resources and alternative solutions:

* **[AMIA Open Source / ffmprovisr](https://amiaopensource.github.io/ffmprovisr/):** An invaluable repository of FFmpeg command-line scripts and logic blueprints maintained by the Association of Moving Image Archivists, designed to illustrate specific data manipulation techniques.
* **[pilotpirxie / json-to-ffmpeg](https://github.com/pilotpirxie/json-to-ffmpeg):** An experimental Node/TypeScript command-line tool that translates complex multi-track JSON video descriptions (including cross-fades and positional scaling transformations) into standard FFmpeg filtergraphs.
* **[kcsry / ffmpeg-edl](https://github.com/kcsry/ffmpeg-edl):** A Python pipeline wrapper that ingests a tab-separated value (TSV) Edit Decision List to automate segment slicing, tagging, and batch-transcoding chunks via sequential configuration scripts.