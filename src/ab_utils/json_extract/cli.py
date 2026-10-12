import argparse
import json
from pathlib import Path
import subprocess

from ab_utils.gemini.api import fetch_gemini
from ab_utils.gemini.models import GeminiOptions, ResponseMimeType
from ab_utils.gemini.constants import DEFAULT_GEMINI_MODEL
from ab_utils.utils import json_to_csv

from .models import Invoice
from .constants import APP_NAME, JSON_EXTRACT_PROMPT


def add_parser(subparsers):
    parser: argparse.ArgumentParser = subparsers.add_parser(APP_NAME, help="Extract JSON from an image",
                                                            description="Extract JSON data from an image.")
    # Input options
    parser.add_argument("files", nargs="+",
                        type=Path, help="Path to one or more files")
    parser.add_argument("-t", "--type", default=None,
                        help="Type of input image (ex: 'invoice')")
    parser.add_argument("-p", "--prompt", default=JSON_EXTRACT_PROMPT,
                        help=f"ICS extraction prompt (default: {JSON_EXTRACT_PROMPT})")
    parser.add_argument("-m", "--model", default=DEFAULT_GEMINI_MODEL,
                        help=f"Gemini model (default: {DEFAULT_GEMINI_MODEL})")

    # Output options
    parser.add_argument("--csv", action="store_true", help="output as CSV")
    parser.add_argument("-o", "--output", default=None, help="Output file")
    parser.add_argument("-c", "--copy", action="store_true",
                        help="copy to clipboard.")

    parser.set_defaults(func=run)


def run(args: argparse.Namespace):
    print("Starting JSON extraction...")

    is_invoice = args.type == "invoice"
    output_file_path = Path(args.output) if args.output else None
    output_file_path_type = output_file_path.suffix.lower().lstrip(
        ".") if output_file_path else None

    if output_file_path is not None:
        if output_file_path_type not in ["json", "csv"]:
            raise ValueError(
                f"Unsupported output file type: {output_file_path_type}")
        if args.csv and output_file_path_type != "csv":
            raise ValueError(
                f"CSV output requested but output file type is {output_file_path_type}")

    response = fetch_gemini(args.prompt, GeminiOptions(
        model=args.model,
        files=args.files or [],
        response_mime_type=(ResponseMimeType.JSON),
        response_schema=Invoice if is_invoice else None
    ))

    response_text = response.text or "{}"
    json_data = json.loads(response_text)
    json_output = json.dumps(json_data, indent=2)
    csv_output = Invoice.model_validate_json(
        response_text).get_formatted_csv() if is_invoice else json_to_csv(json_data)

    # Output
    if args.copy:
        subprocess.run(
            ["pbcopy"], input=csv_output if args.csv else json_output, text=True)
        print(f"{'CSV' if args.csv else 'JSON'} copied to clipboard.")

    if output_file_path:
        output_file_path.write_text(
            csv_output if output_file_path_type == "csv" else json_output)
        print(f"Output written to {output_file_path.name}")
    else:
        print(csv_output if args.csv else json_output)
