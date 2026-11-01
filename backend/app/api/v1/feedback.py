from fastapi import APIRouter
from app.schemas.ask import FeedbackRequest
import uuid

router = APIRouter()


@router.post("/feedback")
async def submit_feedback(req: FeedbackRequest):
    return {
        "feedback_id": str(uuid.uuid4())[:8],
        "status": "queued_for_review",
        "answer_id": req.answer_id,
    }
