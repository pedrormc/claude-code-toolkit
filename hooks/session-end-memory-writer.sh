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

# Prepend new session entry under "## Últimas 3 sessões" section, TRUNCATE to keep=3.
# Fix 2026-05-12 [DESKTOP]: awk antigo nunca truncava — active.md inflava sem limite.
LINE="- $TIMESTAMP $ENV_TAG: $CWD_BASE"
KEEP=3
TMP=$(mktemp)
awk -v line="$LINE" -v keep="$KEEP" '
  BEGIN { in_section = 0; count = 0 }
  /^## Últimas 3 sessões/ {
    print
    print line
    in_section = 1
    count = 1
    next
  }
  in_section && /^- / {
    if (count < keep) { print; count++ }
    next
  }
  in_section && (/^## / || /^$/) {
    in_section = 0
    print
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
