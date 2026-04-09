#!/usr/bin/env bash
# ~/.claude/hooks/session-end-memory-writer.sh
# Updates active.md last-sessions + triggers INDEX rebuild + auto-commits.

set -uo pipefail

case "${OSTYPE:-unknown}" in
  msys*|cygwin*|win32*) VAULT="$HOME/Documents/obsidiano" ;;
  *) VAULT="$HOME/obsidiano" ;;
esac
[ -d "$VAULT" ] || VAULT="$HOME/Documents/obsidiano"

ACTIVE="$VAULT/Claude/memory/active.md"
[ -f "$ACTIVE" ] || exit 0  # no memory yet, exit clean

TIMESTAMP=$(date +"%Y-%m-%d %H:%M")
ENV_TAG="${CLAUDE_ENV_TAG:-DESKTOP}"
CWD_BASE=$(basename "$(pwd)")

# Append new session entry under "## Últimas 3 sessões" section
LINE="- $TIMESTAMP $ENV_TAG: $CWD_BASE"
TMP=$(mktemp)
awk -v line="$LINE" '
  /^## Últimas 3 sessões/ {
    print
    print line
    next
  }
  { print }
' "$ACTIVE" > "$TMP" && mv "$TMP" "$ACTIVE"

# Trigger INDEX rebuild in background (only if script exists)
if [ -x "$HOME/.claude/scripts/memory-index-rebuild.sh" ]; then
  ("$HOME/.claude/scripts/memory-index-rebuild.sh" &) >/dev/null 2>&1
fi

# Auto-commit silently (no push)
(cd "$VAULT" && git add Claude/memory/active.md Claude/memory/INDEX.md 2>/dev/null && \
  git commit -q -m "auto: session end ${ENV_TAG} ${TIMESTAMP}" 2>/dev/null) || true

exit 0
