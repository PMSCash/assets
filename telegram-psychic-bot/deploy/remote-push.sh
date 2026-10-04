#!/usr/bin/env bash
# Push telegram-psychic-bot/ to a VPS and run deploy/install.sh over SSH.
#
# Required:
#   SSH_HOST   e.g. 5.223.73.223
#   SSH_USER   e.g. root or ubuntu
# Auth (one of):
#   SSH_KEY            path to private key
#   SSH_PASSWORD       password (needs sshpass)
# Optional Telegram env (loaded from local .env if present):
#   TELEGRAM_BOT_TOKEN / TELEGRAM_TOKEN, TELEGRAM_CHAT_ID / CHAT_ID
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SSH_HOST="${SSH_HOST:-}"
SSH_USER="${SSH_USER:-}"
SSH_PORT="${SSH_PORT:-22}"
REMOTE_TMP="${REMOTE_TMP:-/tmp/telegram-psychic-bot-src}"

if [[ -z "${SSH_HOST}" || -z "${SSH_USER}" ]]; then
  echo "Set SSH_HOST and SSH_USER (and SSH_KEY or SSH_PASSWORD)." >&2
  exit 1
fi

# Load local secrets for server .env bootstrap (never printed).
if [[ -f "${ROOT}/.env" ]]; then
  set -a
  # shellcheck disable=SC1091
  source "${ROOT}/.env"
  set +a
fi

SSH_OPTS=(-p "${SSH_PORT}" -o StrictHostKeyChecking=accept-new)
if [[ -n "${SSH_KEY:-}" ]]; then
  SSH_OPTS+=(-i "${SSH_KEY}" -o IdentitiesOnly=yes -o BatchMode=yes)
fi

run_ssh() {
  if [[ -n "${SSH_PASSWORD:-}" && -z "${SSH_KEY:-}" ]]; then
    if ! command -v sshpass >/dev/null 2>&1; then
      echo "sshpass is required for password auth. Install it or use SSH_KEY." >&2
      exit 1
    fi
    SSHPASS="${SSH_PASSWORD}" sshpass -e ssh "${SSH_OPTS[@]}" "${SSH_USER}@${SSH_HOST}" "$@"
  else
    ssh "${SSH_OPTS[@]}" "${SSH_USER}@${SSH_HOST}" "$@"
  fi
}

run_rsync() {
  if [[ -n "${SSH_PASSWORD:-}" && -z "${SSH_KEY:-}" ]]; then
    if ! command -v sshpass >/dev/null 2>&1; then
      echo "sshpass is required for password auth." >&2
      exit 1
    fi
    export SSHPASS="${SSH_PASSWORD}"
    rsync -az --delete \
      --exclude '.venv/' \
      --exclude '.env' \
      --exclude '__pycache__/' \
      --exclude '.git/' \
      -e "sshpass -e ssh ${SSH_OPTS[*]}" \
      "${ROOT}/" "${SSH_USER}@${SSH_HOST}:${REMOTE_TMP}/"
  else
    rsync -az --delete \
      --exclude '.venv/' \
      --exclude '.env' \
      --exclude '__pycache__/' \
      --exclude '.git/' \
      -e "ssh ${SSH_OPTS[*]}" \
      "${ROOT}/" "${SSH_USER}@${SSH_HOST}:${REMOTE_TMP}/"
  fi
}

echo "==> Syncing to ${SSH_USER}@${SSH_HOST}:${REMOTE_TMP}"
run_ssh "mkdir -p '${REMOTE_TMP}'"
run_rsync

# Pass secrets via a remote env file so values with spaces/special chars are safe.
# File is deleted after install; never printed.
echo "==> Bootstrapping remote install env"
run_ssh "umask 077; cat > /tmp/psychic-bot-install.env" <<EOF
SRC_DIR=${REMOTE_TMP}
TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN:-}
TELEGRAM_TOKEN=${TELEGRAM_TOKEN:-}
TELEGRAM_CHAT_ID=${TELEGRAM_CHAT_ID:-}
CHAT_ID=${CHAT_ID:-}
OPENAI_API_KEY=${OPENAI_API_KEY:-}
LOG_LEVEL=${LOG_LEVEL:-INFO}
BOT_DISPLAY_NAME=${BOT_DISPLAY_NAME:-Projekt212 Oracle}
EOF

echo "==> Running install.sh on server"
run_ssh "set -a; source /tmp/psychic-bot-install.env; set +a; sudo --preserve-env=SRC_DIR,TELEGRAM_BOT_TOKEN,TELEGRAM_TOKEN,TELEGRAM_CHAT_ID,CHAT_ID,OPENAI_API_KEY,LOG_LEVEL,BOT_DISPLAY_NAME bash '${REMOTE_TMP}/deploy/install.sh'; rm -f /tmp/psychic-bot-install.env"

echo "==> Verifying service"
run_ssh "sudo systemctl is-active psychic-bot && sudo systemctl --no-pager --full status psychic-bot | head -20"

echo "==> remote-push complete"
