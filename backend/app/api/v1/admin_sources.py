from fastapi import APIRouter, Depends
from app.core.deps import require_admin, require_reviewer

router = APIRouter()


@router.get("/sources")
def list_sources():
    return [
        {
            "id": "00000000-0000-0000-0000-000000000001",
            "slug": "demo-handbook-2026",
            "authority": "Example State Board (DEMO)",
            "title": "Admission Handbook 2026-27",
            "version_label": "v1",
            "status": "current",
            "page_count": 8,
            "chunk_count": 14,
            "effective_from": "2026-06-01",
            "effective_until": "2027-05-31",
            "rules_count": 3,
        }
    ]


@router.get("/sources/health")
def source_health():
    return {
        "expiring_soon": [],
        "superseded_referenced": [],
        "unlinked_rules": [],
        "failed_ingestion_jobs": [],
    }
