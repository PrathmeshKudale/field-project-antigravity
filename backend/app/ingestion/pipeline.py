from pathlib import Path
from app.ingestion.extract import extract_pages_from_pdf
from app.ingestion.chunk import chunk_page_by_clauses
from app.ingestion.embed import embedder


def ingest_pdf(pdf_path: str | Path) -> list[dict]:
    pages = extract_pages_from_pdf(pdf_path)
    all_chunks = []
    for p in pages:
        page_chunks = chunk_page_by_clauses(p["text"], p["page_number"])
        for c in page_chunks:
            c["embedding"] = embedder.embed_text(c["text"])
            all_chunks.append(c)
    return all_chunks
