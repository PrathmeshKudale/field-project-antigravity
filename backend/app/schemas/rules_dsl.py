from pydantic import BaseModel
from typing import Any
from datetime import date


class ConditionLeafSchema(BaseModel):
    attr: str
    op: str
    value: Any
    quote: str = ""


class RuleCreateRequest(BaseModel):
    rule_key: str
    route: str
    title: str
    conditions: dict
    caveats: list[str] = []
    effective_from: date | None = None
    effective_until: date | None = None
    source_id: str | None = None
    source_page: int | None = None
    source_clause: str | None = None


class RuleResponse(BaseModel):
    id: str
    rule_key: str
    version: int
    route: str
    title: str
    status: str
    conditions: dict
    caveats: list[str]
    effective_from: date | None
    effective_until: date | None
    is_current: bool
    maker_id: str | None
    checker_id: str | None
