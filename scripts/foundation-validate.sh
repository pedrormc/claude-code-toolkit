#!/usr/bin/env bash
# ~/.claude/scripts/foundation-validate.sh
# Runs foundation-smoke.sh + 7 integration tests (I1-I7 from spec §8.3).

set +e

echo "=== Stage 1: Smoke tests ==="
~/.claude/scripts/foundation-smoke.sh
SMOKE_RC=$?
if [ "$SMOKE_RC" -ne 0 ]; then
  echo "❌ Smoke failed — integration skipped"
  exit 1
fi

echo ""
echo "=== Stage 2: Integration tests ==="

# I1: Memory loader output complete
OUT=$(bash ~/.claude/hooks/session-start-memory-loader.sh 2>&1)
if echo "$OUT" | grep -q "STANDING ORDERS" && ! echo "$OUT" | grep -q "ARQUIVO AUSENTE"; then
  echo "✅ I1: Memory loader output complete"
else
  echo "❌ I1: Memory loader output missing sections or has missing files"
fi

# I2-I7 are interactive or require real Claude sessions — print instructions
cat <<'MANUAL'

=== Stage 3: Manual integration tests (run these interactively) ===

I2: Open `claude`, ask "o que você sabe sobre mim?"
    Expected: response cites CTO Singular, pedrormc, TRIFORCE, 3 envs

I3: Edit Claude/memory/active.md via Edit tool in a claude session.
    Expected: git log -1 in vault shows auto-commit within seconds.

I4: Run ~/.claude/scripts/test-i4-fake-data.sh (spec §8.3.1)
    Expected: promotion in preferences.md, .promotion-log.jsonl updated.

I5: Run memory-revert with the entry_id from I4.
    Expected: entry removed from preferences.md, log marked reverted.

I6: touch ~/Documents/obsidiano/Claude/memory/fake.md && ~/.claude/scripts/memory-index-rebuild.sh
    Expected: INDEX.md contains reference to fake.md. Cleanup: rm fake.md + re-run rebuild.

I7: Open `claude`, type `/`.
    Expected: list includes /office-hours, /autoplan, /review, /ship, /qa, /cso
MANUAL

exit 0
