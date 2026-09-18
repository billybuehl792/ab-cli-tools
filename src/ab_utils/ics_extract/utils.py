def escape_ics(value: str) -> str:
    """Escape text according to the iCalendar format."""
    return (
        str(value)
        .replace("\\", "\\\\")
        .replace(";", "\\;")
        .replace(",", "\\,")
        .replace("\n", "\\n")
    )
