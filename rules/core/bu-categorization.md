# BU Categorization — Regra Soberana #4

> **Decretada em:** 2026-06-05 por DESKTOP
> **Escopo:** TODOS os artefatos Singular criados pelo Pedro, em qualquer ambiente TRIFORCE.
> **Override:** apenas o Pedro pode revogar/alterar.
> **Relação:** 4a dimensão da REGRA SOBERANA #3 (Catalogação Singular). Soma-se a `layer` / `area` / `entidade`, que CONTINUAM existindo intactos. NÃO substitui nada, ADICIONA o campo `bu`.

## A Regra

Todo artefato que o Pedro **CRIAR** (doc, contrato, ata, projeto, skill, memória, automação, slide, POP, dossiê, parecer) **DEVE** ser classificado em **exatamente 1 BU primária** da Singular, registrada no campo `bu`. Se o artefato servir a mais de uma BU, adiciona-se `cross_bu` (lista dos slugs secundários).

Antes de classificar, o artefato passa pelos **3 Pilares (gate)**. Se não passar nos 3, **reprioriza ou descarta**, não classifica.

## Sequência Combinada (ordem obrigatória)

```
Input do Pedro chega
  ↓
1. 3 Abas Master (plano / singular / skip)      — REGRA SOBERANA #1
  ↓
2. Task Orchestration (complexidade + dispatch)  — REGRA SOBERANA #2
  ↓
3. 3 Pilares (gate)                              — passou? segue : reprioriza/descarta
  ↓
4. Classificação BU (campo bu + cross_bu)        — REGRA SOBERANA #4 (parte da #3)
  ↓
5. Ingest Singular_Memory (recall antes / ingest depois) — REGRA SOBERANA #3
```

## Taxonomia Singular — Dimensão BU (4a dimensão)

Campo novo no frontmatter de memórias/docs e no payload Qdrant:

- `bu`: slug primário (1 valor, obrigatório em todo artefato Singular)
- `cross_bu`: lista de slugs secundários (opcional, quando serve 2+ BUs)

As 3 dimensões anteriores permanecem intactas e obrigatórias: `layer` (front/middle/back-office/opco/investida/cliente) + `area` (11 valores) + `entidade` (holding/3 opcos/7 investidas/12 clientes).

**SoT canônica dos slugs e donos:** [[feedback_bu_taxonomy_singular]]. Em qualquer divergência entre esta rule e o arquivo de taxonomy, o `feedback_bu_taxonomy_singular` vence. A tabela abaixo é resumida para lookup rápido.

### 5 BUs CORE

| Slug `bu` | Dono | Foco / Meta |
|-----------|------|-------------|
| `consultorio-comercial` | Simon | Venda replicável até MRR (super meta R$50k/mês a partir de set) |
| `consultorio-operacional` | Arthur Trojan | Entrega consistente + metodologia/templates por frente |
| `fabrica-marketing` | Carol | Operação MKT pra clientes, 8-9 clientes, caixa >= R$10k/mês |
| `produtora-rp` | Ana Luiza | Eventos + RP monetizados (70/30), >= 3 eventos/tri |
| `backoffice-tech` | Robertinho + Volpi | Automatizar 100% dos entregáveis + plataforma de governança |

### Apoio (NÃO são BUs; funções transversais de suporte)

| Slug `bu` | Dono |
|-----------|------|
| `apoio-financeiro` | Sergio |
| `apoio-juridico` | Isa (-> advogado) |
| `apoio-pessoas` | Claudia |
| `apoio-cs` | vazio (Claudia candidata a médio prazo) |
| `apoio-contabil` | JPC |

### Portfólio (NÃO são BUs; investidas/produtos parqueados)

| Slug `bu` | Status |
|-----------|--------|
| `portfolio-power-coffee` | ativo |
| `portfolio-doc-n-easy` | ativo |
| `portfolio-smup` | pausado |
| `portfolio-kristalo` | ativo |
| `portfolio-gecop` | ativo |

### Macro

