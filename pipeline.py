import json
import shutil
import tempfile

from llm import ask_gemma
from prompts import ALL_CAPTIONS_PROMPT
from video import extract_frames


def generate_all_captions(frame_paths):
    response = ask_gemma(
        ALL_CAPTIONS_PROMPT,
        image_paths=frame_paths,
        max_tokens=220,
    )

    print("\n========== RAW MODEL RESPONSE ==========")
    print(response)
    print("========================================\n")

    # Remove markdown code fences if the model returns them
    response = response.strip()

    if response.startswith("```json"):
        response = response.replace("```json", "", 1)

    if response.startswith("```"):
        response = response.replace("```", "", 1)

    if response.endswith("```"):
        response = response[:-3]

    response = response.strip()

    try:
        captions = json.loads(response)

    except json.JSONDecodeError as e:
        print("\n❌ Invalid JSON returned by model:")
        print(response)
        raise Exception(f"Invalid JSON: {e}")

    required = {
        "formal",
        "sarcastic",
        "humorous_tech",
        "humorous_non_tech",
    }

    missing = required - captions.keys()

    if missing:
        raise Exception(
            f"Missing required captions: {missing}"
        )

    return captions


def process_video(video_path):
    temp_dir = tempfile.mkdtemp(prefix="cineforge_")

    try:

        frame_paths = extract_frames(
            video_path,
            output_dir=temp_dir,
            num_frames=2,
        )

        captions = generate_all_captions(frame_paths)

        return captions

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)