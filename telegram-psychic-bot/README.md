# Projekt212 Psychic Telegram Bot

A small, deployable Python Telegram bot that answers in a mystic fortune-teller persona. Entertaining only — `/start` includes a light disclaimer. Works with scripted replies out of the box; optional OpenAI-compatible LLM when a key is set.

## Requirements

- Python 3.11+
- A Telegram bot token from [@BotFather](https://t.me/BotFather)

## Quick start (VPS / systemd)

Preferred path: copy this folder to the server and run `deploy/install.sh` as root. Telegram only — no web UI or open HTTP ports required (outbound HTTPS to `api.telegram.org`).

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

Never commit a real `.env` or token. On the server, secrets live only in `/opt/telegram-psychic-bot/.env` (mode `600`, owned by the service user).

### A) One-shot install on the server

```bash
# as root on the VPS, with this directory present (e.g. /tmp/telegram-psychic-bot-src)
export TELEGRAM_BOT_TOKEN='...'          # or TELEGRAM_TOKEN
export TELEGRAM_CHAT_ID='...'            # optional
sudo -E bash deploy/install.sh
```

This creates `/opt/telegram-psychic-bot`, a venv, `psychicbot` system user, writes `.env` from the environment (if missing), installs `psychic-bot.service`, and enables it.

### B) Push from your laptop / agent (when SSH works)

```bash
cd telegram-psychic-bot
cp .env.example .env   # fill TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID locally (gitignored)

export SSH_HOST=5.223.73.223
export SSH_USER=root                   # or ubuntu / your user with sudo
export SSH_KEY=~/.ssh/id_ed25519       # or: export SSH_PASSWORD='...'
bash deploy/remote-push.sh
```

### Useful systemd commands

```bash
sudo systemctl status psychic-bot
sudo systemctl restart psychic-bot
sudo systemctl stop psychic-bot
journalctl -u psychic-bot -f
```

### Manual steps (equivalent to install.sh)

```bash
sudo mkdir -p /opt/telegram-psychic-bot
sudo rsync -a --exclude '.venv' --exclude '.env' ./ /opt/telegram-psychic-bot/
cd /opt/telegram-psychic-bot
sudo python3 -m venv .venv
sudo .venv/bin/pip install -r requirements.txt
sudo cp .env.example .env && sudo nano .env   # set token
sudo useradd --system --home /opt/telegram-psychic-bot --shell /usr/sbin/nologin psychicbot || true
sudo chown -R psychicbot:psychicbot /opt/telegram-psychic-bot
sudo chmod 600 /opt/telegram-psychic-bot/.env
sudo cp deploy/psychic-bot.service /etc/systemd/system/psychic-bot.service
sudo systemctl daemon-reload
sudo systemctl enable --now psychic-bot
```

Foreground smoke test (optional): `sudo -u psychicbot /opt/telegram-psychic-bot/.venv/bin/python -m bot` from `/opt/telegram-psychic-bot`.

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
