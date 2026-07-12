import base64
import json
import os
from io import BytesIO

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

FIREWORKS_API_KEY = os.getenv("FIREWORKS_API_KEY", "")
FIREWORKS_BASE_URL = "https://api.fireworks.ai/inference/v1"
MODEL = "accounts/fireworks/models/qwen3p7-plus"

client = OpenAI(
    api_key=FIREWORKS_API_KEY, 
    base_url=FIREWORKS_BASE_URL, 
    timeout=120.0, 
    max_retries=3
)

def image_to_base64(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def describe_frames(frames_paths: list, prompt: str, max_tokens: int = 1536) -> str:
    """Send JPEG frames (raw base64, chronological order) plus a prompt; return text."""
    content = []
    for path in frames_paths:
        b64 = image_to_base64(path)
        content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}})
    
    content.append({"type": "text", "text": prompt})
    
    print("=" * 60)
    print(f"Calling Fireworks AI ({MODEL}) - describe_frames...")
    print(f"Images: {len(frames_paths)}")
    print("=" * 60)
    
    response = client.chat.completions.create(
        model=MODEL,
        max_tokens=max_tokens,
        reasoning_effort="none",
        messages=[{"role": "user", "content": content}],
    )
    return response.choices[0].message.content.strip()

def generate_json(prompt: str, schema: dict, frames_paths: list = None, max_tokens: int = 1024) -> dict:
    """Generate a JSON object guaranteed to match `schema` (structured outputs)."""
    if frames_paths:
        content = []
        for path in frames_paths:
            b64 = image_to_base64(path)
            content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}})
        content.append({"type": "text", "text": prompt})
        print(f"Calling Fireworks AI ({MODEL}) - generate_json with {len(frames_paths)} images...")
    else:
        content = prompt
        print(f"Calling Fireworks AI ({MODEL}) - generate_json without images...")
        
    response = client.chat.completions.create(
        model=MODEL,
        max_tokens=max_tokens,
        reasoning_effort="none",
        response_format={
            "type": "json_schema",
            "json_schema": {"name": "Response", "schema": schema, "strict": False},
        },
        messages=[{"role": "user", "content": content}],
    )
    try:
        return json.loads(response.choices[0].message.content.strip())
    except Exception as e:
        print(f"Failed to decode JSON: {response.choices[0].message.content}")
        raise e