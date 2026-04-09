#!/usr/bin/env bash
# ~/.claude/scripts/memory-revert.sh
# Reverts an auto-promotion by entry_id.

set -euo pipefail

if [ $# -lt 1 ]; then
  echo "Uso: memory-revert <entry-id>" >&2
  echo "Example: memory-revert prom-2026-04-15-abc123def456" >&2
  exit 1
fi

ENTRY_ID="$1"

case "${OSTYPE:-unknown}" in
  msys*|cygwin*|win32*) VAULT="$HOME/Documents/obsidiano" ;;
  *) VAULT="$HOME/obsidiano" ;;
esac

LOG="$VAULT/Claude/memory/.promotion-log.jsonl"
[ -f "$LOG" ] || { echo "no promotion log found at $LOG" >&2; exit 1; }

ENTRY=$(grep "\"entry_id\":\"$ENTRY_ID\"" "$LOG" | tail -1)
if [ -z "$ENTRY" ]; then
  echo "entry_id not found in log: $ENTRY_ID" >&2
  exit 1
fi

TARGET=$(echo "$ENTRY" | jq -r '.target')
TARGET_FILE="$VAULT/Claude/memory/$TARGET"

if [ ! -f "$TARGET_FILE" ]; then
  echo "target file missing: $TARGET_FILE" >&2
  exit 1
fi

# Remove lines from the "## [auto-promoted" heading matching entry_id until the next "##" or EOF
# Pass entry_id via -v to keep the awk program purely single-quoted (no shell interpolation)
awk -v eid="$ENTRY_ID" '
  /^## \[auto-promoted/ { in_block = 1; buffer = $0; next }
  in_block && index($0, "entry_id: " eid) { in_block = 2; buffer = ""; next }
  in_block == 1 && /^##/ { in_block = 0; print buffer; print; next }
  in_block == 1 { buffer = buffer "\n" $0; next }
  in_block == 2 && /^##/ { in_block = 0; print; next }
  in_block == 2 { next }
  { print }
  END { if (in_block == 1) print buffer }
' "$TARGET_FILE" > "$TARGET_FILE.tmp" && mv "$TARGET_FILE.tmp" "$TARGET_FILE"

# Mark log entry as reverted
TIMESTAMP=$(date -Iseconds)
echo "{\"timestamp\":\"$TIMESTAMP\",\"action\":\"revert\",\"entry_id\":\"$ENTRY_ID\",\"reverted\":true}" >> "$LOG"

# Commit
(cd "$VAULT" && git add "Claude/memory/$TARGET" "Claude/memory/.promotion-log.jsonl" && \
  git commit -q -m "revert: memory promotion $ENTRY_ID") || true

echo "✅ reverted: $ENTRY_ID from $TARGET"
exit 0
