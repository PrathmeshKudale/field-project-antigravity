from fastapi import APIRouter
from app.schemas.pathway import PathwayCheckRequest, PathwayCheckResponse, RouteStatus
from app.rules.engine import evaluate_rule
from app.rules.next_question import compute_next_questions
from app.rules.facts import get_facts_dictionary
from pathlib import Path
import json

router = APIRouter()


def load_demo_rules() -> list[dict]:
    p = Path("d:/field_project_1/student-1/data/demo/rules.demo.json")
    if p.exists():
        with open(p, encoding="utf-8") as f:
            return json.load(f).get("rules", [])
    return []


@router.get("/facts/dictionary")
def facts_dictionary():
    return get_facts_dictionary()


@router.post("/pathway/check", response_model=PathwayCheckResponse)
def check_pathway(req: PathwayCheckRequest):
    """Evaluate user facts against published rules deterministically."""
    rules = load_demo_rules()
    eval_results = []
    routes = []
    eligible_targets = []

    for r in rules:
        res = evaluate_rule(r, req.facts)
        eval_results.append(res)
        routes.append(RouteStatus(
            route=res["route"],
            title=res["title"],
            status=res["status"],
            eligibility=res["eligibility"],
            trace=res["trace"],
            caveats=res["caveats"],
        ))
        if res["status"] == "PASS":
            eligible_targets.append(res["route"])

    next_qs = compute_next_questions(eval_results, req.facts)

    return PathwayCheckResponse(
        routes=routes,
        eligible_targets=eligible_targets,
        next_questions=next_qs,
        corpus_version=1,
    )
