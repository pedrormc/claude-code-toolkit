#!/usr/bin/env bash
# ~/.claude/hooks/session-start-memory-loader.sh
# Loads unified memory (vault + auto-memory) into session context.
# Failure-tolerant: always exits 0. See spec §7.2.

set -uo pipefail

LOG="$HOME/.claude/hooks/session-start-memory-loader.log"

log_err() {
  echo "[$(date -Iseconds)] $1" >> "$LOG"
}

safe_cat() {
  if [ -f "$1" ]; then
    cat "$1"
  else
    echo "<!-- ARQUIVO AUSENTE: $1 -->"
    log_err "missing: $1"
  fi
}

# Detect OS to locate vault (use default expansion to prevent nounset errors)
case "${OSTYPE:-unknown}" in
  msys*|cygwin*|win32*)
    VAULT="$HOME/Documents/obsidiano"
    ;;
  linux*)
    if [ -d "/data/data/com.termux" ]; then
      VAULT="$HOME/obsidiano"
    else
      VAULT="$HOME/obsidiano"
    fi
    ;;
  *)
    VAULT="$HOME/Documents/obsidiano"
    ;;
esac

# Check vault reachability
if [ ! -d "$VAULT/Claude" ]; then
  cat <<DEGRADED
=== ⚠️ MEMORY LOADER DEGRADED — partial context only ===
Reason: vault Claude/ directory not found at $VAULT/Claude
Full log: $LOG
DEGRADED
  log_err "vault unreachable: $VAULT/Claude"
  exit 0
fi

# Compute cwd hash for auto-memory lookup
CWD_HASH=$(pwd | sed 's/\//-/g; s/://g')
PROJECT_MEM="$HOME/.claude/projects/$CWD_HASH/memory"

cat <<HEADER
=== 🧠 MEMÓRIA UNIFICADA (carregada em $(date +%Y-%m-%dT%H:%M:%S)) ===

> Fontes: vault Obsidian ($VAULT) + auto-memory do harness ($PROJECT_MEM)
> Edições devem usar memory-update.sh, NÃO Edit direto.

=== 📜 STANDING ORDERS (Claude/CLAUDE.md) ===
HEADER

safe_cat "$VAULT/Claude/CLAUDE.md"

echo ""
echo "=== 🗺️ INDEX MEMÓRIA UNIFICADA (Claude/memory/INDEX.md) ==="
safe_cat "$VAULT/Claude/memory/INDEX.md"

echo ""
echo "=== 🧠 CLAUDE MEMORY (global, 6 arquivos) ==="
for f in user preferences active decisions people projects; do
  echo ""
  echo "--- Claude/memory/$f.md ---"
  safe_cat "$VAULT/Claude/memory/$f.md"
done

echo ""
echo "=== 🤖 AUTO-MEMORY (cwd: $(pwd)) ==="
if [ -d "$PROJECT_MEM" ]; then
  for f in "$PROJECT_MEM"/*.md; do
    [ -f "$f" ] || continue
    echo ""
    echo "--- $(basename "$f") ---"
    cat "$f"
  done
else
  echo "(sem auto-memory pra este cwd ainda)"
fi

echo ""
echo "=== FIM DA MEMÓRIA UNIFICADA ==="
exit 0
