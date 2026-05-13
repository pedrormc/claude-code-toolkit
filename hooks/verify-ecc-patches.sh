#!/usr/bin/env bash
# verify-ecc-patches.sh — auto-reaplica patches do ECC se um update os sobrescreveu.
# Hooked em SessionStart (síncrono, timeout curto).
#
# Patches verificados:
#   1. session-start.js filter pra scheduled-task summaries
#
# Falha modo: fail-open (sai 0 mesmo se a re-aplicação falhar, só loga em $LOG)
#
# [Registrado por: DESKTOP — 2026-05-12]

set -uo pipefail
LOG="$HOME/.claude/_archive/verify-ecc-patches.log"
mkdir -p "$(dirname "$LOG")"

stamp() { date +"%Y-%m-%d %H:%M:%S"; }
log() { echo "[$(stamp)] $*" >> "$LOG"; }

PATCH_MARKER='PATCH 2026-05-12 \[DESKTOP\]: filter scheduled-task summaries'

declare -a TARGETS=(
  "$HOME/.claude/plugins/marketplaces/everything-claude-code/scripts/hooks/session-start.js"
  "$HOME/.claude/plugins/cache/everything-claude-code/everything-claude-code/1.8.0/scripts/hooks/session-start.js"
)

reapply_session_start() {
  local target="$1"
  log "Re-applying session-start.js filter on: $target"
  # Backup pre-reapply
  cp "$target" "${target}.pre-reapply-$(date +%Y%m%d-%H%M%S)" 2>/dev/null

  # Use sed to inject filter (multi-line). Posix-safe.
  # We replace the `const recentSessions = findFiles(sessionsDir, '*-session.tmp', { maxAge: 7 });`
  # line with the filtered version.
  python -c "
import sys, re
p = '$target'
with open(p, 'r', encoding='utf-8') as f:
    content = f.read()
if 'PATCH 2026-05-12 [DESKTOP]: filter scheduled-task summaries' in content:
    print('already patched')
    sys.exit(0)
old = \"  const recentSessions = findFiles(sessionsDir, '*-session.tmp', { maxAge: 7 });\"
new = (
    \"  // PATCH 2026-05-12 [DESKTOP]: filter scheduled-task summaries — see ~/.claude/patches/ecc-session-start-filter.md\n\"
    \"  const allRecent = findFiles(sessionsDir, '*-session.tmp', { maxAge: 7 });\n\"
    \"  const recentSessions = allRecent.filter(s => {\n\"
    \"    const c = readFile(s.path) || '';\n\"
    \"    return !c.includes('<scheduled-task name=') &&\n\"
    \"           !c.includes('automated run of a scheduled task');\n\"
    \"  });\"
)
if old not in content:
    print('skip (anchor missing)')
    sys.exit(0)
content = content.replace(old, new, 1)
with open(p, 'w', encoding='utf-8') as f:
    f.write(content)
print('patched')
" 2>>"$LOG" || log "re-apply failed: $target"
}

for tgt in "${TARGETS[@]}"; do
  if [[ ! -f "$tgt" ]]; then
    log "skip (not found): $tgt"
    continue
  fi
  if grep -q "PATCH 2026-05-12 \[DESKTOP\]: filter scheduled-task summaries" "$tgt"; then
    : # ok
  else
    log "PATCH MISSING on: $tgt — re-applying"
    reapply_session_start "$tgt"
  fi
done

exit 0
