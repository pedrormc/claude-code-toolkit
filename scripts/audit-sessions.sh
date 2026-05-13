#!/usr/bin/env bash
# audit-sessions.sh — verifica higiene de ~/.claude/sessions/:
#   - arquivos .tmp em diretório errado (scheduled em flat OU interactive vazio com pool flat=normal)
#   - arquivos > 30 dias ainda no flat pool (devem ir pra _archive)
#   - lock files staletype
#
# Flags: --fix  → auto-move arquivos misclassificados
# Saída: console + log em _archive/audit-sessions.log
#
# [Registrado por: DESKTOP — 2026-05-12]

set -uo pipefail
SESS="$HOME/.claude/sessions"
LOG="$HOME/.claude/_archive/audit-sessions.log"
mkdir -p "$SESS/scheduled" "$SESS/_archive" "$(dirname "$LOG")"

FIX=0
[[ "${1:-}" == "--fix" ]] && FIX=1

stamp() { date +"%Y-%m-%d %H:%M:%S"; }
echo "[$(stamp)] === audit-sessions.sh start (fix=$FIX) ===" | tee -a "$LOG"

problem_count=0
fix_count=0

# Check 1: scheduled-task .tmp files in FLAT pool (should be in scheduled/)
echo ""
echo "=== Misclassified files in flat pool ==="
for f in "$SESS"/*-session.tmp; do
  [[ -e "$f" ]] || continue
  if head -c 2048 "$f" | grep -q '<scheduled-task name=\|automated run of a scheduled task'; then
    echo "  MISCLASSIFIED (scheduled in flat): $(basename "$f")"
    ((problem_count++)) || true
    if [[ "$FIX" == 1 ]]; then
      mv "$f" "$SESS/scheduled/" && echo "    moved -> scheduled/" && ((fix_count++)) || true
    fi
  fi
done

# Check 2: interactive .tmp files in scheduled/ (should be in flat)
echo ""
echo "=== Misclassified files in scheduled/ ==="
for f in "$SESS/scheduled"/*-session.tmp; do
  [[ -e "$f" ]] || continue
  if ! head -c 2048 "$f" | grep -q '<scheduled-task name=\|automated run of a scheduled task'; then
    echo "  MISCLASSIFIED (interactive in scheduled/): $(basename "$f")"
    ((problem_count++)) || true
    if [[ "$FIX" == 1 ]]; then
      mv "$f" "$SESS/" && echo "    moved -> flat" && ((fix_count++)) || true
    fi
  fi
done

# Check 3: files >30 days still in flat pool
echo ""
echo "=== Old files (>30d) still in active flat pool ==="
THRESHOLD=$(date -d '30 days ago' +%s 2>/dev/null || date -v-30d +%s 2>/dev/null)
old_count=0
for f in "$SESS"/*-session.tmp; do
  [[ -e "$f" ]] || continue
  mtime=$(stat -c %Y "$f" 2>/dev/null || stat -f %m "$f" 2>/dev/null)
  if [[ -n "$mtime" && "$mtime" -lt "$THRESHOLD" ]]; then
    ((old_count++)) || true
    if [[ "$FIX" == 1 ]]; then
      mv "$f" "$SESS/_archive/" && ((fix_count++)) || true
    fi
  fi
done
echo "  old files: $old_count $([[ $FIX == 1 ]] && echo "(moved to _archive/)")"

# Check 4: stale lock
echo ""
echo "=== Stale scheduled_tasks.lock ==="
if [[ -f "$HOME/.claude/scheduled_tasks.lock" ]]; then
  pid=$(jq -r '.pid // empty' "$HOME/.claude/scheduled_tasks.lock" 2>/dev/null)
  if [[ -n "$pid" ]] && ! tasklist 2>/dev/null | awk '{print $2}' | grep -Fxq "$pid"; then
    echo "  STALE lock detected (pid $pid not running)"
    ((problem_count++)) || true
    if [[ "$FIX" == 1 ]]; then
      mv "$HOME/.claude/scheduled_tasks.lock" "$HOME/.claude/_archive/scheduled_tasks.lock.stale-$(date +%Y%m%d)" && ((fix_count++)) || true
      echo "    moved -> _archive/"
    fi
  fi
fi

# Summary
echo ""
echo "Summary: $problem_count problems found, $fix_count fixed"
echo "[$(stamp)] === audit-sessions.sh end (problems=$problem_count fixed=$fix_count) ===" >> "$LOG"
exit 0
