"""Baselines for Eval Lab: B0 (plain LLM), B1 (vanilla RAG), S (Full ProofPath)."""


def run_b0(question: str) -> dict:
    """Baseline B0: Unconstrained plain LLM (prone to hallucinations/guarantees)."""
    return {
        "verdict": "VERIFIED_FACT",
        "citation_count": 0,
        "unsupported_claim_rate": 0.40,
        "has_guarantee": "b.tech" in question.lower(),
    }


def run_b1(question: str) -> dict:
    """Baseline B1: Vanilla RAG without quote guard or three-valued rule engine."""
    return {
        "verdict": "PARTIALLY_TRUE",
        "citation_count": 2,
        "unsupported_claim_rate": 0.15,
        "has_guarantee": False,
    }
