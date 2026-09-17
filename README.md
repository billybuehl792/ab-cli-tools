# AB Apps

A collection of CLI tools for A & B Roofing and Construction.

## Installation

This project uses [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

### Gemini API Key

The Gemini API key must be available as a global environment variable named `GEMINI_API_KEY`.

On macOS/Linux, add the following to your shell configuration file (for example, `~/.zshrc`):

```bash
export GEMINI_API_KEY="your-api-key-here"
```

Then reload your shell:

```bash
source ~/.zshrc
```

Verify that the variable is available:

```bash
echo $GEMINI_API_KEY
```

The application reads the API key from the environment automatically.

## Commands

### JSON Extract

Extract structured JSON data from one or more images.

```bash
uv run ab-utils json-extract image1.jpg image2.jpg
```

Multiple images can be provided:

```bash
uv run ab-utils json-extract image1.jpg image2.jpg image3.jpg
```

You can also use shell globbing:

```bash
uv run ab-utils json-extract ./images/*.jpg
```

Write the extracted JSON to a file:

```bash
uv run ab-utils json-extract image1.jpg image2.jpg --output output.json
```

### ICS Extract

Extract calendar events from an image and create an ICS calendar file.

```bash
uv run ab-utils ics-extract calendar.jpg
```

Specify an output file:

```bash
uv run ab-utils ics-extract calendar.jpg --output events.ics
```

Specify the expected number of events:

```bash
uv run ab-utils ics-extract calendar.jpg --expected-events 5
```

Combine options:

```bash
uv run ab-utils ics-extract calendar.jpg \
    --expected-events 5 \
    --output events.ics
```

## Help

Show all available commands:

```bash
uv run ab-utils --help
```

Show help for a specific command:

```bash
uv run ab-utils json-extract --help
```

```bash
uv run ab-utils ics-extract --help
```
