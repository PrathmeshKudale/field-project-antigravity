from fastapi import APIRouter, Header
from pydantic import BaseModel
from typing import Any
import uuid

router = APIRouter()

_REPORTS: list[dict] = []


class CreateReportRequest(BaseModel):
    title: str = "Family Report"
    notes: str | None = None
    question: str
    verdict: str
    summary: str
    evidence: list[dict] = []
    routes: list[dict] = []


@router.post("/reports")
async def save_report(
    req: CreateReportRequest,
    idempotency_key: str | None = Header(None, alias="Idempotency-Key"),
):
    report_id = str(uuid.uuid4())
    report = {
        "id": report_id,
        "title": req.title,
        "notes": req.notes,
        "question": req.question,
        "verdict": req.verdict,
        "summary": req.summary,
        "evidence": req.evidence,
        "routes": req.routes,
        "corpus_version": 1,
    }
    _REPORTS.append(report)
    return {"id": report_id, "status": "saved"}


@router.get("/reports")
async def list_reports():
    return _REPORTS


@router.delete("/reports/{report_id}")
async def delete_report(report_id: str):
    global _REPORTS
    _REPORTS = [r for r in _REPORTS if r["id"] != report_id]
    return {"status": "deleted"}
