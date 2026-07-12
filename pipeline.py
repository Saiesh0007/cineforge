import json
import shutil
import tempfile
import sys
import traceback

from llm import describe_frames, generate_json
from prompts import (
    DESCRIBE_FACTS_PROMPT,
    CANDIDATE_SCHEMA,
    STYLE_GUIDE,
    facts_schema,
    specialist_prompt,
    selection_prompt,
    audit_schema,
    audit_prompt,
)
from video import extract_frames


def get_grounding(frame_paths):
    prompt = DESCRIBE_FACTS_PROMPT.format(n=len(frame_paths))
    result = generate_json(prompt, facts_schema(), frames_paths=frame_paths, max_tokens=1536)
    
    description = str(result.get("description", "")).strip()
    facts = [str(f).strip() for f in result.get("facts", []) if str(f).strip()]
    return description, facts


def specialists_and_select(description: str, facts: list, styles: list, frame_paths: list) -> dict:
    candidates = {}
    prior_captions = []
    
    for s in styles:
        if s not in STYLE_GUIDE:
            continue
        try:
            prompt = specialist_prompt(s, description, facts, prior_captions=prior_captions)
            # The specialist generation does not need the images, it's text-only based on the facts
            cands = generate_json(prompt, CANDIDATE_SCHEMA, frames_paths=None, max_tokens=800)
            candidates[s] = cands
            prior_captions.extend([cands.get("a", ""), cands.get("b", "")])
        except Exception as e:
            print(f"Specialist call failed for {s}: {e}", file=sys.stderr)
            traceback.print_exc()

    result = {}
    if candidates:
        sel_schema = {
            "type": "object",
            "properties": {s: {"type": "string"} for s in candidates},
            "required": list(candidates),
            "additionalProperties": False,
        }
        try:
            prompt = selection_prompt(description, facts, candidates)
            chosen = generate_json(prompt, sel_schema, frames_paths=frame_paths, max_tokens=2000)
            for s in candidates:
                result[s] = str(chosen.get(s, "")).strip()
        except Exception as e:
            print(f"Selection failed: {e}", file=sys.stderr)
            traceback.print_exc()
            
        for s in candidates:
            if not result.get(s, "").strip():
                result[s] = str(candidates[s].get("a", "")).strip()

    # Audit pass
    audited_result = {}
    for s, caption in result.items():
        if not caption:
            audited_result[s] = caption
            continue
        try:
            print(f"Running audit pass for {s}...")
            prompt = audit_prompt(s, description, facts, caption)
            audit_resp = generate_json(prompt, audit_schema(), frames_paths=frame_paths, max_tokens=800)
            audited_result[s] = str(audit_resp.get("caption", caption)).strip()
        except Exception as e:
            print(f"Audit failed for {s}: {e}", file=sys.stderr)
            traceback.print_exc()
            audited_result[s] = caption
                
    return {s: audited_result.get(s, "") for s in styles}


def generate_all_captions(frame_paths):
    description, facts = get_grounding(frame_paths)
    
    styles = ["formal", "sarcastic", "humorous_tech", "humorous_non_tech"]
    captions = specialists_and_select(description, facts, styles, frame_paths)
    
    required = set(styles)
    missing = required - set(captions.keys())

    if missing:
        raise Exception(f"Missing required captions: {missing}")

    return captions


def process_video(video_path):
    temp_dir = tempfile.mkdtemp(prefix="cineforge_")

    try:
        frame_paths = extract_frames(
            video_path,
            output_dir=temp_dir,
            num_frames=15,
        )
        
        print(f"Extracted {len(frame_paths)} frames for {video_path}")

        captions = generate_all_captions(frame_paths)

        return captions

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)