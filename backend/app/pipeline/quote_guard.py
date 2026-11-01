import unicodedata
import re

MIN_WORDS = 6
MIN_CHARS = 25
MAX_CHARS = 400


def _normalise(text: str) -> str:
    """NFKC normalise, casefold, collapse whitespace."""
    if not text:
        return ""
    text = unicodedata.normalize("NFKC", text)
    text = text.casefold()
    text = re.sub(r"\s+", " ", text).strip()
    return text


def validate(quote: str, chunk_text: str) -> bool:
    """Return True if quote appears verbatim in chunk_text after normalisation,
    has 6+ words and 25 to 400 chars. Otherwise False."""
    if not quote or not chunk_text:
        return False
    q = _normalise(quote)
    c = _normalise(chunk_text)
    if len(q) < MIN_CHARS or len(q) > MAX_CHARS:
        return False
    if len(q.split()) < MIN_WORDS:
        return False
    return q in c
