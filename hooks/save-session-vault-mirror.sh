#!/usr/bin/env bash
# ~/.claude/hooks/save-session-vault-mirror.sh
# Mirrors ~/.claude/sessions/*-session.tmp to vault/Claude/sessions/*.md

set -uo pipefail

case "${OSTYPE:-unknown}" in
  msys*|cygwin*|win32*) VAULT="$HOME/Documents/obsidiano/Claude/sessions" ;;
  *) VAULT="$HOME/obsidiano/Claude/sessions" ;;
esac

mkdir -p "$VAULT" 2>/dev/null || true

SOURCE_DIR="$HOME/.claude/sessions"
LATEST=$(ls -t "$SOURCE_DIR"/*-session.tmp 2>/dev/null | head -1 || true)

if [ -n "$LATEST" ] && [ -f "$LATEST" ]; then
  DEST="$VAULT/$(basename "$LATEST" .tmp).md"
  # Fix 2026-05-12 [DESKTOP]: idempotência — só copia se source é mais novo que dest.
  if [ ! -f "$DEST" ] || [ "$LATEST" -nt "$DEST" ]; then
    cp "$LATEST" "$DEST"
  fi
fi

exit 0
