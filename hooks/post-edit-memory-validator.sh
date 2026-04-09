#!/usr/bin/env bash
# ~/.claude/hooks/post-edit-memory-validator.sh
# Non-blocking YAML validator for memory files. Warns on stderr, never fails.
# Always exits 0 — a typo must never block an in-progress session.

set -uo pipefail

HOOK_INPUT=$(cat)
TOOL_NAME=$(echo "$HOOK_INPUT" | jq -r '.tool_name // ""' 2>/dev/null || echo "")
FILE_PATH=$(echo "$HOOK_INPUT" | jq -r '.tool_input.file_path // ""' 2>/dev/null || echo "")

# Filter: only act on memory files (portable match: Unix / or Windows \)
case "$FILE_PATH" in
  */obsidiano/Claude/memory/*.md|*/.claude/projects/*/memory/*.md)
    ;;
  *)
    # Also try Windows-style paths with backslashes
    if echo "$FILE_PATH" | grep -qE "[/\\\\]obsidiano[/\\\\]Claude[/\\\\]memory[/\\\\]"; then
      :  # match, proceed
    else
      exit 0
    fi
    ;;
esac

# Validate YAML frontmatter
if [ -f "$FILE_PATH" ]; then
  MARKERS=$(head -20 "$FILE_PATH" | grep -c '^---$' || true)
  if [ "$MARKERS" -lt 2 ]; then
    echo "⚠️ memory-validator: YAML frontmatter missing or malformed in $FILE_PATH" >&2
  else
    # Auto-update last_updated
    TODAY=$(date +%Y-%m-%d)
    if grep -q "^last_updated:" "$FILE_PATH"; then
      sed -i.bak "s/^last_updated: .*/last_updated: $TODAY/" "$FILE_PATH" 2>/dev/null
      rm -f "$FILE_PATH.bak"
    fi
  fi

  # Auto-commit if in vault (portable path match: Unix / or Windows \ or mixed)
  if echo "$FILE_PATH" | grep -qE "[/\\\\]obsidiano[/\\\\]Claude[/\\\\]memory[/\\\\]"; then
    # Locate vault root by trimming everything from /Claude/memory/ onwards
    VAULT_DIR=$(echo "$FILE_PATH" | sed 's|[/\\]Claude[/\\]memory[/\\].*||')
    (cd "$VAULT_DIR" && git add "$FILE_PATH" && git commit -q -m "memory: auto-update $(basename "$FILE_PATH")" 2>/dev/null) || true
  fi
fi

exit 0
