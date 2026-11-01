import pytest
from app.pipeline.quote_guard import validate, _normalise


def test_exact_match():
    chunk = "A candidate who has passed the Class X examination and holds a Two-Year Craft Certificate"
    quote = "A candidate who has passed the Class X examination"
    assert validate(quote, chunk) is True


def test_normalised_whitespace():
    chunk = "eligible  for  Direct   Second\n Year  admission to a Diploma in a Mapped Branch"
    quote = "eligible for Direct Second Year admission to a Diploma"
    assert validate(quote, chunk) is True


def test_case_insensitive():
    chunk = "A Candidate Who Has Passed The Class X Examination and holds a Two-Year Craft Certificate"
    quote = "a candidate who has passed the class x examination"
    assert validate(quote, chunk) is True


def test_too_short_words():
    chunk = "A candidate who has passed the Class X examination"
    quote = "A candidate who"  # only 3 words (min 6 required)
    assert validate(quote, chunk) is False


def test_too_short_chars():
    chunk = "one two three four five six"
    quote = "one two three four five six"  # 27 chars, check boundary
    assert len(quote) >= 25
    assert validate(quote, chunk) is True


def test_too_long_chars():
    chunk = "a " * 300
    quote = "a " * 205  # > 400 chars
    assert validate(quote, chunk) is False


def test_not_in_chunk():
    chunk = "Admission rules for technical qualifications in Example State"
    quote = "A candidate who has passed the Class X examination"
    assert validate(quote, chunk) is False


def test_empty_inputs():
    assert validate("", "some chunk text here that is long enough") is False
    assert validate("valid length quote that matches", "") is False
