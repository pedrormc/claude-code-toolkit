#!/usr/bin/env bash
# Smoke test — valida orquestrador end-to-end com fixture.
set -euo pipefail

# Guard: precisa Git Bash com coreutils
command -v stat >/dev/null || { echo "ERRO: rodar em Git Bash (precisa coreutils)"; exit 2; }

SKILL_DIR="$HOME/.claude/skills/reuniao"
TMP_OUT="$(mktemp -d)"
trap "rm -rf $TMP_OUT" EXIT

# Convert paths to Windows-style for Python
to_win() {
  if command -v cygpath >/dev/null 2>&1; then
    cygpath -w "$1"
  else
    echo "$1"
  fi
}

# master.json mínimo simulando reunião comercial
cat > "$TMP_OUT/master.json" <<'EOF_MASTER'
{
  "meta": {
    "data": "19 de maio de 2026",
    "tipo_reuniao": "Comercial — smoke",
    "cliente": {"nome": "TestCo", "slug": "tst", "vertical": "Smoke Industry"}
  },
  "participantes": {"presentes": ["Pedro"], "ausentes": []},
  "objetivo": "Smoke test do orquestrador.",
  "topicos": [{"titulo": "Tópico 1 — Smoke", "discussao": ["Texto smoke."], "decisoes": ["Aprovado smoke."]}],
  "encaminhamentos": [
    {"acao": "Validar smoke", "responsavel": "Pedro", "prazo": "19/05"},
    {"acao": "Confirmar Drive", "responsavel": "Pedro", "prazo": "19/05"}
  ],
  "plano_comercial": {"metas": ["10 clientes"], "abordagem": "Inbound", "ticket_medio": "R$ 100"}
}
EOF_MASTER

# selection com 3 builders + PII confirmada (caminho aprovado)
cat > "$TMP_OUT/selection.json" <<'EOF_SEL'
{
  "selected_builders": ["ata-reuniao", "doc-tarefas-completas", "doc-plano-comercial"],
  "drive_folder_name": "reuniao tst",
  "pii_confirmado": true,
  "cliente_externo": true
}
EOF_SEL

MASTER_WIN=$(to_win "$TMP_OUT/master.json")
SEL_WIN=$(to_win "$TMP_OUT/selection.json")
OUT_WIN=$(to_win "$TMP_OUT/out/")

# roda orquestrador
RESULT_JSON=$(python "$SKILL_DIR/reuniao.py" "$MASTER_WIN" "$SEL_WIN" "$OUT_WIN")
echo "$RESULT_JSON"

# valida resultado
STATUS=$(echo "$RESULT_JSON" | python -c "import json,sys; print(json.load(sys.stdin)['status'])")
DOC_COUNT=$(echo "$RESULT_JSON" | python -c "import json,sys; print(len(json.load(sys.stdin)['docs']))")

if [ "$STATUS" = "ok" ] && [ "$DOC_COUNT" -eq 3 ]; then
  echo ""
  echo "SMOKE PASS — 3/3 docs gerados, status=ok"
  ls -la "$TMP_OUT/out/"
  exit 0
else
  echo ""
  echo "SMOKE FAIL — status=$STATUS, docs=$DOC_COUNT"
  exit 1
fi
