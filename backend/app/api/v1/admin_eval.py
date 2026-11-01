from fastapi import APIRouter
from app.eval.harness import run_eval

router = APIRouter()


@router.get("/eval/results")
def eval_results():
    return run_eval(["B0", "B1", "S"])


@router.post("/eval/run")
def trigger_eval_run():
    return run_eval(["B0", "B1", "S"])
