JSON_EXTRACT_PROMPT = """
Extract all meaningful information from these document pages
into a structured JSON object.

Treat all provided files as pages belonging to the same document.

There is no fixed schema. Choose the structure that best represents
the information present.

Include all meaningful metadata and line items.
Combine information across pages where appropriate.
Do not duplicate information.
Do not invent information that is not present.
Return valid JSON only.
"""

INVOICE_JSON_EXTRACT_PROMPT = """
Extract every line item from this invoice.

Return ONLY valid JSON in this exact general structure:

{
"title": "...",
"description": "...",
"items": [
        {
        "description": "...",
        "quantity": 0,
        "unit_price": 0,
        "amount": 0
        }
]
}

Rules:
- Include every invoice line item.
- Preserve the description exactly as it appears when possible.
- Use null when a field is not present or cannot be read.
- Do not invent information.
- Do not include invoice totals, tax, shipping, payments, or other
information that is not a line item.
- Combine line items across multiple pages.
- Return JSON only.
"""
