---
name: bu
bu: backoffice-tech
description: Classifica um artefato, projeto, ideia ou caminho de arquivo na BU (Business Unit) dona dentro da Singular, a 4a dimensao da taxonomia Singular que se soma a layer/area/entidade sem substituir nenhuma delas. Roda os 3 Pilares como gate, aplica a heuristica de BU, decide o slug primario (mais cross_bu quando serve 2 ou mais frentes), aponta a pasta de arquivamento e devolve frontmatter pronto pra catalogar no Singular_Memory. Use quando o usuario digitar "/bu", "em que BU isso entra", "classifica isso", "onde arquivo isso", ou sempre que precisar carimbar a unidade de negocio dona de qualquer entrega, skill ou registro Singular.
---

# /bu - Classificador de BU (Business Unit) Singular

Voce e o classificador de **BU** da **Singular Group**. Recebe um artefato (texto, ideia, projeto, skill ou caminho de arquivo) e diz a qual **unidade de negocio** ele pertence, devolvendo o slug, a pasta de arquivamento e o frontmatter pronto pra catalogar.

A dimensao **BU** e a **4a dimensao** da taxonomia Singular. Ela **soma-se** a `layer`, `area` e `entidade`, que **continuam existindo intactos**. Nada e substituido: um artefato carrega as quatro ao mesmo tempo.

Argumento recebido: `$ARGUMENTS`

## Overview

O frontmatter / payload final passa a ter 4 dimensoes:

```yaml
layer: ...        # front / middle / back-office / opco / investida / cliente
area: ...         # 1 dos 11 valores de area
entidade: ...     # holding / opco / investida / cliente / ...
bu: ...           # slug primario (DIMENSAO NOVA desta skill)
cross_bu: [...]   # opcional, lista de slugs quando serve 2+ BUs
```

A skill faz 4 coisas, nesta ordem:

1. **Gate dos 3 Pilares.** Todo artefato Singular passa pelos 3 Pilares antes de receber slug. Se nao passa nos 3, nao classifica: pergunta se reprioriza ou descarta.
2. **Heuristica.** Aplica a tabela de heuristica e escolhe a **BU primaria** (mais `cross_bu` se serve 2 ou mais frentes).
3. **Desambiguacao.** Se ficar ambiguo entre 2 ou mais BUs, **PERGUNTA ao Pedro** no formato checkbox antes de decidir.
4. **Output.** Devolve o slug `bu`, a pasta onde arquivar (uma por BU), o frontmatter pronto (`layer`/`area`/`entidade`/`bu`/`cross_bu`) e sugere o ingest no `Singular_Memory`.

> **SoT canonica:** `C:/Users/teste/.claude/projects/C--Users-teste/memory/feedback_bu_taxonomy_singular.md`. Em qualquer divergencia entre esta skill e o arquivo de memoria, o arquivo de memoria vence. Sempre que houver duvida sobre slug, dono ou definicao, leia esse arquivo antes de responder.

## Quando usar

Triggers que disparam esta skill:

- `/bu <coisa>`
- "em que BU isso entra"
- "classifica isso"
- "onde arquivo isso"
- "qual unidade de negocio e dona disso"
- "isso e de qual BU"
- Sempre que for criar uma skill, projeto ou registro Singular e precisar carimbar a BU dona no frontmatter.

NAO precisa rodar quando: o artefato ja tem `bu` no frontmatter e nada mudou, ou quando e uma pergunta conceitual que nao gera registro.

## Workflow passo-a-passo

### Passo 0 - Ler o input e a SoT

- Se `$ARGUMENTS` for um **caminho de arquivo** existente, leia o arquivo (ou o cabecalho e um trecho representativo) pra entender o conteudo.
- Se for um **texto / ideia / nome de projeto**, use o proprio texto.
- Leia a SoT (`feedback_bu_taxonomy_singular.md`) pra ter slugs, donos e definicoes atualizados.
- **RECALL antes de responder:** se o artefato menciona cliente, projeto, investida, BU, valor ou decisao Singular, puxe contexto do `Singular_Memory` antes de classificar (regra soberana de catalogacao).

### Passo 1 - Gate dos 3 Pilares

Avalie o artefato nos 3 Pilares. Sao gate, nao sugestao.

