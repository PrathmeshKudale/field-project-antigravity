import pytest
from app.api.v1.ask import ask_question
from app.schemas.ask import AskRequest


def test_ask_endpoint_myth_false():
    req = AskRequest(question="ITI ke baad seedha B.Tech ho sakta hai?")
    data = ask_question(req)
    assert data.verdict == "MYTH_FALSE"
    assert len(data.claims) >= 1
    assert data.claims[0].stance == "contradicts"
    assert len(data.evidence) >= 1
    assert data.evidence[0].quote_valid is True
    assert data.corpus_version >= 1


def test_ask_endpoint_context_dependent():
    req = AskRequest(question="ITI ke baad diploma kaise milega?")
    data = ask_question(req)
    assert data.verdict == "CONTEXT_DEPENDENT"
    assert len(data.evidence) >= 1
    assert data.evidence[0].quote_valid is True
    assert len(data.next_questions) >= 1


def test_ask_endpoint_banned_claim_abstention():
    req = AskRequest(question="100% guarantee placement and job after diploma?")
    data = ask_question(req)
    assert data.verdict in ("INSUFFICIENT_EVIDENCE", "CONTEXT_DEPENDENT")
    # Verify no banned words in explanation
    for line in data.explanation:
        assert "100%" not in line
        assert "admission confirmed" not in line.lower()
