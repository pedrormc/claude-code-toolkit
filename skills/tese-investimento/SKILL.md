---
name: tese-investimento
description: Estrutura teses de investimento (operações tipo equity ou aplicações conservadoras) com checklist + personas críticas + prompts pra slides. Use quando o usuário pedir pra montar um pitch de investimento, comparar opções de aplicação, ou criticar uma tese existente. PT-BR informal.
---

# Skill: tese-investimento (v0.5 fast-track)

> **Versão atual:** v0.5 — modo manual, sem auto-trigger de personas, sem sync. Foco em produzir `tese.md` + `slides.md` do caso comparativo.

## Quando usar

- Pedro pede `/tese-investimento <slug>` ou similar
- Pedro fala "vamos estruturar uma tese de investimento"
- Caso atual: comparativo PowerCoff (R$ 10k equity) vs sóbrio Simon (R$ 30k aplicação) pra parceiro 29/04

## Workflow v0.5

1. **Bootstrap:** Pedro invoca com slug. Cria pasta `C:\Users\teste\plano\singular\investimentos\<slug>\` se não existir. Cria `meta.yaml` stub com `slug`, `tipo`, `modo: B`, `criado_em`, `versao: 0.5`.

2. **Definir tipo:** perguntar `operacao | aplicacao | comparativo`. Se `comparativo`, perguntar sub-teses (ex: `[powercoff, sobrio-simon]`).

3. **Coletar checklist:** ler `checklist-default.md`, conduzir conversa cobrindo os 10 itens. Sem auto-trigger — Pedro fala livre, Claude vai marcando mentalmente. Quando tiver dúvida em algum item, perguntar diretamente.

4. **Crítica multi-persona (manual):** depois do checklist coberto, ler cada uma das 5 personas (`personas/*.md`) e produzir 1 turno de crítica por persona. Cada persona retorna: 1 pergunta, 1 observação, 1 heurística aplicada. Output vai pra memória da conversa (não escreve em arquivo separado em v0.5).

5. **Síntese da tese:** com todas críticas absorvidas, escrever `tese.md` na pasta do caso. Usa estrutura: contexto, tese central, retorno esperado, riscos principais, mitigações, conclusão.

6. **Geração dos slides:** ler `templates/comparativo.md`, gerar `slides.md` na pasta do caso com 8 slides (cada um = ## Slide N: <Título> + prompt pronto pra colar em IA de design).

## Comandos suportados em v0.5

- `silenciar personas` — desliga crítica multi-persona neste turno
- `voltar personas` — re-ativa
- `forçar geração` — gera tese+slides mesmo sem checklist completo (equivale ao `--force-generate` da v1)

## Output v0.5

- `tese.md` na pasta do caso
- `slides.md` na pasta do caso
- `meta.yaml` stub atualizado com `status: ready`

## NÃO faz em v0.5 (vai pra v1)

- Auto-trigger de personas baseado em tópico
- Gate bloqueante do checklist (10/10)
- Escrita de `brief.md` e `criticas.md` separados
- Sync vault + drive automáticos
- Modo `--deep`
- Templates `operacao-startup` e `aplicacao-financeira`

## Spec completo

`docs/superpowers/specs/2026-04-28-tese-investimento-design.md`
