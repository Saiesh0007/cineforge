import os
import subprocess


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

    return float(subprocess.check_output(cmd).decode().strip())


def extract_frames(video_path, output_dir="frames", num_frames=8):

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