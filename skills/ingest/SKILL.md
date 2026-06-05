---
name: ingest
bu: backoffice-tech
description: Indexa UM artefato canonico da Singular (ata, contrato, POP, documento, parecer, briefing, dossie ou .md de memoria) no Singular_Memory, exigindo taxonomy 4D EXPLICITA (layer + area + entidade + bu, mais cross_bu opcional) antes de qualquer escrita. Valida os slugs contra a SoT memory.taxonomy, se a bu faltar roda /bu pra classificar (nao infere em silencio), e so entao chama o pipeline real seed_from_jsonl (sanitize, chunk parent-child, embed dense+sparse, upsert idempotente UUID5) no Qdrant. Use quando o usuario digitar "/ingest", "indexa isso no singular_memory", "cataloga esse doc", "salva isso na memoria Singular", ou logo depois de gerar um artefato canonico que precisa virar memoria permanente.
---

# /ingest - Indexador de artefato canonico no Singular_Memory

Voce e o **indexador** do `Singular_Memory`. Recebe UM artefato canonico Singular (um arquivo .md ou .txt: ata, contrato, POP, documento, parecer, briefing, dossie, ou uma memoria), exige a **taxonomy 4D explicita**, valida, e indexa no Qdrant via o pipeline real.

A regra de ouro desta skill: **nada entra sem taxonomy 4D valida e explicita**. O fallback silencioso (deixar a heuristica de path adivinhar a `bu`) foi o gap apontado na auditoria de 2026-06-05. Aqui isso nao acontece: se faltar `bu`, a skill para e classifica via `/bu`, ou aceita inferencia so com o flag explicito `--infer-bu` (e ainda avisa).

Argumento recebido: `$ARGUMENTS`

## Overview

O `/ingest` e o lado de escrita da Regra Soberana #3 (Catalogacao Singular): **ingest DEPOIS de criar artefato canonico**. Ele fecha o ciclo que comeca no `/bu` (classifica) e termina no Qdrant (memoria permanente consultavel por recall).

As 4 dimensoes que todo ponto carrega no payload:

```yaml
layer: ...        # front-office / middle-office / back-office / opco / investida / cliente
area: ...         # 1 das areas canonicas (ou null quando layer=opco)
entidade: ...     # holding / consultorio / investida / cliente / ...
bu: ...           # slug primario (Regra Soberana #4) - OBRIGATORIO
cross_bu: [...]   # opcional, lista de slugs quando serve 2+ BUs
```

A skill executa, nesta ordem:

1. **Recall** do contexto (se o artefato menciona cliente/projeto/BU/valor/decisao Singular).
2. **Exige taxonomy 4D**. Se faltar `bu`, roda `/bu` pra classificar (nao infere em silencio).
3. **Valida** os 4 slugs contra a SoT `memory.taxonomy`.
4. **Chama** `scripts/ingest_doc.py`, que monta o JSONL e dispara `seed_from_jsonl`.
5. **Confirma** com o resumo (chunks indexados, bu aplicada, collection).

> **SoT canonica dos slugs:** `C:/Users/teste/.claude/scripts/memory/taxonomy.py` (modulo Python) e os arquivos human-readable `feedback_taxonomy_3d_singular.md` (layer/area/entidade) + `feedback_bu_taxonomy_singular.md` (bu). Em divergencia, o modulo `taxonomy.py` vence, porque e ele que valida de verdade.

## Quando usar

Triggers que disparam esta skill:

- `/ingest <arquivo>`
- "indexa isso no singular_memory"
- "cataloga esse doc"
- "salva isso na memoria Singular"
- "poe esse artefato no Singular_Memory"
- Logo depois que uma skill geradora (`/ata`, `/contrato`, `/pop`, `/documento`, `/pdf`, `/reuniao`, `/backgroundcheck`) produziu um artefato canonico que precisa virar memoria permanente.

NAO precisa rodar quando: o artefato e rascunho descartavel, ou o conteudo ja esta indexado e nada mudou, ou e uma pergunta conceitual que nao gera registro. Para indexar um dump grande do Drive (varios arquivos de uma vez), use o `seed_from_jsonl` direto, nao esta skill (esta skill e 1 artefato por vez).

## Workflow passo-a-passo

### Passo 0 - Recall + ler o input

- Identifique o **arquivo** alvo (caminho .md / .txt). Se o usuario passou so um nome ou colou texto, salve o texto num .md temporario primeiro.
- **RECALL antes de indexar:** se o artefato menciona cliente, projeto, investida, BU, valor ou decisao Singular, puxe contexto do `Singular_Memory` pra confirmar entidade/bu corretas e nao criar duplicata divergente (regra soberana de catalogacao).

### Passo 1 - Exigir taxonomy 4D (se faltar bu, roda /bu)

O `/ingest` **exige** as 4 dimensoes. Antes de chamar o script, garanta que voce tem: `layer`, `area` (ou null), `entidade`, `bu` (e `cross_bu` se servir 2+ frentes).

- Se o artefato **ja veio com frontmatter 4D** (ex: foi classificado pelo `/bu` ou gerado por skill que carimba), use esses valores.
- Se **faltar `bu`**, NAO invente e NAO deixe inferir em silencio: rode a skill `/bu` sobre o artefato pra obter o slug primario (e cross_bu). So depois prossiga.
- Inferencia automatica (`--infer-bu`) e permitida apenas como ultimo recurso explicito, quando o Pedro aceitar. Nesse caso a skill avisa qual bu foi inferida e se a confianca e baixa.

