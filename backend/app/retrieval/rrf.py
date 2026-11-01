"""Reciprocal Rank Fusion (RRF) for combining vector and BM25/FTS search results."""


def rrf_score(ranks: list[int | None], k: int = 60) -> float:
    score = 0.0
    for r in ranks:
        if r is not None:
            score += 1.0 / (k + r)
    return score


def fuse_rankings(vector_ranked_ids: list[str], fts_ranked_ids: list[str], k: int = 60) -> list[str]:
    all_ids = set(vector_ranked_ids) | set(fts_ranked_ids)
    scores = {}

    v_rank = {id_: i + 1 for i, id_ in enumerate(vector_ranked_ids)}
    f_rank = {id_: i + 1 for i, id_ in enumerate(fts_ranked_ids)}

    for doc_id in all_ids:
        scores[doc_id] = rrf_score([v_rank.get(doc_id), f_rank.get(doc_id)], k=k)

    return sorted(scores.keys(), key=lambda x: scores[x], reverse=True)
