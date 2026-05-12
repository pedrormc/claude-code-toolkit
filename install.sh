#!/bin/bash
# Claude Code Toolkit — Instalador Automatico
# Usage: bash install.sh [--force]
#
# Copia agents, rules, skills, scripts, statusline, teams, scheduled-tasks,
# templates e configs para ~/.claude/
# Instala plugins via marketplace
#
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

ERRORS=0
WARNINGS=0

log()  { printf "${GREEN}[OK]${NC} %s\n" "$1"; }
warn() { printf "${YELLOW}[!!]${NC} %s\n" "$1"; WARNINGS=$((WARNINGS + 1)); }
info() { printf "${CYAN}[>>]${NC} %s\n" "$1"; }
err()  { printf "${RED}[ERR]${NC} %s\n" "$1"; ERRORS=$((ERRORS + 1)); }
fail() { printf "${RED}[FATAL]${NC} %s\n" "$1"; exit 1; }

# ── Pre-checks ──

echo ""
printf "${BOLD}Claude Code Toolkit — Instalador${NC}\n"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if ! command -v claude &>/dev/null; then
  fail "Claude Code nao encontrado. Instale primeiro: https://docs.anthropic.com/en/docs/claude-code"
fi

if ! command -v node &>/dev/null; then
  fail "Node.js nao encontrado. Instale v18+."
fi

if ! command -v git &>/dev/null; then
  fail "Git nao encontrado."
fi

# Detect platform
OS="unknown"
case "$(uname -s)" in
  Linux*)   OS="linux";;
  Darwin*)  OS="macos";;
  MINGW*|MSYS*|CYGWIN*) OS="windows";;
esac

CLAUDE_VERSION=$(claude --version 2>/dev/null || echo "unknown")
info "Claude Code: $CLAUDE_VERSION"
info "Plataforma: $OS"
info "Destino: $CLAUDE_DIR"
echo ""

# ── Backup ──

if [[ -d "$CLAUDE_DIR" ]] && [[ "$FORCE" != true ]]; then
  BACKUP_DIR="$CLAUDE_DIR/backups/toolkit-$(date +%Y%m%d-%H%M%S)"
  mkdir -p "$BACKUP_DIR"

  for f in settings.json settings.local.json mcp.json statusline.sh; do
    [[ -f "$CLAUDE_DIR/$f" ]] && cp "$CLAUDE_DIR/$f" "$BACKUP_DIR/" 2>/dev/null || true
  done

  [[ -d "$CLAUDE_DIR/agents" ]] && cp -r "$CLAUDE_DIR/agents" "$BACKUP_DIR/" 2>/dev/null || true
  [[ -d "$CLAUDE_DIR/rules" ]] && cp -r "$CLAUDE_DIR/rules" "$BACKUP_DIR/" 2>/dev/null || true
  [[ -d "$CLAUDE_DIR/skills" ]] && cp -r "$CLAUDE_DIR/skills" "$BACKUP_DIR/" 2>/dev/null || true

  log "Backup criado: $BACKUP_DIR"
fi

# ── Create directories ──

info "Criando diretorios..."
dirs=(
  "$CLAUDE_DIR/agents"
  "$CLAUDE_DIR/rules/common"
  "$CLAUDE_DIR/rules/typescript"
  "$CLAUDE_DIR/scripts/ralph"
  "$CLAUDE_DIR/skills/learned"
  "$CLAUDE_DIR/plugins"
  "$CLAUDE_DIR/teams/default/inboxes"
  "$CLAUDE_DIR/scheduled-tasks"
  "$CLAUDE_DIR/templates"
)
for d in "${dirs[@]}"; do
  mkdir -p "$d"
done
log "Diretorios criados"

# ── Helper: copy with verification ──

copy_verified() {
  local src="$1"
  local dst="$2"
  local label="${3:-$src}"

  if [[ ! -e "$src" ]]; then
    err "Arquivo fonte nao encontrado: $label"
    return 1
  fi

  cp "$src" "$dst"

  if [[ ! -e "$dst" ]]; then
    err "Falha ao copiar: $label"
    return 1
  fi
  return 0
}

# ── Copy Agents ──

info "Instalando agents..."
AGENT_COUNT=0
for f in "$SCRIPT_DIR/agents/"*.md; do
  [[ -f "$f" ]] || continue
  name=$(basename "$f")
  copy_verified "$f" "$CLAUDE_DIR/agents/$name" "agent/$name" && AGENT_COUNT=$((AGENT_COUNT + 1))
done
log "$AGENT_COUNT agents instalados"

# ── Copy Rules ──

info "Instalando rules..."
RULE_COUNT=0

