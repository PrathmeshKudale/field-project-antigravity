import pymupdf
from pathlib import Path


def extract_pages_from_pdf(pdf_path: str | Path) -> list[dict]:
    """Extract text and metadata page by page from official PDF."""
    doc = pymupdf.open(str(pdf_path))
    pages = []
    for i, page in enumerate(doc):
        text = page.get_text()
        pages.append({
            "page_number": i + 1,
            "text": text,
            "char_count": len(text),
        })
    doc.close()
    return pages
