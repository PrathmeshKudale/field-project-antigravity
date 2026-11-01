"""Table extraction helpers for trade mapping schedules."""


def parse_mapping_table(text: str) -> list[dict]:
    mappings = []
    for line in text.splitlines():
        if "maps directly to" in line or "map directly to" in line:
            parts = line.split("maps directly to")
            if len(parts) == 2:
                mappings.append({
                    "trade": parts[0].strip().replace("-", "").strip(),
                    "branch": parts[1].strip().replace(".", "").strip(),
                })
    return mappings
