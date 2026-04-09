#!/usr/bin/env bash
# ~/.claude/scripts/foundation-uninstall.sh
# Universal Foundation rollback — removes hooks, cron, preserves vault memory.

set -uo pipefail

echo "⚠️  Foundation uninstall — this will remove hooks and cron but keep vault memory."
read -r -p "Continue? (yes/N): " CONFIRM
[ "$CONFIRM" = "yes" ] || { echo "aborted"; exit 0; }

# Second-layer safety: backup current settings.json BEFORE restore (in case restore itself fails)
if [ -f ~/.claude/settings.json ]; then
  cp ~/.claude/settings.json ~/.claude/settings.json.uninstall-bak
  echo "✅ current settings saved to settings.json.uninstall-bak"
fi

# Restore settings.json from pre-foundation backup
if [ -f ~/.claude/settings.json.pre-foundation-bak ]; then
  cp ~/.claude/settings.json.pre-foundation-bak ~/.claude/settings.json
  echo "✅ restored settings.json from pre-foundation backup"
else
  echo "⚠️  no pre-foundation backup found — settings.json left as-is"
fi

# Delete hooks
rm -f ~/.claude/hooks/session-start-memory-loader.sh
rm -f ~/.claude/hooks/session-end-memory-writer.sh
rm -f ~/.claude/hooks/post-edit-memory-validator.sh
rm -f ~/.claude/hooks/save-session-vault-mirror.sh
echo "✅ removed hooks"

# Delete scripts (preserve memory-update.sh and memory-revert.sh as they may be in use)
rm -f ~/.claude/scripts/memory-auto-promote.sh
rm -f ~/.claude/scripts/memory-index-rebuild.sh
rm -f ~/.claude/scripts/foundation-smoke.sh
rm -f ~/.claude/scripts/foundation-validate.sh
rm -f ~/.claude/scripts/test-i4-fake-data.sh
echo "✅ removed scripts (kept memory-update.sh + memory-revert.sh)"

# Delete namespace cheatsheet
rm -f ~/.claude/rules/common/namespace-cheatsheet.md

# Delete cron / Task Scheduler entries
case "${OSTYPE:-unknown}" in
  msys*|cygwin*|win32*)
    schtasks /delete /tn "Claude Memory Auto-Promote" /f 2>/dev/null || true
    schtasks /delete /tn "Claude Memory Index Rebuild" /f 2>/dev/null || true
    echo "✅ removed Task Scheduler entries"
    ;;
  linux*)
    (crontab -l 2>/dev/null | grep -v "memory-auto-promote\|memory-index-rebuild") | crontab -
    echo "✅ removed cron entries"
    ;;
esac

echo ""
echo "Foundation hooks/scripts/rules removed."
echo "Vault memory PRESERVED at ~/Documents/obsidiano/Claude/"
echo "To fully remove vault memory: rm -rf ~/Documents/obsidiano/Claude/"
echo "To restore pre-Foundation state: git -C ~/Documents/obsidiano checkout pre-foundation-2026-04-09"
exit 0
