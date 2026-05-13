#!/usr/bin/env bash
# sync-triforce.sh — propaga mudanças do Desktop (SoT) pros ambientes Mobile e VPS.
# Mecanismo: git push do toolkit + scp dos hooks/scripts críticos.
#
# Uso:
#   sync-triforce.sh status         → mostra divergências entre Desktop/Mobile/VPS
#   sync-triforce.sh push --dry-run → simula propagação
#   sync-triforce.sh push           → propaga real (precisa SSH configurado)
#
# Hosts:
#   vps        → admin@<lightsail-ip>  (Lightsail)
#   vps-claude → root@<digitalocean-ip> (DigitalOcean)
#   mobile     → SEM SSH (Termux); usa git pull manual
#
# [Registrado por: DESKTOP — 2026-05-12]

set -uo pipefail
CMD="${1:-status}"
DRY="${2:-}"

OPENSSH="/c/Windows/System32/OpenSSH/ssh.exe"
[[ ! -x "$OPENSSH" ]] && OPENSSH="ssh"

CRITICAL_HOOKS=(
  "$HOME/.claude/hooks/verify-ecc-patches.sh"
  "$HOME/.claude/hooks/session-start-memory-loader.sh"
  "$HOME/.claude/hooks/session-end-memory-writer.sh"
  "$HOME/.claude/hooks/save-session-vault-mirror.sh"
  "$HOME/.claude/hooks/post-edit-memory-validator.sh"
  "$HOME/.claude/hooks/obsidian-auto-save.sh"
)

CRITICAL_SCRIPTS=(
  "$HOME/.claude/scripts/audit-hooks.sh"
  "$HOME/.claude/scripts/audit-sessions.sh"
  "$HOME/.claude/scripts/memory-update.sh"
  "$HOME/.claude/scripts/memory-revert.sh"
)

CRITICAL_RULES_DIR="$HOME/.claude/rules"

show_status() {
  echo "=== TRIFORCE Status ==="
  echo ""
  echo "Desktop (this): $(uname -a)"
  echo "Critical hooks present:"
  for h in "${CRITICAL_HOOKS[@]}"; do
    [[ -f "$h" ]] && echo "  OK $h" || echo "  MISSING $h"
  done
  echo ""
  echo "VPS reachable:"
  $OPENSSH -o ConnectTimeout=5 -o BatchMode=yes vps "echo OK" 2>&1 | head -3 || true
  $OPENSSH -o ConnectTimeout=5 -o BatchMode=yes vps-claude "echo OK" 2>&1 | head -3 || true
  echo ""
  echo "Last sync (per log):"
  tail -3 "$HOME/.claude/_archive/sync-triforce.log" 2>/dev/null || echo "  never"
}

push_to_vps() {
  local target="$1"  # "vps" or "vps-claude"
  local dry="$2"
  echo ""
  echo "=== Pushing to $target ==="

  if [[ "$dry" == "--dry-run" ]]; then
    echo "  DRY: would scp ${#CRITICAL_HOOKS[@]} hooks to $target:~/.claude/hooks/"
    echo "  DRY: would scp ${#CRITICAL_SCRIPTS[@]} scripts to $target:~/.claude/scripts/"
    echo "  DRY: would rsync rules/ to $target:~/.claude/rules/"
    return 0
  fi

  if ! $OPENSSH -o ConnectTimeout=5 -o BatchMode=yes "$target" "echo OK" >/dev/null 2>&1; then
    echo "  SKIP: $target not reachable"
    return 1
  fi

  # Use scp via OpenSSH
  local SCP=$(dirname "$OPENSSH")/scp.exe
  [[ ! -x "$SCP" ]] && SCP="scp"

  for h in "${CRITICAL_HOOKS[@]}"; do
    [[ -f "$h" ]] && "$SCP" -q "$h" "$target:~/.claude/hooks/$(basename "$h")" 2>&1 | head -3
  done
  for s in "${CRITICAL_SCRIPTS[@]}"; do
    [[ -f "$s" ]] && "$SCP" -q "$s" "$target:~/.claude/scripts/$(basename "$s")" 2>&1 | head -3
  done

  echo "  ECC patch metadata: $(basename ~/.claude/patches/ecc-session-start-filter.md)"
  "$SCP" -q ~/.claude/patches/ecc-session-start-filter.md "$target:~/.claude/patches/" 2>&1 | head -3

  echo "[$(date +%Y-%m-%dT%H:%M)] sync $target ok" >> "$HOME/.claude/_archive/sync-triforce.log"
}

case "$CMD" in
  status)
    show_status
    ;;
  push)
    push_to_vps vps "$DRY"
    push_to_vps vps-claude "$DRY"
    echo ""
    echo "Mobile: SEM SSH. Pra sincronizar Mobile, manualmente:"
    echo "  No Termux: cd ~/triforce-toolkit && git pull"
    echo "  Toolkit repo: github.com/pedrormc/claude-code-toolkit"
    ;;
  *)
    echo "Usage: sync-triforce.sh {status|push [--dry-run]}"
    exit 2
    ;;
esac

exit 0
