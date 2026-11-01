import json
from pathlib import Path


def load_mappings() -> list[dict]:
    p = Path("d:/field_project_1/student-1/data/demo/mappings.demo.json")
    if p.exists():
        with open(p, encoding="utf-8") as f:
            data = json.load(f)
            return data.get("mappings", [])
    return []


def is_trade_mapped(iti_trade: str, target_branch: str | None = None) -> bool:
    mappings = load_mappings()
    t_clean = iti_trade.strip().casefold()
    for m in mappings:
        if m.get("iti_trade", "").casefold() == t_clean:
            if not target_branch:
                return True
            if m.get("diploma_branch", "").casefold() == target_branch.strip().casefold():
                return True
    return False
