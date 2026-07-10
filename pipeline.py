from llm import ask_gemma
from prompts import OBSERVER_PROMPT, STYLE_PROMPTS


def build_scene_memory(frame_paths):

    return ask_gemma(
        OBSERVER_PROMPT,
        image_paths=frame_paths,
        max_tokens=700,
    )


def generate_caption(scene_memory, style):

    prompt = f"""
Scene Memory:

{scene_memory}

{STYLE_PROMPTS[style]}

Return ONLY the caption.
"""

    return ask_gemma(prompt)


def generate_all_captions(frame_paths):

    scene_memory = build_scene_memory(frame_paths[:2])

    captions = {}

    for style in STYLE_PROMPTS:
        captions[style] = generate_caption(
            scene_memory,
            style,
        )

    return scene_memory, captions