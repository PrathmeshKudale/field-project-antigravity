"""
db/compat.py — provides SQLAlchemy column types that work on both
PostgreSQL (production) and SQLite (local dev / tests).

Usage:
    from app.db.compat import UUID, JSONB
"""
import os

_DATABASE_URL = os.environ.get("DATABASE_URL", "")
_IS_SQLITE = _DATABASE_URL.startswith("sqlite") or not _DATABASE_URL

if _IS_SQLITE:
    # SQLite-compatible fallbacks
    from sqlalchemy import Text, String

    class UUID(String):  # type: ignore[no-redef]
        """UUID stored as VARCHAR(36) on SQLite."""
        def __init__(self, as_uuid: bool = True, **kw):
            super().__init__(36, **kw)
            self.as_uuid = as_uuid

    class JSONB(Text):  # type: ignore[no-redef]
        """JSONB stored as TEXT on SQLite (serialised via Python json)."""
        pass

else:
    from sqlalchemy.dialects.postgresql import UUID, JSONB  # type: ignore[no-redef,assignment]
