from enum import Enum
from dataclasses import dataclass


class Verdict(str, Enum):
    VERIFIED_FACT = "VERIFIED_FACT"
    MYTH_FALSE = "MYTH_FALSE"
    PARTIALLY_TRUE = "PARTIALLY_TRUE"
    CONTEXT_DEPENDENT = "CONTEXT_DEPENDENT"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"


@dataclass
class ClaimItem:
    claim: str
    stance: str  # supports | contradicts | partial | none
    chunk_id: str | None = None
    quote: str | None = None
    quote_valid: bool = False


def aggregate(
    claims: list[ClaimItem],
    has_stale_source: bool = False,
    needs_rule_engine: bool = False,
    out_of_scope: bool = False,
) -> Verdict:
    """Pure-code deterministic aggregator: maps claims + rule needs + freshness to one of five verdicts."""
    if out_of_scope or not claims:
        return Verdict.INSUFFICIENT_EVIDENCE

    valid_claims = [c for c in claims if c.quote_valid]
    if not valid_claims:
        return Verdict.INSUFFICIENT_EVIDENCE

    stances = [c.stance for c in valid_claims]
    has_support = any(s == "supports" for s in stances)
    has_contradict = any(s == "contradicts" for s in stances)
    has_partial = any(s == "partial" for s in stances)
    has_none = any(s == "none" for s in stances)

    if needs_rule_engine and not has_contradict:
        return Verdict.CONTEXT_DEPENDENT

    if has_contradict and has_support:
        return Verdict.PARTIALLY_TRUE

    if has_contradict and not has_support:
        return Verdict.MYTH_FALSE

    if has_support and not has_contradict and not has_none and not has_partial:
        return Verdict.VERIFIED_FACT

    if has_partial or (has_support and has_none):
        return Verdict.PARTIALLY_TRUE

    if has_none and not has_support:
        return Verdict.INSUFFICIENT_EVIDENCE

    return Verdict.CONTEXT_DEPENDENT
