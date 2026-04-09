#!/usr/bin/env bash
# ~/.claude/scripts/foundation-smoke.sh
# Runs all 13 Foundation smoke tests (spec §8.2).

set +e  # don't exit on first failure — we want to run all tests

PASS=0
FAIL=0
declare -a FAILED_TESTS

run_test() {
  local num="$1"
  local name="$2"
  local cmd="$3"
  local check="$4"

  local result
  result=$(eval "$cmd" 2>&1)
  if echo "$result" | eval "$check" >/dev/null 2>&1; then
    echo "✅ S$num: $name"
    PASS=$((PASS + 1))
  else
    echo "❌ S$num: $name"
    FAILED_TESTS+=("S$num: $name — $result")
    FAIL=$((FAIL + 1))
  fi
}

# Resolve vault path (portable)
case "${OSTYPE:-unknown}" in
  msys*|cygwin*|win32*) VAULT="$HOME/Documents/obsidiano" ;;
  *) VAULT="$HOME/obsidiano" ;;
esac
[ -d "$VAULT" ] || VAULT="$HOME/Documents/obsidiano"

echo "=== Foundation Smoke Tests (13) ==="
echo ""

run_test 1 "Vault CLAUDE.md is loader" \
  "head -5 '$VAULT/CLAUDE.md'" \
  "grep -q 'Vault Claude Instructions'"

run_test 2 "Claude/CLAUDE.md exists" \
  "test -f '$VAULT/Claude/CLAUDE.md' && echo ok" \
  "grep -q ok"

run_test 3 "Zel persona extracted" \
  "head -10 '$VAULT/Claude/personas/zel.md'" \
  "grep -qi 'zel'"

run_test 4 "6 memory files populated" \
  "find '$VAULT/Claude/memory' -maxdepth 1 -name '*.md' | wc -l" \
  "awk '{exit !(\$1 >= 6)}'"

run_test 5 "active.md has real sections" \
  "grep -c '^##' '$VAULT/Claude/memory/active.md'" \
  "awk '{exit !(\$1 >= 3)}'"

run_test 6 "INDEX.md auto_generated" \
  "cat '$VAULT/Claude/memory/INDEX.md'" \
  "grep -q 'auto_generated: true'"

run_test 7 "Gstack installed" \
  "ls ~/.claude/plugins/ 2>/dev/null | grep -c gstack; ls ~/.claude/skills/ 2>/dev/null | grep -c gstack" \
  "awk 'BEGIN{t=0} {t+=\$1} END{exit !(t >= 1)}'"

run_test 8 "SessionStart hook exists" \
  "test -x ~/.claude/hooks/session-start-memory-loader.sh && echo ok" \
  "grep -q ok"

run_test 9 "Session-end hook exists" \
  "test -x ~/.claude/hooks/session-end-memory-writer.sh && echo ok" \
  "grep -q ok"

run_test 10 "Ralph disabled (jq strict)" \
  "jq -e '.disabledPlugins | any(. | test(\"ralph\"; \"i\"))' ~/.claude/settings.json 2>/dev/null && echo ok" \
  "grep -q ok"

run_test 11 "Namespace rule exists" \
  "test -f ~/.claude/rules/common/namespace-cheatsheet.md && echo ok" \
  "grep -q ok"

run_test 12 "MCPVault configured" \
  "(jq -e '.mcpServers.obsidian.command // .mcpServers.MCPVault.command' ~/.claude/mcp.json 2>/dev/null || jq -e '.mcpServers.obsidian.command // .mcpServers.MCPVault.command' ~/.claude.json 2>/dev/null) && echo ok" \
  "grep -q ok"

run_test 13 "Auto-promote script exists" \
  "test -x ~/.claude/scripts/memory-auto-promote.sh && echo ok" \
  "grep -q ok"

echo ""
echo "=== Results: $PASS passed / $FAIL failed ==="

if [ "$FAIL" -gt 0 ]; then
  echo ""
  echo "Failures:"
  for t in "${FAILED_TESTS[@]}"; do
    echo "  $t"
  done
  exit 1
fi

exit 0
