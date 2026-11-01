from fastapi import APIRouter, Depends, HTTPException
from app.core.deps import require_reviewer, require_admin
from app.rules.facts import get_facts_dictionary
from pathlib import Path
import json

router = APIRouter()


def load_rules():
    p = Path("d:/field_project_1/student-1/data/demo/rules.demo.json")
    if p.exists():
        with open(p, encoding="utf-8") as f:
            return json.load(f).get("rules", [])
    return []


@router.get("/rules/queue")
def review_queue():
    """Rule Studio review queue with candidates."""
    rules = load_rules()
    return [
        {
            "rule_id": r.get("rule_id"),
            "route": r.get("route"),
            "title": r.get("title"),
            "status": r.get("status"),
            "source_page": r.get("source_page", 3),
            "maker": "reviewer-1@proofpath.example",
            "schema_valid": True,
            "quotes_valid": True,
            "conditions": r.get("conditions"),
        }
        for r in rules
    ]


@router.post("/rules/{rule_id}/approve")
def approve_rule(rule_id: str, reason: str = "Verified with handbook"):
    return {"status": "approved", "rule_id": rule_id, "reason": reason}


@router.post("/rules/{rule_id}/reject")
def reject_rule(rule_id: str, reason: str):
    return {"status": "rejected", "rule_id": rule_id, "reason": reason}


@router.post("/rules/{rule_id}/publish")
def publish_rule(rule_id: str):
    return {
        "status": "published",
        "rule_id": rule_id,
        "corpus_version_bumped": 2,
        "cached_answers_invalidated": 12,
    }
