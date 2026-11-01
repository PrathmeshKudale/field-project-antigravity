import re


def chunk_page_by_clauses(page_text: str, page_number: int) -> list[dict]:
    """Split page text into clause-level chunks."""
    chunks = []
    pattern = re.compile(r"(Clause\s+\d+(?:\.\d+)*[^
]*)")
    parts = pattern.split(page_text)

    if len(parts) <= 1:
        # Fallback: whole page or paragraph
        chunks.append({
            "page_number": page_number,
            "chunk_index": 0,
            "clause_ref": None,
            "text": page_text.strip(),
            "token_count": len(page_text.split()),
        })
        return chunks

    for i in range(1, len(parts), 2):
        header = parts[i].strip()
        body = parts[i+1].strip() if i+1 < len(parts) else ""
        full_text = f"{header}\n{body}"
        chunks.append({
            "page_number": page_number,
            "chunk_index": i // 2,
            "clause_ref": header,
            "text": full_text,
            "token_count": len(full_text.split()),
        })

    return chunks
