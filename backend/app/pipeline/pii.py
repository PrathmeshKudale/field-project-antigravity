import re

_PHONE = re.compile(r"\b(?:\+91[\s-]?)?[6-9]\d{9}\b")
_EMAIL = re.compile(r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b")
_AADHAAR = re.compile(r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}\b")
_NAME_PREFIXES = re.compile(r"\b(Mr\.|Mrs\.|Ms\.|Dr\.|Shri|Smt\.)\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*", re.IGNORECASE)


def scrub(text: str) -> str:
    """Remove PII from text before external LLM calls or logging."""
    if not text:
        return text
    text = _PHONE.sub("[PHONE]", text)
    text = _EMAIL.sub("[EMAIL]", text)
    text = _AADHAAR.sub("[AADHAAR]", text)
    text = _NAME_PREFIXES.sub("[NAME]", text)
    return text
