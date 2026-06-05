#!/usr/bin/env bash
# =============================================================================
# sync-rules.sh - Detector de drift + sync das Regras Soberanas para o toolkit
# -----------------------------------------------------------------------------
# SoT: /c/Users/teste/.claude/rules/core/identity.md (+ bu-categorization.md).
# Copias derivadas: CLAUDE.md, triforce/three-tabs-config.md, plano/PRIORIDADE.md,
# vault Obsidian. Este script NAO regenera copias derivadas: ele (1) detecta se
# os marcadores das 3 Regras Soberanas estao presentes nos arquivos-chave e
# (2) sincroniza ~/.claude/rules/core/*.md para o repo do toolkit quando diferem.
#
# Uso:
#   sync-rules.sh            detecta drift dos marcadores E sincroniza o toolkit
#   sync-rules.sh --check    SO detecta drift (read-only, nao copia nada)
#   sync-rules.sh -h|--help  mostra esta ajuda
#
# Exit codes:
#   0  todos os marcadores criticos presentes (sync pode ter copiado arquivos)
#   1  pelo menos um marcador critico MISSING (plugavel no audit-hooks.sh)
#   2  erro de uso / pre-condicao (ex: SoT ausente)
#
# Plugavel no audit-hooks.sh: rode "sync-rules.sh --check" como smoke-test; se
# sair != 0, a auditoria sinaliza que uma copia derivada perdeu uma regra.
#
# [Registrado por: DESKTOP - 2026-06-05]
# =============================================================================

set -u

# ---------------------------------------------------------------------------
# Paths (Git Bash no Windows). $HOME = /c/Users/teste.
# ---------------------------------------------------------------------------
CLAUDE_DIR="$HOME/.claude"
RULES_CORE="$CLAUDE_DIR/rules/core"
TOOLKIT_CORE="/c/Users/teste/Desktop/claude-code-toolkit/rules/core"

# Arquivos onde os marcadores DEVEM existir (rotulo:caminho).
TARGETS=(
  "CLAUDE.md:$CLAUDE_DIR/CLAUDE.md"
  "rules/core/identity.md:$RULES_CORE/identity.md"
  "toolkit/rules/core/identity.md:$TOOLKIT_CORE/identity.md"
)

# Arquivos core que o toolkit deve espelhar (sync passo 3).
SYNC_FILES=("identity.md" "bu-categorization.md" "task-orchestration.md")

# ---------------------------------------------------------------------------
# Marcadores esperados. Cada entrada: "Nome legivel|regex ERE".
# A regex e tolerante as duas redacoes (CLAUDE.md usa "REGRA SOBERANA #N",
# identity.md usa o titulo da secao, ex "Catalogacao Singular").
# Acentos opcionais via classes pra robustez (Cataloga(c)ao, Categoriza(c)ao).
# ---------------------------------------------------------------------------
MARKERS=(
  "3 Abas Master|3 Abas Master"
  "REGRA SOBERANA #3 (Catalogacao)|REGRA SOBERANA #3|Cataloga.?[cç][aã]o Singular"
  "REGRA SOBERANA #4 (Categorizacao por BU)|REGRA SOBERANA #4|Categoriza.?[cç][aã]o por BU"
)

# ---------------------------------------------------------------------------
# Flags
# ---------------------------------------------------------------------------
CHECK_ONLY=0
for arg in "$@"; do
  case "$arg" in
    --check) CHECK_ONLY=1 ;;
    -h|--help)
      sed -n '2,25p' "$0" | sed 's/^# \{0,1\}//'
      exit 0
      ;;
    *)
      echo "ERRO: argumento desconhecido: $arg (use --check ou --help)" >&2
      exit 2
      ;;
  esac
done

# ---------------------------------------------------------------------------
# Cores (degradam pra vazio se nao for TTY)
# ---------------------------------------------------------------------------
if [ -t 1 ]; then
  C_GREEN="\033[32m"; C_RED="\033[31m"; C_YELLOW="\033[33m"; C_BOLD="\033[1m"; C_RST="\033[0m"
else
  C_GREEN=""; C_RED=""; C_YELLOW=""; C_BOLD=""; C_RST=""
fi

pass() { printf "  ${C_GREEN}PASS${C_RST}    %s\n" "$1"; }
miss() { printf "  ${C_RED}MISSING${C_RST} %s\n" "$1"; }
warn() { printf "  ${C_YELLOW}WARN${C_RST}    %s\n" "$1"; }
info() { printf "  %s\n" "$1"; }

CRITICAL_MISSING=0

