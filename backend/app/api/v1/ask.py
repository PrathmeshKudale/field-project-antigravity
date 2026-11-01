from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import StreamingResponse
from app.schemas.ask import AskRequest, AskResponse
from app.pipeline.orchestrator import process_question
from app.core.deps import get_optional_user
import json
import time

router = APIRouter()


@router.post("/ask", response_model=AskResponse)
def ask_question(
    req: AskRequest,
    user=Depends(get_optional_user),
):
    """Process question and return evidence-grounded answer with passport."""
    return process_question(req.question)


@router.get("/ask/stream")
def ask_stream(question: str):
    """SSE streaming ask endpoint with labeled stepper stages."""
    def event_generator():
        stages = [
            ("understanding", "Understanding your question"),
            ("retrieving", "Finding sources"),
            ("verifying", "Checking each statement"),
            ("explaining", "Preparing your answer"),
        ]

        for s_id, s_label in stages:
            yield f"data: {json.dumps({'type': 'stage', 'stage': s_id, 'label': s_label})}\n\n"
            time.sleep(0.1)

        res = process_question(question)
        payload = {
            "type": "result",
            "verdict": res.verdict,
            "summary": res.summary,
            "claims": [c.model_dump() for c in res.claims],
            "evidence": [e.model_dump() for e in res.evidence],
            "explanation": res.explanation,
            "next_questions": res.next_questions,
            "corpus_version": res.corpus_version,
            "language": res.language,
        }
        yield f"data: {json.dumps(payload)}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )
