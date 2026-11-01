from fastapi import APIRouter
from app.security.audit_chain import verify_chain, compute_entry_hash

router = APIRouter()

_ENTRIES = [
    {
        "id": "1",
        "actor_id": "system",
        "action": "corpus.init",
        "object_type": "corpus",
        "object_id": "v1",
        "payload": {"status": "seeded"},
        "created_at": "2026-10-31T09:00:00Z",
    }
]
_ENTRIES[0]["entry_hash"] = compute_entry_hash(_ENTRIES[0], "genesis")


@router.get("/audit")
def list_audit_logs():
    return _ENTRIES


@router.get("/audit/verify")
def verify_audit_chain():
    is_valid, broken_idx = verify_chain(_ENTRIES)
    return {
        "is_valid": is_valid,
        "first_broken_index": broken_idx,
        "total_entries": len(_ENTRIES),
    }
