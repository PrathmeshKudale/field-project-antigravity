import json
from pathlib import Path


def get_facts_dictionary() -> dict:
    p = Path("d:/field_project_1/student-1/data/demo/facts.dictionary.json")
    if p.exists():
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    return {"version": "1.0", "attributes": []}
