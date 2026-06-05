---
name: reuniao
bu: backoffice-tech
cross_bu: [consultorio-operacional, holding, apoio-juridico]
description: Recebe transcrição/notas de reunião, lê a transcrição COMPLETA e faz um brainstorm de quais documentos .docx Singular agregam (ata sempre + até ~5 derivados de alto impacto, incluindo tipos NOVOS fora do catálogo), pergunta ao Pedro com a justificativa de cada um, gera só os aprovados numa pasta Drive `Zel/reuniao <slug>/`, e aprende tipos novos automaticamente no catálogo. Use quando o usuário digitar /reuniao seguido de texto, ou pedir "processa essa reunião", "monta a pasta dessa reunião", "gera os docs dessa reunião", "kit completo da reunião".
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

Catálogo SEED de 17 tipos em `catalog.json` (cresce sozinho via auto-improve). Montadores em `montadores.py` — inclui montadores **genéricos** (`monta_doc_generico`, `monta_pop_generico`) que constroem QUALQUER tipo novo brainstormado a partir de um plano de seções/passos. Orquestrador em `reuniao.py`.

> O catálogo é ponto de partida, NÃO teto. A skill propõe tipos fora dele quando agregam e aprende os aprovados.

## Fluxo de execução (10 passos — NÃO pule)

### Passo 1 — Leitura COMPLETA da transcrição (sem limitar)

Leia a transcrição/notas **inteira, do começo ao fim** — nunca resuma ou trunque antes de entender. Não há limite de tipos de documento aqui: o catálogo é só um ponto de partida, não um teto.

Extraia:
- **Tipo de reunião:** comercial / técnica / estratégica / kickoff / retro / 1:1 / daily / interna
- **Cliente externo (se houver):** nome, vertical, contatos
- **Participantes:** presentes + ausentes
- **Tópicos discutidos:** com discussão + decisões
- **Encaminhamentos:** ação + responsável + prazo
- **Riscos / pendências**
- **Tudo que "pede" um artefato:** decisão a registrar, processo a padronizar, material a entregar ao cliente, número/meta a formalizar, conceito a documentar — anote mesmo que NÃO exista um tipo pronto no catálogo pra isso.

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

### Passo 3 — Brainstorm de valor (≤5 derivados de alto impacto)

Este é o coração da skill. Combine DUAS fontes de candidatos:

**(a) Match do catálogo** — carregue `catalog.json` e marque:
- `flag == "always"` → sempre (`ata-reuniao`; é a base, não conta no limite de 5)
- `flag == "auto_suggest"` → se a condição satisfaz (ex: `len(encaminhamentos) ≥ 2`)
- `flag == "learned"` ou sem flag → match score: quantos `triggers` (case-insensitive) aparecem no texto

**(b) Brainstorm ABERTO** — independente do catálogo, olhando ESTA reunião pergunte:
> "Que documento faria esta conversa virar ação, decisão, processo ou material entregável? O que o Pedro vai querer reler, assinar ou mandar pra alguém depois?"
>
> Proponha tipos NOVOS (fora dos 17) sempre que agregarem de verdade — ex.: roadmap trimestral, matriz RACI, one-pager pra investidor, FAQ de objeções, termo de acordo, plano de contratação, runbook de incidente, análise de cenário. Cada tipo novo nasce como `doc-<slug>` (base `/documento`) ou `pop-<slug>` (base `/pop`).

**Curadoria (enxuto / alto impacto):** junte (a)+(b), ranqueie por impacto real e **fique com no máximo ~5 derivados** (além da ata). Corte redundância e doc genérico que não muda nada. Pra cada finalista escreva:
- `key`, `label`, `skill_base` (`documento`/`pop`), `is_new` (bool)
- **`rationale`** — UMA linha dizendo *por que esse doc agrega NESTA reunião*, ancorada no que foi dito (não genérica)

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

### Passo 5 — AskUserQuestion multiSelect (com a justificativa de cada doc)

Use a tool `AskUserQuestion` (multiSelect) mostrando, pra CADA candidato, o `rationale`. Pré-marque os de maior impacto. Sinalize tipos novos com 🆕. Exemplo do que o Pedro vê:

```
Detectei: reunião <tipo> sobre <tema> [cliente: <nome> (<slug>)].
Marquei os de maior impacto — desmarque o que não quiser:

[✓] ata-reuniao — base, sempre gerada
[✓] doc-tarefas-completas — 5 encaminhamentos com responsável/prazo → vira checklist acionável
[✓] doc-roadmap-trimestral 🆕 — fecharam piloto de 3 meses c/ revisão mensal; falta o roadmap dos marcos
[✓] doc-briefing-posicionamento — definiram público 25-45 B+ e tom de voz → consolida o briefing
[ ] pop-roteiro-roleplay — não houve treino comercial nesta reunião
```

Fora dos docs, inclua sempre:
- ⚠️ aviso de PII se o Passo 4 achou algo (com cliente externo → confirmar antes do upload)
- pasta Drive sugerida (`Zel/reuniao <slug>/`) com opção de override

Se há tipos novos (🆕) entre os marcados, avise no fechamento: *"Os 🆕 entram no catálogo automaticamente pra próximas reuniões."* — **não** pergunte de novo se quer salvar (decisão do Pedro: auto-improve automático).

Aguarde resposta. Se Pedro desmarcar tudo (até a ata), aborta limpo.

### Passo 6 — Compor master.json + selection.json

Crie `output_dir = /c/Users/teste/Desktop/reunioes/<slug>-<data>/`.

