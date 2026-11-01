import pytest
import unicodedata
from app.pipeline.quote_guard import validate, _normalise


@pytest.mark.parametrize("quote,chunk", [
    ("A candidate who has passed the Class X examination", "A candidate who has passed the Class X examination and holds certificate"),
    ("eligible for Direct Second Year admission to a Diploma", "Candidate shall be eligible for Direct Second Year admission to a Diploma programme"),
    ("short", "A candidate who has passed the Class X examination"),
    ("nonexistent quote that does not exist in chunk", "A candidate who has passed the Class X examination"),
    ("", ""),
    ("   ", "some text"),
    ("a " * 300, "a " * 400),
])
def test_quote_guard_properties(quote, chunk):
    res = validate(quote, chunk)
    assert isinstance(res, bool)
    if res is True:
        # If true, must satisfy length and word count invariants
        q_norm = _normalise(quote)
        assert len(q_norm) >= 25
        assert len(q_norm) <= 400
        assert len(q_norm.split()) >= 6
        assert q_norm in _normalise(chunk)
