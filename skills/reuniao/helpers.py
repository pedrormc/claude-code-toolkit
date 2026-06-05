"""
Helpers para a skill /reuniao:
- PII detector (LGPD compliance)
- Slug resolver (cliente → abreviação curta)
- Folder name resolver (resolve conflitos no Drive)
- Audit log writer
"""
import json
import re
import unicodedata
from datetime import datetime
from pathlib import Path

SKILL_DIR = Path(__file__).parent
SECRETS_PATH = Path.home() / ".claude/secrets/reuniao.json"

PII_PATTERNS = {
    "cpf": r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b",
    "cnpj": r"\b\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}\b",
    "cartao": r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b",
    "cep": r"\b\d{5}-?\d{3}\b",
    "telefone": r"\b(?:\+?55\s?)?\(?\d{2}\)?\s?9?\d{4}-?\d{4}\b",
    "email": r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b",
}


def load_secrets():
    return json.loads(SECRETS_PATH.read_text(encoding="utf-8"))


def detect_pii(text: str) -> dict:
    """Retorna {tipo_pii: count_de_ocorrências}."""
    findings = {}
    for name, pattern in PII_PATTERNS.items():
        matches = re.findall(pattern, text)
        if matches:
            findings[name] = len(matches)
    return findings


def slugify(s: str) -> str:
    """Lowercase, sem acento, espaço→hifen, alfanumérico."""
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    s = s.lower()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"\s+", "-", s).strip("-")
    return s


def resolve_cliente_slug(nome_cliente: str, clientes_path: Path = None) -> tuple[str, bool]:
    """Retorna (slug, is_novo). Consulta clientes.json; se não achar, retorna slug derivado + flag novo."""
    if clientes_path is None:
        clientes_path = SKILL_DIR / "clientes.json"
    clientes = json.loads(clientes_path.read_text(encoding="utf-8"))
    nome_lc = nome_cliente.lower().strip()
    if nome_lc in clientes:
        return clientes[nome_lc], False
    fallback = slugify(nome_cliente)[:4]
    return fallback, True


def save_cliente_slug(nome_cliente: str, slug: str, clientes_path: Path = None) -> None:
    """Persiste cliente novo. Faz backup .bak.<timestamp> antes."""
    if clientes_path is None:
        clientes_path = SKILL_DIR / "clientes.json"
    clientes = json.loads(clientes_path.read_text(encoding="utf-8"))
    if slug in clientes.values():
        raise ValueError(f"Slug '{slug}' já está em uso. Escolher outro.")
    backup = clientes_path.with_suffix(f".bak.{datetime.now().strftime('%Y%m%d-%H%M%S')}")
    backup.write_text(clientes_path.read_text(encoding="utf-8"), encoding="utf-8")
    clientes[nome_cliente.lower().strip()] = slug
    clientes_path.write_text(json.dumps(clientes, ensure_ascii=False, indent=2), encoding="utf-8")


def resolve_folder_name(slug_cliente: str, data_iso: str, existing_names: list[str]) -> str:
    """Resolve conflito de nome de pasta Drive.
    Tenta 'reuniao <slug>'; se existe, append data; se existe, append letra.
    """
    base = f"reuniao {slug_cliente}".strip()
    if base not in existing_names:
        return base
    with_date = f"{base} {data_iso[:10]}"
    if with_date not in existing_names:
        return with_date
    for letra in "bcdefghij":
        with_letra = f"{with_date} {letra}"
        if with_letra not in existing_names:
            return with_letra
    raise RuntimeError(f"Não foi possível resolver conflito de pasta para '{base}'")


LEARNED_FLAG = "learned"
VALID_SKILL_BASES = {"ata", "documento", "pop"}
VALID_MONTADORES = {"generico", "generico_pop"}


def append_learned_type(catalog_path: Path, entry: dict) -> tuple[bool, str]:
    """Auto-improve: persiste um tipo de doc NOVO (brainstormado e aprovado) no catálogo.

    Retorna (persistido, motivo).
    - Idempotente: se entry['key'] já existe no catálogo → no-op (False, "já existe").
    - Faz backup .bak.<timestamp> antes de gravar (nunca sobrescreve sem cópia).
    - NUNCA edita/remove entradas existentes — só faz append (feedback_never_delete).
    - Valida o mínimo p/ o orquestrador conseguir construir o tipo depois.
    """
    required = {"key", "skill_base", "naming_template", "montador", "master_field"}
    missing = required - set(entry)
    if missing:
        return False, f"entry inválida: faltam campos {sorted(missing)}"
    if entry["skill_base"] not in VALID_SKILL_BASES:
        return False, f"skill_base inválida: {entry['skill_base']}"
    if entry["montador"] not in VALID_MONTADORES:
        return False, f"montador inválido: {entry['montador']}"

    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    existing_keys = {e["key"] for e in catalog.get("tipos", [])}
    if entry["key"] in existing_keys:
        return False, "já existe no catálogo"

    learned = {
        "key": entry["key"],
        "skill_base": entry["skill_base"],
        "label": entry.get("label", entry["key"]),
        "naming_template": entry["naming_template"],
        "scope": entry.get("scope", "internal"),
        "flag": LEARNED_FLAG,
        "montador": entry["montador"],
        "master_field": entry["master_field"],
        "triggers": entry.get("triggers", []),
        "fields_required": entry.get("fields_required", [entry["master_field"]]),
        "learned_at": datetime.now().isoformat(),
        "learned_from": entry.get("learned_from", ""),
    }

    backup = catalog_path.with_suffix(f".bak.{datetime.now().strftime('%Y%m%d-%H%M%S')}")
    backup.write_text(catalog_path.read_text(encoding="utf-8"), encoding="utf-8")

    catalog.setdefault("tipos", []).append(learned)
    catalog_path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8")
    return True, "persistido"


def write_audit_log(output_dir: Path, payload: dict) -> Path:
    """Grava audit.log na pasta local para auditoria LGPD."""
    log = output_dir / "audit.log"
    entry = {**payload, "timestamp": datetime.now().isoformat()}
    log.write_text(json.dumps(entry, ensure_ascii=False, indent=2), encoding="utf-8")
    return log
