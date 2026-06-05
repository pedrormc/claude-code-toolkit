#!/usr/bin/env python
"""
Orquestrador da skill /reuniao.
Uso: python reuniao.py <master.json> <selection.json> <output_dir>

Lê master.json (conteúdo) + selection.json (builders selecionados),
gera N .docx invocando os build.py das skills irmãs via subprocess.

Política transacional: partial success aceito. Aborta apenas se 0 docs geram.
"""
import json
import os
import subprocess
import sys
from pathlib import Path
from subprocess import TimeoutExpired

SKILL_DIR = Path(__file__).parent
sys.path.insert(0, str(SKILL_DIR))
from montadores import MONTADORES, GENERIC_MONTADORES
from helpers import append_learned_type

# Catálogo. Override via env REUNIAO_CATALOG (usado pelos testes pra não poluir o real).
CATALOG_PATH = Path(os.environ.get("REUNIAO_CATALOG") or (SKILL_DIR / "catalog.json"))

SKILL_BASE_BUILD = {
    "ata": Path.home() / ".claude/skills/ata/build.py",
    "documento": Path.home() / ".claude/skills/documento/build.py",
    "pop": Path.home() / ".claude/skills/pop/build.py",
}

BUILDER_TIMEOUT_SEC = 60
MIN_DOCX_SIZE = 30_000


def load_catalog():
    return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))


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


def resolve_montador(key, spec):
    """Resolve o montador. Tipos canônicos → MONTADORES[key] (fn(master)).
    Tipos NOVOS/aprendidos → genérico via spec['montador'], com spec injetado.
    Retorna uma callable fn(master) ou None.
    """
    fn = MONTADORES.get(key)
    if fn:
        return fn
    gen = spec.get("montador")
    gen_fn = GENERIC_MONTADORES.get(gen)
    if gen_fn:
        return lambda m: gen_fn(m, spec)
    return None


def main(master_path, selection_path, output_dir):
    master = json.loads(Path(master_path).read_text(encoding="utf-8"))
    selection = json.loads(Path(selection_path).read_text(encoding="utf-8"))
    catalog = {e["key"]: e for e in load_catalog()["tipos"]}

    # Auto-improve: tipos NOVOS brainstormados nesta reunião. Mescla no catálogo
    # em memória pra conseguir construí-los AGORA; persiste depois (só os que geraram).
    learned_specs = {e["key"]: e for e in selection.get("learned_types", [])}
    for key, spec in learned_specs.items():
        catalog.setdefault(key, spec)

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
        montador = resolve_montador(key, spec)
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

    # Auto-improve (automático): persiste no catálogo todo tipo NOVO que gerou .docx OK.
    # Best-effort — falha aqui nunca derruba a entrega (o doc já foi gerado).
    learned_persisted, learned_skipped = [], []
    built_keys = {r["key"] for r in results}
    for key in learned_specs:
        if key not in built_keys:
            continue
        try:
            ok, motivo = append_learned_type(CATALOG_PATH, learned_specs[key])
            (learned_persisted if ok else learned_skipped).append({"key": key, "motivo": motivo})
        except Exception as e:
            learned_skipped.append({"key": key, "motivo": f"erro ao persistir: {e}"})

    return {
        "status": "ok" if not failures else "partial",
        "docs": results,
        "failures": failures,
        "learned_persisted": learned_persisted,
        "learned_skipped": learned_skipped,
    }


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Uso: python reuniao.py <master.json> <selection.json> <output_dir>", file=sys.stderr)
        sys.exit(2)
    result = main(sys.argv[1], sys.argv[2], sys.argv[3])
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result["status"] != "aborted" else 1)