Componha `master.json` com TODO o conteúdo extraído (não só dos selecionados — preserva contexto pra re-rodada). Schema dos tipos canônicos em §6.1 do spec. **Para cada tipo NOVO (🆕) selecionado**, adicione o plano de conteúdo sob a chave `master_field` (a mesma referida no `selection`):
```json
"roadmap_trimestral": {
  "titulo": "Roadmap do Piloto — 3 Meses",
  "tldr": "Marcos mensais do piloto com revisão ao fim de cada mês.",
  "secoes": [
    {"titulo": "Mês 1 — Setup", "listas": [{"itens": ["..."]}]},
    {"titulo": "Mês 2 — Tração", "paragrafos": ["..."]},
    {"titulo": "Mês 3 — Revisão", "destaque": "Decisão de continuar/encerrar"}
  ]
}
```
(POP novo usa `{titulo, objetivo, passos:[{titulo, paragrafos|listas|acao_final}]}`.)

Componha `selection.json`:
```json
{
  "selected_builders": ["ata-reuniao", "doc-tarefas-completas", "doc-roadmap-trimestral"],
  "drive_folder_name": "reuniao pwr",
  "data_geracao": "<ISO 8601>",
  "pii_confirmado": true,
  "cliente_externo": true,
  "learned_types": [
    {
      "key": "doc-roadmap-trimestral",
      "skill_base": "documento",
      "label": "Roadmap trimestral / de piloto",
      "naming_template": "doc-roadmap-trimestral-<cliente>.docx",
      "scope": "external_specific",
      "montador": "generico",
      "master_field": "roadmap_trimestral",
      "triggers": ["roadmap", "piloto", "marcos", "trimestre", "revisão mensal"],
      "fields_required": ["roadmap_trimestral"],
      "learned_from": "reuniao pwr"
    }
  ]
}
```
- `learned_types` traz a entrada de catálogo COMPLETA **só dos tipos 🆕 selecionados**. `triggers` = 3-5 palavras-chave da reunião pra esse tipo casar de novo no futuro. `montador`: `"generico"` (base /documento) ou `"generico_pop"` (base /pop).
- Tipos já existentes no catálogo NÃO entram em `learned_types` (só em `selected_builders`).
- `naming_template` pode usar `<cliente>`, `<assunto>`, `<local>` (resolvidos pelo orquestrador) ou um nome literal já seguro.

Aplique norma culta PT-BR em todo conteúdo antes de gravar (use `~/.claude/skills/pop/references/accents.md`).

### Passo 7 — Rodar orquestrador

```bash
python ~/.claude/skills/reuniao/reuniao.py \
  /c/Users/teste/Desktop/reunioes/<slug>-<data>/master.json \
  /c/Users/teste/Desktop/reunioes/<slug>-<data>/selection.json \
  /c/Users/teste/Desktop/reunioes/<slug>-<data>/
```

Parse o JSON de retorno. Se `status == "aborted"`, reporta erro ao Pedro e para. O retorno traz também:
- `learned_persisted[]` — tipos 🆕 que geraram .docx OK e foram gravados no `catalog.json` (auto-improve).
- `learned_skipped[]` — tipos 🆕 que não persistiram (`{key, motivo}`: ex. "já existe no catálogo"). Não é erro fatal — o .docx já foi gerado.

Reporte ambos no Passo 10.

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
6. 🧠 **Aprendido no catálogo:** liste os tipos 🆕 de `learned_persisted` — "aparecem sozinhos em reuniões futuras sobre o tema". Se houver `learned_skipped`, mencione em 1 linha.

## Auto-improve (catálogo que aprende)

O catálogo NÃO é fixo. Todo tipo novo (🆕) que o Pedro aprovar e que gerar `.docx` com sucesso é **anexado automaticamente** ao `catalog.json` (`flag: "learned"`), com backup `.bak.<timestamp>` antes de gravar. Efeito composto: na próxima reunião que tocar no mesmo assunto, o tipo aparece sozinho no match do catálogo (via `triggers`) — a skill fica mais esperta a cada uso.

Garantias (helper `append_learned_type`):
- **Append-only:** nunca sobrescreve nem remove tipos existentes.
- **Idempotente:** se a `key` já existe, é no-op (não duplica) → vai pra `learned_skipped`.
- **Best-effort:** se a gravação falhar, o doc já foi entregue; a falha não derruba a reunião.
- **Automático (decisão do Pedro):** sem pergunta extra "quer salvar?". Aprovou o 🆕 → entra no catálogo.

Inspecionar o que a skill já aprendeu:
```bash
python -c "import json; [print(t['key'],'—',t.get('learned_from','')) for t in json.load(open(r'C:/Users/teste/.claude/skills/reuniao/catalog.json'))['tipos'] if t.get('flag')=='learned']"
```

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
- Mínimo: se Pedro desmarca tudo (inclusive a ata) → aborta limpo
- Curadoria: ata + até ~5 derivados de alto impacto por rodada (enxuto). O catálogo cresce sem teto via auto-improve, mas cada reunião entrega o que importa, não tudo.
- Texto < 200 chars → aborta pedindo mais contexto

## Referência

- Spec: `C:\Users\teste\plano\singular\docs\specs\2026-05-19-skill-reuniao-design.md`
- Plano: `C:\Users\teste\plano\singular\docs\plans\2026-05-19-skill-reuniao-implementation.md`
- Ground truth: `~/.claude/skills/reuniao/examples/powercoffee-reference.md`
- Acentuação: `~/.claude/skills/pop/references/accents.md`
- Template oficial: `~/.claude/skills/pop/template.docx` (imutável)
