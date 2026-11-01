from app.llm.base import LLMProvider


class OllamaProvider(LLMProvider):
    async def complete(self, prompt: str, schema_name: str | None = None) -> str:
        return "{}"
