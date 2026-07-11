from llm import ask_gemma
from prompts import OBSERVER_PROMPT, ALL_CAPTIONS_PROMPT


def build_scene_memory(frame_paths):
    return ask_gemma(
        OBSERVER_PROMPT,
        image_paths=frame_paths,
        max_tokens=500,
    )


def generate_all_captions(frame_paths):

    scene_memory = build_scene_memory(frame_paths[:2])

    prompt = ALL_CAPTIONS_PROMPT.format(
        scene_memory=scene_memory
    )

    response = ask_gemma(
        prompt,
        max_tokens=500,
    )

    captions = {}

    current = None

    for line in response.splitlines():

        line = line.strip()

        if line.startswith("FORMAL:"):
            current = "formal"
            captions[current] = line.replace("FORMAL:", "").strip()

        elif line.startswith("SARCASTIC:"):
            current = "sarcastic"
            captions[current] = line.replace("SARCASTIC:", "").strip()

        elif line.startswith("TECH:"):
            current = "humorous_tech"
            captions[current] = line.replace("TECH:", "").strip()

        elif line.startswith("CASUAL:"):
            current = "humorous_non_tech"
            captions[current] = line.replace("CASUAL:", "").strip()

        elif current:
            captions[current] += " " + line

    return scene_memory, captions