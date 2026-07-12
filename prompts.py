import json

STYLE_GUIDE = {
    "formal": (
        "Professional, objective, factual tone, like a news-agency or stock-footage caption. "
        "One clear declarative sentence stating what the video shows. "
        "No slang, no humour, no exclamation marks, no opinions."
    ),
    "sarcastic": (
        "Dry, deadpan, ironic, lightly mocking. Use understatement, mock admiration, or "
        "faint praise aimed at something actually visible in the clip. "
        "One sentence. Subtle wit, not mean-spirited or absurd."
    ),
    "humorous_tech": (
        "Genuinely funny, built on a technology or programming joke (e.g. bugs, deploys, "
        "merge conflicts, CPUs, Wi-Fi, AI, loading screens) mapped onto what is literally "
        "happening in the clip. One to two sentences. The scene must still be recognisable "
        "from the caption."
    ),
    "humorous_non_tech": (
        "Genuinely funny, warm, relatable everyday humour that anyone would get. "
        "Absolutely NO technology, programming, internet, or science references. "
        "One to two sentences about everyday life, feelings, food, weather, work, etc., "
        "grounded in what the clip shows."
    ),
}

PERSONAS = {
    "formal": (
        "You are a senior news-agency caption writer. Your captions are precise, "
        "objective, single-sentence, publishable as-is."
    ),
    "sarcastic": (
        "You are a dry, deadpan comedy writer known for ironic, mock-admiring "
        "one-liners. Your sarcasm is unmistakable but never mean."
    ),
    "humorous_tech": (
        "You are a comedy writer for a developer audience. Your jokes map bugs, "
        "deploys, CPUs, Wi-Fi and AI onto everyday scenes, and they actually land."
    ),
    "humorous_non_tech": (
        "You are a warm observational comedian. Your jokes are about everyday life - "
        "food, moods, weather, work - and never mention technology or science."
    ),
}

CAPTION_EXEMPLARS = {
    "sarcastic": [
        "Ah yes, dozens of giant balloons expensively drifting wherever the wind feels like taking them, truly humanity's boldest answer to a question nobody asked.",
        "Wow, a man hitting hot metal with a hammer over and over until it becomes slightly flatter hot metal, riveting stuff from the cutting edge of the year 1400.",
    ],
    "humorous_tech": [
        "Sunrise rollout: fifty hot-air balloons spinning up over the valley like autoscaled pods, and impressively not a single one crashed on launch.",
        "This blacksmith is just debugging hardware with a hammer: heat the metal, whack it, inspect the output, repeat until the sword finally compiles.",
    ],
    "humorous_non_tech": [
        "Fifty balloons drifting over the river at sunrise, all pretending they know where they're going, just like the rest of us before breakfast.",
        "A man with the arm strength of three gym memberships keeps whacking that glowing metal like it owes him money, and the sparks clearly agree.",
    ],
}

DISCIPLINE = (
    "GROUNDING DISCIPLINE (the judge penalizes any invented detail):\n"
    "- Use ONLY what the frames/FACTS show. Never invent actions the subject is not clearly doing.\n"
    "- Use the observed setting EXACTLY. Do not rename it unless that is what is shown.\n"
    "- If a location, brand, city, org, or sign is not clearly readable, stay generic.\n"
    "- Never mention missing audio, playback speed, frames, filters, or video/encoding artifacts.\n"
    "- Never invent dialogue or intentions."
)

DESCRIBE_FACTS_PROMPT = (
    "You are shown {n} frames sampled evenly, in chronological order, from a single video clip "
    "(roughly 30 seconds to 2 minutes long). Respond with a single JSON object with two fields:\n\n"
    "- \"description\": a factual, neutral description of the clip — the setting and time of "
    "day, the main subject(s), what they are doing, how the action progresses across the "
    "frames, and any distinctive visual details (colours, weather, objects, visible text, "
    "camera angle or motion). 4-6 sentences.\n"
    "- \"facts\": a list of 5-10 short, independently-checkable claims about what is literally "
    "visible in the frames (specific objects, colours, actions, setting details, on-screen "
    "text). Each fact should be concrete enough that someone looking only at the frames could "
    "verify it. Order the facts from most visually prominent and persistent (the main subject "
    "and its central action, visible across many frames) to least (background or single-frame "
    "details), and only state a colour of a background element if it is unambiguous.\n\n"
    "Describe only what is clearly visible in the frames; do not speculate or invent details. "
    "Do not identify a city, country, company, building, or sign text unless it is large, "
    "legible, and unambiguous in the sampled frames.\n\n"
    + DISCIPLINE
)

CANDIDATE_SCHEMA = {
    "type": "object",
    "properties": {"a": {"type": "string"}, "b": {"type": "string"}},
    "required": ["a", "b"],
    "additionalProperties": False,
}

