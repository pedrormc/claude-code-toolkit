---
name: task-orchestration-rule
description: Toda task do Pedro DEVE acionar a melhor combinação de agents+skills disponíveis pra executar com máxima qualidade
type: core
scope: global
source: rules-core
last_updated: 2026-05-12
---

# Task Orchestration — Regra Soberana

> **Decretada em:** 2026-05-12 por DESKTOP
> **Aplica em:** TODAS as tasks do Pedro, em qualquer ambiente TRIFORCE
> **Override:** apenas o Pedro pode revogar

## A Regra

Para **toda task** que o Pedro propor, ANTES de executar, o Claude **DEVE**:

1. **Classificar a complexidade** (trivial / simples / média / complexa / multi-subsistema)
2. **Identificar agents+skills relevantes** (não 1, todos que possam ajudar — mas dispatch só os úteis)
3. **Decidir estratégia de dispatch** (direto, single-skill, paralelo, pipeline)
4. **Executar com máxima concorrência possível** (parallel sub-agents read-only quando aplicável)
5. **Reportar brevemente** qual rota foi escolhida e por quê (1-2 linhas, não enumerar todos)

**NÃO PERGUNTAR** "qual skill devo usar?" — escolher e agir. Pergunta só se ambíguo entre 2+ rotas igualmente válidas.

## Classificação de Tasks

| Tipo | Sinais | Estratégia |
|------|--------|-----------|
| **Trivial** | Pergunta factual, status check, "que horas são", config trivial | Resposta direta, sem agent/skill |
| **Simples** | 1 arquivo, 1 conceito, < 3 passos | 1 skill primária OU execução direta |
| **Média** | Multi-arquivo, 1 subsistema, 3-10 passos | Skill primária + agent específico em paralelo |
| **Complexa** | Multi-arquivo + multi-decisão + tradeoffs | brainstorming → writing-plans → subagent-driven-development |
| **Multi-subsistema** | Toca 3+ áreas distintas (frontend + backend + infra + segurança) | Agentes paralelos read-only pra audit + síntese + plano de execução |
| **Bug/erro** | "Não funciona", "deu pau", "erro X" | systematic-debugging OU gstack:investigate (sistemático, root cause) |

## Tabela de Roteamento (lookup rápido)

| Tarefa | Primary | Secondary (paralelo se aplicável) |
|--------|---------|----------------------------------|
| **Nova feature** | `superpowers:brainstorming` → `writing-plans` | ECC `planner`, local `frontend-specialist` ou `api-specialist` |
| **Bug investigation** | `superpowers:systematic-debugging` | gstack `/investigate`, ECC `build-error-resolver` |
| **Code review pre-merge** | `superpowers:requesting-code-review` | ECC `code-reviewer`, ECC `security-reviewer` |
| **Code review pós-deploy** | gstack `/review` | gstack `/canary` (monitoramento) |
| **Architecture decision** | `superpowers:brainstorming` → ECC `architect` | local `research-agent` (prior art) |
| **Performance issue** | gstack `/benchmark` | gstack `/health`, vercel:performance-optimizer |
| **Security audit** | gstack `/cso` (completo OWASP+STRIDE+supply chain) | ECC `security-reviewer` (agent pré-commit) |
| **Deploy** | gstack `/ship` | vercel:deploy, gstack `/land-and-deploy`, local `devops-agent` |
| **Testes** | `superpowers:test-driven-development` | ECC `tdd-guide`, ECC `e2e-runner`, gstack `/qa` |
| **Documentação** | gstack `/document-release` | ECC `doc-updater` |
| **Pesquisar lib/tech** | local `research-agent` | exa-web-search MCP, gh search |
| **Refactor large** | `superpowers:brainstorming` → `writing-plans` | ECC `refactor-cleaner`, agentes paralelos em worktree |
| **Audit ambiente Claude Code** | local `prompt-engineer` agent | 6 agentes paralelos read-only (ver rebuild 2026-05-12) |
| **Dashboard/UI** | gstack `/design-consultation` (system) → `/design-html` | `ui-ux-pro-max`, ECC `frontend-slides` |
| **Contrato Singular** | skill `/contrato` | Qdrant Nexo_Adv MCP (obrigatório, ver feedback_contratos_singular) |
| **Background check** | skill `/backgroundcheck` | Sem skip de societário (ver feedback_backgroundcheck_societario) |
| **Slides Singular** | skill `/slide` | brand assets em Desktop/dondon/pop |
| **WhatsApp send** | skill `whatsapp-evolution` | reference_evolution_api |
| **n8n workflow** | n8n-mcp tools | gh search pra prior art |
| **HubSpot CRM** | hubspot-singular OU hubspot-smup MCP | hubspot-mcp-expert skill |
| **Drive upload** | `mcp__google-drive__uploadFile` | feedback_drive_upload_zel (pasta Zel obrigatória) |
| **Memory update** | `~/.claude/scripts/memory-update.sh` | NÃO Edit direto (ver namespace-cheatsheet) |
| **Salvar progresso** | ECC `save-session` | gstack `/checkpoint` |
| **Retomar sessão** | ECC `resume-session` | — |
| **Health check ambiente** | `~/.claude/scripts/audit-hooks.sh` | audit-sessions.sh, sync-triforce status |
| **Sync TRIFORCE** | `~/.claude/scripts/sync-triforce.sh push` | manual git pull no Mobile |

