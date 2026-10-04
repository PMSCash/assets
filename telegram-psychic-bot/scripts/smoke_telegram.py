#!/usr/bin/env python3
"""Live Telegram smoke test: getMe + outbound message + handler round-trip.

Requires TELEGRAM_BOT_TOKEN (or TELEGRAM_TOKEN) and TELEGRAM_CHAT_ID (or CHAT_ID).
Does not print secrets.
"""

from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path
from types import SimpleNamespace

# Allow `python scripts/smoke_telegram.py` from repo folder.
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from telegram import Bot  # noqa: E402
from telegram.ext import Application  # noqa: E402

from bot.config import load_settings  # noqa: E402
from bot.handlers import help_cmd, start_cmd, tarot_cmd, text_message  # noqa: E402
from bot.scripted import scripted_reading  # noqa: E402


class CaptureMessage:
    def __init__(self, text: str, user_id: int, chat_id: int) -> None:
        self.text = text
        self.replies: list[str] = []
        self.from_user = SimpleNamespace(id=user_id)
        self.chat = SimpleNamespace(id=chat_id)
        self._chat_id = chat_id

    async def reply_text(self, text: str, **kwargs) -> None:  # noqa: ANN003
        self.replies.append(text)


async def _handler_roundtrip(settings) -> None:
    app = Application.builder().token(settings.telegram_bot_token).build()
    app.bot_data["settings"] = settings
    await app.initialize()

    chat_id = int(settings.telegram_chat_id or 1)
    user_id = chat_id
    message = CaptureMessage("/start", user_id=user_id, chat_id=chat_id)
    update = SimpleNamespace(
        effective_message=message,
        effective_user=message.from_user,
        effective_chat=message.chat,
    )

    class Ctx:
        application = app
        args: list[str] = []
        bot = app.bot

        async def bot_send_chat_action(self, **kwargs):  # noqa: ANN003
            return None

    # handlers call context.bot.send_chat_action — use real bot (harmless) or stub
    ctx = Ctx()

    await start_cmd(update, ctx)  # type: ignore[arg-type]
    await help_cmd(update, ctx)  # type: ignore[arg-type]
    await tarot_cmd(update, ctx)  # type: ignore[arg-type]

    message.text = "What does the week hold for me?"
    await text_message(update, ctx)  # type: ignore[arg-type]

    await app.shutdown()

    if len(message.replies) < 4:
        raise SystemExit(
            f"handler round-trip failed: got {len(message.replies)} replies"
        )
    print(f"handler_roundtrip ok ({len(message.replies)} replies)")


async def main() -> None:
    os.chdir(ROOT)
    settings = load_settings()
    if not settings.telegram_chat_id:
        raise SystemExit("TELEGRAM_CHAT_ID (or CHAT_ID) required for smoke test")

    bot = Bot(settings.telegram_bot_token)
    async with bot:
        me = await bot.get_me()
        print(f"getMe ok: @{me.username} id={me.id}")

        reading = scripted_reading(
            "Smoke test: send a mystic hello",
            user_id=int(settings.telegram_chat_id),
        )
        outbound = (
            "✨ *Projekt212 Oracle smoke test*\n\n"
            f"{reading}\n\n"
            "_If you see this, outbound messaging works. "
            "Reply with any question (or /tarot) to exercise receive._"
        )
        sent = await bot.send_message(
            chat_id=settings.telegram_chat_id,
            text=outbound,
            parse_mode="Markdown",
        )
        print(f"sendMessage ok: message_id={sent.message_id}")

    await _handler_roundtrip(settings)
    print("smoke_telegram PASSED")


if __name__ == "__main__":
    asyncio.run(main())
