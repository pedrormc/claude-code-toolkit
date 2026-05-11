#!/usr/bin/env bash
# obsidian-auto-save.sh
# SessionEnd (and fallback Stop) hook — appends a compact recap of the current
# Claude Code session to today's daily note in the Obsidian vault.
#
# Behaviour rules:
#   * silent: never prints to stdout/stderr (would leak into TUI)
#   * idempotent: marks the session as already-saved via a marker file so
#     re-firing the hook in the same session does not duplicate content
#   * skips trivial sessions (<2 user turns) and sessions with no real user text
#   * never copies secrets — relies on the deterministic formatter which only
#     touches session metadata (tool counts, file paths, command names,
#     user prompt SAMPLES), so sensitive tool outputs never enter the note
#
# Payload received on stdin (JSON, from Claude Code):
#   { "session_id": "...", "transcript_path": "...",
#     "hook_event_name": "SessionEnd"|"Stop", "reason": "exit|clear|logout|..." }

set -uo pipefail

# Mute everything — a hook that prints breaks the TUI and can trigger re-runs
exec >/dev/null 2>&1

PAYLOAD=$(cat)

# Extract JSON fields using Node (no jq dependency on Windows)
SESSION_ID=$(printf '%s' "$PAYLOAD" | node -e 'let d="";process.stdin.on("data",c=>d+=c).on("end",()=>{try{process.stdout.write(String(JSON.parse(d).session_id||""))}catch{}})')
REASON=$(printf '%s' "$PAYLOAD" | node -e 'let d="";process.stdin.on("data",c=>d+=c).on("end",()=>{try{process.stdout.write(String(JSON.parse(d).reason||""))}catch{}})')
EVENT=$(printf '%s' "$PAYLOAD" | node -e 'let d="";process.stdin.on("data",c=>d+=c).on("end",()=>{try{process.stdout.write(String(JSON.parse(d).hook_event_name||""))}catch{}})')

[ -z "$SESSION_ID" ] && exit 0

# Skip on `clear` — user is resetting conversation, not ending the day
if [ "$REASON" = "clear" ]; then exit 0; fi

# Only act on real session endings to avoid firing on every assistant turn
if [ "$EVENT" = "Stop" ] && [ "$REASON" != "exit" ] && [ "$REASON" != "logout" ]; then
  exit 0
fi

case "${OSTYPE:-unknown}" in
  msys*|cygwin*|win32*) VAULT="$HOME/Documents/obsidiano" ;;
  *) VAULT="$HOME/obsidiano" ;;
esac
[ -d "$VAULT" ] || VAULT="$HOME/Documents/obsidiano"
[ -d "$VAULT" ] || exit 0

DIARY_DIR="$VAULT/Diário"
mkdir -p "$DIARY_DIR"
DATE=$(date +%Y-%m-%d)
DAILY="$DIARY_DIR/${DATE}.md"

# Idempotency marker per session — avoid duplicate appends if the hook fires twice
MARKER_DIR="$HOME/.claude/projects/C--Users-teste/tool-results"
mkdir -p "$MARKER_DIR"
MARKER="$MARKER_DIR/obsidian-autosave-${SESSION_ID}.done"
[ -f "$MARKER" ] && exit 0

# Render recap. Formatter returns empty when session has no meaningful content.
RECAP=$(node "$HOME/.claude/scripts/obsidian-session-format.js" --auto "$SESSION_ID" 2>/dev/null)
[ -z "$RECAP" ] && exit 0

# Create daily from scratch if missing
if [ ! -f "$DAILY" ]; then
  {
    printf '# %s — Recap do dia\n\n' "$DATE"
  } > "$DAILY"
fi

{
  printf '\n'
  printf '%s\n' "$RECAP"
  printf '\n'
} >> "$DAILY"

touch "$MARKER"
exit 0
