import argparse
import json
from pathlib import Path

from .api import fetch_gemini
from .models import GeminiOptions, ResponseMimeType
from .constants import APP_NAME, DEFAULT_GEMINI_MODEL


def add_parser(subparsers):
    parser = subparsers.add_parser(
        APP_NAME, help="Gemini request with prompt", description="Gemini AI call.")
    parser.add_argument("prompt", help="Gemini request prompt")
    parser.add_argument("-f", "--files", nargs="+",
                        type=Path, help="Path to one or more files")
    parser.add_argument("-t", "--response-type", choices=[
                        "text", "json"], default="text", help="Response type (default: text)")

    parser.add_argument("-m", "--model", default=DEFAULT_GEMINI_MODEL,
                        help=f"Gemini model (default: {DEFAULT_GEMINI_MODEL})")
    parser.add_argument("-o", "--output", default=None, type=Path,
                        help="Output path for the response file (ex: output.txt)")

    parser.set_defaults(func=run)


def run(args: argparse.Namespace):
    is_json_output = args.response_type == 'json'

    options = GeminiOptions(
        model=args.model,
        files=args.files or [],
        response_mime_type=(
            ResponseMimeType.JSON if is_json_output else ResponseMimeType.TEXT),
    )

    response = fetch_gemini(args.prompt, options)

    output = (
        json.dumps(json.loads(response.text or "{}"), indent=2)
        if is_json_output
        else response.text or ""
    )

    if args.output:
        output_file = Path(args.output)
        output_file.write_text(output)
        print(f"Output written to {output_file.name}")
    else:
        print(output)
