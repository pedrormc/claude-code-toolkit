#!/bin/bash
# Claude Code Toolkit — Instalador Automatico
# Usage: bash install.sh [--force]
#
# Copia agents, rules, skills, scripts, statusline e configs para ~/.claude/
# Instala plugins via marketplace
# Flags:
#   --force   Sobrescreve arquivos existentes sem perguntar

set -euo pipefail

CLAUDE_DIR="$HOME/.claude"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

FORCE=false
[[ "${1:-}" == "--force" ]] && FORCE=true

log()  { printf "${GREEN}[OK]${NC} %s\n" "$1"; }
warn() { printf "${YELLOW}[!!]${NC} %s\n" "$1"; }
info() { printf "${CYAN}[>>]${NC} %s\n" "$1"; }
err()  { printf "${RED}[ERR]${NC} %s\n" "$1"; }

# ── Pre-checks ──

if ! command -v claude &>/dev/null; then
  err "Claude Code nao encontrado. Instale primeiro: https://docs.anthropic.com/en/docs/claude-code"
  exit 1
fi

if ! command -v node &>/dev/null; then
  err "Node.js nao encontrado. Instale v18+."
  exit 1
fi

CLAUDE_VERSION=$(claude --version 2>/dev/null || echo "unknown")
info "Claude Code detectado: $CLAUDE_VERSION"
info "Diretorio de instalacao: $CLAUDE_DIR"
echo ""

# ── Backup ──

if [[ -d "$CLAUDE_DIR" ]] && [[ "$FORCE" != true ]]; then
  BACKUP_DIR="$CLAUDE_DIR/backups/toolkit-$(date +%Y%m%d-%H%M%S)"
  mkdir -p "$BACKUP_DIR"

  # Backup existing configs
  for f in settings.json settings.local.json mcp.json statusline.sh; do
    [[ -f "$CLAUDE_DIR/$f" ]] && cp "$CLAUDE_DIR/$f" "$BACKUP_DIR/" 2>/dev/null || true
  done

  [[ -d "$CLAUDE_DIR/agents" ]] && cp -r "$CLAUDE_DIR/agents" "$BACKUP_DIR/" 2>/dev/null || true
  [[ -d "$CLAUDE_DIR/rules" ]] && cp -r "$CLAUDE_DIR/rules" "$BACKUP_DIR/" 2>/dev/null || true

  log "Backup criado em: $BACKUP_DIR"
fi

# ── Create directories ──

info "Criando diretorios..."
mkdir -p "$CLAUDE_DIR/agents"
mkdir -p "$CLAUDE_DIR/rules/common"
mkdir -p "$CLAUDE_DIR/rules/typescript"
mkdir -p "$CLAUDE_DIR/scripts/ralph"
mkdir -p "$CLAUDE_DIR/skills"

# ── Copy Agents ──

info "Instalando agents..."
cp "$SCRIPT_DIR/agents/"*.md "$CLAUDE_DIR/agents/"
log "5 agents instalados: api-specialist, devops-agent, frontend-specialist, prompt-engineer, research-agent"

# ── Copy Rules ──

info "Instalando rules..."
cp "$SCRIPT_DIR/rules/common/"*.md "$CLAUDE_DIR/rules/common/"
cp "$SCRIPT_DIR/rules/typescript/"*.md "$CLAUDE_DIR/rules/typescript/"
cp "$SCRIPT_DIR/rules/parallel-agents.md" "$CLAUDE_DIR/rules/"
log "15 rules instaladas (9 common + 5 typescript + 1 parallel-agents)"

# ── Copy Skills ──

info "Instalando skills..."
for skill_dir in "$SCRIPT_DIR/skills/"*/; do
  skill_name=$(basename "$skill_dir")
  mkdir -p "$CLAUDE_DIR/skills/$skill_name"
  cp "$skill_dir"* "$CLAUDE_DIR/skills/$skill_name/" 2>/dev/null || true
done
log "8 skills instalados (hubspot-mcp-expert + 7 n8n skills)"

# ── Copy Scripts ──

info "Instalando scripts..."
cp "$SCRIPT_DIR/scripts/claude-notify.js" "$CLAUDE_DIR/scripts/"
cp "$SCRIPT_DIR/scripts/toast-notify.js" "$CLAUDE_DIR/scripts/"
cp "$SCRIPT_DIR/scripts/ralph/"* "$CLAUDE_DIR/scripts/ralph/" 2>/dev/null || true
log "Scripts de notificacao e Ralph instalados"

