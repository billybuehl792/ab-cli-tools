APP_NAME = "json-extract"

JSON_EXTRACT_PROMPT = """
Extract the information from the provided image or document.

Return the extracted information as valid JSON.

- Extract only information that is actually present.
- Do not invent, infer, or estimate values.
- Preserve the values and meaning of the source document.
- Use null when information is not present.
- Return repeated items as separate elements.
- Do not include markdown or explanatory text.
"""