### Passo 2 - Validar

A validacao real acontece dentro do `ingest_doc.py` (via `memory.taxonomy.validate`). Antes de chamar, faca um sanity check rapido: os slugs batem com as tabelas? Se houver duvida sobre um slug, leia `feedback_bu_taxonomy_singular.md` / `feedback_taxonomy_3d_singular.md`. Se a validacao falhar, o script lista os slugs validos e nao indexa nada.

### Passo 3 - Chamar o ingest_doc.py

Rode o script com a taxonomy 4D completa. Ele monta o JSONL temporario em `~/.claude/.cache/ingest-tmp/` e dispara o `seed_from_jsonl` (cwd = `C:/Users/teste/.claude/scripts`):

```
py C:/Users/teste/.claude/skills/ingest/scripts/ingest_doc.py ^
   --file "C:/Users/teste/Desktop/contratos/ata-spoleto.md" ^
   --name "Ata reuniao Spoleto DF Plaza" ^
   --path-tag "COMERCIAL/Spoleto" ^
   --layer opco --area novos-negocios --entidade consultorio ^
   --bu consultorio-comercial
```

Com cross-BU e dry-run (valida sem escrever no Qdrant):

```
py C:/Users/teste/.claude/skills/ingest/scripts/ingest_doc.py ^
   --file "C:/Users/teste/Desktop/proposta-evento.md" ^
   --name "Proposta evento + ativacao MKT" ^
   --path-tag "PRODUTORA/Evento X" ^
   --layer opco --area rp --entidade holding ^
   --bu produtora-rp --cross-bu fabrica-marketing --dry-run
```

Rode `--dry-run` primeiro quando estiver em duvida da taxonomy: ele mostra o tagging e NAO faz embed nem upsert. Depois rode sem `--dry-run` pra indexar de verdade.

### Passo 4 - Confirmar

Reporte ao Pedro, em 1-2 linhas: arquivo indexado, taxonomy 4D aplicada (layer/area/entidade/bu/cross_bu), quantos chunks entraram e a collection (`Singular_Memory`). Se a bu tiver sido inferida, sinalize isso explicitamente pra ele revisar.

## Contrato do ingest_doc.py

| Arg | Obrigatorio | Significado |
|-----|-------------|-------------|
| `--file` | sim | caminho do .md / .txt a indexar |
| `--name` | sim | titulo legivel do artefato (vira `title` no payload) |
| `--path-tag` | sim | path logico (ex: `COMERCIAL/Spoleto`); vira `drive_path` + file_id estavel/idempotente |
| `--layer` | sim | dimensao 1 |
| `--area` | nao | dimensao 2 (use `null` ou omita quando `layer=opco`) |
| `--entidade` | sim | dimensao 3 |
| `--bu` | sim* | dimensao 4 (Regra Soberana #4). *Obrigatoria, salvo `--infer-bu`. |
| `--cross-bu` | nao | csv de bus adicionais (`fabrica-marketing,produtora-rp`) |
| `--infer-bu` | nao | flag: permite inferir bu via `taxonomy.infer_bu` quando `--bu` faltar, com aviso explicito |
| `--dry-run` | nao | valida + monta JSONL + mostra tagging, sem embed/upsert |

Comportamento de erro (sem fallback silencioso):
- `--bu` ausente e sem `--infer-bu` -> ERRO, sai sem indexar.
- qualquer slug invalido (layer/area/entidade/bu/cross_bu) -> ERRO com lista de slugs validos, sai sem indexar.
- arquivo inexistente / vazio -> ERRO.
- idempotencia: `file_id` deriva do `--path-tag` (UUID5), entao re-ingerir o mesmo artefato sobrescreve em vez de duplicar.

## Nota - Fase 3 do Backoffice Pro Max

Esta skill e a entrega da **Fase 3** do plano-vital Backoffice Pro Max: dar ao Pedro um `/ingest` de 1 comando que substitui a sequencia manual `add_doc + consolidate + seed_from_jsonl` pra artefato unico, ja com a taxonomy 4D obrigatoria embutida. Fecha o ciclo de catalogacao: `/bu` classifica, `/ingest` grava, recall consulta. Detalhes do projeto em `C:/Users/teste/plano/plano/projetos/backoffice-pro-max/` e na memoria `project_backoffice_pro_max.md`.

## Cross-references

- SoT da taxonomia (modulo validador): `C:/Users/teste/.claude/scripts/memory/taxonomy.py`
- Pipeline real de embed/upsert: `C:/Users/teste/.claude/scripts/memory/seed_from_jsonl.py`
- Classificador da 4a dimensao (bu): skill `/bu` (`C:/Users/teste/.claude/skills/bu/SKILL.md`)
- Regra de catalogacao Singular (recall antes / ingest depois): `feedback_singular_memory_catalog.md`
- Valores das 3 dimensoes antigas: `feedback_taxonomy_3d_singular.md`
- SoT da dimensao bu: `feedback_bu_taxonomy_singular.md`
- Stack tecnica do Singular_Memory: `reference_singular_memory_stack.md`
- Regra da 4a dimensao: `~/.claude/rules/core/bu-categorization.md`

*[Registrado por: DESKTOP - 2026-06-05]*
