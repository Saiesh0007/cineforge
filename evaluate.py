import json
import os
import time
import traceback

from pipeline import process_video
from video import download_video

if os.path.exists("/input/tasks.json"):
    # Docker / AMD evaluator
    INPUT_PATH = "/input/tasks.json"
    OUTPUT_PATH = "/output/results.json"
else:
    # Local development
    INPUT_PATH = "input/tasks.json"
    OUTPUT_PATH = "output/results.json"


def load_tasks():
    with open(INPUT_PATH, "r") as f:
        data = json.load(f)

    if isinstance(data, dict) and "tasks" in data:
        return data["tasks"]

    return data


def save_results(results):
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    with open(OUTPUT_PATH, "w") as f:
        json.dump(results, f, indent=2)


def process_task(task):

    task_id = task.get("task_id") or task.get("id")
    video_url = task.get("video_url") or task.get("url")

    print("=" * 70)
    print(f"TASK {task_id}")
    print("=" * 70)

    t0 = time.time()

    print("Downloading video...")
    video_path = download_video(video_url)
    print(f"Download completed in {time.time()-t0:.2f}s")

    t1 = time.time()

    print("Generating captions...")
    captions = process_video(video_path)
    print(f"Caption generation completed in {time.time()-t1:.2f}s")

    print(f"TOTAL TASK TIME: {time.time()-t0:.2f}s")

    return {
        "task_id": task_id,
        "captions": captions,
    }


def main():

    total_start = time.time()

    print("=" * 70)
    print("CINEFORGE EVALUATION STARTED")
    print("=" * 70)

    tasks = load_tasks()

    results = []

    # Create initial results file immediately
    save_results(results)

    for i, task in enumerate(tasks):

        print(f"\nProcessing {i+1}/{len(tasks)}")

        try:

            result = process_task(task)

            results.append(result)

        except Exception as e:

            traceback.print_exc()

            results.append(
                {
                    "task_id": task.get("task_id"),
                    "captions": {
                        "formal": "Unable to generate caption.",
                        "sarcastic": "Well, that didn't go as planned.",
                        "humorous_tech": "Exception thrown during caption generation.",
                        "humorous_non_tech": "Something unexpected happened.",
                    },
                    "error": str(e),
                }
            )

        # Save after every task
        save_results(results)

        print("Results saved.")

    print("=" * 70)
    print(f"TOTAL EVALUATION TIME: {time.time()-total_start:.2f}s")
    print("=" * 70)


if __name__ == "__main__":
    main()