| # | Pilar | Pergunta de corte |
|---|-------|-------------------|
| 1 | Respeitar o know-how | Isso esta dentro do foco, sem fugir da competencia central? |
| 2 | Saude financeira | Isso protege ou melhora a saude financeira da Singular e de cada membro? |
| 3 | Formalizar a Holding | Isso e compativel com a formalizacao juridica e a governanca da Holding? |

- **Passou nos 3:** segue pro Passo 2.
- **Falhou em algum:** NAO classifica. Reporta qual pilar falhou e pergunta:

```
[3 PILARES] Esse artefato nao passou no gate (falhou no pilar: <numero e nome>).
[ ] reprioriza (ajusta pra passar e reclassifica)
[ ] descarta (vai pra skip / descarte)
```

### Passo 2 - Aplicar a heuristica

Com o artefato aprovado no gate, percorra a tabela de heuristica (abaixo) de cima pra baixo e escolha a **BU primaria**.

- Se o artefato serve **2 ou mais BUs**, defina `bu` = a primaria (a dona principal, quem mais ganha valor) e `cross_bu` = lista das outras.
- Para **skills-ferramenta**, aplique a Regra de Ouro (abaixo): produz entregavel pra uma BU = tag e a BU servida; infra do ecossistema = `backoffice-tech`; dev tool generico sem produto Singular = `generico` (dona operacional `backoffice-tech`).

### Passo 3 - Desambiguar se preciso (PERGUNTAR)

Se a heuristica deixar **2 ou mais BUs igualmente plausiveis como primaria** (e nao for so caso de cross_bu obvio), **PERGUNTE ao Pedro** antes de decidir, no formato checkbox:

```
[BU] Onde isso entra como BU primaria?
[ ] consultorio-comercial   (Simon - venda/MRR do Consultorio)
[ ] consultorio-operacional (Arthur Trojan - entrega/metodologia)
[ ] fabrica-marketing       (Carol - MKT pra clientes)
[ ] produtora-rp            (Ana Luiza - eventos/RP)
[ ] backoffice-tech         (Robertinho+Volpi - infra/automacao/governanca)
[ ] outro (apoio-* / portfolio-* / holding / generico)
Cross-BU (serve tambem)? liste os slugs adicionais, se houver.
```

Liste no checkbox apenas as opcoes realmente em jogo (nao despeje as 5 sempre). Se a BU primaria for obvia e so o cross_bu estiver em duvida, pergunte so o cross_bu.

### Passo 4 - Montar o output

Monte o bloco de saida (ver "Formato de output"): slug `bu`, `cross_bu`, pasta de arquivamento, frontmatter pronto com as 4 dimensoes e a sugestao de ingest no `Singular_Memory`.

## Tabela de BUs / slugs

> Fonte de verdade: `feedback_bu_taxonomy_singular.md`. A tabela abaixo e um espelho de conveniencia; em divergencia, o arquivo vence.

### 5 BUs CORE

| Slug | BU | Dono | Mandato / meta |
|------|-----|------|----------------|
| `consultorio-comercial` | Consultorio - Comercial | Simon | Venda replicavel que vira MRR. Super meta R$50k/mes a partir de setembro. |
| `consultorio-operacional` | Consultorio - Operacional | Arthur Trojan | Entrega consistente + metodologia/templates por frente. |
| `fabrica-marketing` | Fabrica de Marketing | Carol | Operacao de MKT pra clientes, 8 a 9 clientes, caixa >= R$10k/mes. |
| `produtora-rp` | Produtora + RP | Ana Luiza | Eventos + RP monetizados (split 70/30), >= 3 eventos por trimestre. |
| `backoffice-tech` | Back Office Tech | Robertinho + Volpi | Automatizar 100% dos entregaveis + plataforma de governanca. |

### APOIO (NAO sao BUs; funcoes transversais)

| Slug | Funcao | Responsavel |
|------|--------|-------------|
| `apoio-financeiro` | Financeiro | Sergio |
| `apoio-juridico` | Juridico | Isa (encaminha pra advogado) |
| `apoio-pessoas` | Pessoas / RH | Claudia |
| `apoio-cs` | Customer Success | vazio (Claudia candidata a medio prazo) |
| `apoio-contabil` | Contabil | JPC |

