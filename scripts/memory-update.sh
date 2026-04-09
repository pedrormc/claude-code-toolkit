#!/usr/bin/env bash
# ~/.claude/scripts/memory-update.sh
# Unified API for writing to any of the 3 memory systems.

set -euo pipefail

if [ $# -lt 2 ]; then
  echo "Uso: memory-update {auto|claude|vault} <args>" >&2
  echo "  auto <type> <content>           - writes to auto-memory (per-cwd)" >&2
  echo "  claude <file> <content>         - writes to Claude/memory/ (vault)" >&2
  echo "  vault <relative-path> <content> - writes to vault humano" >&2
  exit 1
fi

SYSTEM="$1"; shift

case "${OSTYPE:-unknown}" in
  msys*|cygwin*|win32*) VAULT="$HOME/Documents/obsidiano" ;;
  *) VAULT="$HOME/obsidiano" ;;
esac
[ -d "$VAULT" ] || VAULT="$HOME/Documents/obsidiano"

case "$SYSTEM" in
  auto)
    TYPE="$1"; CONTENT="$2"
    CWD_HASH=$(pwd | sed 's/\//-/g; s/://g')
    DEST="$HOME/.claude/projects/$CWD_HASH/memory/${TYPE}_$(date +%s).md"
    mkdir -p "$(dirname "$DEST")"
    cat > "$DEST" <<EOF
---
name: $TYPE
description: Auto-update via memory-update.sh
type: $TYPE
scope: per-cwd
source: auto-memory
last_updated: $(date +%Y-%m-%d)
---

$CONTENT
EOF
    echo "wrote: $DEST"
    ;;
  claude)
    FILE="$1"; CONTENT="$2"
    DEST="$VAULT/Claude/memory/$FILE"
    [ -f "$DEST" ] || { echo "file not found: $DEST" >&2; exit 1; }
    case "$FILE" in
      decisions.md|people.md)
        printf "\n%s\n" "$CONTENT" >> "$DEST"
        ;;
      *)
        printf "%s" "$CONTENT" > "$DEST"
        ;;
    esac
    (cd "$VAULT" && git add "Claude/memory/$FILE" && git commit -q -m "memory: $FILE update" 2>/dev/null) || true
    echo "wrote: $DEST"
    ;;
  vault)
    FILE="$1"; CONTENT="$2"
    DEST="$VAULT/$FILE"
    mkdir -p "$(dirname "$DEST")"
    printf "\n%s\n" "$CONTENT" >> "$DEST"
    (cd "$VAULT" && git add "$FILE" && git commit -q -m "vault: $FILE update" 2>/dev/null) || true
    echo "wrote: $DEST"
    ;;
  *)
    echo "unknown system: $SYSTEM (expected auto|claude|vault)" >&2
    exit 1
    ;;
esac

exit 0
