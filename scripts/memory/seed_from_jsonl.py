"""Seed Singular_Memory a partir de um dump JSONL.

Cada linha do JSONL = um documento:
{
  "file_id": "drive-file-id",
  "name": "Nome do arquivo",
  "path": "TECH/Marketplace Singular.gdoc",
  "mime_type": "application/vnd.google-apps.document",
  "content": "<texto extraído>",
  "modified_time": "..."
}

Pipeline (adapta qdrant-vetor-sparseV4.py do Pedro):
  1. sanitize() — bloqueia secrets
  2. chunk_text() — parent-child genérico
  3. auto-tag por path heurístico
  4. embed batch (OpenAI dense + fastembed sparse)
  5. upsert idempotente (UUID5 determinístico)
  6. log + checkpoint a cada arquivo

Uso:
  py -3 -m memory.seed_from_jsonl --jsonl <path> [--resume] [--limit N] [--dry-run]
"""
import os
import re
import json
import uuid
import time
import argparse
from datetime import datetime
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from qdrant_client import QdrantClient, models
from openai import OpenAI
from fastembed import SparseTextEmbedding

try:
    from memory.taxonomy import coerce_taxonomy
except ImportError:  # quando rodado de dentro de scripts/memory/
    from taxonomy import coerce_taxonomy

load_dotenv(os.path.expanduser("~/.claude/.env"))

# ===================== CONFIG =====================
QDRANT_URL = os.environ["QDRANT_URL"]
QDRANT_API_KEY = os.environ.get("QDRANT_API_KEY") or None
COLLECTION = os.environ.get("SINGULAR_MEMORY_COLLECTION", "Singular_Memory")
EMBEDDING_BATCH_SIZE = 70   # bate calibração V4 (≈210k tokens, abaixo do limite 300k)
UPLOAD_BATCH_SIZE = 64
MAX_CHARS_SAFE = 18000      # trunca texto gigante antes do embed
CHILD_CHUNK_CHARS = 2000    # ≈500 tokens
PARENT_CHUNK_CHARS = 8000   # ≈2000 tokens
OVERLAP_CHARS = 400         # ≈100 tokens

CHECKPOINT_PATH = Path("~/.claude/.cache/singular-seed-checkpoint.json").expanduser()
LOG_PATH = Path("~/.claude/logs/memory/ingestion.jsonl").expanduser()

