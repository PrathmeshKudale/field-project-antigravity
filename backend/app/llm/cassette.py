"""Recorded LLM cassettes for offline CI and reproducible evaluations."""
import json
from pathlib import Path


class CassetteStore:
    def __init__(self, cassette_dir: str = "backend/tests/cassettes"):
        self.cassette_dir = Path(cassette_dir)
        self.cassette_dir.mkdir(parents=True, exist_ok=True)

    def get(self, key: str) -> str | None:
        p = self.cassette_dir / f"{key}.json"
        if p.exists():
            with open(p, encoding="utf-8") as f:
                return json.load(f).get("response")
        return None

    def save(self, key: str, prompt: str, response: str) -> None:
        p = self.cassette_dir / f"{key}.json"
        with open(p, "w", encoding="utf-8") as f:
            json.dump({"prompt": prompt, "response": response}, f, indent=2)


cassette_store = CassetteStore()
