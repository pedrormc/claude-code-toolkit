#!/usr/bin/env bash
# ~/.claude/scripts/test-i4-fake-data.sh
# Creates 3 synthetic auto-memory entries in distinct fake project cwds,
# with mtimes older than 7 days, to exercise the auto-promote pipeline.

set -euo pipefail

PROJECTS="$HOME/.claude/projects"
TARGETS=(
  "$PROJECTS/fake-proj-alpha/memory"
  "$PROJECTS/fake-proj-beta/memory"
  "$PROJECTS/fake-proj-gamma/memory"
)

for dir in "${TARGETS[@]}"; do
  mkdir -p "$dir"
  cat > "$dir/feedback_lang.md" <<'EOF'
---
name: Communication style
description: PT-BR informal, sem emojis, direto
type: feedback
scope: per-cwd
source: auto-memory
last_updated: 2026-03-20
---

PT-BR informal, direto, sem emojis a menos que explicitamente solicitado.
EOF
  touch -d "14 days ago" "$dir/feedback_lang.md"
done

echo "✅ 3 synthetic entries created (14 days old)"
echo ""
echo "Next steps:"
echo "  bash ~/.claude/scripts/memory-auto-promote.sh"
echo "  grep -A5 'auto_promoted: true' ~/Documents/obsidiano/Claude/memory/preferences.md"
echo "  tail -3 ~/Documents/obsidiano/Claude/memory/.promotion-log.jsonl"
echo ""
echo "Cleanup after test:"
echo "  rm -rf $PROJECTS/fake-proj-{alpha,beta,gamma}"
