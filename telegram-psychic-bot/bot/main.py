"""Application bootstrap with logging and graceful shutdown."""

from __future__ import annotations

import logging
import signal
import sys

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)

from bot.config import load_settings
from bot.handlers import (
    error_handler,
    help_cmd,
    horoscope_cmd,
    start_cmd,
    tarot_cmd,
    text_message,
)


def _configure_logging(level: str) -> None:
    logging.basicConfig(
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        level=getattr(logging, level, logging.INFO),
        stream=sys.stdout,
    )
    # Keep third-party noise down unless debugging.
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)


def build_app() -> Application:
    settings = load_settings()
    _configure_logging(settings.log_level)

    app = (
        Application.builder()
        .token(settings.telegram_bot_token)
        .build()
    )
    app.bot_data["settings"] = settings

    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("tarot", tarot_cmd))
    app.add_handler(CommandHandler("horoscope", horoscope_cmd))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, text_message)
    )
    app.add_error_handler(error_handler)

    mode = "LLM" if settings.llm_enabled else "scripted"
    logging.getLogger(__name__).info(
        "Starting %s (reply mode: %s)",
        settings.bot_display_name,
        mode,
    )
    return app


def main() -> None:
    app = build_app()

    # python-telegram-bot handles SIGINT/SIGTERM for graceful stop in run_polling.
    # Ensure default signal handlers remain cooperative on Linux VPS.
    for sig in (signal.SIGINT, signal.SIGTERM):
        signal.signal(sig, signal.SIG_DFL)

    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