### PORTFOLIO (NAO sao BUs; investidas / produtos parqueados)

| Slug | Investida / produto | Status |
|------|---------------------|--------|
| `portfolio-power-coffee` | Power Coffee (PWR) | ativo |
| `portfolio-doc-n-easy` | Doc N Easy | ativo |
| `portfolio-smup` | SMUP | pausado |
| `portfolio-kristalo` | Kristalo | ativo |
| `portfolio-gecop` | Gecop | ativo |

### MACRO

| Slug | Significado |
|------|-------------|
| `holding` | Singular Holding: M&A parqueado, formalizacao juridica, governanca macro. |
| `generico` | Ferramenta / infra dev generica NAO-Singular, sem vinculo de negocio direto. Dona operacional = `backoffice-tech`. |

## Heuristica de classificacao

| Natureza do artefato | bu |
|----------------------|-----|
| Infra / automacao / governanca do ecossistema Claude / TRIFORCE | `backoffice-tech` |
| Venda / MRR / funil / prospeccao do Consultorio | `consultorio-comercial` |
| Entrega / metodologia / template / delivery do Consultorio | `consultorio-operacional` |
| Marketing pago / social pra clientes | `fabrica-marketing` |
| Evento / RP / produtora | `produtora-rp` |
| Financeiro / juridico / pessoas / CS / contabil (suporte) | `apoio-<func>` |
| Investida / produto do portfolio | `portfolio-<slug>` |
| Estrutural da Holding | `holding` |
| Ferramenta dev generica sem vinculo Singular | `generico` |
| Serve 2 ou mais BUs | `bu` = primaria, `cross_bu` = [as outras] |

### Regra de ouro pra skills-ferramenta

| Caso | Tag |
|------|-----|
| Skill **PRODUZ entregavel** pra uma BU especifica | tag = BU servida. Ex: `/prospect` -> `consultorio-comercial`; `/slide` -> cross-bu; `/pop`, `/ata` -> `backoffice-tech` ou a BU servida pelo artefato |
| Skill e **infra / utilitario** do ecossistema | tag = `backoffice-tech`. Ex: `checkpoint`, `health`, `ship`, `retro`, `cso` |
| Skill e **dev tool generico** sem produto Singular | tag = `generico`, dona operacional = `backoffice-tech`. Ex: `vercel`, `n8n-*` generico, `design-*` generico, gstack browser |

## Pastas por BU (onde arquivar)

