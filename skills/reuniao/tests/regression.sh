#!/usr/bin/env bash
# Regression test — valida que /ata, /documento, /pop continuam funcionando.
set -euo pipefail

# Guard: precisamos de coreutils (stat -c, sha256sum) — só Git Bash no Windows
command -v stat >/dev/null && command -v sha256sum >/dev/null || {
  echo "ERRO: precisa de Git Bash com coreutils (stat -c, sha256sum). Saindo."
  exit 2
}

FIXTURES_DIR="$(dirname "$0")/fixtures"
BASELINE_DIR="$(dirname "$0")/baseline"
TMP_OUT="$(mktemp -d)"
trap "rm -rf $TMP_OUT" EXIT

# Convert paths to Windows-style for Python (Python on Windows doesn't understand /tmp/...)
to_win() {
  if command -v cygpath >/dev/null 2>&1; then
    cygpath -w "$1"
  else
    echo "$1"
  fi
}

PASS=true
for skill in ata documento pop; do
  FIXTURE_WIN=$(to_win "$FIXTURES_DIR/$skill.content.json")
  OUT_WIN=$(to_win "$TMP_OUT/$skill.docx")
  python "$HOME/.claude/skills/$skill/build.py" \
    "$FIXTURE_WIN" \
    "$OUT_WIN" 2>/dev/null

  if [ ! -f "$TMP_OUT/$skill.docx" ]; then
    echo "❌ $skill: build.py não gerou .docx"
    PASS=false
    continue
  fi

  # 1. Tamanho ±10% (proxy frouxo)
  expected=$(stat -c%s "$BASELINE_DIR/$skill.docx")
  actual=$(stat -c%s "$TMP_OUT/$skill.docx")
  delta_abs=$(( actual > expected ? actual - expected : expected - actual ))
  threshold=$(( expected / 10 ))

  size_ok=true
  if [ "$delta_abs" -gt "$threshold" ]; then
    echo "⚠️  $skill: size delta $delta_abs > ±10% threshold ($threshold)"
    size_ok=false
  fi

  # 2. Estrutura zip (paths internos do .docx) — DETERMINÍSTICO
  actual_structure=$(python -c "
import zipfile
zf = zipfile.ZipFile(r'$OUT_WIN')
print('\n'.join(sorted(zf.namelist())))
")
  expected_structure=$(cat "$BASELINE_DIR/$skill.structure.txt")

  structure_ok=true
  if [ "$actual_structure" != "$expected_structure" ]; then
    echo "❌ $skill: estrutura zip divergiu do baseline"
    diff <(echo "$expected_structure") <(echo "$actual_structure") | head -20
    structure_ok=false
  fi

  if $size_ok && $structure_ok; then
    echo "✅ $skill: OK (size=$actual ±$delta_abs, estrutura intacta)"
  else
    PASS=false
  fi
done

if $PASS; then
  echo ""
  echo "REGRESSION PASS — 3/3 skills irmãs intactas"
  exit 0
else
  echo ""
  echo "REGRESSION FAIL"
  exit 1
fi
