#!/usr/bin/env bash
# =============================================================================
# build-all-rules.sh - Regenera ALL_RULES.md a partir de rules/**/*.md
# -----------------------------------------------------------------------------
# Concatena TODAS as regras customizadas do repo num unico arquivo de consulta,
# com indice + anchors. As regras de plugins (everything-claude-code, superpowers
# etc.) sao carregadas dinamicamente pelo proprio plugin com versao pinada e NAO
# sao vendorizadas aqui (era a fonte do drift do ALL_RULES.md antigo).
#
# Roda em qualquer repo que tenha rules/ na raiz (toolkit OU ~/.claude):
# detecta a raiz como o diretorio-pai deste script.
#
# Uso:
#   build-all-rules.sh           regenera <repo>/ALL_RULES.md
#   build-all-rules.sh -h|--help mostra esta ajuda
#
# [Registrado por: DESKTOP - 2026-06-05]
# =============================================================================

set -euo pipefail

case "${1:-}" in
  -h|--help) sed -n '2,21p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
  "") : ;;
  *) echo "ERRO: argumento desconhecido: $1 (use --help)" >&2; exit 2 ;;
esac

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO"

if [ ! -d rules ]; then
  echo "ERRO: $REPO/rules nao existe. Nada a gerar." >&2
  exit 2
fi

OUT="$REPO/ALL_RULES.md"
DATE="$(date +%Y-%m-%d)"

# Lista determinística das regras (path-sorted, locale C).
mapfile -t FILES < <(find rules -type f -name '*.md' | LC_ALL=C sort)

if [ "${#FILES[@]}" -eq 0 ]; then
  echo "ERRO: nenhum .md em rules/" >&2
  exit 2
fi

anchor() { printf 'custom-%s' "$(printf '%s' "$1" | sed 's/\.md$//; s#/#-#g')"; }

{
  echo "# Todas as Regras Ativas do Claude Code"
  echo
  echo "> Arquivo gerado automaticamente por \`scripts/build-all-rules.sh\`. NAO editar a mao."
  echo "> Atualizado em: $DATE"
  echo "> Fonte: \`rules/\` deste repo (espelho de \`~/.claude/rules/\`)."
  echo
  echo "## Indice"
  echo
  echo "### Regras Customizadas (${#FILES[@]} arquivos)"
  for f in "${FILES[@]}"; do
    rel="${f#rules/}"
    printf -- '- [%s](#%s)\n' "$rel" "$(anchor "$rel")"
  done
  echo
  echo "> Regras de plugins (everything-claude-code, superpowers, ralph, ui-ux-pro-max, vercel etc.) sao carregadas dinamicamente pelo plugin com versao pinada e NAO sao vendorizadas aqui. Inventario e roteamento: \`rules/common/namespace-cheatsheet.md\`."
  echo
  echo "---"
  echo "---"
  echo
  echo "# REGRAS CUSTOMIZADAS"
  echo
  echo "> Fonte: \`~/.claude/rules/\`. Tem prioridade sobre regras de plugins."
  for f in "${FILES[@]}"; do
    rel="${f#rules/}"
    echo
    echo "---"
    echo
    printf '<a id="%s"></a>\n' "$(anchor "$rel")"
    echo
    printf '## `rules/%s`\n' "$rel"
    echo
    cat "$f"
    echo
  done
} > "$OUT"

echo "OK ALL_RULES.md regenerado: ${#FILES[@]} regras, $(wc -l < "$OUT") linhas -> $OUT"
