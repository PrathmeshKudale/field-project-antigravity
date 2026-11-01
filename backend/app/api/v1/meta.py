from fastapi import APIRouter
from app.core.config import settings
from app.schemas.common import CorpusMeta

router = APIRouter()


@router.get("/corpus", response_model=CorpusMeta)
def get_corpus_meta():
    return CorpusMeta(
        corpus_mode=settings.corpus_mode,
        corpus_version=1,
        last_updated="31 October 2026",
        source_count=1,
        rule_count=3,
    )
