"""Rule extractor stub for Rule Studio candidate generation."""


def extract_candidate_rules_from_text(page_text: str, page_number: int, source_slug: str) -> list[dict]:
    candidates = []
    if "Direct Second Year" in page_text and "Class X" in page_text:
        candidates.append({
            "rule_key": f"EXTRACTED-DSE-P{page_number}",
            "route": "ITI_TO_DIPLOMA_DSE",
            "title": f"Extracted DSE Rule from page {page_number}",
            "source_slug": source_slug,
            "source_page": page_number,
            "conditions": {
                "all": [
                    {"attr": "ssc.passed", "op": "eq", "value": True, "quote": "A candidate who has passed the Class X examination"},
                    {"attr": "qualification.type", "op": "in", "value": ["ITI"], "quote": "and holds a Two-Year Craft Certificate"},
                ]
            },
            "caveats": ["Extracted automatically by Rule Studio. Requires reviewer verification."]
        })
    return candidates
