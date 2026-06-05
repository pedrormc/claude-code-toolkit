"""Cria a collection Singular_Memory no Qdrant.

Schema: replica o Nexo_Adv (qdrant-vetor-sparseV4.py do Pedro):
  - dense_vector: 3072d (OpenAI text-embedding-3-large), Cosine
  - sparse_vector: bm42 (fastembed local)

Adapta payload pra Singular: child_text + parent_context + taxonomy 3D
(layer/area/entidade) em vez de law_area.

Idempotente: se já existir, skip; pra recriar, passar --recreate.
"""
import os
import sys
import argparse
from dotenv import load_dotenv
from qdrant_client import QdrantClient, models

load_dotenv(os.path.expanduser("~/.claude/.env"))

QDRANT_URL = os.environ["QDRANT_URL"]
QDRANT_API_KEY = os.environ.get("QDRANT_API_KEY") or None
COLLECTION = os.environ.get("SINGULAR_MEMORY_COLLECTION", "Singular_Memory")

# Payload indices pra filtros eficientes na Recall
PAYLOAD_INDICES = [
    ("layer", "keyword"),
    ("area", "keyword"),
    ("entidade", "keyword"),
    ("bu", "keyword"),
    ("cross_bu", "keyword"),
    ("type", "keyword"),
    ("session_id", "keyword"),
    ("source_file", "keyword"),
    ("session_date", "keyword"),
    ("zel", "keyword"),  # per-Zel isolation (D2) — turn-summary rows; seed rows have no 'zel'
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--recreate", action="store_true",
                    help="Deleta collection existente e cria do zero (CUIDADO)")
    args = ap.parse_args()

    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY, timeout=60.0)

    exists = client.collection_exists(collection_name=COLLECTION)
    if exists and args.recreate:
        print(f"[!] Deletando collection existente '{COLLECTION}'...")
        client.delete_collection(collection_name=COLLECTION)
        exists = False

    if exists:
        print(f"OK Collection '{COLLECTION}' ja existe. Skip create.")
        info = client.get_collection(collection_name=COLLECTION)
        print(f"   Pontos: {info.points_count}, status: {info.status}")
    else:
        print(f"[*] Criando collection '{COLLECTION}'...")
        client.create_collection(
            collection_name=COLLECTION,
            vectors_config={
                "dense_vector": models.VectorParams(
                    size=3072,
                    distance=models.Distance.COSINE,
                ),
            },
            sparse_vectors_config={
                "sparse_vector": models.SparseVectorParams(
                    index=models.SparseIndexParams(on_disk=False),
                ),
            },
        )
        print(f"OK Collection '{COLLECTION}' criada (dense:3072 Cosine + sparse:bm42).")

    # Criar payload indices pra filtros rapidos
    print(f"\n[*] Criando payload indices em {COLLECTION}...")
    for field_name, schema in PAYLOAD_INDICES:
        try:
            client.create_payload_index(
                collection_name=COLLECTION,
                field_name=field_name,
                field_schema=schema,
            )
            print(f"   OK index '{field_name}' ({schema})")
        except Exception as e:
            msg = str(e)
            if "already exists" in msg.lower() or "exists" in msg.lower():
                print(f"   - index '{field_name}' ja existe (skip)")
            else:
                print(f"   ! erro index '{field_name}': {msg[:100]}")

    print("\n=== STATUS FINAL ===")
    info = client.get_collection(collection_name=COLLECTION)
    print(f"Collection: {COLLECTION}")
    print(f"Pontos:     {info.points_count}")
    print(f"Status:     {info.status}")
    print(f"Vectors:    dense (3072d Cosine) + sparse (bm42)")
    print(f"Indices:    {[f for f, _ in PAYLOAD_INDICES]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
