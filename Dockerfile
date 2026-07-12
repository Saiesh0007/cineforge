FROM python:3.11-slim

WORKDIR /app

# Install ffmpeg
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Build argument
ARG FIREWORKS_API_KEY

# Make it available at runtime
ENV FIREWORKS_API_KEY=$FIREWORKS_API_KEY

COPY . .

CMD ["python", "evaluate.py"]