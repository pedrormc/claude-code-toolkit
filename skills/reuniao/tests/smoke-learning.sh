#!/usr/bin/env bash
# Smoke test — caminho NOVO: brainstorm → tipo fora do catálogo → montador genérico
# → auto-improve (catálogo aprende). Roda contra cópia descartável do catálogo
# (REUNIAO_CATALOG) pra NUNCA poluir o catalog.json real.
set -euo pipefail

command -v stat >/dev/null || { echo "ERRO: rodar em Git Bash (precisa coreutils)"; exit 2; }

SKILL_DIR="$HOME/.claude/skills/reuniao"
TMP_OUT="$(mktemp -d)"
trap "rm -rf $TMP_OUT" EXIT

to_win() { if command -v cygpath >/dev/null 2>&1; then cygpath -w "$1"; else echo "$1"; fi; }

# Catálogo descartável = cópia do real
cp "$SKILL_DIR/catalog.json" "$TMP_OUT/catalog.json"
CAT_WIN=$(to_win "$TMP_OUT/catalog.json")
export REUNIAO_CATALOG="$CAT_WIN"

TIPOS_ANTES=$(python -c "import json; print(len(json.load(open(r'$CAT_WIN'))['tipos']))")

# master.json: ata (canônico) + um tipo NOVO 'analise_cenario' com plano de seções inline
cat > "$TMP_OUT/master.json" <<'EOF_MASTER'
{
  "meta": {
    "data": "1 de junho de 2026",
    "tipo_reuniao": "Estratégica — smoke learning",
    "cliente": {"nome": "TestCo", "slug": "tst", "vertical": "Smoke Industry"}
  },
  "participantes": {"presentes": ["Pedro"], "ausentes": []},
  "objetivo": "Validar caminho de brainstorm + auto-improve.",
  "topicos": [{"titulo": "Cenários", "discussao": ["Discutimos 3 cenários."], "decisoes": ["Seguir cenário B."]}],
  "encaminhamentos": [{"acao": "Detalhar cenário B", "responsavel": "Pedro", "prazo": "05/06"}],
  "analise_cenario": {
    "titulo": "Análise de Cenários — TestCo",
    "titulo_curto": "CENÁRIOS",
    "tldr": "Três cenários avaliados; recomendação pelo cenário B.",
    "secoes": [
      {"titulo": "1. Cenário A — Conservador", "paragrafos": ["Crescimento lento, baixo risco."]},
      {"titulo": "2. Cenário B — Recomendado", "destaque": "Equilíbrio risco/retorno"},
      {"titulo": "3. Cenário C — Agressivo", "listas": [{"itens": ["Alto investimento", "Alto risco"]}]}
    ]
  }
}
EOF_MASTER

# selection.json: ata + tipo novo; learned_types descreve a entrada de catálogo do novo
cat > "$TMP_OUT/selection.json" <<'EOF_SEL'
{
  "selected_builders": ["ata-reuniao", "doc-analise-cenario"],
  "drive_folder_name": "reuniao tst",
  "pii_confirmado": true,
  "cliente_externo": false,
  "learned_types": [
    {
      "key": "doc-analise-cenario",
      "skill_base": "documento",
      "label": "Análise de cenários",
      "naming_template": "doc-analise-cenario-<cliente>.docx",
      "scope": "external_specific",
      "montador": "generico",
      "master_field": "analise_cenario",
      "triggers": ["cenário", "cenarios", "análise de cenário", "trade-off"],
      "fields_required": ["analise_cenario"],
      "learned_from": "reuniao tst (smoke)"
    }
  ]
}
EOF_SEL

MASTER_WIN=$(to_win "$TMP_OUT/master.json")
SEL_WIN=$(to_win "$TMP_OUT/selection.json")
OUT_WIN=$(to_win "$TMP_OUT/out/")

# --- Run 1: deve gerar 2 docs e APRENDER o tipo novo ---
RESULT1=$(python "$SKILL_DIR/reuniao.py" "$MASTER_WIN" "$SEL_WIN" "$OUT_WIN")
echo "--- Run 1 ---"; echo "$RESULT1"

STATUS1=$(echo "$RESULT1" | python -c "import json,sys; print(json.load(sys.stdin)['status'])")
DOCS1=$(echo "$RESULT1" | python -c "import json,sys; print(len(json.load(sys.stdin)['docs']))")
LEARNED1=$(echo "$RESULT1" | python -c "import json,sys; d=json.load(sys.stdin); print(','.join(x['key'] for x in d.get('learned_persisted',[])))")
TIPOS_DEPOIS=$(python -c "import json; print(len(json.load(open(r'$CAT_WIN'))['tipos']))")
NOVO_NO_CAT=$(python -c "import json; print(any(t['key']=='doc-analise-cenario' and t.get('flag')=='learned' for t in json.load(open(r'$CAT_WIN'))['tipos']))")

# --- Run 2: idempotência — não duplica, vai pra learned_skipped ---
RESULT2=$(python "$SKILL_DIR/reuniao.py" "$MASTER_WIN" "$SEL_WIN" "$(to_win "$TMP_OUT/out2/")")
echo "--- Run 2 (idempotência) ---"; echo "$RESULT2"
SKIPPED2=$(echo "$RESULT2" | python -c "import json,sys; d=json.load(sys.stdin); print(','.join(x['key'] for x in d.get('learned_skipped',[])))")
TIPOS_FINAL=$(python -c "import json; print(len(json.load(open(r'$CAT_WIN'))['tipos']))")

echo ""
echo "tipos antes=$TIPOS_ANTES depois=$TIPOS_DEPOIS final=$TIPOS_FINAL | learned1=$LEARNED1 skipped2=$SKIPPED2 novo_no_cat=$NOVO_NO_CAT"

PASS=true
[ "$STATUS1" = "ok" ]                                  || { echo "FAIL: status run1 = $STATUS1"; PASS=false; }
[ "$DOCS1" -eq 2 ]                                     || { echo "FAIL: docs run1 = $DOCS1 (esperado 2)"; PASS=false; }
[ "$LEARNED1" = "doc-analise-cenario" ]                || { echo "FAIL: learned_persisted run1 = '$LEARNED1'"; PASS=false; }
[ "$NOVO_NO_CAT" = "True" ]                            || { echo "FAIL: tipo novo não entrou no catálogo com flag learned"; PASS=false; }
[ "$TIPOS_DEPOIS" -eq $((TIPOS_ANTES + 1)) ]           || { echo "FAIL: catálogo não cresceu +1 (antes=$TIPOS_ANTES depois=$TIPOS_DEPOIS)"; PASS=false; }
[ "$SKIPPED2" = "doc-analise-cenario" ]                || { echo "FAIL: run2 deveria pular (idempotência), skipped='$SKIPPED2'"; PASS=false; }
[ "$TIPOS_FINAL" -eq "$TIPOS_DEPOIS" ]                 || { echo "FAIL: run2 duplicou no catálogo (final=$TIPOS_FINAL)"; PASS=false; }

if $PASS; then
  echo ""
  echo "SMOKE-LEARNING PASS — brainstorm→genérico→auto-improve OK, idempotente, catálogo real intacto"
  exit 0
else
  echo ""
  echo "SMOKE-LEARNING FAIL"
  exit 1
fi
