from pathlib import Path
from chunking.pdf_parser import parse_pdf

def parse_document(path):
    suffix = Path(path).suffix.lower()

    if suffix in {".pdf", ".docx", ".txt"}:
        return parse_pdf(path)
    else:
        raise ValueError("Unknown document type")

