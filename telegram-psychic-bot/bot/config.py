"""Environment-based configuration. Secrets are never hardcoded."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    telegram_bot_token: str
    openai_api_key: str | None
    openai_base_url: str
    openai_model: str
    log_level: str
    bot_display_name: str
    telegram_chat_id: str | None = None

    @property
    def llm_enabled(self) -> bool:
        return bool(self.openai_api_key)


def load_settings() -> Settings:
    load_dotenv()

    # Prefer TELEGRAM_BOT_TOKEN; accept TELEGRAM_TOKEN as a common alias.
    token = (
        os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
        or os.getenv("TELEGRAM_TOKEN", "").strip()
    )
    if not token:
        raise SystemExit(
            "TELEGRAM_BOT_TOKEN (or TELEGRAM_TOKEN) is required. "
            "Copy .env.example to .env and set your BotFather token."
        )

    openai_key = os.getenv("OPENAI_API_KEY", "").strip() or None
    chat_id = (
        os.getenv("TELEGRAM_CHAT_ID", "").strip()
        or os.getenv("CHAT_ID", "").strip()
        or None
    )

    return Settings(
        telegram_bot_token=token,
        openai_api_key=openai_key,
        openai_base_url=os.getenv(
            "OPENAI_BASE_URL", "https://api.openai.com/v1"
        ).strip(),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip(),
        log_level=os.getenv("LOG_LEVEL", "INFO").strip().upper(),
        bot_display_name=os.getenv(
            "BOT_DISPLAY_NAME", "Projekt212 Oracle"
        ).strip(),
        telegram_chat_id=chat_id,
    )