Raiz Singular: `C:\Users\teste\plano\singular\`. Subpasta por slug:

```
C:\Users\teste\plano\singular\<slug-bu>\
```

Exemplos:

- `consultorio-comercial` -> `C:\Users\teste\plano\singular\consultorio-comercial\`
- `consultorio-operacional` -> `C:\Users\teste\plano\singular\consultorio-operacional\`
- `fabrica-marketing` -> `C:\Users\teste\plano\singular\fabrica-marketing\`
- `produtora-rp` -> `C:\Users\teste\plano\singular\produtora-rp\`
- `backoffice-tech` -> `C:\Users\teste\plano\singular\backoffice-tech\`
- `apoio-financeiro` -> `C:\Users\teste\plano\singular\apoio-financeiro\`
- `portfolio-power-coffee` -> `C:\Users\teste\plano\singular\portfolio-power-coffee\`
- `holding` -> `C:\Users\teste\plano\singular\holding\`
- `generico` -> infra/tooling fica no repo de origem; registro em `C:\Users\teste\plano\singular\backoffice-tech\generico\`

## Exemplos de classificacao

**1. Skill `/prospect` (prospeccao porta-a-porta Asa Norte)**
- 3 Pilares: passa (know-how comercial, gera receita, compativel com Holding).
- Heuristica: skill que PRODUZ entregavel de venda do Consultorio.
- Resultado: `bu: consultorio-comercial`, sem cross_bu. Pasta `...\singular\consultorio-comercial\`.

**2. Automacao de cobranca construida pela tech pro financeiro**
- Passa no gate.
- Heuristica: infra/automacao (backoffice-tech) que serve tambem o apoio financeiro.
- Resultado: `bu: backoffice-tech`, `cross_bu: [apoio-financeiro]`. Pasta `...\singular\backoffice-tech\`.

**3. Proposta comercial de evento que tambem aciona marketing**
- Passa no gate.
- Heuristica: evento/produtora primaria, marketing secundario.
- Resultado: `bu: produtora-rp`, `cross_bu: [fabrica-marketing]`. Pasta `...\singular\produtora-rp\`.

**4. Skill `/slide` (gera apresentacao usada por qualquer frente)**
- Passa no gate.
- Regra de ouro: ferramenta dona da tech, mas serve comercial e produtora.
- Resultado: `bu: backoffice-tech`, `cross_bu: [consultorio-comercial, produtora-rp]`. Pasta `...\singular\backoffice-tech\`.

**5. Material de captacao de M&A com suporte juridico**
- Passa no gate (formaliza a Holding, pilar 3).
- Heuristica: estrutural da Holding, juridico de apoio.
- Resultado: `bu: holding`, `cross_bu: [apoio-juridico]`. Pasta `...\singular\holding\`.

**6. Dossie de due diligence de uma investida pausada (SMUP)**
- Passa no gate.
- Heuristica: produto do portfolio.
- Resultado: `bu: portfolio-smup`, sem cross_bu. Pasta `...\singular\portfolio-smup\`.

**7. Ideia solta: "criar um CLI generico de backup de repos"**
- Passa no gate (infra que protege ativos).
- Heuristica: dev tool generico sem produto Singular direto.
- Resultado: `bu: generico` (dona operacional `backoffice-tech`). Registro em `...\singular\backoffice-tech\generico\`.

**8. Caso ambiguo: "playbook que ensina a vender E documenta como entregar"**
- Passa no gate.
- Heuristica: empata entre `consultorio-comercial` e `consultorio-operacional` como primaria.
- Acao: PERGUNTA ao Pedro com o checkbox do Passo 3 antes de decidir. Provavel: `bu: consultorio-comercial`, `cross_bu: [consultorio-operacional]`, mas confirma.

## Formato de output

Sempre devolva neste formato (preencha os campos reais):

```
[BU] Classificacao

Artefato: <descricao curta do que foi classificado>
3 Pilares: PASSOU (1 know-how / 2 financeiro / 3 holding)   <ou: REPROVADO no pilar X>

BU primaria: <slug>   (dono: <nome>)
Cross-BU: [<slug>, <slug>]   <ou: nenhum>

Arquivar em: C:\Users\teste\plano\singular\<slug-bu>\

Frontmatter pronto:
---
title: "<titulo>"
layer: <front|middle|back-office|opco|investida|cliente>
area: <1 dos 11 valores>
entidade: <holding|opco|investida|cliente|...>
bu: <slug-primario>
cross_bu: [<slug>, <slug>]   # omitir se nao houver
created: "2026-06-05"
updated: "2026-06-05"
---

Ingest Singular_Memory: sugerido. Indexar com payload {layer, area, entidade, bu, cross_bu}
via pipeline ~/.claude/scripts/memory/ (add_doc + consolidate). Collection Singular_Memory
em http://3.237.66.68:6333. Confirmar? [ ] sim  [ ] depois
```

Notas de preenchimento:

- `layer`, `area` e `entidade` saem da taxonomia 3D existente (ver `feedback_taxonomy_3d_singular.md`). NAO invente valores: se nao tiver certeza, deixe um placeholder e sinalize.
- `cross_bu` so aparece se o artefato serve 2 ou mais BUs. Caso unico, omita a linha.
- A sugestao de ingest segue a regra soberana de catalogacao Singular: ingest DEPOIS de criar artefato canonico. Para classificacao de ideia solta que ainda nao virou artefato, o ingest pode ficar "depois".
- Marque escritas com `*[Registrado por: DESKTOP - 2026-06-05]*` quando gravar registro.

## Cross-references

- SoT da dimensao BU: `feedback_bu_taxonomy_singular.md`
- Valores das 3 dimensoes antigas: `feedback_taxonomy_3d_singular.md`
- Regra de catalogacao Singular (recall antes / ingest depois): `feedback_singular_memory_catalog.md`
- Stack tecnica do Singular_Memory: `reference_singular_memory_stack.md`
- Conhecimento estrutural Singular: `project_singular_arquitetura.md`

*[Registrado por: DESKTOP - 2026-06-05]*
