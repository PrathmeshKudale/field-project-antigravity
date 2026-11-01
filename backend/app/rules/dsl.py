from pydantic import BaseModel
from typing import Any, Union


class ConditionLeaf(BaseModel):
    attr: str
    op: str
    value: Any
    quote: str = ""


class AllGroup(BaseModel):
    conditions: list["RuleNode"]


class AnyGroup(BaseModel):
    conditions: list["RuleNode"]


RuleNode = Union[AllGroup, AnyGroup, ConditionLeaf]

AllGroup.model_rebuild()
AnyGroup.model_rebuild()


def parse_conditions(data: dict) -> RuleNode:
    """Parse a condition dict tree into RuleNode objects."""
    if "all" in data:
        return AllGroup(conditions=[parse_conditions(c) if isinstance(c, dict) and ("all" in c or "any" in c) else ConditionLeaf(**c) for c in data["all"]])
    if "any" in data:
        return AnyGroup(conditions=[parse_conditions(c) if isinstance(c, dict) and ("all" in c or "any" in c) else ConditionLeaf(**c) for c in data["any"]])
    return ConditionLeaf(**data)
