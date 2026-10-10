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

JSON_INVOICE_EXTRACT_PROMPT = """
Extract line items according to the document's table structure, not according to individual lines of text.

- Each physical table row represents exactly one line item.
- The item number and item description are separate text lines within the same cell. Combine them into a single line item; never create separate items for the item number and description.
- Associate the quantity, unit of measure (UOM), item number, description, price per UOM, and amount that appear on the same horizontal row.
- The item number is an identifier, not a separate line item.
- Product descriptions may wrap onto multiple lines. Combine all lines belonging to the same description into one description string, preserving their text and order.
- Read the table horizontally across its columns. Do not interpret vertical spacing, wrapped text, or page layout as evidence of a new line item.
- Start a new line item only when a new table row begins with its own quantity and corresponding item details.
- Include charges such as delivery as line items when they occupy their own table row.
- Preserve the original order of line items in the document.
- If a row contains an item number but its description wraps onto the next line, keep both in the same item object. If a row contains a description but no visible item number, still extract it as one item.

Accuracy is more important than producing additional items. Do not split one physical table row into multiple line items.
"""