for f in "$SCRIPT_DIR/rules/common/"*.md; do
  [[ -f "$f" ]] || continue
  name=$(basename "$f")
  copy_verified "$f" "$CLAUDE_DIR/rules/common/$name" "rules/common/$name" && RULE_COUNT=$((RULE_COUNT + 1))
done

for f in "$SCRIPT_DIR/rules/typescript/"*.md; do
  [[ -f "$f" ]] || continue
  name=$(basename "$f")
  copy_verified "$f" "$CLAUDE_DIR/rules/typescript/$name" "rules/typescript/$name" && RULE_COUNT=$((RULE_COUNT + 1))
done

if [[ -f "$SCRIPT_DIR/rules/parallel-agents.md" ]]; then
  copy_verified "$SCRIPT_DIR/rules/parallel-agents.md" "$CLAUDE_DIR/rules/parallel-agents.md" "rules/parallel-agents.md" && RULE_COUNT=$((RULE_COUNT + 1))
fi

log "$RULE_COUNT rules instaladas"

# ── Copy Skills ──

info "Instalando skills..."
SKILL_COUNT=0
for skill_dir in "$SCRIPT_DIR/skills/"*/; do
  [[ -d "$skill_dir" ]] || continue
  skill_name=$(basename "$skill_dir")
  mkdir -p "$CLAUDE_DIR/skills/$skill_name"

  for f in "$skill_dir"*; do
    [[ -f "$f" ]] || continue
    copy_verified "$f" "$CLAUDE_DIR/skills/$skill_name/$(basename "$f")" "skills/$skill_name/$(basename "$f")"
  done
  SKILL_COUNT=$((SKILL_COUNT + 1))
done
log "$SKILL_COUNT skills instalados"

# ── Copy Scripts ──

info "Instalando scripts..."
SCRIPT_COUNT=0

for f in claude-notify.js toast-notify.js; do
  if [[ -f "$SCRIPT_DIR/scripts/$f" ]]; then
    copy_verified "$SCRIPT_DIR/scripts/$f" "$CLAUDE_DIR/scripts/$f" "scripts/$f" && SCRIPT_COUNT=$((SCRIPT_COUNT + 1))
  fi
done

if [[ -d "$SCRIPT_DIR/scripts/ralph" ]]; then
  for f in "$SCRIPT_DIR/scripts/ralph/"*; do
    [[ -f "$f" ]] || continue
    copy_verified "$f" "$CLAUDE_DIR/scripts/ralph/$(basename "$f")" "scripts/ralph/$(basename "$f")" && SCRIPT_COUNT=$((SCRIPT_COUNT + 1))
  done
fi

log "$SCRIPT_COUNT scripts instalados"

# ── Copy Statusline ──

info "Instalando statusline..."
if copy_verified "$SCRIPT_DIR/statusline.sh" "$CLAUDE_DIR/statusline.sh" "statusline.sh"; then
  chmod +x "$CLAUDE_DIR/statusline.sh"
  log "Statusline instalada"
fi

# ── Copy Plugins Config ──

info "Instalando plugins config..."
if [[ -f "$SCRIPT_DIR/plugins/blocklist.json" ]]; then
  copy_verified "$SCRIPT_DIR/plugins/blocklist.json" "$CLAUDE_DIR/plugins/blocklist.json" "plugins/blocklist.json"
  log "Plugin blocklist instalada"
fi

# ── Copy Teams ──

info "Instalando teams..."
if [[ -d "$SCRIPT_DIR/teams" ]]; then
  cp -r "$SCRIPT_DIR/teams/"* "$CLAUDE_DIR/teams/" 2>/dev/null || true
  log "Teams config instalada"
fi

# ── Copy Scheduled Tasks ──

info "Instalando scheduled tasks..."
TASK_COUNT=0
for task_dir in "$SCRIPT_DIR/scheduled-tasks/"*/; do
  [[ -d "$task_dir" ]] || continue
  task_name=$(basename "$task_dir")
  mkdir -p "$CLAUDE_DIR/scheduled-tasks/$task_name"
  for f in "$task_dir"*; do
    [[ -f "$f" ]] || continue
    copy_verified "$f" "$CLAUDE_DIR/scheduled-tasks/$task_name/$(basename "$f")" "scheduled-tasks/$task_name/$(basename "$f")"
  done
  TASK_COUNT=$((TASK_COUNT + 1))
done
log "$TASK_COUNT scheduled tasks instaladas"

# ── Copy Templates ──

