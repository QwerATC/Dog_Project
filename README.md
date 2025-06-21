# Dog_Project
Detect if the dogs in on top of the couch

This repository also includes utilities for parsing engineering PDF drawings. The
`scripts/pdf_extractor.py` script scans a PDF for common fields such as "RIM
ELEVATION", "INVERT", "SUMP", "RING & COVER" and "REBAR" and extracts any
numeric values that follow those labels.

## Usage

```bash
python scripts/pdf_extractor.py path/to/drawing.pdf -o output.json
```

The command outputs a JSON file listing all the values found for each field.