# ── Copy Statusline ──

info "Instalando statusline..."
cp "$SCRIPT_DIR/statusline.sh" "$CLAUDE_DIR/statusline.sh"
chmod +x "$CLAUDE_DIR/statusline.sh"
log "Statusline customizada instalada"

# ── Copy Configs ──

info "Instalando configuracoes..."

if [[ "$FORCE" == true ]] || [[ ! -f "$CLAUDE_DIR/settings.json" ]]; then
  cp "$SCRIPT_DIR/config/settings.json" "$CLAUDE_DIR/settings.json"
  log "settings.json instalado"
else
  warn "settings.json ja existe. Use --force para sobrescrever (backup foi criado)"
fi

if [[ "$FORCE" == true ]] || [[ ! -f "$CLAUDE_DIR/settings.local.json" ]]; then
  cp "$SCRIPT_DIR/config/settings.local.json" "$CLAUDE_DIR/settings.local.json"
  log "settings.local.json instalado"
else
  warn "settings.local.json ja existe. Use --force para sobrescrever"
fi

if [[ ! -f "$CLAUDE_DIR/mcp.json" ]]; then
  cp "$SCRIPT_DIR/config/mcp.json" "$CLAUDE_DIR/mcp.json"
  warn "mcp.json instalado — EDITE com suas API keys antes de usar!"
else
  warn "mcp.json ja existe. Nao sobrescrevendo (pode conter suas API keys)"
fi

# ── Install Plugins ──

echo ""
info "Instalando plugins via marketplace..."

install_plugin() {
  local name="$1"
  local marketplace="$2"

  if claude plugins install "$name" --marketplace "$marketplace" 2>/dev/null; then
    log "Plugin instalado: $name"
  else
    warn "Plugin $name pode ja estar instalado ou falhou. Verifique manualmente."
  fi
}

install_plugin "everything-claude-code" "everything-claude-code"
install_plugin "superpowers" "superpowers-marketplace"
install_plugin "ralph-skills" "ralph-marketplace"
install_plugin "ui-ux-pro-max" "ui-ux-pro-max-skill"

# ── Install n8n-mcp ──

echo ""
info "Verificando n8n-mcp..."
if command -v n8n-mcp &>/dev/null || npm list -g n8n-mcp &>/dev/null 2>&1; then
  log "n8n-mcp ja instalado globalmente"
else
  info "Instalando n8n-mcp globalmente..."
  npm install -g n8n-mcp 2>/dev/null && log "n8n-mcp instalado" || warn "Falha ao instalar n8n-mcp. Instale manualmente: npm install -g n8n-mcp"
fi

# ── Summary ──

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
printf "${BOLD}${GREEN}  Instalacao concluida!${NC}\n"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
printf "  ${CYAN}Agents:${NC}     5 (api-specialist, devops, frontend, prompt-engineer, research)\n"
printf "  ${CYAN}Rules:${NC}      15 (9 common + 5 typescript + 1 parallel-agents)\n"
printf "  ${CYAN}Skills:${NC}     8 (1 hubspot + 7 n8n)\n"
printf "  ${CYAN}Plugins:${NC}    4 (ECC, Superpowers, Ralph, UI/UX Pro Max)\n"
printf "  ${CYAN}Scripts:${NC}    3 (notify, toast, ralph)\n"
printf "  ${CYAN}MCP:${NC}        2 (n8n, TestSprite)\n"
echo ""

if grep -q "YOUR_" "$CLAUDE_DIR/mcp.json" 2>/dev/null; then
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  printf "  ${YELLOW}ACAO NECESSARIA:${NC}\n"
  printf "  Edite ${BOLD}~/.claude/mcp.json${NC} e substitua os placeholders:\n"
  printf "    - YOUR_TESTSPRITE_API_KEY_HERE\n"
  printf "    - YOUR_N8N_INSTANCE_URL\n"
  printf "    - YOUR_N8N_API_KEY_HERE\n"
  printf "    - PATH_TO_N8N_MCP\n"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
fi

echo ""
printf "  Reinicie o Claude Code para aplicar todas as mudancas.\n"
echo ""
