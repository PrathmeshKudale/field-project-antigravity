from app.schemas.pipeline import UnderstandOut


def heuristic_understand(question: str) -> UnderstandOut:
    """Rule/heuristic-based understanding fallback for fast or replay execution."""
    q = question.lower()
    
    # Detect language
    is_hinglish = any(w in q for w in ["ke baad", "kaise", "hoga", "ho sakta", "kya", "milega", "sawaal", "hai", "karna"])
    language = "hinglish" if is_hinglish else "en"

    # Detect route and intent
    if "12th" in q or "class 12" in q or "class xii" in q or "hsc" in q or "intermediate" in q:
        return UnderstandOut(
            language=language,
            intent="eligibility_check",
            extracted_facts={"qualification.type": "HSC", "route.target": "HSC_TO_TECHNICAL_PATHWAYS"},
            atomic_claims=[
                "HSC (Class XII) in Science, Technical, or Vocational stream qualifies for Polytechnic Diploma and Engineering pathways",
                "Eligibility requires minimum aggregate marks in qualifying examination"
            ],
            missing_fields=["stream", "marks.percent"],
            needs_rule_engine=True,
            out_of_scope=False,
        )
    elif "b.tech" in q and ("iti" in q or "direct" in q or "seedha" in q):
        return UnderstandOut(
            language=language,
            intent="eligibility_check",
            extracted_facts={"qualification.type": "ITI", "route.target": "ITI_TO_DEGREE_DIRECT"},
            atomic_claims=["Direct ITI to B.Tech entry is permitted"],
            missing_fields=[],
            needs_rule_engine=True,
            out_of_scope=False,
        )
    elif "diploma" in q and ("iti" in q or "dse" in q or "second year" in q or "2nd year" in q):
        facts = {"qualification.type": "ITI", "route.target": "ITI_TO_DIPLOMA_DSE"}
        if "electrician" in q:
            facts["qualification.trade"] = "Electrician"
            facts["craft_certificate.mapped_trade"] = True
        return UnderstandOut(
            language=language,
            intent="eligibility_check",
            extracted_facts=facts,
            atomic_claims=[
                "Two-Year ITI certificate holders may enter Diploma 2nd year",
                "Admission is subject to mapped trade and minimum qualifying marks"
            ],
            missing_fields=["marks.percent", "qualification.trade"],
            needs_rule_engine=True,
            out_of_scope=False,
        )
    elif "guarantee" in q or "100%" in q or "job" in q or "salary" in q:
        return UnderstandOut(
            language=language,
            intent="guarantee_check",
            extracted_facts={},
            atomic_claims=["Diploma guarantees a job with fixed placement"],
            missing_fields=[],
            needs_rule_engine=False,
            out_of_scope=False,
        )
    elif "hostel" in q or "scholarship amount" in q:
        return UnderstandOut(
            language=language,
            intent="local_rule_check",
            extracted_facts={},
            atomic_claims=[],
            missing_fields=[],
            needs_rule_engine=False,
            out_of_scope=True,
        )
    else:
        return UnderstandOut(
            language=language,
            intent="general_inquiry",
            extracted_facts={},
            atomic_claims=["Eligibility requires passing recognized qualifying examinations"],
            missing_fields=["qualification.type"],
            needs_rule_engine=True,
            out_of_scope=False,
        )
