from app.llm.base import LLMProvider


class GroqProvider(LLMProvider):
    async def complete(self, prompt: str, schema_name: str | None = None) -> str:
        return "{}"
