import argparse
from pathlib import Path
from uuid import uuid4
from datetime import date, datetime, timedelta, timezone

from ab_utils.gemini.api import fetch_gemini
from ab_utils.gemini.models import GeminiOptions, ResponseMimeType
from ab_utils.constants import COMPANY_NAME, DEFAULT_GEMINI_MODEL
from .models import CalendarEvents
from .utils import escape_ics
from .constants import APP_NAME, ICS_EXTRACT_PROMPT


def create_ics(calendar_events: CalendarEvents, output_path: Path = Path("output.ics")):
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        f"PRODID:-//{escape_ics(COMPANY_NAME)}//Roofing Jobs//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
    ]

    # Use one timestamp for all events in this file
    dtstamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    for event in calendar_events.events:
        # Pydantic CalendarEvent object
        event_date = event.date

        # If date is a string, convert it
        if isinstance(event_date, str):
            event_date = date.fromisoformat(event_date)

        end_date = event_date + timedelta(days=1)

        description = "\n".join([
            f"Phone: {event.phone or 'N/A'}",
            f"Shingle Color: {event.shingle_color or 'N/A'}",
            f"Job Runner: {event.job_runner or 'N/A'}",
            f"Notes: {event.blue_notes or 'N/A'}",
        ])

        lines.extend([
            "BEGIN:VEVENT",
            f"UID:{uuid4()}@abroofing",
            f"DTSTAMP:{dtstamp}",
            f"DTSTART;VALUE=DATE:{event_date.strftime('%Y%m%d')}",
            f"DTEND;VALUE=DATE:{end_date.strftime('%Y%m%d')}",
            f"SUMMARY:{escape_ics(event.homeowner + ' - Whole Roof')}",
            f"LOCATION:{escape_ics(event.location or '')}",
            f"DESCRIPTION:{escape_ics(description)}",
            "END:VEVENT",
        ])

    lines.append("END:VCALENDAR")

    Path(output_path).write_text("\r\n".join(lines) + "\r\n", encoding="utf-8")


def add_parser(subparsers):
    parser: argparse.ArgumentParser = subparsers.add_parser(APP_NAME, help="Extract calendar events from an image",
                                                            description="Extract calendar events from an image.")
    parser.add_argument("files", nargs="+",
                        type=Path, help="Path to one or more files")
    parser.add_argument("-p", "--prompt", default=ICS_EXTRACT_PROMPT,
                        help=f"ICS extraction prompt (default: {ICS_EXTRACT_PROMPT})")
    parser.add_argument("-m", "--model", default=DEFAULT_GEMINI_MODEL,
                        help=f"Gemini model (default: {DEFAULT_GEMINI_MODEL})")
    parser.add_argument("-o", "--output", default="output.ics",
                        help="Output path for the ICS file (default: output.ics)")
    parser.add_argument("-n", "--events", type=int,
                        default=None, help="Expected number of events in the image")

    parser.set_defaults(func=run)


def run(args: argparse.Namespace):
    output_file = Path(args.output)

    response = fetch_gemini(args.prompt, GeminiOptions(
        model=args.model,
        files=args.files or [],
        response_mime_type=(ResponseMimeType.JSON),
        response_schema=CalendarEvents
    ))
    result = CalendarEvents.model_validate_json(response.text or "{}")

    print("\nExtracted Calendar Data:\n", result.model_dump_json(indent=2))

    create_ics(result, output_file)

    print(f"\nOutput .ics written to {output_file.name}")
