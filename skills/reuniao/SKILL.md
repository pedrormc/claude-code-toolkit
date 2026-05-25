---
name: reuniao
description: Recebe transcrição/notas de reunião e gera uma SUITE COMPLETA de documentos .docx Singular (ata + N documentos derivados + N POPs derivados) numa pasta Drive dedicada `Zel/reuniao <slug>/`. Analisa o texto, consulta catálogo de 17 tipos canônicos, sugere quais documentos fazem sentido, e gera apenas os que o Pedro aprovar. Use quando o usuário digitar /reuniao seguido de texto, ou pedir "processa essa reunião", "monta a pasta dessa reunião", "gera os docs dessa reunião".
---

# /reuniao — Suite generativa de documentos pós-reunião

Orquestrador que reusa `/ata`, `/documento` e `/pop` para gerar a suite completa de documentos derivados de uma reunião, agrupada em pasta Drive dedicada.

## Quando usar

Invoque quando o usuário:
- Digitar `/reuniao` (com ou sem `@cliente`) seguido de texto da reunião
- Pedir "processa essa reunião", "monta a pasta da reunião", "gera os docs"
- Entregar transcrição/notas e pedir "kit completo da reunião"
- Quiser replicar o padrão da pasta `Zel/reuniao pwr/` (powercoffee)

**Não usar quando:**
- For só uma ata simples → `/ata`
- For só 1 documento avulso → `/documento`
- For só 1 POP → `/pop`

## Arquitetura

A skill é orquestrador PURO. Não tem `build.py` próprio nem template `.docx`. Reusa:
- `~/.claude/skills/ata/build.py` (para `ata-*`)
- `~/.claude/skills/documento/build.py` (para `doc-*`)
- `~/.claude/skills/pop/build.py` (para `pop-*`)

Catálogo de 17 tipos em `catalog.json`. Montadores em `montadores.py`. Orquestrador em `reuniao.py`.

## Fluxo de execução (10 passos — NÃO pule)

### Passo 1 — Análise do texto

Leia a transcrição/notas e extraia:
- **Tipo de reunião:** comercial / técnica / estratégica / kickoff / retro / 1:1 / daily / interna
- **Cliente externo (se houver):** nome, vertical, contatos
- **Participantes:** presentes + ausentes
- **Tópicos discutidos:** com discussão + decisões
- **Encaminhamentos:** ação + responsável + prazo
- **Riscos / pendências**
- **Sinais por tipo de doc:** posicionamento, cronograma editorial, TikTok, marketplace, etc.

**Regra crítica:** NUNCA invente nomes, datas, decisões. Campos ausentes → marcar "A definir".

### Passo 2 — Resolver slug do cliente

```bash
# Lê clientes.json
python -c "
import json, sys
sys.path.insert(0, '$HOME/.claude/skills/reuniao')
from helpers import resolve_cliente_slug
slug, is_novo = resolve_cliente_slug('<nome cliente>')
print(f'slug={slug} novo={is_novo}')
"
```

Se `is_novo=True`, **pergunte ao Pedro** a abreviação a usar (3-4 letras) e salve via `save_cliente_slug`.

Se reunião não tem cliente externo → slug = "singular".

### Passo 3 — Filtro do catálogo

Carregue `catalog.json`. Para cada tipo:
- `flag == "always"` → sempre inclui (apenas `ata-reuniao`)
- `flag == "auto_suggest"` → inclui se condição satisfaz (ex: `len(encaminhamentos) ≥ 2`)
- Sem flag → calcula match score: quantos triggers (case-insensitive) aparecem no texto da reunião

Inclua todo tipo com `score > 0` ou `flag` ativa.

### Passo 4 — Detector de PII

```bash
python -c "
import sys; sys.path.insert(0, '$HOME/.claude/skills/reuniao')
from helpers import detect_pii
findings = detect_pii('''<TEXTO INTEIRO DA REUNIÃO>''')
print(findings)
"
```

Se houver findings **E** há cliente externo → no passo 5 incluir aviso PII.

### Passo 5 — AskUserQuestion multiSelect

Pergunte ao Pedro quais documentos gerar:

```
Detectei: reunião <tipo> sobre <tema> [com cliente: <nome> (<slug>)].
Sugestões (pre-selecionados marcados ✓):

[✓] ata-reuniao — sempre
[✓] doc-tarefas-completas — auto-sugerido (5 encaminhamentos)
[✓] doc-plano-comercial — match: "plano", "metas vendas"
[ ] doc-briefing-posicionamento — match: "posicionamento"
[ ] pop-roteiro-roleplay — match: "script vendas"
[ ] doc-decisao — match: "decidimos"
...

⚠️ PII detectada: 2 CPF, 1 email — pasta vai pra Drive Singular com auto-share. Confirma?

Pasta sugerida: `Zel/reuniao pwr/`. Override?
```

Aguarde resposta. Se Pedro deselecionar tudo, aborta limpo.

### Passo 6 — Compor master.json + selection.json

Crie `output_dir = /c/Users/teste/Desktop/reunioes/<slug>-<data>/`.

