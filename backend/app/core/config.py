import os
from pydantic import BaseModel, Field
from typing import Literal

try:
    from pydantic_settings import BaseSettings
except ImportError:
    class BaseSettings(BaseModel):  # type: ignore
        def __init__(self, **values):
            init_vals = {}
            for field_name in type(self).model_fields:
                env_val = os.getenv(field_name.upper())
                if env_val is not None:
                    init_vals[field_name] = env_val
            init_vals.update(values)
            super().__init__(**init_vals)


class Settings(BaseSettings):
    # Database
    database_url: str = Field(
        default="postgresql+asyncpg://proofpath:proofpath@localhost:5432/proofpath"
    )

    # Security
    secret_key: str = Field(default="proofpath-dev-secret-key-change-in-production")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24 * 7  # 7 days

    # ── Google OAuth 2.0 ──────────────────────────────────────
    google_client_id: str = Field(default="")
    google_client_secret: str = Field(default="")
    google_redirect_uri: str = Field(default="http://localhost:5173/auth/callback")

    # LLM
    gemini_api_key: str = Field(default="")
    groq_api_key: str = Field(default="")
    llm_mode: Literal["live", "record", "replay"] = "replay"
    llm_model: str = "gemini-1.5-flash"
    daily_llm_budget: int = 100
    answer_lang_default: Literal["en", "hinglish"] = "en"

    # Embedder
    embedder: Literal["gemini", "local"] = "local"
    embedding_dim: int = 768

    # App — corpus_mode "reviewed" = real uploaded documents; "demo" = bundled demo set
    corpus_mode: Literal["demo", "reviewed"] = "reviewed"
    app_name: str = "ProofPath"
    app_version: str = "0.1.0"
    debug: bool = False

    # Rate limiting
    rate_limit_ask: str = "20/minute"
    rate_limit_global: str = "100/minute"

    # Cloudflare
    cloudflare_turnstile_secret: str = Field(default="")
    skip_turnstile: bool = True

    # CORS
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
    ]


settings = Settings()
