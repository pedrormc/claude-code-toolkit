---
name: new-projeto-backoffice
bu: backoffice-tech
description: Cria a estrutura de um projeto Singular novo seguindo o padrao de arquitetura obrigatorio (memory + MEMORY.md indice + doc canonical PROJETO.md + Qdrant Singular_Memory + Obsidian mirror + Git), ja com a BU primaria carimbada (4a dimensao da taxonomia). Roda scaffold.py pra montar a arvore em plano/singular/_bu/<bu>/<slug>/ de forma idempotente e imprime o checklist manual dos passos de rede/git. Use quando o usuario digitar "/new-projeto-backoffice", "novo projeto singular", "iniciar projeto backoffice", "comecar projeto novo", ou sempre que for instaurar um projeto Singular do zero e precisar que ele ja nasca catalogado com bu e no padrao de arquitetura obrigatorio.
---

# /new-projeto-backoffice - Scaffold de projeto Singular novo

Voce instaura um **projeto Singular novo** do jeito certo: ja nascendo com a **BU primaria** carimbada (Regra Soberana #4) e no **padrao de arquitetura obrigatorio** (feedback_architecture_memory_pattern). Em vez de criar pastas e arquivos a mao (e esquecer metade), esta skill roda um scaffold deterministico e devolve o checklist do que falta fazer manualmente (rede e git).

Argumento recebido: `$ARGUMENTS`

## Overview

Todo sistema novo da Singular DEVE usar 6 componentes (feedback_architecture_memory_pattern):

1. `memory/` com frontmatter tipado
2. `MEMORY.md` indice
3. doc canonical (`PROJETO.md`)
4. index no Qdrant `Singular_Memory`
5. mirror no Obsidian vault
6. Git

O `scaffold.py` automatiza os passos **1, 2 e 3** (cria pastas e arquivos em disco, idempotente, sem rede) e imprime um **checklist manual** pros passos **4, 5 e 6** (Obsidian, ingest no Singular_Memory, git), que envolvem rede / repo e nao sao executados automaticamente.

O projeto nasce em:

```
C:\Users\teste\plano\singular\_bu\<slug-bu>\<slug-projeto>\
```

ja com `bu` (e `cross_bu` opcional) no frontmatter do `PROJETO.md` e do `project_<slug>.md`. As outras 3 dimensoes (`layer`/`area`/`entidade`) entram como placeholder `TODO` e sao preenchidas depois (a skill `/bu` ajuda a carimbar).

## Quando usar

Triggers que disparam esta skill:

- `/new-projeto-backoffice <nome>`
- "novo projeto singular"
- "iniciar projeto backoffice"
- "comecar um projeto novo" (no contexto Singular)
- "criar a estrutura de um projeto"
- Sempre que for instaurar um projeto Singular do zero e precisar que ele ja nasca catalogado com `bu` e no padrao de arquitetura obrigatorio.

NAO precisa rodar quando: o projeto ja existe (ja tem pasta + PROJETO.md), ou quando e so uma tarefa dentro de um projeto existente.

## Workflow passo-a-passo

### Passo 0 - Classificar a BU (gate, via /bu)

Antes de criar qualquer coisa, o projeto precisa de uma **BU primaria**. Rode o gate dos **3 Pilares** e a heuristica de BU (skill `/bu`):

1. **3 Pilares (gate):** 1) Respeitar o know-how, 2) Saude financeira, 3) Formalizar a Holding. Nao passou nos 3 -> NAO cria projeto: pergunta se reprioriza ou descarta.
2. **Heuristica de BU:** decide o slug `bu` primario (mais `cross_bu` se serve 2+ frentes). Use `/bu` se a BU nao for obvia.
3. **Ambiguidade entre 2+ BUs primarias -> PERGUNTAR** ao Pedro no formato checkbox antes de seguir:

```
[BU] Onde este projeto entra como BU primaria?
[ ] consultorio-comercial   (Simon)
[ ] consultorio-operacional (Arthur Trojan)
[ ] fabrica-marketing       (Carol)
[ ] produtora-rp            (Ana Luiza)
[ ] backoffice-tech         (Robertinho + Volpi)
[ ] outro (apoio-* / portfolio-* / holding / generico)
Cross-BU (serve tambem)? liste os slugs adicionais, se houver.
```

Tambem defina, junto com o Pedro: **nome legivel**, **slug kebab** (pasta) e **categoria** (default `singular`).

### Passo 1 - Rodar o scaffold

Com `nome`, `slug`, `bu` (e `cross_bu` opcional) definidos, rode o scaffold a partir de `C:/Users/teste/.claude/scripts/` (pra que o import `memory.taxonomy` funcione) OU chame o arquivo direto:

