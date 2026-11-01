import hashlib
import json
from typing import Any


def make_cache_key(provider: str, model: str, prompt_version: str, schema_name: str, input_text: str, corpus_version: int) -> str:
    raw = f"{provider}:{model}:{prompt_version}:{schema_name}:{input_text}:{corpus_version}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()
