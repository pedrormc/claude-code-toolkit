#!/usr/bin/env bash
# ~/.claude/scripts/memory-index-rebuild.sh
# Regenerates Claude/memory/INDEX.md from live filesystem state.

set -uo pipefail

case "${OSTYPE:-unknown}" in
  msys*|cygwin*|win32*) VAULT="$HOME/Documents/obsidiano" ;;
  *) VAULT="$HOME/obsidiano" ;;
esac
[ -d "$VAULT/Claude/memory" ] || exit 0

INDEX="$VAULT/Claude/memory/INDEX.md"
TODAY=$(date +%Y-%m-%d)
NOW_ISO=$(date -Iseconds)
ENV_TAG="${CLAUDE_ENV_TAG:-DESKTOP}"
PROJECTS_DIR="$HOME/.claude/projects"

{
  cat <<EOF
---
name: Memory Master Index
description: Mapa unificado dos 3 sistemas de memória (auto + claude + vault)
type: reference
scope: global
source: claude-memory
last_updated: $TODAY
auto_generated: true
---

> **NÃO EDITAR MANUALMENTE.** Gerado por \`~/.claude/scripts/memory-index-rebuild.sh\`.
> Última geração: $NOW_ISO ($ENV_TAG)

## 🧠 Claude Memory (global, distilled)

| Arquivo | Tipo | Última atualização |
|---|---|---|
EOF

  for f in user preferences active decisions people projects; do
    FILE="$VAULT/Claude/memory/$f.md"
    if [ -f "$FILE" ]; then
      TYPE=$(grep '^type:' "$FILE" | head -1 | awk '{print $2}')
      LAST=$(grep '^last_updated:' "$FILE" | head -1 | awk '{print $2}')
      echo "| [$f.md]($f.md) | $TYPE | $LAST |"
    fi
  done

  cat <<EOF

## 🤖 Auto-Memory (per-project, harness)

Localização: \`~/.claude/projects/<cwd>/memory/\`

| Projeto (cwd) | Arquivos | Última atividade |
|---|---|---|
EOF

  if [ -d "$PROJECTS_DIR" ]; then
    for proj_dir in "$PROJECTS_DIR"/*/; do
      [ -d "$proj_dir/memory" ] || continue
      NAME=$(basename "$proj_dir")
      COUNT=$(find "$proj_dir/memory" -maxdepth 1 -name "*.md" 2>/dev/null | wc -l)
      LATEST=$(ls -t "$proj_dir/memory"/*.md 2>/dev/null | head -1)
      if [ -n "$LATEST" ]; then
        MTIME=$(stat -c '%y' "$LATEST" 2>/dev/null | cut -d' ' -f1 || echo "-")
        echo "| \`$NAME\` | $COUNT | $MTIME |"
      fi
    done
  fi

  cat <<EOF

## 📚 Vault Manual (Obsidian, humano)

| Pasta | Conteúdo |
|---|---|
EOF

  # List vault top-level folders (exclude Claude/, .obsidian/, .git/)
  for dir in "$VAULT"/*/; do
    NAME=$(basename "$dir")
    case "$NAME" in
      Claude|.obsidian|.git) continue ;;
    esac
    [ -d "$dir" ] || continue
    FILE_COUNT=$(find "$dir" -maxdepth 1 -name "*.md" 2>/dev/null | wc -l)
    echo "| [$NAME/](../../$NAME/) | $FILE_COUNT arquivos .md |"
  done

  cat <<EOF

---

*[Registrado por: $ENV_TAG — $TODAY]*
EOF
} > "$INDEX.tmp" && mv "$INDEX.tmp" "$INDEX"

exit 0
