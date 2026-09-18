import argparse
import json
from pathlib import Path

from ab_utils.gemini.api import fetch_gemini
from ab_utils.gemini.models import GeminiOptions, ResponseMimeType
from ab_utils.gemini.constants import DEFAULT_GEMINI_MODEL

from .constants import APP_NAME, INVOICE_JSON_EXTRACT_PROMPT, JSON_EXTRACT_PROMPT


def add_parser(subparsers):
    parser: argparse.ArgumentParser = subparsers.add_parser(APP_NAME, help="Extract JSON from an image",
                                                            description="Extract JSON data from an image.")
    parser.add_argument("files", nargs="+",
                        type=Path, help="Path to one or more files")
    parser.add_argument("-t", "--type", default=None,
                        help="Type of input image (ex: 'invoice')")
    parser.add_argument("-p", "--prompt", default=None,
                        help=f"ICS extraction prompt (default: {JSON_EXTRACT_PROMPT})")
    parser.add_argument("-m", "--model", default=DEFAULT_GEMINI_MODEL,
                        help=f"Gemini model (default: {DEFAULT_GEMINI_MODEL})")
    parser.add_argument("-o", "--output", default=None,
                        help="Output JSON file")

    parser.set_defaults(func=run)


def run(args: argparse.Namespace):
    prompt = JSON_EXTRACT_PROMPT
    if not args.prompt:
        if args.type == "invoice":
            prompt = INVOICE_JSON_EXTRACT_PROMPT

    response = fetch_gemini(prompt, GeminiOptions(
        model=args.model,
        files=args.files or [],
        response_mime_type=(ResponseMimeType.JSON),
    ))

    output = json.dumps(json.loads(response.text or "{}"), indent=2)

    if args.output:
        output_file = Path(args.output)
        output_file.write_text(output)
        print(f"Output written to {output_file.name}")
    else:
        print(output)
