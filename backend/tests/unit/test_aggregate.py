import pytest
from app.pipeline.aggregate import aggregate, ClaimItem, Verdict


def test_all_supported():
    claims = [
        ClaimItem(claim="C1", stance="supports", quote_valid=True),
        ClaimItem(claim="C2", stance="supports", quote_valid=True),
    ]
    assert aggregate(claims) == Verdict.VERIFIED_FACT


def test_all_contradicted():
    claims = [
        ClaimItem(claim="C1", stance="contradicts", quote_valid=True),
    ]
    assert aggregate(claims) == Verdict.MYTH_FALSE


def test_mixed_supported_and_contradicted():
    claims = [
        ClaimItem(claim="C1", stance="supports", quote_valid=True),
        ClaimItem(claim="C2", stance="contradicts", quote_valid=True),
    ]
    assert aggregate(claims) == Verdict.PARTIALLY_TRUE


def test_needs_rule_engine():
    claims = [
        ClaimItem(claim="C1", stance="supports", quote_valid=True),
    ]
    assert aggregate(claims, needs_rule_engine=True) == Verdict.CONTEXT_DEPENDENT


def test_out_of_scope_abstains():
    claims = [
        ClaimItem(claim="C1", stance="supports", quote_valid=True),
    ]
    assert aggregate(claims, out_of_scope=True) == Verdict.INSUFFICIENT_EVIDENCE


def test_invalid_quote_drops_to_insufficient():
    claims = [
        ClaimItem(claim="C1", stance="supports", quote_valid=False),
    ]
    assert aggregate(claims) == Verdict.INSUFFICIENT_EVIDENCE


def test_empty_claims():
    assert aggregate([]) == Verdict.INSUFFICIENT_EVIDENCE
