import json
from pathlib import Path
from app.retrieval.rrf import fuse_rankings
from app.retrieval.filters import filter_chunks


def load_demo_chunks() -> list[dict]:
    handbook_path = Path("d:/field_project_1/student-1/data/demo/demo_policy_handbook.txt")
    if not handbook_path.exists():
        return []

    text = handbook_path.read_text(encoding="utf-8")
    chunks = []
    pages = text.split("[PAGE ")

    for idx, page_content in enumerate(pages):
        if not page_content.strip():
            continue
        # Split into clauses
        clauses = page_content.split("Clause ")
        for c_idx, clause in enumerate(clauses):
            if not clause.strip():
                continue
            lines = clause.strip().split("\n")
            clause_header = lines[0]
            clause_num = clause_header.split()[0] if clause_header else f"{idx}.{c_idx}"
            chunks.append({
                "id": f"chunk-p{idx}-c{c_idx}",
                "source_slug": "demo-handbook-2026",
                "source_title": "Admission Handbook 2026-27",
                "authority": "Example State Board (DEMO)",
                "source_status": "current",
                "source_state": "Example State",
                "source_academic_year": "2026-27",
                "version_label": "v1",
                "page_number": idx,
                "clause_ref": f"Clause {clause_num}",
                "text": clause.strip(),
            })
    return chunks


def search_hybrid(query: str, top_k: int = 8, state: str | None = None) -> list[dict]:
    """Hybrid retrieval combining keyword matching and vector simulation."""
    all_chunks = load_demo_chunks()
    valid_chunks = filter_chunks(all_chunks, state=state)

    q_lower = query.lower()
    q_terms = [w.lower() for w in q_lower.split() if len(w) > 2]

    # Keyword search scoring
    keyword_scored = []
    for c in valid_chunks:
        text_lower = c["text"].lower()
        score = sum(1 for term in q_terms if term in text_lower)
        if score > 0:
            keyword_scored.append((c, score))

    keyword_scored.sort(key=lambda x: x[1], reverse=True)
    fts_ranked = [c["id"] for c, _ in keyword_scored]

    # Semantic vector rank simulation: boost clauses matching key concepts
    vector_ranked = []
    for c in valid_chunks:
        text_lower = c["text"].lower()
        sim_score = 0
        if any(t in q_lower for t in ["12th", "class xii", "class 12", "hsc", "intermediate"]):
            if "hsc: higher secondary certificate" in text_lower or "class xii" in text_lower or "first year" in text_lower:
                sim_score += 5
        if "iti" in q_lower and "two-year craft certificate" in text_lower:
            sim_score += 3
        if "b.tech" in q_lower and "degree" in text_lower:
            sim_score += 2
        if "diploma" in q_lower and "direct second year" in text_lower:
            sim_score += 2
        if "guarantee" in q_lower and "placement" in text_lower:
            sim_score += 4
        if sim_score > 0:
            vector_ranked.append((c["id"], sim_score))

    vector_ranked.sort(key=lambda x: x[1], reverse=True)
    vector_ids = [doc_id for doc_id, _ in vector_ranked]

    # RRF fusion
    fused_ids = fuse_rankings(vector_ids, fts_ranked)
    id_map = {c["id"]: c for c in valid_chunks}

    results = []
    for fid in fused_ids[:top_k]:
        if fid in id_map:
            results.append(id_map[fid])

    # If nothing matched, return the first few chunks as fallback
    if not results and valid_chunks:
        results = valid_chunks[:top_k]

    return results
