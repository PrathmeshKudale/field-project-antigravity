"""Patch all model files to use app.db.compat instead of postgresql dialect types."""
import re, pathlib

MODELS_DIR = pathlib.Path(r"d:\field_project_1\student-1\backend\app\db\models")

OLD = "from sqlalchemy.dialects.postgresql import UUID, JSONB"
NEW = "from app.db.compat import UUID, JSONB"
OLD2 = "from sqlalchemy.dialects.postgresql import UUID"
NEW2 = "from app.db.compat import UUID"

patched = []
for f in MODELS_DIR.glob("*.py"):
    text = f.read_text(encoding="utf-8")
    changed = text.replace(OLD, NEW).replace(OLD2, NEW2)
    # avoid double-import if both UUID and JSONB were in same line (already handled above)
    if changed != text:
        f.write_text(changed, encoding="utf-8")
        patched.append(f.name)

print("Patched:", patched)

