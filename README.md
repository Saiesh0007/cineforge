# CineForge

![Python](https://img.shields.io/badge/Python-3.11%2B-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-App-ff4b4b)

CineForge is a Python-based video captioning app that turns short video clips into polished, multi-style captions. It samples frames from a video, uses an LLM to understand the scene, and produces captions in several tones such as formal, sarcastic, tech-humor, and casual humor.

## What the project does

CineForge helps you turn raw video content into ready-to-use captions for social media, demos, or creative workflows. The app supports two main workflows:

- A Streamlit web app for uploading a video and generating captions interactively.
- A batch evaluation pipeline for processing multiple videos from a task list.

The core flow is:

1. Extract representative frames from the video.
2. Build a factual scene description from those frames.
3. Generate captions in multiple styles.
4. Return the final captions for preview or export.

## Why the project is useful

- Fast prototyping for video caption generation.
- Multiple caption styles from one video input.
- Grounded prompt design that focuses on visible facts rather than invented details.
- Works both interactively and in automated batch runs.
- Includes container support through [Dockerfile](Dockerfile) for consistent setup.

## Getting started

### Prerequisites

- Python 3.11 or newer
- ffmpeg and ffprobe installed and available on your PATH
- A Fireworks AI API key for the caption-generation model

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure your environment

Create a `.env` file in the project root with your API key:

```env
FIREWORKS_API_KEY=your_api_key_here
```

### Run the Streamlit app

```bash
streamlit run app.py
```

Then open the local URL shown by Streamlit, upload a video, and click Generate Captions.

### Run the batch evaluation pipeline

The repository includes a sample task file at [input/tasks.json](input/tasks.json). You can process it with:

```bash
python evaluate.py
```

The script downloads each video, generates captions, and writes results to [output/results.json](output/results.json).

### Run with Docker

```bash
docker build --build-arg FIREWORKS_API_KEY=your_api_key_here -t cineforge .
```

```bash
docker run --rm -v ${PWD}/input:/app/input -v ${PWD}/output:/app/output cineforge
```

## Project structure

- [app.py](app.py) — Streamlit frontend for interactive caption generation.
- [pipeline.py](pipeline.py) — Orchestrates frame-based scene understanding and caption generation.
- [llm.py](llm.py) — Wrapper for the Fireworks AI chat completion API.
- [video.py](video.py) — Downloads videos and extracts frames with ffmpeg.
- [prompts.py](prompts.py) — Prompt templates and style definitions.
- [evaluate.py](evaluate.py) — Batch runner for processing multiple tasks.
- [requirements.txt](requirements.txt) — Python dependencies.
- [Dockerfile](Dockerfile) — Container definition for reproducible runs.

## Where to get help

If you run into issues, start by checking the relevant files:

- [app.py](app.py) for the UI flow
- [pipeline.py](pipeline.py) for caption generation logic
- [video.py](video.py) for ffmpeg and download behavior

For bug reports or feature requests, please open an issue in the repository or contact the maintainers directly.

## Maintainers and contributions

CineForge is maintained by the current project contributors. Contributions are welcome via pull requests and issues.

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for the contribution workflow and guidelines.

When contributing:

- Keep changes focused and well documented.
- Update or add tests when behavior changes.
- Use clear commit messages and explain the intent of your changes.
