import hashlib
import json
from typing import Any


def compute_entry_hash(entry: dict[str, Any], prev_hash: str) -> str:
    """Compute SHA-256 hash of an audit entry chained to the previous hash."""
    payload = json.dumps({
        "prev": prev_hash,
        "id": str(entry.get("id", "")),
        "actor": str(entry.get("actor_id", "")),
        "action": str(entry.get("action", "")),
        "object_type": str(entry.get("object_type", "")),
        "object_id": str(entry.get("object_id", "")),
        "payload": entry.get("payload", {}),
        "ts": str(entry.get("created_at", "")),
    }, sort_keys=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def verify_chain(entries: list[dict[str, Any]]) -> tuple[bool, int | None]:
    """Verify the hash chain. Returns (is_valid, first_broken_index_or_None)."""
    prev_hash = "genesis"
    for i, entry in enumerate(entries):
        expected = compute_entry_hash(entry, prev_hash)
        actual = entry.get("entry_hash")
        if actual != expected:
            return False, i
        prev_hash = actual
    return True, None
