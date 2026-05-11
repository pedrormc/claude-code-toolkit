"""
Cliente de busca jurídica no Qdrant Nexo_Adv (REST direto via httpx).

Por que httpx em vez de qdrant-client?
- Cloudflare na frente expõe só HTTPS:443; o qdrant-client Python tenta porta 6333 por default mesmo com URL HTTPS, gera ConnectTimeout.
- httpx fala REST puro contra o domínio público, sem assumir porta/gRPC.

Uso CLI:
    python qdrant_search.py "obrigação de meio versus resultado"
    python qdrant_search.py "indenização representante comercial" --area Empresarial
    python qdrant_search.py "multa cláusula penal" --area Civel --top 10

Uso programático:
    from qdrant_search import NexoAdvClient
    client = NexoAdvClient()
    chunks = client.search("LGPD em contrato", top_k=5)
"""

import argparse
import json
import os
import sys
from pathlib import Path

import httpx
from dotenv import load_dotenv
from openai import OpenAI

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent

load_dotenv(SKILL_DIR / ".env")

QDRANT_URL = os.getenv("QDRANT_URL", "https://seu-qdrant.exemplo.com").rstrip("/")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "Nexo_Adv")
EMBED_MODEL = os.getenv("EMBED_MODEL", "text-embedding-3-large")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

VALID_AREAS = {
    "Administrativo", "Ambiental", "Civel", "Consumidor", "Contitucional",
    "Digital", "Eleitoral", "Empresarial", "Familia", "Penal",
    "Previdenciario", "Processual_civil", "Trabalhista", "Tributario",
}


class NexoAdvClient:
    def __init__(self):
        if not OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY ausente no .env da skill")
        if not QDRANT_API_KEY:
            raise RuntimeError("QDRANT_API_KEY ausente no .env da skill")
        self.openai = OpenAI(api_key=OPENAI_API_KEY)
        self.http = httpx.Client(
            base_url=QDRANT_URL,
            headers={"api-key": QDRANT_API_KEY, "Content-Type": "application/json"},
            timeout=60.0,
        )
        self.collection = QDRANT_COLLECTION

    def embed(self, text: str) -> list[float]:
        """Gera embedding 3072d (text-embedding-3-large) — bate com Nexo_Adv."""
        text = text.replace("\n", " ").strip()
        resp = self.openai.embeddings.create(model=EMBED_MODEL, input=[text])
        return resp.data[0].embedding

    def search(
        self,
        query: str,
        top_k: int = 5,
        area: str | None = None,
        only_parents: bool = False,
    ) -> list[dict]:
        """
        Dense search no Nexo_Adv (named vector 'dense_vector', 3072d, Cosine).

        - query: texto da consulta jurídica
        - top_k: quantos chunks retornar
        - area: filtra por law_area (ex: "Empresarial", "Trabalhista")
        - only_parents: retorna apenas chunks do tipo parent_node
        """
        if area and area not in VALID_AREAS:
            print(f"AVISO: area '{area}' não está no conjunto conhecido. "
                  f"Válidas: {sorted(VALID_AREAS)}", file=sys.stderr)

        vector = self.embed(query)

        must = []
        if area:
            must.append({"key": "law_area", "match": {"value": area}})
        if only_parents:
            must.append({"key": "type", "match": {"value": "parent_node"}})

        body = {
            "query": vector,
            "using": "dense_vector",
            "limit": top_k,
            "with_payload": True,
            "with_vector": False,
        }
        if must:
            body["filter"] = {"must": must}

        resp = self.http.post(f"/collections/{self.collection}/points/query", json=body)
        if resp.status_code != 200:
            raise RuntimeError(f"Qdrant {resp.status_code}: {resp.text[:300]}")

        data = resp.json()
        points = (data.get("result") or {}).get("points", [])

        chunks = []
        for p in points:
            payload = p.get("payload") or {}
            chunks.append({
                "score": p.get("score"),
                "id": str(p.get("id")),
                "law_area": payload.get("law_area"),
                "source_file": payload.get("source_file"),
                "article_ref": payload.get("article_ref"),
                "type": payload.get("type"),
                "child_text": payload.get("child_text", ""),
                "parent_context": payload.get("parent_context", ""),
            })
        return chunks


def main():
    ap = argparse.ArgumentParser(description="Busca semântica no Nexo_Adv (Qdrant)")
    ap.add_argument("query", help="Consulta jurídica em linguagem natural")
    ap.add_argument("--area", help="Filtrar por law_area", default=None)
    ap.add_argument("--top", type=int, default=5, help="Quantidade de resultados")
    ap.add_argument("--parents", action="store_true", help="Apenas parent_node")
    ap.add_argument("--json", action="store_true", help="Output JSON puro")
    args = ap.parse_args()

    client = NexoAdvClient()
    chunks = client.search(args.query, top_k=args.top, area=args.area, only_parents=args.parents)

    if args.json:
        print(json.dumps(chunks, ensure_ascii=False, indent=2))
        return

    print(f"\n=== {len(chunks)} resultados para: {args.query!r} ===")
    if args.area:
        print(f"=== Filtro: law_area = {args.area} ===")
    print()

    for i, c in enumerate(chunks, 1):
        score = c.get("score") or 0
        print(f"--- [{i}] score={score:.4f} | {c['law_area']} | {c['type']} ---")
        print(f"Fonte: {c['source_file']}")
        if c.get("article_ref"):
            ref = (c["article_ref"] or "")[:120].replace("\n", " ")
            print(f"Ref:   {ref}")
        text = (c["child_text"] or "")[:500].replace("\n", " ")
        more = "..." if len(c.get("child_text") or "") > 500 else ""
        print(f"Texto: {text}{more}")
        print()


if __name__ == "__main__":
    main()
