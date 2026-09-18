APP_NAME = "ics-extract"

ICS_EXTRACT_PROMPT = """
    You are extracting roofing job appointments from a photograph of work-order sheets.

    The photograph contains multiple roofing job sheets. Some sheets have a YELLOW HIGHLIGHTED section on the top left of the pages.

    ONLY create an event for a job sheet that has a yellow highlighted section.

    IMPORTANT:

    * The yellow highlighted section contains the scheduled date and the person/team running the job.
    * Ignore dates that appear elsewhere on the page or in the calendar visible in the background.
    * Do not create events for sheets without a yellow highlighted section.
    * Each extracted event is an ALL-DAY event.
    * Carefully read both printed text and handwritten text.
    * Extract the location from the SAME work-order sheet as the event.

    For each qualifying job sheet:

    1. DATE

    * Extract the date from the yellow highlighted section.
    * The highlighted section may contain a handwritten day/date such as "Thurs 9/3".
    * Use the numeric date as the event date.
    * The year should be 2026 unless another year is explicitly indicated.
    * Do not use dates printed elsewhere on the work-order sheet.

    2. EVENT TITLE

    * Format exactly as:
        "<HOMEOWNER> - Whole Roof"
    * Use the homeowner's full name as written on the work-order sheet.

    3. LOCATION

    * Extract the job location from the corresponding work-order sheet.
    * The location should represent the ACTUAL PROPERTY where the roofing work is being performed.
    * Do NOT use the company/office address, mailing address, phone number, or any location belonging to another job sheet.
    * Prefer a complete street address when one is visible.
    * Format the location as a normal mailing/street address whenever possible:
        "<street number> <street name> <street type>, <city>, <state> <ZIP>"
    * Normalize obvious abbreviations and formatting when doing so makes the address clearer. For example:
        "1234 ELM HILL - SOLON"
        → "1234 Elm Hill Rd, Solon, OH"
    * If the sheet provides a street number and street name but omits the street type, infer the street type ONLY when it is reasonably clear from the street name/location.
    * If the city is provided, include it.
    * If the state is not written but can be reasonably determined from the city/location, use the state abbreviation.
    * If a ZIP code is visible, include it.
    * If the exact street address cannot be determined, provide the most specific location that can be reasonably established from the sheet, such as:
        "<street name>, <city>, <state>"
    * NEVER invent a house number, ZIP code, or other specific address detail without reasonable evidence.
    * When there are multiple possible locations on the sheet, prioritize the location associated with the homeowner/job being scheduled.
    * Accuracy is more important than forcing a complete address.

    4. EVENT DESCRIPTION
    Include the following information:

    Phone: <phone number>
    Shingle Color: <shingle color>
    Job Runner: <person/team written on yellow highlighted section>
    Notes: <blue highlighted handwritten notes>

    Preserve the meaning of the handwritten notes as accurately as possible.
    Transcribe the blue-highlighted notes, including important instructions, requests, or warnings.

    If any requested field cannot be read, use null rather than guessing.

    5. JOB RUNNER

    * Read this from the yellow highlighted section.
    * Preserve the wording as written, for example:
        "Bob w/ Dave"
        "Mike w/ Alex"
    * Do not infer or invent a job runner from other parts of the image.

    6. BLUE NOTES

    * Only include the handwritten notes that are highlighted in BLUE.
    * Carefully distinguish blue-highlighted notes from black handwritten text and yellow highlighted section text.
    * Transcribe the blue notes as accurately as possible.
    * If multiple blue notes appear on the sheet, combine them into one Notes field.

    7. HOMEOWNER / PHONE / SHINGLE COLOR

    * Read these from the corresponding work-order sheet.
    * Do not use information from another sheet.
    * Preserve names and phone numbers exactly as written when possible.

    8. LOCATION ACCURACY

    * Location is the one field where a reasonable best-effort normalization/inference is expected.
    * Do not simply return the raw text if it is clearly shorthand.
    * Convert shorthand location notation into a recognizable address format when the information supports doing so.
    * For example:
        "1234 ELM HILL - SOLON"
        should be interpreted as a property at approximately:
        "1234 Elm Hill Rd, Solon, OH"
        rather than preserving "1234 ELM HILL - SOLON" verbatim.
    * However, do not fabricate missing address components.
    * If uncertain, use the most specific defensible location rather than guessing an exact address.

    Return ONLY structured data matching the provided schema.

    Do not create events for:

    * Calendar dates visible in the background
    * Sheets without yellow highlighted sections
    * Dates written elsewhere on the work-order sheet unless they are also the scheduled date on the yellow highlighted section
    * Locations belonging to another work-order sheet
"""