## Estratégias de Dispatch

### 1. Direto (trivial)
> Resposta sem ferramenta. Ex: "o que é uma feature flag?"

### 2. Single-skill (simples/média)
> Invoca 1 skill, segue workflow dela. Ex: gerar contrato → `/contrato`.

### 3. Pipeline (complexa)
> `brainstorming` (alinha) → `writing-plans` (spec) → `subagent-driven-development` (execução com checkpoints) → `code-reviewer` (review). Cada etapa tem gate.

### 4. Parallel agents read-only (multi-subsistema)
> Para auditoria, mapeamento, descoberta: 4-8 agentes em paralelo, cada um foca uma área. Eu sintetizo. Exemplo deste rebuild: 6 agentes (hooks/rules/plugins/memory/scripts/performance). Use `Agent` tool com `run_in_background: true` e brief específico por agente.

### 5. Parallel agents write (refactor amplo)
> Cada agente em `isolation: "worktree"`. Eu reviso e mergeio. Ver `~/.claude/rules/parallel-agents.md`.

### 6. Investigative loop (bug crítico)
> `systematic-debugging` → root cause → fix mínimo → verification-before-completion → commit.

## Como Decidir (Heurística)

```
Task chega:
├── Trivial (pergunta factual, status)? → estratégia 1 (direto)
├── User invocou skill explicitamente (/cmd)? → respeita, segue workflow daquela skill
├── Match único na tabela acima? → estratégia 2 (single-skill)
├── Bug/erro reportado? → estratégia 6 (investigative)
├── 3+ subsistemas (frontend+backend+infra+sec...)? → estratégia 4 (parallel read-only)
├── Nova feature ou refactor complexo? → estratégia 3 (pipeline)
└── Refactor que toca muito arquivo? → estratégia 5 (parallel write em worktree)
```

## Reporting

Após decidir, **antes de executar**, declarar em 1-2 linhas:

> "[Orquestração] Task X classificada como Y. Dispatch: skill Z + agentes A, B em paralelo."

Não enumerar opções rejeitadas. Não pedir confirmação se a rota é óbvia.

## Anti-patterns (evitar)

1. **Dispatch de agent pra task que faria em 2 ferramenta calls direto** — overhead pior que valor.
2. **Listar 5 skills "que poderiam ajudar" e pedir pro user escolher** — decida você.
3. **Sequencial quando podia ser paralelo** — sempre prefira concorrência onde não há dependência.
4. **Repetir trabalho que subagent já fez** — confia no relatório do agent, não duplica.
5. **Brainstorming pra task trivial** — overkill que irrita o user (memory: "preferir ações diretas").
6. **Enumerate todas skills disponíveis em cada turn** — caro em tokens (já temos skillOverrides cortando 4-5K).

## Memory & Override

- Se o user disser **"sem orquestração, só faz X"** → modo direto, ignora regra nesta task.
- Se o user disser **"chama todos os agentes"** → modo paralelo aggressive (estratégia 4 mesmo se task média).
- Se o user disser **"ultrathink"** → adicionar análise profunda + considerar estratégia 3 ou 4 mesmo em tasks médias.

## Cross-references

- Cheatsheet completa: `~/.claude/rules/common/namespace-cheatsheet.md`
- Agents inventário: `~/.claude/rules/common/agents.md`
- Workflow git: `~/.claude/rules/common/git-workflow.md`
- 3 Abas Master (categoriza ANTES da orquestração): `~/.claude/rules/core/identity.md`
- Parallel agents safety: `~/.claude/rules/parallel-agents.md`

## Sequência Combinada com 3 Abas

```
Input do Pedro chega
  ↓
1. Categoriza nas 3 Abas Master (plano/singular/skip) — REGRA SOBERANA #1
  ↓
2. Aplica Task Orchestration (esta regra) — REGRA SOBERANA #2
  ↓
3. Executa com agents/skills escolhidos
  ↓
4. Reporta breve
```

## Sincronização

Esta regra é Master Desktop SoT. Replicada em (devem refletir):
- `~/.claude/CLAUDE.md` (referência curta + link aqui)
- `~/.claude/projects/C--Users-teste/memory/feedback_task_orchestration.md` (memory)
- TRIFORCE Mobile/VPS: propagar via `sync-triforce.sh push`

*[Registrado por: DESKTOP — 2026-05-12]*
