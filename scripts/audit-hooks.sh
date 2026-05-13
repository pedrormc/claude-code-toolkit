#!/usr/bin/env bash
# audit-hooks.sh — smoke-tests pra todos os hooks declarados em settings.json.
# Rota: roda sob demanda OU agendado (Task Scheduler).
# Saída: linha por hook com PASS/FAIL/SKIP.
# Exit 0 sempre (não falha workflows que dependem dele).
#
# [Registrado por: DESKTOP — 2026-05-12]

set -uo pipefail
SETTINGS="$HOME/.claude/settings.json"
LOG="$HOME/.claude/_archive/audit-hooks.log"
mkdir -p "$(dirname "$LOG")"

stamp() { date +"%Y-%m-%d %H:%M:%S"; }
RESULT_OK=0
RESULT_FAIL=0
RESULT_SKIP=0

declare -a RESULTS=()

run_test() {
  local name="$1"; local cmd="$2"; local expect="$3"
  local actual
  actual=$(eval "$cmd" 2>&1 || true)
  if echo "$actual" | grep -q "$expect"; then
    RESULTS+=("  PASS  $name")
    ((RESULT_OK++)) || true
  else
    RESULTS+=("  FAIL  $name (expected: $expect)")
    ((RESULT_FAIL++)) || true
  fi
}

skip_test() {
  RESULTS+=("  SKIP  $1 ($2)")
  ((RESULT_SKIP++)) || true
}

echo "[$(stamp)] === audit-hooks.sh start ===" | tee -a "$LOG"

# ============ Smoke tests ============

# 1. settings.json syntax
if jq -e . "$SETTINGS" >/dev/null 2>&1; then
  RESULTS+=("  PASS  settings.json JSON syntax")
  ((RESULT_OK++)) || true
else
  RESULTS+=("  FAIL  settings.json JSON syntax (BLOCKER — fix immediately)")
  ((RESULT_FAIL++)) || true
fi

# 2. verify-ecc-patches.sh present + ECC patches in place
if [[ -x "$HOME/.claude/hooks/verify-ecc-patches.sh" ]]; then
  ECC_PRIMARY="$HOME/.claude/plugins/cache/everything-claude-code/everything-claude-code/1.8.0/scripts/hooks/session-start.js"
  if grep -q "PATCH 2026-05-12 \[DESKTOP\]: filter scheduled-task" "$ECC_PRIMARY" 2>/dev/null; then
    RESULTS+=("  PASS  ECC session-start.js patched (filter scheduled-task)")
    ((RESULT_OK++)) || true
  else
    RESULTS+=("  FAIL  ECC patch MISSING — run verify-ecc-patches.sh")
    ((RESULT_FAIL++)) || true
  fi
else
  skip_test "ECC patch verify" "verify-ecc-patches.sh not executable"
fi

# 3. claude-notify.js (Notification hook)
if [[ -f "$HOME/.claude/scripts/claude-notify.js" ]]; then
  if echo '{"hook_event_name":"Notification","notification_type":"test"}' | timeout 5 node "$HOME/.claude/scripts/claude-notify.js" >/dev/null 2>&1; then
    RESULTS+=("  PASS  claude-notify.js (Notification)")
    ((RESULT_OK++)) || true
  else
    RESULTS+=("  FAIL  claude-notify.js exited non-zero (exit/timeout)")
    ((RESULT_FAIL++)) || true
  fi
else
  skip_test "claude-notify.js" "file missing"
fi

# 4. session-end-memory-writer (Stop hook) — checked it has new truncation logic
if grep -q "count < keep" "$HOME/.claude/hooks/session-end-memory-writer.sh" 2>/dev/null; then
  RESULTS+=("  PASS  session-end-memory-writer.sh has truncation patch")
  ((RESULT_OK++)) || true
else
  RESULTS+=("  FAIL  session-end-memory-writer.sh missing truncation patch")
  ((RESULT_FAIL++)) || true
fi

# 5. obsidian-auto-save.sh — dry-run via Stop reason!=exit (should exit 0 noop)
if [[ -x "$HOME/.claude/hooks/obsidian-auto-save.sh" ]]; then
  exitcode=$(echo '{"hook_event_name":"Stop","reason":"completed","session_id":"audit"}' | timeout 10 "$HOME/.claude/hooks/obsidian-auto-save.sh" >/dev/null 2>&1; echo $?)
  if [[ "$exitcode" == "0" ]]; then
    RESULTS+=("  PASS  obsidian-auto-save.sh noop on Stop completed")
    ((RESULT_OK++)) || true
  else
    RESULTS+=("  FAIL  obsidian-auto-save.sh non-zero on Stop completed (exit=$exitcode)")
    ((RESULT_FAIL++)) || true
  fi
else
  skip_test "obsidian-auto-save.sh" "not executable"
fi

