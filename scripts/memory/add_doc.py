"""Helper: lê drive-tmp/<id>.txt + metadados via CLI e monta drive-tmp/<id>.doc.json.

Uso:
  py -3 -m memory.add_doc --file-id X --name "Y" --path "Z" [--mime-type ...]
"""
import argparse
import json
import sys
from pathlib import Path

DRIVE_TMP = Path("C:/Users/teste/.claude/.cache/drive-tmp")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file-id", required=True)
    ap.add_argument("--name", required=True)
    ap.add_argument("--path", required=True)
    ap.add_argument("--mime-type", default="application/vnd.google-apps.document")
    args = ap.parse_args()

    txt_path = DRIVE_TMP / f"{args.file_id}.txt"
    if not txt_path.exists():
        print(f"ERRO: {txt_path} nao existe")
        return 1

    content = txt_path.read_text(encoding="utf-8")
    if len(content) > 60000:
        content = content[:60000]

    rec = {
        "file_id": args.file_id,
        "name": args.name,
        "path": args.path,
        "mime_type": args.mime_type,
        "content": content,
    }
    out_path = DRIVE_TMP / f"{args.file_id}.doc.json"
    out_path.write_text(json.dumps(rec, ensure_ascii=False), encoding="utf-8")
    print(f"OK {len(content)} chars -> {out_path.name}")
    # Limpa o .txt depois de consolidar
    txt_path.unlink()
    return 0


if __name__ == "__main__":
    sys.exit(main())
