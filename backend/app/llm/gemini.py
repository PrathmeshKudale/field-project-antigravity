import httpx
import json
import logging
from typing import Any
from app.core.config import settings

logger = logging.getLogger("proofpath.gemini")

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models"


def generate_content_gemini(
    prompt: str,
    system_instruction: str | None = None,
    json_mode: bool = False,
    model: str = "gemini-1.5-flash",
) -> str | None:
    """
    Direct REST API client for Google Gemini 1.5.
    Works seamlessly without needing external google-generativeai package.
    """
    api_key = settings.gemini_api_key
    if not api_key:
        return None

    url = f"{GEMINI_API_URL}/{model}:generateContent?key={api_key}"

    contents: list[dict[str, Any]] = [
        {
            "role": "user",
            "parts": [{"text": prompt}],
        }
    ]

    payload: dict[str, Any] = {
        "contents": contents,
        "generationConfig": {
            "temperature": 0.2,
            "maxOutputTokens": 1024,
        },
    }

    if json_mode:
        payload["generationConfig"]["responseMimeType"] = "application/json"

    if system_instruction:
        payload["systemInstruction"] = {
            "parts": [{"text": system_instruction}]
        }

    try:
        with httpx.Client(timeout=20.0) as client:
            resp = client.post(url, json=payload)
            if resp.status_code == 200:
                data = resp.json()
                candidates = data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts:
                        return parts[0].get("text", "")
            else:
                logger.warning(f"Gemini API returned status {resp.status_code}: {resp.text}")
    except Exception as e:
        logger.error(f"Error calling Gemini API: {e}")

    return None
