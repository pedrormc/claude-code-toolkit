# Singular_Memory — Sistema de Memoria Permanente

> Stack de memoria permanente da Singular Group sobre Qdrant. Implementada como parte do Backoffice Pro Max (Fase 1, 2026-05-19).

## Visao Geral

O Singular_Memory permite que o Claude Code tenha **contexto persistente** sobre toda a Singular Group: clientes, projetos, investidas, decisoes, contratos, atas, POPs. Funciona como um "cerebro" que acumula conhecimento a cada interacao.

### Stack Tecnica

| Componente | Tecnologia |
|-----------|------------|
| Vector DB | Qdrant (self-hosted, AWS Lightsail) |
| Dense embeddings | OpenAI `text-embedding-3-large` (3072 dims) |
| Sparse embeddings | fastembed `bm42` |
| Search | Hybrid (dense + sparse), RRF fusion |
| Chunking | Parent-child (documento → chunks) |
| IDs | UUID5 determinístico (namespace + content hash) |
| Collection | `Singular_Memory` |

### Taxonomy 3D

Todo documento catalogado usa 3 dimensoes:

| Dimensao | Valores |
|----------|---------|
| **layer** | front-office, middle-office, back-office, opco, investida, cliente |
| **area** | comercial, financeiro, juridico, tech, people, operacional, institucional, marketing, produto, compliance, estrategia |
| **entidade** | holding, Singular Venture, SMUP, Singular Consultoria, PWR Coffee, Bossfit, Adonai, etc. |

### Regra Soberana #3 (Catalogacao Singular)

Toda interacao com material Singular DEVE seguir o ciclo:

1. **RECALL** — Antes de responder sobre clientes/projetos/investidas/BUs/valores/decisoes, consultar o Singular_Memory
2. **INGEST** — Depois de criar contrato/ata/POP/slide/proposta canonica, indexar no Singular_Memory
3. **CATALOGAR** — Usar taxonomy 3D (layer/area/entidade) em frontmatter de memorias e payload Qdrant

## Scripts

Todos em `scripts/memory/`:

| Script | Funcao | Uso |
|--------|--------|-----|
| `create_collection.py` | Cria collection no Qdrant com schema hybrid (dense + sparse) | Setup inicial |
| `add_doc.py` | Adiciona documento ao Qdrant com parent-child chunking | Ingest de novos docs |
| `consolidate_jsonl.py` | Consolida multiplos JSONL em arquivo unico | Manutencao |
| `seed_from_jsonl.py` | Faz seed da collection a partir de JSONL pre-processado | Bulk load |
| `__init__.py` | Package init | Import |

### Exemplo de uso

```python
# Recall: buscar contexto antes de responder
from qdrant_client import QdrantClient
from openai import OpenAI

client = QdrantClient(url="http://YOUR_QDRANT_URL:6333")
openai = OpenAI()

query_embedding = openai.embeddings.create(
    model="text-embedding-3-large",
    input="PWR Coffee investimento"
).data[0].embedding

results = client.query_points(
    collection_name="Singular_Memory",
    query=query_embedding,
    limit=5
)
```

### Ingest via scripts

```bash
# Adicionar documento
python ~/.claude/scripts/memory/add_doc.py \
  --file "caminho/do/documento.md" \
  --layer "middle-office" \
  --area "financeiro" \
  --entidade "PWR Coffee"

# Seed a partir de JSONL
python ~/.claude/scripts/memory/seed_from_jsonl.py \
  --input "dados.jsonl" \
  --collection "Singular_Memory"
```

## Configuracao

### Requisitos

- Python 3.10+
- `pip install qdrant-client openai fastembed`
- Acesso ao Qdrant server (URL + porta 6333)
- API key OpenAI (para embeddings)

### Env vars

```bash
export QDRANT_URL="http://YOUR_QDRANT_URL:6333"
export OPENAI_API_KEY="sk-..."
```

> **ATENCAO:** URLs e API keys reais estao no ambiente Desktop do Pedro, NUNCA commitados no repo.

## Fase atual

- **Fase 1** (2026-05-19): Collection criada, 16 chunks iniciais, smoke test OK
- **Fases 2-6**: Pendentes (auto-ingest, skills awareness, Hermes-style recall, UI)

## Referencia

- Spec: `C:/Users/teste/plano/plano/projetos/backoffice-pro-max/`
- Memory records: `~/.claude/projects/*/memory/reference_singular_memory_stack.md`
- Taxonomy: `~/.claude/projects/*/memory/feedback_taxonomy_3d_singular.md`