# 6. post-edit-memory-validator.sh — silent on non-memory file
if [[ -x "$HOME/.claude/hooks/post-edit-memory-validator.sh" ]]; then
  output=$(echo '{"tool_input":{"file_path":"/tmp/random.md"}}' | timeout 5 "$HOME/.claude/hooks/post-edit-memory-validator.sh" 2>&1)
  if [[ -z "$output" ]]; then
    RESULTS+=("  PASS  post-edit-memory-validator silent on non-memory file")
    ((RESULT_OK++)) || true
  else
    RESULTS+=("  FAIL  post-edit-memory-validator spoke when should be silent: $output")
    ((RESULT_FAIL++)) || true
  fi
else
  skip_test "post-edit-memory-validator.sh" "not executable"
fi

# 7. save-session-vault-mirror.sh — idempotent
if [[ -x "$HOME/.claude/hooks/save-session-vault-mirror.sh" ]]; then
  if timeout 5 "$HOME/.claude/hooks/save-session-vault-mirror.sh" >/dev/null 2>&1; then
    RESULTS+=("  PASS  save-session-vault-mirror.sh runs without error")
    ((RESULT_OK++)) || true
  else
    RESULTS+=("  FAIL  save-session-vault-mirror.sh errored")
    ((RESULT_FAIL++)) || true
  fi
else
  skip_test "save-session-vault-mirror.sh" "not executable"
fi

# 8. any-buddy binary present (SessionStart secondary)
if command -v any-buddy >/dev/null 2>&1 || [[ -f "$HOME/AppData/Roaming/npm/any-buddy.cmd" ]]; then
  RESULTS+=("  PASS  any-buddy binary present")
  ((RESULT_OK++)) || true
else
  RESULTS+=("  FAIL  any-buddy binary NOT found — hook will fail silently")
  ((RESULT_FAIL++)) || true
fi

# 9. session-start-memory-loader.sh present + runs
if [[ -x "$HOME/.claude/hooks/session-start-memory-loader.sh" ]]; then
  if echo '{"hook_event_name":"SessionStart","cwd":"'"$PWD"'"}' | timeout 10 "$HOME/.claude/hooks/session-start-memory-loader.sh" >/dev/null 2>&1; then
    RESULTS+=("  PASS  session-start-memory-loader.sh runs ok")
    ((RESULT_OK++)) || true
  else
    RESULTS+=("  FAIL  session-start-memory-loader.sh errored")
    ((RESULT_FAIL++)) || true
  fi
else
  skip_test "session-start-memory-loader.sh" "not executable"
fi

# 10. statusline.sh — should respond to JSON stdin
if [[ -f "$HOME/.claude/statusline.sh" ]]; then
  output=$(echo '{"model":{"display_name":"test"},"workspace":{"current_dir":"/tmp"},"transcript_path":"/tmp/x.jsonl"}' | timeout 5 bash "$HOME/.claude/statusline.sh" 2>&1)
  if [[ -n "$output" ]]; then
    RESULTS+=("  PASS  statusline.sh produces output")
    ((RESULT_OK++)) || true
  else
    RESULTS+=("  FAIL  statusline.sh empty output")
    ((RESULT_FAIL++)) || true
  fi
fi

# 11. active.md not bloated (<= 50 lines is sane)
ACTIVE_LINES=$(wc -l < "$HOME/Documents/obsidiano/Claude/memory/active.md" 2>/dev/null || echo 0)
if [[ "$ACTIVE_LINES" -le 50 ]]; then
  RESULTS+=("  PASS  active.md size $ACTIVE_LINES lines (under 50)")
  ((RESULT_OK++)) || true
else
  RESULTS+=("  FAIL  active.md bloated: $ACTIVE_LINES lines (>50)")
  ((RESULT_FAIL++)) || true
fi

# 12. No stale scheduled_tasks.lock
if [[ -f "$HOME/.claude/scheduled_tasks.lock" ]]; then
  pid=$(jq -r '.pid // empty' "$HOME/.claude/scheduled_tasks.lock" 2>/dev/null)
  if [[ -n "$pid" ]] && tasklist 2>/dev/null | awk '{print $2}' | grep -Fxq "$pid"; then
    RESULTS+=("  PASS  scheduled_tasks.lock pid $pid alive")
    ((RESULT_OK++)) || true
  else
    RESULTS+=("  FAIL  stale scheduled_tasks.lock (pid $pid not running)")
    ((RESULT_FAIL++)) || true
  fi
else
  RESULTS+=("  PASS  no scheduled_tasks.lock (no scheduled task running)")
  ((RESULT_OK++)) || true
fi

# 13. ECC patch verifier exit
if "$HOME/.claude/hooks/verify-ecc-patches.sh" >/dev/null 2>&1; then
  RESULTS+=("  PASS  verify-ecc-patches.sh exits ok")
  ((RESULT_OK++)) || true
else
  RESULTS+=("  FAIL  verify-ecc-patches.sh errored")
  ((RESULT_FAIL++)) || true
fi

# ============ Print results ============
echo ""
printf '%s\n' "${RESULTS[@]}"
echo ""
echo "Summary: $RESULT_OK passed, $RESULT_FAIL failed, $RESULT_SKIP skipped"
echo "[$(stamp)] === audit-hooks.sh end (ok=$RESULT_OK fail=$RESULT_FAIL skip=$RESULT_SKIP) ===" >> "$LOG"
printf '%s\n' "${RESULTS[@]}" >> "$LOG"

exit 0
