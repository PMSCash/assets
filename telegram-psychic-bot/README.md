# Projekt212 Psychic Telegram Bot

A small, deployable Python Telegram bot that answers in a mystic fortune-teller persona. Entertaining only — `/start` includes a light disclaimer. Works with scripted replies out of the box; optional OpenAI-compatible LLM when a key is set.

## Requirements

- Python 3.11+
- A Telegram bot token from [@BotFather](https://t.me/BotFather)

## Quick start (VPS)

```bash
# on the server
sudo mkdir -p /opt/telegram-psychic-bot
sudo rsync -a ./ /opt/telegram-psychic-bot/   # or git clone / copy this folder
cd /opt/telegram-psychic-bot

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
nano .env   # set TELEGRAM_BOT_TOKEN (and optionally OPENAI_API_KEY)
```

### Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `TELEGRAM_BOT_TOKEN` | yes* | Token from BotFather (`TELEGRAM_TOKEN` alias also accepted) |
| `TELEGRAM_CHAT_ID` | no | Optional chat id for smoke tests / proactive pings (`CHAT_ID` alias) |
| `OPENAI_API_KEY` | no | Enables AI mystic replies; without it, scripted replies are used |
| `OPENAI_BASE_URL` | no | Default `https://api.openai.com/v1` (any OpenAI-compatible API) |
| `OPENAI_MODEL` | no | Default `gpt-4o-mini` |
| `LOG_LEVEL` | no | Default `INFO` |
| `BOT_DISPLAY_NAME` | no | Default `Projekt212 Oracle` |

\* One of `TELEGRAM_BOT_TOKEN` or `TELEGRAM_TOKEN` is required.

Never commit a real `.env` or token.

### Run in the foreground (smoke test)

```bash
cd /opt/telegram-psychic-bot
source .venv/bin/activate
python -m bot
```

Message the bot on Telegram: `/start`, then ask a question, or try `/tarot` / `/horoscope leo`.

### Run with systemd (recommended)

```bash
sudo useradd --system --home /opt/telegram-psychic-bot --shell /usr/sbin/nologin psychicbot
sudo chown -R psychicbot:psychicbot /opt/telegram-psychic-bot

sudo cp deploy/psychic-bot.service /etc/systemd/system/psychic-bot.service
sudo systemctl daemon-reload
sudo systemctl enable --now psychic-bot
sudo systemctl status psychic-bot
journalctl -u psychic-bot -f
```

Graceful shutdown: `sudo systemctl stop psychic-bot` (SIGINT/SIGTERM handled by the polling loop).

## Commands

- `/start` — welcome + entertainment disclaimer
- `/help` — command list
- `/tarot` — single-card draw
- `/horoscope` / `/horoscope <sign>` — short daily vibe
- Free text — psychic-style reading (LLM if configured, else scripted)

## Local development

From this directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill TELEGRAM_BOT_TOKEN
python -m bot
```

### Smoke test (optional)

With `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` set in `.env`:

```bash
python scripts/smoke_telegram.py
```

This checks `getMe`, sends one outbound message to your chat, and exercises handlers locally. It never prints the token.

## Notes

- Idempotent to restart: polling uses `drop_pending_updates=True` on start.
- If the LLM call fails, the bot falls back to scripted mystic replies automatically.
