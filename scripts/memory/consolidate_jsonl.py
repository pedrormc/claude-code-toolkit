"""Consolida pares (drive-tmp/<id>.txt + drive-tmp/<id>.meta.json) → JSONL.

Cada par:
  drive-tmp/<file_id>.txt           = content puro
  drive-tmp/<file_id>.meta.json     = {"name":"","path":"","mime_type":""}

Append-only no JSONL final. Idempotente via file_id.
"""
import argparse
import json
import sys
from pathlib import Path

DRIVE_TMP = Path("C:/Users/teste/.claude/.cache/drive-tmp")
JSONL = Path("C:/Users/teste/.claude/.cache/singular-drive-dump.jsonl")


def load_existing_ids() -> set[str]:
    if not JSONL.exists():
        return set()
    ids = set()
    with open(JSONL, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
                if "file_id" in rec:
                    ids.add(rec["file_id"])
            except Exception:
                continue
    return ids


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--clean-tmp", action="store_true")
    args = ap.parse_args()

    if not DRIVE_TMP.exists():
        print(f"ERRO: pasta {DRIVE_TMP} nao existe")
        return 1

    existing = load_existing_ids()
    print(f"[consolidate] {len(existing)} file_ids ja no JSONL")

    JSONL.parent.mkdir(parents=True, exist_ok=True)
    doc_files = sorted(DRIVE_TMP.glob("*.doc.json"))
    print(f"[consolidate] {len(doc_files)} .doc.json em drive-tmp/")

    added, skipped, errors = 0, 0, 0
    files_to_clean = []

    with open(JSONL, "a", encoding="utf-8") as out:
        for doc in doc_files:
            fid = doc.name.replace(".doc.json", "")
            try:
                rec = json.loads(doc.read_text(encoding="utf-8"))
                if not rec.get("content") or len(rec["content"].strip()) < 30:
                    skipped += 1
                    files_to_clean.append(doc)
                    continue
                if fid in existing:
                    skipped += 1
                    files_to_clean.append(doc)
                    continue
                if len(rec["content"]) > 60000:
                    rec["content"] = rec["content"][:60000]
                out.write(json.dumps(rec, ensure_ascii=False) + "\n")
                added += 1
                existing.add(fid)
                files_to_clean.append(doc)
            except Exception as e:
                errors += 1
                print(f"  ! erro em {fid}: {e}")

    print(f"\n=== CONSOLIDATE ===")
    print(f"Adicionados: {added}")
    print(f"Skipped:     {skipped}")
    print(f"Erros:       {errors}")
    print(f"Total no JSONL: {len(existing)}")

    if args.clean_tmp:
        for f in files_to_clean:
            try:
                f.unlink()
            except Exception:
                pass
        print(f"[clean] arquivos drive-tmp/ removidos")
    return 0


if __name__ == "__main__":
    sys.exit(main())
