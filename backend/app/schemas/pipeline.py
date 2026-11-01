from pydantic import BaseModel, Field
from typing import Literal


class UnderstandOut(BaseModel):
    language: Literal["en", "hinglish", "hi", "mr"] = "en"
    intent: str
    extracted_facts: dict = Field(default_factory=dict)
    atomic_claims: list[str] = Field(default_factory=list, max_length=5)
    missing_fields: list[str] = Field(default_factory=list)
    needs_rule_engine: bool = False
    out_of_scope: bool = False


class ClaimVerification(BaseModel):
    claim: str
    stance: Literal["supports", "contradicts", "partial", "none"]
    chunk_id: str | None = None
    quote: str | None = None
    confidence_note: str | None = None


class VerifyOut(BaseModel):
    verifications: list[ClaimVerification] = Field(default_factory=list)


class ExplainIn(BaseModel):
    verdict: str
    validated_facts: list[dict]
    language: str
    missing_fields: list[str] = Field(default_factory=list)


class ExplainOut(BaseModel):
    summary: str
    explanation: list[str]
    caveats: list[str] = Field(default_factory=list)
