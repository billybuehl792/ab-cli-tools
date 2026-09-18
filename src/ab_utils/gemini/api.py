import os
from typing import TypeVar
from google import genai
from pydantic import BaseModel

from .models import GeminiOptions


client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


def fetch_gemini(prompt: str, options: GeminiOptions = GeminiOptions()):
    """API call to Google Gemini."""

    print("Fetching Gemini...")
    config = genai.types.GenerateContentConfig(
        response_mime_type=options.response_mime_type)

    if options.response_schema:
        config.response_schema = options.response_schema

    chat = client.chats.create(model=options.model, config=config)

    files: list[genai.types.File] = []

    for f in options.files:
        file = client.files.upload(file=f)
        files.append(file)
        print(f"Uploaded {f.name}")

    return chat.send_message([*files, prompt])
