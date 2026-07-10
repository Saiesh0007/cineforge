import base64
from io import BytesIO

from PIL import Image
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

load_dotenv()

MODEL = "google/gemma-4-31B-it"

client = InferenceClient(
    token=os.getenv("HF_TOKEN")
)

MAX_SIDE = 384


def image_to_data_url(image_path):
    img = Image.open(image_path).convert("RGB")
    img.thumbnail((MAX_SIDE, MAX_SIDE))

    buffer = BytesIO()
    img.save(buffer, format="JPEG", quality=60, optimize=True)

    encoded = base64.b64encode(buffer.getvalue()).decode()

    return f"data:image/jpeg;base64,{encoded}"


def ask_gemma(prompt, image_paths=None, max_tokens=512):

    content = []

    if image_paths:
        for image in image_paths:
            content.append(
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image_to_data_url(image)
                    },
                }
            )

    content.append(
        {
            "type": "text",
            "text": prompt,
        }
    )

    try:
        print("Images:", len(image_paths) if image_paths else 0)
        print("Model:", MODEL)
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": content,
                }
            ],
            max_tokens=max_tokens,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print("HF ERROR:")
        print(repr(e))
        raise