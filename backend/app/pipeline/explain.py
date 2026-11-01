import re

# Banned guarantee phrases invariant 5
BANNED_PATTERNS = [
    re.compile(r"\bguarantee(?:d|s)?\b", re.IGNORECASE),
    re.compile(r"\b100%\b"),
    re.compile(r"\bdefinitely\b", re.IGNORECASE),
    re.compile(r"\badmission confirmed\b", re.IGNORECASE),
    re.compile(r"\bjob assured\b", re.IGNORECASE),
    re.compile(r"\bsalary assured\b", re.IGNORECASE),
]


def validate_explanation(text: str) -> bool:
    """Check that explanation text does not contain banned claims."""
    for pattern in BANNED_PATTERNS:
        if pattern.search(text):
            return False
    return True


def render_template_explanation(verdict: str, language: str = "en", route_title: str | None = None) -> list[str]:
    """Fallback deterministic explanation when LLM is unavailable or fails validation."""
    if language == "hinglish":
        if verdict == "VERIFIED_FACT":
            return [
                "Official state admission documents ke mutabiq yeh conditions confirm hui hain.",
                "Yeh eligibility check hai, admission confirmation nahi hai.",
                "Seat allotment centralized merit rounds par nirbhar karta hai."
            ]
        elif verdict == "MYTH_FALSE":
            return [
                "Official rules ke mutabiq yeh route direct allowed nahi hai.",
                "ITI se seedha B.Tech mein admission nahi hota; pehle diploma karna zaroori hai.",
                "Rule 3.4 ke anusar polytechnic diploma ke baad hi degree lateral entry milti hai."
            ]
        elif verdict == "CONTEXT_DEPENDENT":
            return [
                "Aapki qualification route par depend karti hai.",
                "Direct Second Year diploma ke liye 2-year mapped ITI trade aur 50% marks zaroori hain.",
                "Apna trade aur marks bata kar exact eligibility check karein."
            ]
        else:
            return [
                "Hamare approved sources mein is specific sawal ki jankari nahi mili.",
                "Apne state technical board ki official website ya helpline se sampark karein."
            ]
    else:
        if verdict == "VERIFIED_FACT":
            return [
                "Official state admission guidelines confirm the stated eligibility pathway.",
                "This checks criteria on record; it is decision support and not an admission guarantee.",
                "Final seat allocation depends on centralized counseling and document verification."
            ]
        elif verdict == "MYTH_FALSE":
            return [
                "Official regulations explicitly prohibit direct entry through this pathway.",
                "Clause 3.4 states standalone ITI qualifications do not allow direct B.Tech entry.",
                "Candidates must first complete a polytechnic diploma before seeking lateral entry degree admission."
            ]
        elif verdict == "CONTEXT_DEPENDENT":
            return [
                "Eligibility depends on the specific trade completed, qualifying marks, and state rules.",
                "Two-year mapped ITI trades qualify for Direct Second Year Diploma with minimum 50% marks.",
                "Provide your specific trade and aggregate marks to resolve eligibility."
            ]
        else:
            return [
                "Our approved official sources do not establish an answer to this question.",
                "Please consult the official state technical education brochure or institute helpline."
            ]
