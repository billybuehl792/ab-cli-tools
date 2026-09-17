import argparse
import csv
import json
from pathlib import Path
import sys
from google import genai

from ab_utils.gemini_client import client as gemini_client
from ab_utils.constants import GEMINI_APP_NAME, DEFAULT_GEMINI_MODEL


def fetch_gemini(prompt: str, model: str, file_paths: list[Path] = [], as_json=False):
    """Call Google Gemini."""

    mime_type = "application/json" if as_json else "text/plain"
    chat = gemini_client.chats.create(
        model=model,
        config=genai.types.GenerateContentConfig(response_mime_type=mime_type))

    if (len(file_paths) > 0):
        files: list[genai.types.File] = []
        for file_path in file_paths:
            file = gemini_client.files.upload(file=file_path)
            files.append(file)
            print(f"Uploaded {file_path.name}")

        response = chat.send_message([*files, prompt])
    else:
        response = chat.send_message([prompt])

    return response.text


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
    response_type = args.type
    as_json = response_type != "string"

    files: list[Path] = []
    if args.files:
        for file in args.files:
            files.append(Path(file))

    result = fetch_gemini(args.prompt, args.model, files, as_json)

    if as_json:
        formatted_json = json.loads(result or "{}")
        if response_type == "json":
            if output_file:
                with open(output_file, "w") as f:
                    json.dump(formatted_json, f, indent=2)
            else:
                print(json.dumps(formatted_json, indent=2))
        elif response_type == "csv":
            if output_file:
                with open(output_file, "w") as f:
                    writer = csv.DictWriter(
                        f, fieldnames=formatted_json.keys())
                    writer.writeheader()
                    writer.writerow(formatted_json)
            else:
                writer = csv.DictWriter(
                    sys.stdout, fieldnames=formatted_json.keys())
                writer.writeheader()
                writer.writerow(formatted_json)
    else:
        if output_file:
            with open(output_file, "w") as f:
                f.write(result or "")
        else:
            print(result)

    if output_file:
        print(f"Output written to: {output_file.name}")
