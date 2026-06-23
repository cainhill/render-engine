import os
import csv
import subprocess
from pathlib import Path

MANIFEST_DIR = "/data/manifest"
OUTPUT_DIR = "/data/dest-videos"
SRC_DIR = "/data/src-videos"

TARGET_WIDTH = 1280
TARGET_HEIGHT = 720


def ffmpeg_filter(rotation: int):
    """
    Returns ffmpeg filter string for rotation + scaling.
    """
    base = []

    # Rotation handling
    if rotation == 90:
        base.append("transpose=1")
    elif rotation == 180:
        base.append("hflip,vflip")
    elif rotation == 270:
        base.append("transpose=2")

    # Normalise to 720p with padding, force square pixels, and enforce strict 30 fps
    base.append(
        f"scale={TARGET_WIDTH}:{TARGET_HEIGHT}:force_original_aspect_ratio=decrease,"
        f"pad={TARGET_WIDTH}:{TARGET_HEIGHT}:(ow-iw)/2:(oh-ih)/2,"
        f"setsar=1,"
        f"fps=30"
    )

    return ",".join(base)


def parse_manifest(path):
    clips = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            clips.append(row)
    return clips


def build_concat_list(clips, temp_dir):
    """
    Creates trimmed + processed clips and returns concat file list.
    """
    concat_file = os.path.join(temp_dir, "concat.txt")

    with open(concat_file, "w") as f:
        for i, clip in enumerate(clips):
            src = os.path.join(SRC_DIR, clip["source"])
            start = float(clip["start_time"])
            end = float(clip["end_time"])
            rotation = int(clip.get("rotation", 0))

            out_clip = os.path.join(temp_dir, f"clip_{i}.mp4")

            vf = ffmpeg_filter(rotation)

            # Placed -ss and -to BEFORE -i to fix timeline tracking bugs.
            # Added uniform audio parameters (-ar and -ac) to avoid concat alignment issues.
            cmd = [
                "ffmpeg",
                "-y",
                "-ss", str(start),
                "-to", str(end),
                "-i", src,
                "-vf", vf,
                "-c:v", "libx264",
                "-preset", "veryfast",
                "-crf", "23",
                "-c:a", "aac",
                "-ar", "44100",
                "-ac", "2",
                "-movflags", "+faststart",
                out_clip
            ]

            subprocess.run(cmd, check=True)

            f.write(f"file '{out_clip}'\n")

    return concat_file


def render_video(concat_file, output_path):
    with open(concat_file) as f:
        print("Concat map configuration:")
        print(f.read())
    
    # Utilizing safe 0 to allow absolute paths in the temp directory file list
    cmd = [
        "ffmpeg",
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_file,
        "-map", "0:v",
        "-map", "0:a?",
        "-c:v", "libx264",
        "-c:a", "aac",
        output_path
    ]

    subprocess.run(cmd, check=True)


def should_render(manifest_path, output_path):
    if not os.path.exists(output_path):
        return True

    return os.path.getmtime(manifest_path) > os.path.getmtime(output_path)


def process_manifest(manifest_path):
    rel_path = os.path.relpath(manifest_path, MANIFEST_DIR)
    output_path = os.path.join(
        OUTPUT_DIR,
        rel_path.replace(".csv", ".mp4")
    )

    if not should_render(manifest_path, output_path):
        print(f"Skipping: {output_path}")
        return

    print(f"Rendering: {output_path}")

    clips = parse_manifest(manifest_path)

    temp_dir = os.path.join("/tmp", os.path.basename(manifest_path))
    os.makedirs(temp_dir, exist_ok=True)

    concat_file = build_concat_list(clips, temp_dir)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    render_video(concat_file, output_path)

    print(f"Done: {output_path}")


def main():
    for root, _, files in os.walk(MANIFEST_DIR):
        for file in files:
            if file.endswith(".csv"):
                manifest_path = os.path.join(root, file)
                process_manifest(manifest_path)


if __name__ == "__main__":
    main()