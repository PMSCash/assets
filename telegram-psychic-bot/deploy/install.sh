#!/usr/bin/env bash
# Install / upgrade the psychic bot on a Linux VPS (systemd).
# Run as root on the server from the unpacked bot directory, or via remote-push.sh.
set -euo pipefail

APP_DIR="${APP_DIR:-/opt/telegram-psychic-bot}"
SERVICE_NAME="${SERVICE_NAME:-psychic-bot}"
SERVICE_USER="${SERVICE_USER:-psychicbot}"
SRC_DIR="${SRC_DIR:-$(cd "$(dirname "$0")/.." && pwd)}"

if [[ "$(id -u)" -ne 0 ]]; then
  echo "Run as root (sudo)." >&2
  exit 1
fi

echo "==> Installing from ${SRC_DIR} -> ${APP_DIR}"

if ! id -u "${SERVICE_USER}" >/dev/null 2>&1; then
  useradd --system --home "${APP_DIR}" --shell /usr/sbin/nologin "${SERVICE_USER}"
fi

mkdir -p "${APP_DIR}"
# Sync code; never overwrite an existing server .env with an empty/example file.
rsync -a --delete \
  --exclude '.venv/' \
  --exclude '.env' \
  --exclude '__pycache__/' \
  --exclude '.git/' \
  "${SRC_DIR}/" "${APP_DIR}/"

if [[ ! -f "${APP_DIR}/.env" ]]; then
  if [[ -n "${TELEGRAM_BOT_TOKEN:-${TELEGRAM_TOKEN:-}}" ]]; then
    umask 077
    {
      echo "TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN:-${TELEGRAM_TOKEN}}"
      echo "TELEGRAM_TOKEN=${TELEGRAM_TOKEN:-${TELEGRAM_BOT_TOKEN}}"
      [[ -n "${TELEGRAM_CHAT_ID:-${CHAT_ID:-}}" ]] && echo "TELEGRAM_CHAT_ID=${TELEGRAM_CHAT_ID:-${CHAT_ID}}"
      [[ -n "${GROQ_API_KEY:-}" ]] && echo "GROQ_API_KEY=${GROQ_API_KEY}"
      [[ -n "${OPENAI_API_KEY:-}" ]] && echo "OPENAI_API_KEY=${OPENAI_API_KEY}"
      [[ -n "${OPENAI_BASE_URL:-}" ]] && echo "OPENAI_BASE_URL=${OPENAI_BASE_URL}"
      [[ -n "${OPENAI_MODEL:-}" ]] && echo "OPENAI_MODEL=${OPENAI_MODEL}"
      echo "LOG_LEVEL=${LOG_LEVEL:-INFO}"
      echo "BOT_DISPLAY_NAME=${BOT_DISPLAY_NAME:-Projekt212 Oracle}"
    } >"${APP_DIR}/.env"
    echo "==> Wrote ${APP_DIR}/.env from environment"
  else
    cp "${APP_DIR}/.env.example" "${APP_DIR}/.env"
    echo "==> Created ${APP_DIR}/.env from example — edit it before starting the service" >&2
  fi
fi
chmod 600 "${APP_DIR}/.env"

export DEBIAN_FRONTEND=noninteractive
if command -v apt-get >/dev/null 2>&1; then
  apt-get update -qq
  apt-get install -y -qq python3 python3-venv python3-pip rsync
fi

python3 -m venv "${APP_DIR}/.venv"
"${APP_DIR}/.venv/bin/pip" install --upgrade pip
"${APP_DIR}/.venv/bin/pip" install -r "${APP_DIR}/requirements.txt"

chown -R "${SERVICE_USER}:${SERVICE_USER}" "${APP_DIR}"

cp "${APP_DIR}/deploy/psychic-bot.service" "/etc/systemd/system/${SERVICE_NAME}.service"
systemctl daemon-reload
systemctl enable --now "${SERVICE_NAME}"
systemctl --no-pager --full status "${SERVICE_NAME}" || true

echo "==> Done. Restart later with: systemctl restart ${SERVICE_NAME}"
echo "==> Logs: journalctl -u ${SERVICE_NAME} -f"