info "Instalando templates..."
TEMPLATE_COUNT=0
if [[ -d "$SCRIPT_DIR/templates" ]]; then
  for f in "$SCRIPT_DIR/templates/"*; do
    [[ -f "$f" ]] || continue
    copy_verified "$f" "$CLAUDE_DIR/templates/$(basename "$f")" "templates/$(basename "$f")" && TEMPLATE_COUNT=$((TEMPLATE_COUNT + 1))
  done
fi
log "$TEMPLATE_COUNT templates instalados"

# ── Copy Identity Templates ──

info "Copiando identity templates (TRIFORCE)..."
if [[ -d "$SCRIPT_DIR/identity" ]]; then
  mkdir -p "$CLAUDE_DIR/identity"
  for f in "$SCRIPT_DIR/identity/"*.md; do
    [[ -f "$f" ]] || continue
    copy_verified "$f" "$CLAUDE_DIR/identity/$(basename "$f")" "identity/$(basename "$f")"
  done
  log "Identity templates copiados para ~/.claude/identity/"

  # Suggest CLAUDE.md setup if not present
  if [[ ! -f "$CLAUDE_DIR/CLAUDE.md" ]]; then
    echo ""
    warn "CLAUDE.md nao encontrado!"
    info "Para configurar a identidade do seu ambiente, copie um template:"
    info "  Desktop: cp ~/.claude/identity/desktop.md ~/.claude/CLAUDE.md"
    info "  Mobile:  cp ~/.claude/identity/mobile.md ~/.claude/CLAUDE.md"
    info "  VPS:     cp ~/.claude/identity/vps.md ~/.claude/CLAUDE.md"
    info "  Veja: https://github.com/pedrormc/TRIFORCE"
    echo ""
  else
    log "CLAUDE.md ja existe — identidade preservada"
  fi
fi

# ── Copy Configs ──

echo ""
info "Instalando configuracoes..."

# settings.json
if [[ "$FORCE" == true ]] || [[ ! -f "$CLAUDE_DIR/settings.json" ]]; then
  copy_verified "$SCRIPT_DIR/config/settings.json" "$CLAUDE_DIR/settings.json" "settings.json"
  log "settings.json instalado"
else
  warn "settings.json ja existe. Use --force para sobrescrever (backup foi criado)"
fi

# settings.local.json
if [[ "$FORCE" == true ]] || [[ ! -f "$CLAUDE_DIR/settings.local.json" ]]; then
  copy_verified "$SCRIPT_DIR/config/settings.local.json" "$CLAUDE_DIR/settings.local.json" "settings.local.json"
  log "settings.local.json instalado"
else
  warn "settings.local.json ja existe. Use --force para sobrescrever"
fi

# mcp.json — never overwrite (contains secrets)
if [[ ! -f "$CLAUDE_DIR/mcp.json" ]]; then
  copy_verified "$SCRIPT_DIR/config/mcp.json" "$CLAUDE_DIR/mcp.json" "mcp.json"
  warn "mcp.json instalado — EDITE com suas API keys antes de usar!"
else
  warn "mcp.json ja existe. Nao sobrescrevendo (pode conter suas API keys)"
fi

# ── Install Plugins ──

echo ""
info "Instalando plugins via marketplace..."

PLUGIN_COUNT=0
install_plugin() {
  local name="$1"
  local marketplace="$2"

  info "  Instalando $name..."
  if claude plugins install "$name" --marketplace "$marketplace" 2>/dev/null; then
    log "  Plugin instalado: $name"
    PLUGIN_COUNT=$((PLUGIN_COUNT + 1))
  else
    # Check if already installed
    if claude plugins list 2>/dev/null | grep -q "$name"; then
      log "  Plugin ja instalado: $name"
      PLUGIN_COUNT=$((PLUGIN_COUNT + 1))
    else
      warn "  Plugin $name falhou. Instale manualmente: claude plugins install $name --marketplace $marketplace"
    fi
  fi
}

install_plugin "everything-claude-code" "everything-claude-code"
install_plugin "superpowers" "superpowers-marketplace"
install_plugin "ralph-skills" "ralph-marketplace"
install_plugin "ui-ux-pro-max" "ui-ux-pro-max-skill"
install_plugin "example-skills" "anthropic-agent-skills"
install_plugin "vercel" "claude-plugins-official"

# ── Install n8n-mcp (optional) ──

echo ""
info "Verificando n8n-mcp..."
if command -v n8n-mcp &>/dev/null || npm list -g n8n-mcp &>/dev/null 2>&1; then
  log "n8n-mcp ja instalado globalmente"
else
  info "Instalando n8n-mcp globalmente..."
  if npm install -g n8n-mcp 2>/dev/null; then
    log "n8n-mcp instalado"
  else
    warn "Falha ao instalar n8n-mcp. Instale manualmente: npm install -g n8n-mcp"
  fi
