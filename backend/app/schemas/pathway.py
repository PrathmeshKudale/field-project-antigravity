from pydantic import BaseModel


class RouteStatus(BaseModel):
    route: str
    title: str
    status: str  # MEETS_CHECKED_CONDITIONS | NOT_ELIGIBLE | NEEDS_MORE_INFORMATION | etc.
    eligibility: str
    trace: list[dict]
    caveats: list[str]


class PathwayCheckRequest(BaseModel):
    facts: dict


class PathwayCheckResponse(BaseModel):
    routes: list[RouteStatus]
    eligible_targets: list[str]
    next_questions: list[str]
    corpus_version: int


class FactsDictionary(BaseModel):
    version: str
    attributes: list[dict]
