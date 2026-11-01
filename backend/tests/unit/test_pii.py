from app.pipeline.pii import scrub


def test_scrub_phone():
    text = "Call me at +91 9876543210 or 8765432109 for details."
    scrubbed = scrub(text)
    assert "[PHONE]" in scrubbed
    assert "9876543210" not in scrubbed


def test_scrub_email():
    text = "My email is student123@example.com please check."
    scrubbed = scrub(text)
    assert "[EMAIL]" in scrubbed
    assert "student123@example.com" not in scrubbed


def test_scrub_aadhaar():
    text = "Aadhaar number is 1234 5678 9012 for admission."
    scrubbed = scrub(text)
    assert "[AADHAAR]" in scrubbed
    assert "1234 5678 9012" not in scrubbed


def test_scrub_clean_text():
    text = "Can I get direct admission into diploma after ITI Electrician?"
    assert scrub(text) == text
