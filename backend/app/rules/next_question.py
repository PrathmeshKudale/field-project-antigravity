from typing import Any


QUESTION_MAP = {
    "qualification.trade": "Which ITI trade or diploma branch did you study?",
    "marks.percent": "What was your qualifying marks percentage?",
    "ssc.passed": "Did you pass Class X (SSC)?",
    "qualification.type": "What is your highest completed qualification (ITI, Diploma, HSC)?",
    "state.name": "Which state are you domiciled in?",
}


def compute_next_questions(eval_results: list[dict], facts: dict[str, Any], max_questions: int = 3) -> list[str]:
    """Determine the most useful questions to resolve UNKNOWN statuses."""
    unknown_counts: dict[str, int] = {}

    for res in eval_results:
        if res.get("status") == "UNKNOWN":
            for cond in res.get("trace", []):
                if cond.get("status") == "UNKNOWN":
                    attr = cond.get("attr")
                    if attr and attr not in facts:
                        unknown_counts[attr] = unknown_counts.get(attr, 0) + 1

    # Sort attributes that resolve the most routes first
    sorted_attrs = sorted(unknown_counts.keys(), key=lambda a: unknown_counts[a], reverse=True)
    questions = []
    for attr in sorted_attrs[:max_questions]:
        q = QUESTION_MAP.get(attr, f"Please provide {attr}")
        questions.append(q)

    return questions