Componha `master.json` com TODO o conteúdo extraído (não só dos selecionados — preserva contexto para re-rodada futura). Schema completo em §6.1 do spec.

Componha `selection.json`:
```json
{
  "selected_builders": [...],
  "drive_folder_name": "reuniao pwr",
  "data_geracao": "<ISO 8601>",
  "pii_confirmado": true | false,
  "cliente_externo": true | false
}
```

Aplique norma culta PT-BR em todo conteúdo antes de gravar (use `~/.claude/skills/pop/references/accents.md`).

### Passo 7 — Rodar orquestrador

```bash
python ~/.claude/skills/reuniao/reuniao.py \
  /c/Users/teste/Desktop/reunioes/<slug>-<data>/master.json \
  /c/Users/teste/Desktop/reunioes/<slug>-<data>/selection.json \
  /c/Users/teste/Desktop/reunioes/<slug>-<data>/
```

Parse o JSON de retorno. Se `status == "aborted"`, reporta erro ao Pedro e para.

### Passo 8 — Setup pasta Drive

Use MCP `google-drive`:

1. **Search nomes existentes** dentro de `Zel/`:
   - `mcp__google-drive__listFolder(folderId="10ARKUMWyFzVkdaPEWLYC9OXWqm0ywS6e")`
2. **Resolve nome final** (sem conflito) — use `resolve_folder_name` em Python ou aplique a regra direto: append data → append letra
3. **Cria pasta** com `mcp__google-drive__createFolder(name=<final>, parentId="10ARKUMWyFzVkdaPEWLYC9OXWqm0ywS6e")`
4. **Auto-share writer** com `mcp__google-drive__addPermission(fileId=<folderId>, emailAddress="pedrorobertomiranda@gmail.com", role="writer", sendNotificationEmail=false)`

### Passo 9 — Upload todos os .docx

Para cada doc em `results.docs[]`:
- `mcp__google-drive__uploadFile(localPath=<path>, parentFolderId=<folderId>, convertToGoogleFormat=false)`
- Capturar `link` retornado

Salve `audit.log` na pasta local com timestamp, count de findings PII, email auto-share, link da pasta Drive.

### Passo 10 — WhatsApp agregado + entrega

UMA mensagem única para `destination_number` de `~/.claude/secrets/reuniao.json`:

```
🗂️ Reunião: <Título>
📁 <link pasta Drive>

Docs gerados (N):
• ata-reuniao-singular-pwr.docx
• doc-tarefas-completas.docx
• doc-plano-comercial-pwr.docx
...
```

Use o script:
```bash
CFG=~/.claude/secrets/reuniao.json
EVOLUTION_API_URL=$(python -c "import json; print(json.load(open('$CFG'))['whatsapp']['evolution_api_url'])") \
EVOLUTION_INSTANCE=$(python -c "import json; print(json.load(open('$CFG'))['whatsapp']['evolution_instance'])") \
EVOLUTION_API_KEY=$(python -c "import json; print(json.load(open('$CFG'))['whatsapp']['evolution_api_key'])") \
node ~/.claude/scripts/whatsapp-send.js text \
  --number "$(python -c 'import json; print(json.load(open("'$CFG'"))["whatsapp"]["destination_number"])')" \
  --message "<mensagem>"
```

**Entrega final ao Pedro no chat (4-6 linhas):**

1. 🔗 Link pasta Drive (no topo, destacado)
2. Tabela enxuta: doc | path local | link Drive individual
3. Confirmação WhatsApp (✅ enviado / ❌ falha + motivo)
4. Sinalização de campos "A definir" se houver
5. Sinalização de `failures` parciais se houver

## Regras críticas

**Identidade visual:** herdada de `/ata`, `/documento`, `/pop` — não negociar.

**Conteúdo:**
- NUNCA inventar nomes, datas, decisões, números
- Aplicar norma culta PT-BR (referência: `~/.claude/skills/pop/references/accents.md`)
- Preservar voz do autor — não sterilizar
- Resumir discussões em parágrafos curtos
- Marcar ambiguidade com `[verificar com autor]`

**Segurança:**
- NUNCA logar conteúdo de `~/.claude/secrets/reuniao.json`
- PII detectada + cliente externo → pergunta confirmação antes de upload
- Audit log obrigatório quando `pii_confirmado: true`

**Limites:**
- Mínimo: ata + 0 outros builders selecionados → aborta com mensagem (não faz sentido)
- Máximo: 17 builders (catálogo inteiro)
- Texto < 200 chars → aborta pedindo mais contexto

## Referência

- Spec: `C:\Users\teste\plano\singular\docs\specs\2026-05-19-skill-reuniao-design.md`
- Plano: `C:\Users\teste\plano\singular\docs\plans\2026-05-19-skill-reuniao-implementation.md`
- Ground truth: `~/.claude/skills/reuniao/examples/powercoffee-reference.md`
- Acentuação: `~/.claude/skills/pop/references/accents.md`
- Template oficial: `~/.claude/skills/pop/template.docx` (imutável)
