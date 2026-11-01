from pydantic import BaseModel
from typing import Any
from datetime import date


class SourceUploadRequest(BaseModel):
    authority: str
    title: str
    state: str | None = None
    academic_year: str | None = None
    version_label: str = "v1"
    effective_from: date | None = None
    effective_until: date | None = None
    source_url: str | None = None


class RuleReviewRequest(BaseModel):
    action: str  # approve | reject
    reason: str


class RulePublishRequest(BaseModel):
    rule_id: str


class UserInviteRequest(BaseModel):
    email: str
    role: str