```
py -3 "C:/Users/teste/.claude/skills/new-projeto-backoffice/scripts/scaffold.py" \
  --nome "Nome Legivel do Projeto" \
  --slug nome-do-projeto-kebab \
  --bu backoffice-tech \
  --cross-bu apoio-financeiro,apoio-juridico \
  --categoria singular
```

O `--bu` e validado contra a taxonomia canonica (`memory/taxonomy.py`, SoT dos slugs). `--cross-bu` e opcional (lista separada por virgula, nao pode conter a propria `bu` primaria). O script:

- cria `_bu/<bu>/<slug>/` + `memory/`;
- escreve `PROJETO.md` (canonical, com Visao geral / Arquitetura / Pendencias);
- escreve `memory/MEMORY.md` (indice) e `memory/project_<slug>.md` (memoria tipada com `bu`);
- e **idempotente**: se `PROJETO.md` ou `project_<slug>.md` ja existem, **avisa e nao sobrescreve**.

Reporte ao Pedro a raiz criada e quais arquivos foram `OK` vs `SKIP`.

### Passo 2 - Executar o checklist manual (passos 4-6)

O script NAO faz rede nem git. Ele imprime um checklist; voce executa (ou agenda) os 3 itens:

1. **Obsidian mirror:** criar nota espelho em `C:/Users/teste/Documents/obsidiano/singular/<slug>.md` com frontmatter (`title`, `category`, `bu`, `status: active`, `created`/`updated: 2026-06-05`). Marcar origem Desktop.
2. **Ingest Singular_Memory:** indexar o `PROJETO.md` no Qdrant (collection `Singular_Memory`, `http://3.237.66.68:6333`) com payload `{layer, area, entidade, bu, cross_bu}`. Use a skill `/ingest` ou o pipeline manual `py -3 -m memory.seed_from_jsonl --jsonl <dump.jsonl>` (cada linha do JSONL leva `bu`/`cross_bu` explicitos). Seguir a regra soberana: ingest DEPOIS de criar o artefato canonical.
3. **Git:** se o projeto virar repo proprio, `git init` + primeiro commit (`chore: scaffold projeto <slug> (bu: <bu>)`). Seguir pull -> commit -> push se houver remote.

Lembrar o Pedro de **preencher os placeholders** `layer`/`area`/`entidade` no frontmatter assim que estiverem definidos (use `/bu`).

### Passo 3 - Registrar na memoria global

Depois do scaffold, registre o projeto novo na memoria global do ecossistema:

- Adicionar uma linha em `C:/Users/teste/.claude/projects/C--Users-teste/memory/MEMORY.md` na secao **Project**, apontando pra `project_<slug>` com 1 frase de resumo + a `bu`.
- Marcar a escrita com `*[Registrado por: DESKTOP - 2026-06-05]*`.

## Estrutura gerada (resumo)

```
C:\Users\teste\plano\singular\_bu\<bu>\<slug>\
  PROJETO.md                 # canonical: frontmatter (bu, cross_bu, layer/area/entidade TODO) + Visao geral / Arquitetura / Pendencias
  memory\
    MEMORY.md                # indice da memoria do projeto
    project_<slug>.md        # memoria raiz tipada (bu no frontmatter)
```

## Notas

- `layer`/`area`/`entidade` ficam como `TODO` no frontmatter ate serem definidos: a 4a dimensao (`bu`) e obrigatoria desde o nascimento, as 3 antigas podem ser carimbadas depois via `/bu`.
- Use hifen, virgula ou dois-pontos no texto gerado. NAO use travessao nem en-dash.
- Marque escritas com `*[Registrado por: DESKTOP - 2026-06-05]*`.

## Cross-references

- Padrao de arquitetura obrigatorio (6 componentes): `~/.claude/projects/C--Users-teste/memory/feedback_architecture_memory_pattern.md`
- Regra de categorizacao por BU (Regra Soberana #4): `~/.claude/rules/core/bu-categorization.md`
- Skill classificadora de BU: `/bu`
- SoT dos slugs de BU: `~/.claude/projects/C--Users-teste/memory/feedback_bu_taxonomy_singular.md`
- Taxonomia canonica (modulo): `~/.claude/scripts/memory/taxonomy.py`
- Regra de catalogacao Singular (recall antes / ingest depois): `~/.claude/projects/C--Users-teste/memory/feedback_singular_memory_catalog.md`
- Arvore de pastas por BU: `C:/Users/teste/plano/singular/_bu/TAXONOMY.md`

*[Registrado por: DESKTOP - 2026-06-05]*
