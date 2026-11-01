from pydantic import BaseModel
from datetime import datetime
import uuid


class ProblemDetail(BaseModel):
    type: str = "about:blank"
    title: str
    status: int
    detail: str
    code: str
    instance: str | None = None
    request_id: str | None = None


class CorpusMeta(BaseModel):
    corpus_mode: str
    corpus_version: int
    last_updated: str
    source_count: int
    rule_count: int


class PaginatedResponse(BaseModel):
    items: list
    total: int
    page: int
    per_page: int
    has_next: bool