| Slug `bu` | Significado |
|-----------|-------------|
| `holding` | Singular Holding: M&A parqueado, formalização jurídica, governança macro |
| `generico` | Ferramenta/infra dev genérica NÃO-Singular (operada pela `backoffice-tech`, sem vínculo de negócio direto) |

## 3 Pilares (gate antes de classificar)

Todo artefato Singular passa pelos 3 Pilares ANTES de receber tag de BU:

1. **Respeitar o know-how** (não fugir do foco)
2. **Saúde financeira** (Singular + cada membro)
3. **Formalizar a Holding**

Não passou nos 3 -> **reprioriza ou descarta**. Não força classificação em algo que falha no gate.

## Heurística de Classificação Rápida

| Natureza do artefato | `bu` |
|----------------------|------|
| infra / automação / governança do ecossistema Claude/TRIFORCE | `backoffice-tech` |
| venda / MRR / funil / prospecção do Consultório | `consultorio-comercial` |
| entrega / metodologia / template / delivery do Consultório | `consultorio-operacional` |
| marketing pago / social pra clientes | `fabrica-marketing` |
| evento / RP / produtora | `produtora-rp` |
| financeiro / jurídico / pessoas / CS / contábil (suporte) | `apoio-<func>` |
| investida / produto do portfólio | `portfolio-<slug>` |
| estrutural da Holding | `holding` |
| ferramenta dev genérica sem vínculo Singular | `generico` |
| serve 2+ BUs | `bu` = primária + `cross_bu` = [outras] |

## Regra de Ouro para Skills-Ferramenta

| Tipo de skill | Tag `bu` |
|---------------|----------|
| skill PRODUZ entregável pra uma BU específica | BU servida (ex: `/prospect` -> `consultorio-comercial`; `/slide` -> cross-bu; `/pop`, `/ata` -> `backoffice-tech` ou BU servida) |
| skill é infra / utilitário do ecossistema | `backoffice-tech` (ex: checkpoint, health, ship, retro, cso) |
| skill é dev tool genérico sem produto Singular | `generico` (dona operacional = `backoffice-tech`) (ex: vercel, n8n-* genérico, design-* genérico, gstack browser) |

## Aplicação

1. **Tag `bu` no frontmatter** de toda memória/doc/artefato Singular (+ `cross_bu` se aplicável).
2. **Pasta correta por BU** no destino (segue a árvore de `plano/singular/` por BU).
3. **Payload Qdrant** com `bu` (+ `cross_bu`) no ingest do Singular_Memory.
4. **Quando ambíguo entre 2+ BUs primárias**, PERGUNTAR ao Pedro antes de classificar:

```
[BU] Qual a BU primária desse artefato?
[ ] consultorio-comercial (Simon)
[ ] consultorio-operacional (Arthur Trojan)
[ ] fabrica-marketing (Carol)
[ ] produtora-rp (Ana Luiza)
[ ] backoffice-tech (Robertinho + Volpi)
[ ] apoio-<func>  [ ] portfolio-<slug>  [ ] holding  [ ] generico
cross_bu (serve outras)? [ ] sim, quais: ____   [ ] não
```

Se a BU for óbvia pela heurística, classifica direto sem perguntar.

## Sincronização (cópias derivadas)

Esta rule é Master Desktop SoT da dimensão BU. Replicada em (devem refletir esta SoT):
- `~/.claude/CLAUDE.md` (persona Master Desktop, bloco REGRA SOBERANA #4 resumido + link aqui)
- `~/.claude/rules/core/identity.md` (sub-seção da Catalogação Singular)
- `github.com/pedrormc/claude-code-toolkit` (toolkit, propagação TRIFORCE)
- SoT dos slugs e donos: memória `feedback_bu_taxonomy_singular` ([[feedback_bu_taxonomy_singular]])

**Workflow de mudança:** editar aqui primeiro (regra) e em `feedback_bu_taxonomy_singular` (slugs/donos), depois propagar para CLAUDE.md, identity.md e toolkit.

*[Registrado por: DESKTOP — 2026-06-05]*
