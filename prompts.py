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

ALL_CAPTIONS_PROMPT = """
You are an expert caption writer.

Using the scene memory below, generate FOUR captions.

Scene Memory:

{scene_memory}

Requirements:

1. Formal
- Professional
- 25-60 words

2. Sarcastic
- Dry irony
- Based only on the scene

3. Tech Humor
- Programming/AI joke
- Based only on the scene

4. Casual Humor
- Everyday funny
- Natural

Return EXACTLY in this format:

FORMAL:
...

SARCASTIC:
...

TECH:
...

CASUAL:
...
"""