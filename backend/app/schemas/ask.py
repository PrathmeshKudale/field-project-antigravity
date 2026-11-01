from pydantic import BaseModel, Field
from datetime import datetime
import uuid


class ClaimResult(BaseModel):
    claim: str
    stance: str  # supports | contradicts | partial | none
    chunk_id: str | None
    quote: str | None
    quote_valid: bool
    source_id: str | None
    source_title: str | None
    page_number: int | None


class EvidencePassport(BaseModel):
    authority: str
    document: str
    version: str
    page: int
    clause: str | None
    quote: str
    quote_valid: bool
    freshness_status: str  # current | expiring | stale | superseded
    effective_until: str | None
    source_url: str | None
    corpus_version: int


class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=600)
    idempotency_key: str | None = None


class AskResponse(BaseModel):
    answer_id: str
    verdict: str
    summary: str
    claims: list[ClaimResult]
    evidence: list[EvidencePassport]
    explanation: list[str]
    next_questions: list[str]
    corpus_version: int
    review_flag: bool
    language: str


class FeedbackRequest(BaseModel):
    answer_id: str
    issue: str = Field(max_length=1000)
    category: str | None = None
