from pathlib import Path
import re


APP_NAME = 'roof-estimate'

DEFAULT_LABOR_CATALOG = Path("./config/labor/catalog.json")
DEFAULT_MATERIAL_CATALOG = Path("./config/material/catalog.json")

# Regex

PITCH_PATTERN = re.compile(r"^(\d+)/12 pitch \(Sqft\)$")