fi

# ── Post-install Validation ──

echo ""
info "Validando instalacao..."
VALID=true

check_exists() {
  local path="$1"
  local label="$2"
  if [[ -e "$path" ]]; then
    return 0
  else
    err "Faltando: $label ($path)"
    VALID=false
    return 1
  fi
}

# Core files
check_exists "$CLAUDE_DIR/settings.json" "settings.json"
check_exists "$CLAUDE_DIR/statusline.sh" "statusline.sh"
check_exists "$CLAUDE_DIR/scripts/claude-notify.js" "claude-notify.js"

# Agents
for agent in api-specialist devops-agent frontend-specialist prompt-engineer research-agent; do
  check_exists "$CLAUDE_DIR/agents/$agent.md" "agent: $agent"
done

# Rules - common
for rule in agents coding-style development-workflow git-workflow hooks patterns performance project-categorization security testing; do
  check_exists "$CLAUDE_DIR/rules/common/$rule.md" "rule: common/$rule"
done

# Rules - typescript
for rule in coding-style hooks patterns security testing; do
  check_exists "$CLAUDE_DIR/rules/typescript/$rule.md" "rule: typescript/$rule"
done

check_exists "$CLAUDE_DIR/rules/parallel-agents.md" "rule: parallel-agents"

# Skills custom — 19 skills do Pedro
for skill in \
  ata documento slide \
  backgroundcheck contrato \
  mp4 obsidian pop prospect tese-investimento whatsapp-evolution \
  hubspot-mcp-expert \
  n8n-code-javascript n8n-code-python n8n-expression-syntax \
  n8n-mcp-tools-expert n8n-node-configuration n8n-validation-expert \
  n8n-workflow-patterns; do
  check_exists "$CLAUDE_DIR/skills/$skill/SKILL.md" "skill: $skill"
done

# Directories
check_exists "$CLAUDE_DIR/skills/learned" "dir: skills/learned"
check_exists "$CLAUDE_DIR/templates" "dir: templates"

if [[ "$VALID" == true ]]; then
  log "Validacao completa — todos os arquivos presentes"
else
  err "Alguns arquivos estao faltando. Verifique os erros acima."
fi

# ── Foundation v1 — Memory brain + hooks + scripts ──

echo ""
info "Instalando Foundation v1 (memory brain, hooks, scripts)..."

# Backup existing settings.json before any Foundation changes
if [[ -f "$CLAUDE_DIR/settings.json" && ! -f "$CLAUDE_DIR/settings.json.pre-foundation-bak" ]]; then
  cp "$CLAUDE_DIR/settings.json" "$CLAUDE_DIR/settings.json.pre-foundation-bak"
  log "Backup pre-Foundation: settings.json.pre-foundation-bak"
fi

# Copy hooks
mkdir -p "$CLAUDE_DIR/hooks"
if [[ -d "$SCRIPT_DIR/hooks" ]]; then
  cp "$SCRIPT_DIR/hooks/"*.sh "$CLAUDE_DIR/hooks/"
  chmod +x "$CLAUDE_DIR/hooks/"*.sh
  HOOK_COUNT=$(ls "$CLAUDE_DIR/hooks/"*.sh 2>/dev/null | wc -l)
  log "$HOOK_COUNT hooks instalados"
fi

# Copy triforce config (3-tabs priority + per-env personas)
if [[ -d "$SCRIPT_DIR/triforce" ]]; then
  mkdir -p "$CLAUDE_DIR/triforce"
  cp "$SCRIPT_DIR/triforce/"*.md "$CLAUDE_DIR/triforce/" 2>/dev/null || true
  log "triforce/ instalado (3-abas-master config)"
fi

# Copy ALL scripts (not just memory-* and foundation-*)
info "Copiando todos os scripts (whatsapp, brainstorm, obsidian-session, ralph...)..."
cp "$SCRIPT_DIR/scripts/"*.js "$CLAUDE_DIR/scripts/" 2>/dev/null || true
cp "$SCRIPT_DIR/scripts/"*.ps1 "$CLAUDE_DIR/scripts/" 2>/dev/null || true
chmod +x "$CLAUDE_DIR/scripts/"*.js 2>/dev/null || true

