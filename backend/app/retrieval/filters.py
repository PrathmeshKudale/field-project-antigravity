from typing import Any


def filter_chunks(chunks: list[dict], state: str | None = None, academic_year: str | None = None) -> list[dict]:
    """Filter chunks by state and academic year while keeping current official sources only."""
    filtered = []
    for c in chunks:
        # Exclude superseded or retired sources unless explicitly requested
        if c.get("source_status") in ("superseded", "retired", "failed"):
            continue
        if state and c.get("source_state") and c.get("source_state") != state:
            continue
        if academic_year and c.get("source_academic_year") and c.get("source_academic_year") != academic_year:
            continue
        filtered.append(c)
    return filtered
