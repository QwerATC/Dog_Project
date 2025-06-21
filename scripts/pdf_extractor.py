import re
from typing import Dict, List

import pdfplumber


def extract_info_from_pdf(pdf_path: str) -> Dict[str, List[str]]:
    """Extracts specified information from a PDF drawing.

    The function searches the entire text of the PDF for occurrences of the
    following fields: RIM ELEVATION, INVERT, SUMP, RING & COVER, and REBAR.
    It returns a dictionary mapping each field to a list of values found in
    the document.

    Parameters
    ----------
    pdf_path : str
        Path to the PDF file to parse.

    Returns
    -------
    Dict[str, List[str]]
        A dictionary with keys for each field and lists of strings representing
        the extracted values.
    """
    fields = [
        "RIM ELEVATION",
        "INVERT",
        "SUMP",
        "RING & COVER",
        "REBAR",
    ]
    # Precompile regex patterns to search for numbers (including decimals) after
    # each keyword. Example pattern: "RIM ELEVATION 100.00".
    patterns = {
        field: re.compile(rf"{re.escape(field)}\s*[:\-]?\s*(\d+(?:\.\d+)?)",
                          re.IGNORECASE)
        for field in fields
    }

    # Initialize results dictionary with empty lists for each field
    results = {field: [] for field in fields}

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            for field, pattern in patterns.items():
                for match in pattern.finditer(text):
                    results[field].append(match.group(1))

    return results


if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Extract drawing info from a PDF")
    parser.add_argument("pdf", help="Path to the PDF drawing file")
    parser.add_argument("-o", "--output", help="Path to JSON output file")
    args = parser.parse_args()

    data = extract_info_from_pdf(args.pdf)
    if args.output:
        with open(args.output, "w") as f:
            json.dump(data, f, indent=2)
    else:
        print(json.dumps(data, indent=2))
