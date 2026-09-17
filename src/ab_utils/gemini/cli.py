import argparse
import json
from pathlib import Path
from typing import Literal
from google import genai

from ab_utils.gemini_client import client as gemini_client
from ab_utils.constants import GEMINI_APP_NAME, DEFAULT_GEMINI_MODEL


ResponseType = Literal["json", "string"]


def fetch_gemini(prompt: str, model: str, response_type: ResponseType = "string", file_paths: list[Path] = []) -> str:
    """Call Google Gemini."""

    mime_type = {"json": "application/json",
                 "string": "text/plain"}[response_type]

    chat = gemini_client.chats.create(
        model=model,
        config=genai.types.GenerateContentConfig(response_mime_type=mime_type),
    )

    if (len(file_paths) > 0):
        files: list[genai.types.File] = []
        for file_path in file_paths:
            file = gemini_client.files.upload(file=file_path)
            files.append(file)
            print(f"Uploaded {file_path.name}")

        response = chat.send_message([*files, prompt])
    else:
        response = chat.send_message([prompt])

    result = response.text
    if (response_type == "json"):
        result = json.loads(result or "{}")

    return result


def add_parser(subparsers):
    parser: argparse.ArgumentParser = subparsers.add_parser(
        GEMINI_APP_NAME, help="Gemini request with prompt", description="Gemini AI call.")
    parser.add_argument("prompt", help="Gemini request prompt")
    parser.add_argument("-f", "--files", nargs="+",
                        help="Path to one or more files")
    parser.add_argument("-t", "--type", default="string",
                        help="Response type (default: string)")
    parser.add_argument("-m", "--model", default=DEFAULT_GEMINI_MODEL,
                        help=f"Gemini model (default: {DEFAULT_GEMINI_MODEL})")
    parser.add_argument("-o", "--output", default=None,
                        help="Output path for the response file (ex: output.txt)")
    parser.set_defaults(func=run)


def run(args: argparse.Namespace):
    output_file = Path(args.output) if args.output else None
    response_type = str(args.type)

    files: list[Path] = []
    if args.files:
        for file in args.files:
            files.append(Path(file))

    result = fetch_gemini(args.prompt, args.model, response_type, files)

    if (output_file):
        with open(output_file, "w") as f:
            if response_type == "json":
                json.dump(result, f, indent=2)
            else:
                f.write(result)
            print(f"Output written to: {output_file.name}")
    else:
        if (response_type == "json"):
            print("Extracted JSON:\n\n", json.dumps(result, indent=2))
        else:
            print(result)
