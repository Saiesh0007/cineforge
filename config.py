import os

# Hugging Face Access Token
HF_TOKEN = os.getenv("HF_TOKEN")

# Gemma model
MODEL_ID = "google/gemma-4-31b-it"  # we'll verify availability

# Frame extraction
NUM_FRAMES = 8

# Image resize before sending to Gemma
MAX_IMAGE_SIZE = 896

# Caption styles required by the hackathon
STYLES = [
    "formal",
    "sarcastic",
    "humorous_tech",
    "humorous_non_tech",
]