#!/usr/bin/env python
"""
Orquestrador da skill /reuniao.
Uso: python reuniao.py <master.json> <selection.json> <output_dir>

Lê master.json (conteúdo) + selection.json (builders selecionados),
gera N .docx invocando os build.py das skills irmãs via subprocess.

Política transacional: partial success aceito. Aborta apenas se 0 docs geram.
"""
import json
import subprocess
import sys
from pathlib import Path
from subprocess import TimeoutExpired

SKILL_DIR = Path(__file__).parent
sys.path.insert(0, str(SKILL_DIR))
from montadores import MONTADORES

SKILL_BASE_BUILD = {
    "ata": Path.home() / ".claude/skills/ata/build.py",
    "documento": Path.home() / ".claude/skills/documento/build.py",
    "pop": Path.home() / ".claude/skills/pop/build.py",
}

BUILDER_TIMEOUT_SEC = 60
MIN_DOCX_SIZE = 30_000


def load_catalog():
    return json.loads((SKILL_DIR / "catalog.json").read_text(encoding="utf-8"))


def _slug_assunto(master):
    """Deriva slug curto do assunto da decisão (decisao_adr.titulo) ou do tópico principal."""
    from helpers import slugify
    titulo = (master.get("decisao_adr") or {}).get("titulo", "") or "geral"
    return slugify(titulo)[:40] or "geral"


def _slug_local(master):
    """Deriva slug do local do evento de degustação."""
    from helpers import slugify
    local = (master.get("evento_degustacao") or {}).get("local_slug", "") or "local"
    return slugify(local)[:30] or "local"


def resolve_filename(spec, master):
    cliente_slug = master["meta"].get("cliente", {}).get("slug", "")
    name = spec["naming_template"].replace("<cliente>", cliente_slug)
    name = name.replace("<assunto>", _slug_assunto(master))
    name = name.replace("<local>", _slug_local(master))
    return name


def main(master_path, selection_path, output_dir):
    master = json.loads(Path(master_path).read_text(encoding="utf-8"))
    selection = json.loads(Path(selection_path).read_text(encoding="utf-8"))
    catalog = {e["key"]: e for e in load_catalog()["tipos"]}
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    # PII gate — LGPD compliance (§9.2 do spec)
    # Se há cliente externo E PII não foi confirmado, aborta antes de gerar
    if selection.get("cliente_externo") and not selection.get("pii_confirmado"):
        return {
            "status": "aborted",
            "reason": "PII confirmation required: cliente_externo=true mas pii_confirmado=false",
            "docs": [],
            "failures": [],
        }

    results, failures = [], []

    for key in selection["selected_builders"]:
        spec = catalog.get(key)
        if not spec:
            failures.append({"key": key, "reason": "key não está no catálogo"})
            continue
        montador = MONTADORES.get(key)
        if not montador:
            failures.append({"key": key, "reason": "montador não implementado"})
            continue

        # Validação truthy (não só `in`) — campo {} ou [] também é "ausente" praticamente
        missing = [f for f in spec.get("fields_required", []) if not master.get(f)]
        if missing:
            failures.append({"key": key, "reason": f"campos master ausentes: {missing}"})
            continue

        try:
            content = montador(master)
        except Exception as e:
            failures.append({"key": key, "reason": f"erro no montador: {e}"})
            continue

        filename = resolve_filename(spec, master)
        out_path = out / filename
        json_path = out / f"{out_path.stem}.content.json"
        json_path.write_text(json.dumps(content, ensure_ascii=False, indent=2), encoding="utf-8")

        build_script = SKILL_BASE_BUILD[spec["skill_base"]]
        try:
            cp = subprocess.run(
                [sys.executable, str(build_script), str(json_path), str(out_path)],
                capture_output=True, text=True, timeout=BUILDER_TIMEOUT_SEC,
            )
        except TimeoutExpired:
            failures.append({"key": key, "reason": f"timeout {BUILDER_TIMEOUT_SEC}s"})
            continue

        if cp.returncode != 0 or not out_path.exists() or out_path.stat().st_size < MIN_DOCX_SIZE:
            failures.append({"key": key, "reason": (cp.stderr or "size < min")[:500]})
            continue

        results.append({
            "key": key,
            "path": str(out_path),
            "size": out_path.stat().st_size,
        })

    if not results:
        return {
            "status": "aborted",
            "docs": [],
            "failures": failures,
            "reason": "zero builders geraram .docx",
        }
    return {
        "status": "ok" if not failures else "partial",
        "docs": results,
        "failures": failures,
    }


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Uso: python reuniao.py <master.json> <selection.json> <output_dir>", file=sys.stderr)
        sys.exit(2)
    result = main(sys.argv[1], sys.argv[2], sys.argv[3])
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result["status"] != "aborted" else 1)
