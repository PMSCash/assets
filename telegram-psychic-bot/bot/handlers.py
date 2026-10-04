"""Telegram command and message handlers."""

from __future__ import annotations

import logging

from telegram import Update
from telegram.constants import ChatAction, ParseMode
from telegram.ext import ContextTypes

from bot.config import Settings
from bot.llm import mystic_reply
from bot.persona import HELP_MESSAGE, start_message
from bot.scripted import daily_horoscope, draw_tarot

logger = logging.getLogger(__name__)


def _settings(context: ContextTypes.DEFAULT_TYPE) -> Settings:
    return context.application.bot_data["settings"]


async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_message:
        return
    settings = _settings(context)
    await update.effective_message.reply_text(
        start_message(settings.bot_display_name),
        parse_mode=ParseMode.MARKDOWN,
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_message:
        return
    await update.effective_message.reply_text(
        HELP_MESSAGE,
        parse_mode=ParseMode.MARKDOWN,
    )


async def tarot_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_message or not update.effective_user:
        return
    await update.effective_message.reply_text(
        draw_tarot(user_id=update.effective_user.id),
        parse_mode=ParseMode.MARKDOWN,
    )


async def horoscope_cmd(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    if not update.effective_message or not update.effective_user:
        return
    sign = context.args[0] if context.args else None
    await update.effective_message.reply_text(
        daily_horoscope(sign, user_id=update.effective_user.id),
        parse_mode=ParseMode.MARKDOWN,
    )


async def text_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    if not update.effective_message or not update.effective_user:
        return
    text = update.effective_message.text or ""
    settings = _settings(context)

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action=ChatAction.TYPING,
    )

    reply = await mystic_reply(
        settings,
        text,
        user_id=update.effective_user.id,
    )
    try:
        await update.effective_message.reply_text(
            reply,
            parse_mode=ParseMode.MARKDOWN,
        )
    except Exception:
        # Fallback if model output breaks Markdown
        logger.warning("Markdown reply failed; sending plain text")
        await update.effective_message.reply_text(reply)


async def error_handler(
    update: object, context: ContextTypes.DEFAULT_TYPE
) -> None:
    logger.exception("Unhandled error while processing update: %s", update)