def facts_schema() -> dict:
    return {
        "type": "object",
        "properties": {
            "description": {"type": "string"},
            "facts": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["description", "facts"],
        "additionalProperties": False,
    }

def specialist_prompt(style: str, description: str, facts: list, prior_captions: list = None) -> str:
    exemplars = CAPTION_EXEMPLARS.get(style, [])
    ex_block = ""
    if exemplars:
        ex_lines = "\n".join(f'- "{e}"' for e in exemplars)
        ex_block = (
            "\nExamples of the tone sharpness expected, from OTHER videos (a balloon "
            "festival, a blacksmith) - match their quality, never reuse their "
            f"subjects or jokes:\n{ex_lines}\n"
        )
    facts_block = "\n".join(f"- {f}" for f in facts) if facts else "(none extracted)"
    
    variety_note = ""
    if prior_captions:
        variety_note = (
            "\nCaptions already written for this clip in other styles. "
            "Use a different sentence structure and comedic angle: "
            + " | ".join(prior_captions) + "\n\n"
        )

    return (
        f"{PERSONAS[style]}\n\n"
        "Here is a factual description of a video clip:\n\n"
        f"{description}\n\n"
        "Concrete facts noticed in the frames:\n"
        f"{facts_block}\n\n"
        f'Write TWO different candidate captions for this video in the "{style}" '
        f"style: {STYLE_GUIDE[style]}\n"
        f"{ex_block}\n"
        f"{DISCIPLINE}\n\n"
        f"{variety_note}"
        "The two candidates must take clearly different angles (different detail "
        "focused on, or a different joke/framing). Each caption will be scored by a "
        "judge who watches the video: 1-5 for accuracy (every claim visibly true) and "
        "1-5 for tone fit (the style must be unmistakable, not mild). Write to earn "
        "5/5 on both. Anchor the caption on the MAIN subject and its central action — "
        "the first facts in the list — not on background or peripheral details: a "
        "strict judge marks down any claim about background colours, object counts, "
        "small text, or things visible only for a moment, so a joke built on a shaky "
        "peripheral detail loses points that a joke built on the main action keeps. "
        "Each candidate must be consistent with at least one fact from "
        "the list above and must not contradict the description, be 1-2 sentences, "
        "in English. Never mention frames, images, descriptions, or video analysis. "
        "Avoid named places, brands, or sign text unless the description says they "
        "are unmistakably legible. Respond with only a JSON object with keys \"a\" "
        "and \"b\"."
    )

def selection_prompt(description: str, facts: list, candidates: dict) -> str:
    cand_block = json.dumps(candidates, indent=2)
    facts_block = "\n".join(f"- {f}" for f in facts) if facts else "(none extracted)"
    return (
        "Above are frames sampled evenly, in chronological order, from a video clip. "
        "Here is a factual description of the clip:\n\n"
        f"{description}\n\n"
        "Concrete facts noticed in the frames:\n"
        f"{facts_block}\n\n"
        "For each caption style below there are two candidate captions, \"a\" and "
        f"\"b\":\n\n{cand_block}\n\n"
        "The frames are ground truth. For EACH style, choose the candidate that (1) is "
        "more accurate - every claim visibly true in the frames and consistent with "
        "the facts above - and (2) has the more unmistakable, sharper execution of "
        "its style. Accuracy outranks flash: a funnier caption containing even one "
        "claim a strict judge could not verify from the frames (a background colour, "
        "a count, a fleeting detail) loses to a slightly plainer one whose every "
        "claim is checkable. Return the chosen caption TEXT exactly as written, one "
        "per style, in a JSON object keyed by style name. Do not rewrite, merge, or "
        "edit the captions; copy the winner verbatim."
    )

def audit_schema() -> dict:
    return {
        "type": "object",
        "properties": {
            "caption": {"type": "string"}
        },
        "required": ["caption"],
        "additionalProperties": False,
    }

def audit_prompt(style: str, description: str, facts: list, caption: str) -> str:
    facts_block = "\n".join(f"- {f}" for f in facts) if facts else "(none extracted)"
    return (
        "You are a strict caption quality controller. Below is a factual description and a "
        "list of facts about a video clip, followed by a candidate caption.\n\n"
        "Factual description:\n"
        f"{description}\n\n"
        "Concrete facts:\n"
        f"{facts_block}\n\n"
        f"Candidate caption (style: {style}):\n"
        f"{caption}\n\n"
        "Task:\n"
        "1. Check if the caption contains ANY hallucinated detail, action, named entity, or location "
        "not explicitly supported by the facts/description.\n"
        "2. Check if the caption mentions video artifacts, frames, or missing audio.\n"
        "If it passes, return the caption unchanged. If it fails, rewrite it minimally to pass "
        "while maintaining the style. Return a JSON object with key 'caption'."
    )