# ===================== SANITIZER =====================
SANITIZER_PATTERNS = {
    "openai_key":     re.compile(r"\bsk-[a-zA-Z0-9]{48}\b"),
    "anthropic_key":  re.compile(r"\bsk-ant-[a-zA-Z0-9\-_]{40,}\b"),
    "aws_access_key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "bearer_token":   re.compile(r"\bBearer\s+[A-Za-z0-9\-_\.=]{20,}\b"),
    "cpf":            re.compile(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b"),
    "cnpj":           re.compile(r"\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b"),
    "env_assign":     re.compile(r"^[A-Z][A-Z0-9_]+=[\S]{20,}$", re.MULTILINE),
}

def sanitize(text: str) -> tuple[str, list[str]]:
    """Retorna (texto_redacted, hits)."""
    if not text:
        return "", []
    out = text
    hits = []
    for ptype, regex in SANITIZER_PATTERNS.items():
        for m in regex.finditer(text):
            hits.append(ptype)
            out = out.replace(m.group(0), f"<REDACTED:{ptype}>")
    return out, hits

# ===================== CHUNKER (parent-child) =====================
def chunk_text(text: str) -> list[tuple[str, str, int]]:
    """Retorna list of (child_text, parent_context, chunk_offset)."""
    if not text or not text.strip():
        return []
    chunks = []
    pos = 0
    offset = 0
    n = len(text)
    while pos < n:
        end = min(pos + CHILD_CHUNK_CHARS, n)
        child = text[pos:end]
        # Parent: janela maior centrada em torno do child
        margin = (PARENT_CHUNK_CHARS - CHILD_CHUNK_CHARS) // 2
        p_start = max(0, pos - margin)
        p_end = min(n, end + margin)
        parent = text[p_start:p_end]
        chunks.append((child, parent, offset))
        offset += 1
        if end >= n:
            break
        pos = end - OVERLAP_CHARS
    return chunks

# ===================== AUTO-TAG POR PATH =====================
LEGADO_SLUGS = {
    "BEDRAN": "bedran-nexoadv", "DOC N EASY": "doc-n-easy",
    "PORTAL FITBOX": "portal-fitbox", "SMUPWEB": "smup",
    "VALORA BELEZA": "valora", "DIÁRIOS DE BORDO": "consultorio",
}

def tag_from_path(full_path: str) -> dict:
    """Heurística baseada no path do Drive Rocha."""
    p_upper = full_path.upper()
    # PROJETOS LEGADO específico
    if "PROJETOS LEGADO" in p_upper:
        for name, slug in LEGADO_SLUGS.items():
            if name in p_upper:
                return {"layer": "investida", "area": "bi-analytics", "entidade": slug}
        return {"layer": "investida", "area": "bi-analytics", "entidade": "unknown"}
    # Top-level
    if p_upper.startswith("COMERCIAL/") or "/COMERCIAL/" in p_upper:
        return {"layer": "opco", "area": "novos-negocios", "entidade": "consultorio"}
    if p_upper.startswith("FINANCEIRO/") or "/FINANCEIRO/" in p_upper:
        return {"layer": "back-office", "area": "financas", "entidade": "holding"}
    if "INSTITUCIONAL/JURÍDICO" in p_upper or "INSTITUCIONAL/JURIDICO" in p_upper:
        return {"layer": "back-office", "area": "juridico", "entidade": "holding"}
    if "INSTITUCIONAL/" in p_upper:
        return {"layer": "back-office", "area": "people-workspace", "entidade": "holding"}
    if p_upper.startswith("OPERACIONAL/CONSULTÓRIO") or "OPERACIONAL/CONSULTORIO" in p_upper:
        return {"layer": "opco", "area": "bi-analytics", "entidade": "consultorio"}
    if "OPERACIONAL/" in p_upper:
        return {"layer": "opco", "area": "novos-negocios", "entidade": "consultorio"}
    if p_upper.startswith("TECH/") or "/TECH/" in p_upper:
        return {"layer": "back-office", "area": "tecnologia", "entidade": "holding"}
    # Briefings na raiz (LOE ODONTOLOGIA - Briefing, NOME CLIENTE etc)
    if "BRIEFING" in p_upper:
        # Tenta extrair nome do cliente
        for client_slug in ["loe", "soraya", "ad-energia", "powercoffee"]:
            if client_slug.replace("-", " ").upper() in p_upper or client_slug.upper() in p_upper:
                return {"layer": "cliente", "area": "bi-analytics", "entidade": client_slug}
        return {"layer": "cliente", "area": "bi-analytics", "entidade": "unknown"}
    return {"layer": "back-office", "area": None, "entidade": "holding"}

# ===================== CHECKPOINT =====================
def load_checkpoint() -> set[str]:
    if not CHECKPOINT_PATH.exists():
        return set()
    try:
        with open(CHECKPOINT_PATH, "r", encoding="utf-8") as f:
            return set(json.load(f).get("processed_ids", []))
    except Exception:
        return set()

def save_checkpoint(processed: set[str]):
    CHECKPOINT_PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp = CHECKPOINT_PATH.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump({"processed_ids": sorted(processed),
                   "updated_at": datetime.utcnow().isoformat()}, f, indent=2)
    tmp.replace(CHECKPOINT_PATH)

def log_jsonl(record: dict):
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

# ===================== PROCESSAMENTO =====================
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jsonl", required=True, help="Path do dump JSONL")
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    jsonl_path = Path(args.jsonl).expanduser()
    if not jsonl_path.exists():
        print(f"ERRO: {jsonl_path} nao existe")
        return 1

    # Carrega dump
    docs = []
    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                docs.append(json.loads(line))
            except Exception as e:
                print(f"[skip linha invalida] {e}")
                continue
    print(f"[seed] {len(docs)} documentos no dump")

    if args.dry_run:
        print("[dry-run] mostrando tagging:")
        for d in docs[:20]:
            t = tag_from_path(d.get("path", ""))
            for _k in ("layer", "area", "entidade"):
                if _k in d:
                    t[_k] = d[_k]
            _tax, _inf = coerce_taxonomy(
                {"layer": t["layer"], "area": t["area"], "entidade": t["entidade"],
                 "bu": d.get("bu"), "cross_bu": d.get("cross_bu")}, infer=True)
            _flag = " (bu inferida baixa conf)" if _inf else ""
            print(f"  {d.get('path','?')[:50]:50s} -> {t['layer']}/{t['entidade']} "
                  f"bu={_tax['bu']}{_flag}")
        return 0

    # Clientes
    print("[seed] inicializando clientes...")
    qclient = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY, timeout=60.0)
    oclient = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    print("[seed] carregando modelo sparse bm42 (1a vez baixa ~22MB)...")
    sparse_model = SparseTextEmbedding(model_name="Qdrant/bm42-all-minilm-l6-v2-attentions")
    print("[seed] modelo sparse OK")

    processed = load_checkpoint() if args.resume else set()
    print(f"[seed] checkpoint: {len(processed)} arquivos ja processados")

    count_ok, count_skip, count_err, count_block = 0, 0, 0, 0
    total_chunks = 0
    started = time.time()

    for i, doc in enumerate(docs):
        if args.limit and (count_ok + count_skip + count_err + count_block) >= args.limit:
            break

        file_id = doc.get("file_id") or doc.get("path") or str(i)
        if file_id in processed:
            continue

        name = doc.get("name", "?")
        full_path = doc.get("path", name)
        content = doc.get("content", "")

        if not content or len(content.strip()) < 50:
            count_skip += 1
            log_jsonl({"file_id": file_id, "path": full_path, "status": "skip-empty",
                       "at": datetime.utcnow().isoformat()})
            processed.add(file_id)
            save_checkpoint(processed)
            continue

        # 1) Sanitize
        sanitized, hits = sanitize(content)
        if hits:
            count_block += 1
            log_jsonl({"file_id": file_id, "path": full_path, "status": "blocked-secrets",
                       "hits": hits, "at": datetime.utcnow().isoformat()})
            processed.add(file_id)
            save_checkpoint(processed)
            print(f"  [{i+1}/{len(docs)}] BLOCKED {name[:60]} -> secrets {hits}")
            continue

        # 2) Chunk
        chunks = chunk_text(sanitized)
        if not chunks:
            count_skip += 1
            processed.add(file_id)
            save_checkpoint(processed)
            continue

        # 3) Tags por path (heuristica) + override explicito do record + bu (4a dimensao)
        tags_path = tag_from_path(full_path)
        for _k in ("layer", "area", "entidade"):
            if _k in doc:  # presenca da chave: None explicito tambem sobrescreve o chute do path
                tags_path[_k] = doc[_k]
        tax, _inferred = coerce_taxonomy(
            {"layer": tags_path["layer"], "area": tags_path["area"],
             "entidade": tags_path["entidade"], "bu": doc.get("bu"),
             "cross_bu": doc.get("cross_bu")},
            infer=True,
        )
        if _inferred:
            log_jsonl({"file_id": file_id, "path": full_path,
                       "status": "bu-inferred-lowconf", "bu": tax["bu"],
                       "at": datetime.utcnow().isoformat()})
            print(f"    [bu] inferida (baixa confianca): {tax['bu']} <- "
                  f"{tags_path['layer']}/{tags_path['area']}/{tags_path['entidade']}")

        # 4) Embed em batches
        try:
            child_texts = [c[0][:MAX_CHARS_SAFE] for c in chunks]
            all_points = []
            for start in range(0, len(chunks), EMBEDDING_BATCH_SIZE):
                batch = child_texts[start:start+EMBEDDING_BATCH_SIZE]
                # Dense
                resp = oclient.embeddings.create(input=batch, model="text-embedding-3-large")
                dense_vectors = [d.embedding for d in resp.data]
                # Sparse
                sparse_vectors = list(sparse_model.embed(batch))
                # Build points
                for j, (child, parent, offset) in enumerate(chunks[start:start+EMBEDDING_BATCH_SIZE]):
                    sparse_raw = sparse_vectors[j]
                    sparse_formatted = models.SparseVector(
                        indices=sparse_raw.indices.tolist(),
                        values=sparse_raw.values.tolist(),
                    )
                    # UUID5 determinístico (mesmo formato V4)
                    point_id = str(uuid.uuid5(
                        uuid.NAMESPACE_DNS,
                        (child[:500] + str(file_id) + str(offset))[:1000]
                    ))
                    payload = {
                        "schema_version": "v1",
                        "embedding_model": "openai-text-embedding-3-large",
                        "type": "dado-mestre",
                        "layer": tax["layer"],
                        "area": tax["area"],
                        "entidade": tax["entidade"],
                        "bu": tax["bu"],
                        "cross_bu": tax["cross_bu"],
                        "title": name,
                        "child_text": child,
                        "parent_context": parent,
                        "source_file": f"drive:{file_id}",
                        "drive_path": full_path,
                        "chunk_offset": offset,
                        "session_id": None,
                        "session_date": datetime.utcnow().strftime("%Y-%m-%d"),
                        "ambiente": "desktop",
                        "tags": [full_path.split("/")[0].lower()] if "/" in full_path else [],
                        "confidence": 0.9,  # heurística por path, alta confiança
                        "ingested_at": datetime.utcnow().isoformat(),
                        "ingested_by": "seed-drive",
                        "had_secrets": False,
                    }
                    all_points.append(models.PointStruct(
                        id=point_id,
                        vector={"dense_vector": dense_vectors[j], "sparse_vector": sparse_formatted},
                        payload=payload,
                    ))

            # 5) Upload
            qclient.upload_points(
                collection_name=COLLECTION,
                points=all_points,
                batch_size=UPLOAD_BATCH_SIZE,
                wait=True,
            )
            count_ok += 1
            total_chunks += len(all_points)
            log_jsonl({"file_id": file_id, "path": full_path, "status": "ok",
                       "chunks": len(all_points), "tags": tags_path,
                       "at": datetime.utcnow().isoformat()})
            elapsed = time.time() - started
            rate = (count_ok + count_skip + count_err + count_block) / max(elapsed, 1)
            print(f"  [{i+1}/{len(docs)}] OK {name[:50]:50s} ({len(all_points)} chunks, "
                  f"{tags_path['layer']}/{tags_path['entidade']} bu={tax['bu']}) [{rate:.1f}/s, "
                  f"{total_chunks} total]")

        except Exception as e:
            count_err += 1
            log_jsonl({"file_id": file_id, "path": full_path, "status": "error",
                       "error": str(e)[:300], "at": datetime.utcnow().isoformat()})
            print(f"  [{i+1}/{len(docs)}] ERR {name[:50]} -> {str(e)[:100]}")

        processed.add(file_id)
        save_checkpoint(processed)
        time.sleep(0.3)   # throttle conservador

    elapsed = time.time() - started
    print(f"\n=== SEED COMPLETO ===")
    print(f"OK:       {count_ok}")
    print(f"SKIP:     {count_skip}")
    print(f"BLOCKED:  {count_block}")
    print(f"ERROR:    {count_err}")
    print(f"Chunks:   {total_chunks}")
    print(f"Tempo:    {elapsed/60:.1f} min")
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
