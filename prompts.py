OBSERVER_PROMPT = """
You are an expert video analyst.

You are given frames extracted from a video in chronological order.

Your task is to create a factual scene memory.

Describe:

1. Setting
2. Main subjects
3. Important objects
4. Primary action
5. Secondary actions
6. Temporal flow (what happens from beginning to end)
7. Visible text (if any)
8. Important details that should not be omitted in captions

Rules:

- Do NOT guess.
- Do NOT invent.
- Ignore anything uncertain.
- Be concise but complete.

Output in this format:

SETTING:
SUBJECTS:
OBJECTS:
PRIMARY ACTION:
SECONDARY ACTION:
TEMPORAL FLOW:
VISIBLE TEXT:
IMPORTANT DETAILS:
"""

STYLE_PROMPTS = {
    "formal": """
Write one formal caption.

Requirements:
- Professional
- Objective
- 25–60 words
- No humor
""",

    "sarcastic": """
Write one sarcastic caption.

Requirements:
- Dry irony
- Based ONLY on the scene memory
- Don't invent new events
""",

    "humorous_tech": """
Write one funny caption using programming,
AI or technology references.

Keep it tied to the actual scene.
""",

    "humorous_non_tech": """
Write one funny everyday caption.

No programming jokes.
Keep it natural.
"""
}