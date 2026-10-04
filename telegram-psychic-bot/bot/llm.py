"""Optional OpenAI-compatible client for mystic replies."""

from __future__ import annotations

import logging

import httpx

from bot.config import Settings
from bot.persona import SYSTEM_PROMPT
from bot.scripted import scripted_reading

logger = logging.getLogger(__name__)


async def mystic_reply(
    settings: Settings,
    question: str,
    user_id: int | None = None,
) -> str:
    """Return an LLM reading when configured; otherwise scripted fallback."""
    if not settings.llm_enabled:
        return scripted_reading(question, user_id=user_id)

    url = settings.openai_base_url.rstrip("/") + "/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.openai_api_key}",
        "Content-Type": "application/json",
    }
    # Reasoning-capable Groq models (e.g. gpt-oss) spend tokens on "reasoning"
    # before visible content — keep a higher ceiling so replies aren't empty.
    max_tokens = 800 if "gpt-oss" in settings.openai_model else 280
    payload = {
        "model": settings.openai_model,
        "temperature": 0.9,
        "max_tokens": max_tokens,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": question.strip() or "Offer a short open reading.",
            },
        ],
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            text = data["choices"][0]["message"]["content"].strip()
            if text:
                return text
            logger.warning("LLM returned empty content; using scripted fallback")
    except Exception:
        logger.exception("LLM request failed; using scripted fallback")

    return scripted_reading(question, user_id=user_id)
