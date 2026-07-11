import os
import subprocess
import tempfile

import yt_dlp


def download_video(url):
    os.makedirs("videos", exist_ok=True)

    output_template = os.path.join(
        tempfile.gettempdir(),
        "%(id)s.%(ext)s",
    )

    ydl_opts = {
        "format": "mp4[height<=720]/best[height<=720]/best",
        "outtmpl": output_template,
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,

        # Faster failure
        "retries": 1,
        "fragment_retries": 1,
        "socket_timeout": 15,

        # Generic browser headers
        "http_headers": {
            "User-Agent": (
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/138.0 Safari/537.36"
            )
        },
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(
                url,
                download=True,
            )

            return ydl.prepare_filename(info)

    except Exception as e:
        raise RuntimeError(f"Video download failed: {e}")


def get_duration(video_path):
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        video_path,
    ]

    return float(
        subprocess.check_output(cmd).decode().strip()
    )


def extract_frames(
    video_path,
    output_dir="frames",
    num_frames=2,
):
    os.makedirs(output_dir, exist_ok=True)

    duration = get_duration(video_path)

    padding = duration * 0.05

    frame_paths = []

    for i in range(num_frames):

        timestamp = padding + (
            i * (duration - 2 * padding)
            / max(1, num_frames - 1)
        )

        filename = os.path.join(
            output_dir,
            f"frame_{i:02d}.jpg",
        )

        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-ss",
                str(timestamp),
                "-i",
                video_path,
                "-frames:v",
                "1",
                "-q:v",
                "2",
                filename,
                "-loglevel",
                "error",
            ],
            check=True,
        )

        frame_paths.append(filename)

    return frame_paths