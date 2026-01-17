"""
Services for downloading, transcribing and creating quizzes from YouTube content.

This module provides helpers to validate YouTube URLs, download audio, transcribe
audio with Whisper, and generate quizzes via the OpenAI API. Environment variables
are loaded from a local .env file at import time.
"""

import json
import os
import shutil
import urllib.parse

from dotenv import load_dotenv
import torch
import whisper
import yt_dlp

load_dotenv()

from .prompt import QUIZ_PROMPT


def validate_youtube_url(url):
    """
    Normalize and validate YouTube URLs.
    Returns canonical URLs:
      - Shorts -> https://www.youtube.com/shorts/<ID>
      - Watch  -> https://www.youtube.com/watch?v=<ID>
    Raises ValueError for non-YouTube or unrecognized formats.
    """
    parsed = urllib.parse.urlparse(url)
    netloc = (parsed.netloc or "").lower()
    path = parsed.path or ""
    query = urllib.parse.parse_qs(parsed.query or "")

    def watch_url(video_id):
        if not video_id:
            raise ValueError("Missing video id")
        return f"https://www.youtube.com/watch?v={video_id}"

    # Shortened youtu.be links
    if "youtu.be" in netloc:
        video_id = path.lstrip("/").split("/")[0]
        return watch_url(video_id)

    # Standard YouTube links
    if "youtube.com" in netloc or "youtube-nocookie.com" in netloc:
        parts = [p for p in path.split("/") if p]

        if parts and parts[0] == "watch":
            vid = query.get("v", [None])[0]
            return watch_url(vid)

        if parts and parts[0] == "shorts":
            video_id = parts[1] if len(parts) > 1 else None
            if not video_id:
                raise ValueError("Invalid shorts URL (missing id)")
            return f"https://www.youtube.com/shorts/{video_id}"

        if parts and parts[0] == "embed":
            video_id = parts[1] if len(parts) > 1 else None
            return watch_url(video_id)

        raise ValueError("Unsupported YouTube URL format")

    raise ValueError("URL is not a YouTube link")


def download_audio_from_youtube(youtube_url, output_path):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': False,
        'no_warnings': False,
    }

    if shutil.which("ffmpeg") is None and shutil.which("ffmpeg.exe") is None:
        raise RuntimeError(
            "ffmpeg not found in PATH. Install FFmpeg and add it to PATH. "
            "On Windows: https://ffmpeg.org/download.html or use `choco install ffmpeg` / `scoop install ffmpeg`."
        )

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([youtube_url])
        except Exception as e:
            print(f"Error downloading audio: {e}")


def transcribe_audio(file_path):
    # Check for GPU availability
    if torch.cuda.is_available():
        device = "cuda"
    else:
        device = "cpu"
        print("GPU not available, using CPU for transcription.")

    model_name = os.getenv("WHISPER_MODEL")
    if not model_name:
        model_name = "small"
        print("Environment variable WHISPER_MODEL not set; defaulting to 'small' model.")

    model = whisper.load_model(model_name, device=device)
    result = model.transcribe(audio=file_path + ".mp3", fp16=torch.cuda.is_available())
    return result["text"]


def create_quiz_from_transcript(transcript):
    from openai import OpenAI

    prompt = f"Create a quiz based on the following transcript:\n\n{transcript}\n\n"

    client = OpenAI(
        base_url=os.environ.get("OPENAI_ENDPOINT"),
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    completion = client.chat.completions.create(
        model=os.environ.get("OPENAI_MODEL"),
        messages=[
            {
                "role": "system",
                "content": QUIZ_PROMPT
            },
            {
                "role": "user",
                "content": prompt
            }

        ]
    )
    
    response_text = completion.choices[0].message.content
    print("Quiz generation response:", response_text)
    quiz_text = response_text

    try:
        quiz_obj = json.loads(quiz_text)
    except Exception as e:
        snippet = quiz_text[:1000] if quiz_text else ""
        raise ValueError(
            f"Failed to parse JSON from OpenAI response: {e}. Response snippet: {snippet}"
        )

    return quiz_obj

def cleanup_temp_files(*file_paths):
    for path in file_paths:
        try:
            if os.path.exists(path):
                os.remove(path)
        except Exception as e:
            print(f"Error cleaning up file {path}: {e}")