# Copy Foundation scripts (memory-* and foundation-*)
mkdir -p "$CLAUDE_DIR/scripts"
cp "$SCRIPT_DIR/scripts/memory-"*.sh "$CLAUDE_DIR/scripts/" 2>/dev/null || true
cp "$SCRIPT_DIR/scripts/foundation-"*.sh "$CLAUDE_DIR/scripts/" 2>/dev/null || true
cp "$SCRIPT_DIR/scripts/test-i4-fake-data.sh" "$CLAUDE_DIR/scripts/" 2>/dev/null || true
chmod +x "$CLAUDE_DIR/scripts/memory-"*.sh "$CLAUDE_DIR/scripts/foundation-"*.sh "$CLAUDE_DIR/scripts/test-i4-fake-data.sh" 2>/dev/null || true
log "Foundation scripts instalados (memory-*.sh, foundation-*.sh, test-i4)"

# Copy auto-promote config
mkdir -p "$CLAUDE_DIR/config"
if [[ -f "$SCRIPT_DIR/config/auto-promote.yaml" ]]; then
  cp "$SCRIPT_DIR/config/auto-promote.yaml" "$CLAUDE_DIR/config/"
  log "auto-promote.yaml instalado"
fi

# Install Gstack skill if not already present
if [[ ! -d "$CLAUDE_DIR/skills/gstack" && ! -d "$CLAUDE_DIR/plugins/gstack" ]]; then
  info "Instalando Gstack de garrytan/gstack..."
  if git clone --single-branch --depth 1 https://github.com/garrytan/gstack.git "$CLAUDE_DIR/skills/gstack" 2>/dev/null; then
    (cd "$CLAUDE_DIR/skills/gstack" && [[ -x ./setup ]] && ./setup) || warn "Gstack setup script falhou — verifique manualmente"
    log "Gstack instalado (36 slash commands)"
  else
    warn "Falha ao clonar Gstack. Instale manualmente: git clone https://github.com/garrytan/gstack.git ~/.claude/skills/gstack"
  fi
else
  log "Gstack ja presente"
fi

# Run Foundation smoke test (non-blocking — just reports)
if [[ -x "$CLAUDE_DIR/scripts/foundation-smoke.sh" ]]; then
  info "Rodando smoke test Foundation..."
  if "$CLAUDE_DIR/scripts/foundation-smoke.sh" >/dev/null 2>&1; then
    log "Foundation smoke: 13/13 passou"
  else
    warn "Foundation smoke: alguns testes falharam. Execute manualmente: ~/.claude/scripts/foundation-smoke.sh"
  fi
fi

# ── Summary ──

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [[ $ERRORS -eq 0 ]]; then
  printf "${BOLD}${GREEN}  Instalacao concluida com sucesso!${NC}\n"
else
  printf "${BOLD}${YELLOW}  Instalacao concluida com $ERRORS erro(s) e $WARNINGS aviso(s)${NC}\n"
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
printf "  ${CYAN}Agents:${NC}         $AGENT_COUNT\n"
printf "  ${CYAN}Rules:${NC}          $RULE_COUNT\n"
printf "  ${CYAN}Skills:${NC}         $SKILL_COUNT\n"
printf "  ${CYAN}Plugins:${NC}        $PLUGIN_COUNT\n"
printf "  ${CYAN}Scripts:${NC}        $SCRIPT_COUNT\n"
printf "  ${CYAN}Hooks:${NC}          ${HOOK_COUNT:-5} (session-start, session-end, post-edit, save-session-mirror, obsidian-auto-save)\n"
printf "  ${CYAN}Templates:${NC}      $TEMPLATE_COUNT\n"
printf "  ${CYAN}Scheduled:${NC}      $TASK_COUNT\n"
printf "  ${CYAN}Plataforma:${NC}     $OS\n"
echo ""
printf "  ${CYAN}Foundation:${NC} validate with ${BOLD}~/.claude/scripts/foundation-smoke.sh${NC}\n"
printf "  ${CYAN}Rollback:${NC}   ${BOLD}~/.claude/scripts/foundation-uninstall.sh${NC}\n"
echo ""

# MCP keys reminder
if grep -q "YOUR_" "$CLAUDE_DIR/mcp.json" 2>/dev/null; then
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  printf "  ${YELLOW}ACAO NECESSARIA:${NC}\n"
  printf "  Edite ${BOLD}~/.claude/mcp.json${NC} e substitua os placeholders:\n"
  echo ""
  printf "    - PATH_TO_YOUR_OBSIDIAN_VAULT\n"
  printf "    - YOUR_TESTSPRITE_API_KEY_HERE\n"
  printf "    - YOUR_N8N_INSTANCE_URL\n"
  printf "    - YOUR_N8N_API_KEY_HERE\n"
  printf "    - PATH_TO_N8N_MCP\n"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
fi

echo ""
printf "  Reinicie o Claude Code para aplicar todas as mudancas.\n"
echo ""

exit $ERRORS