# ===========================================================================
# Pre-condicao: SoT precisa existir
# ===========================================================================
if [ ! -f "$RULES_CORE/identity.md" ]; then
  echo "ERRO: SoT ausente: $RULES_CORE/identity.md" >&2
  echo "      Nada a verificar/sincronizar. Abortando." >&2
  exit 2
fi

# ===========================================================================
# PASSO 1-2: Detector de drift dos marcadores
# ===========================================================================
printf "${C_BOLD}== Drift dos marcadores das Regras Soberanas ==${C_RST}\n"

for entry in "${TARGETS[@]}"; do
  label="${entry%%:*}"
  path="${entry#*:}"

  printf "\n${C_BOLD}%s${C_RST}\n" "$label"

  if [ ! -f "$path" ]; then
    # O target do toolkit e opcional: se o clone nao existe aqui (ex: Mobile/VPS),
    # nao e drift de regra, e so ausencia do repo. Warn em vez de critico.
    case "$path" in
      "$TOOLKIT_CORE"/*)
        if [ ! -d "$TOOLKIT_CORE" ]; then
          warn "toolkit nao clonado aqui (pulando): $label"
          continue
        fi
        ;;
    esac
    miss "arquivo ausente: $path"
    CRITICAL_MISSING=$((CRITICAL_MISSING + 1))
    continue
  fi

  for m in "${MARKERS[@]}"; do
    mname="${m%%|*}"
    mregex="${m#*|}"
    if grep -Eq -- "$mregex" "$path"; then
      pass "$mname"
    else
      miss "$mname"
      CRITICAL_MISSING=$((CRITICAL_MISSING + 1))
    fi
  done
done

# ===========================================================================
# PASSO 3: Sync do toolkit (diff + copia ~/.claude/rules/core/*.md -> toolkit)
# ===========================================================================
printf "\n${C_BOLD}== Sync toolkit (rules/core) ==${C_RST}\n"

COPIED=0
SYNC_SKIPPED=0

if [ ! -d "$TOOLKIT_CORE" ]; then
  warn "destino do toolkit ausente: $TOOLKIT_CORE"
  warn "sync ignorado (clone o repo claude-code-toolkit no Desktop pra habilitar)"
  SYNC_SKIPPED=1
elif [ "$CHECK_ONLY" -eq 1 ]; then
  for f in "${SYNC_FILES[@]}"; do
    src="$RULES_CORE/$f"
    dst="$TOOLKIT_CORE/$f"
    [ -f "$src" ] || { warn "fonte ausente, pulando: $f"; continue; }
    if [ ! -f "$dst" ]; then
      info "DRIFT  $f (ausente no toolkit, --check nao copia)"
    elif ! cmp -s "$src" "$dst"; then
      info "DRIFT  $f (difere do toolkit, --check nao copia)"
    else
      info "ok     $f (identico)"
    fi
  done
  info "(--check: nenhuma copia feita)"
else
  for f in "${SYNC_FILES[@]}"; do
    src="$RULES_CORE/$f"
    dst="$TOOLKIT_CORE/$f"
    if [ ! -f "$src" ]; then
      warn "fonte ausente, pulando: $f"
      continue
    fi
    if [ ! -f "$dst" ] || ! cmp -s "$src" "$dst"; then
      if cp -f -- "$src" "$dst"; then
        printf "  ${C_GREEN}COPIED${C_RST}  %s -> toolkit\n" "$f"
        COPIED=$((COPIED + 1))
      else
        miss "falha ao copiar: $f"
        CRITICAL_MISSING=$((CRITICAL_MISSING + 1))
      fi
    else
      info "ok      $f (identico, nao copiou)"
    fi
  done
fi

# ===========================================================================
# Resumo + exit
# ===========================================================================
printf "\n${C_BOLD}== Resumo ==${C_RST}\n"
if [ "$CRITICAL_MISSING" -eq 0 ]; then
  printf "  ${C_GREEN}Marcadores: OK${C_RST} (todos presentes)\n"
else
  printf "  ${C_RED}Marcadores: %d MISSING critico(s)${C_RST}\n" "$CRITICAL_MISSING"
fi

if [ "$CHECK_ONLY" -eq 1 ]; then
  info "Modo: --check (read-only, sem copia)"
elif [ "$SYNC_SKIPPED" -eq 1 ]; then
  info "Sync toolkit: ignorado (destino ausente)"
else
  info "Sync toolkit: $COPIED arquivo(s) copiado(s)"
fi

if [ "$CRITICAL_MISSING" -gt 0 ]; then
  exit 1
fi
exit 0
