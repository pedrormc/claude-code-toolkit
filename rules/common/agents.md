# Agents — Sources of Truth

## Agentes Customizados Locais (`~/.claude/agents/`)

5 agentes definidos pelo Pedro, especializados para o stack Singular:

| Agent | Propósito | Usar quando |
|-------|-----------|-------------|
| `frontend-specialist` | React 19, TS strict, Tailwind v4, acessibilidade | Frontend tasks |
| `api-specialist` | Express REST API, middleware, PostgreSQL, integração backend | Backend tasks |
| `devops-agent` | Vercel deploy, GitHub Actions, Docker, env management | DevOps/infra |
| `research-agent` | Avaliação de libs, prior art, documentação, comparação | Pesquisa tech |
| `prompt-engineer` | Otimizar CLAUDE.md, agents, skills, rules, hooks | Meta-tarefas Claude Code |

**SoT canônica:** os arquivos em `~/.claude/agents/*.md` são a fonte de verdade. Qualquer divergência entre rule e disco → arquivo no disco vence.

## Agentes Vindos de Plugins

### everything-claude-code plugin

Provê agentes que NÃO precisam estar em `~/.claude/agents/`. Invocação via Skill tool (`Skill(everything-claude-code:agent-harness-construction)`) ou agent system do plugin:

- `planner` — planejamento de implementação
- `code-reviewer` — review automatizada
- `tdd-guide` — TDD enforcement
- `security-reviewer` — análise de segurança
- `build-error-resolver` — fix de build errors
- `e2e-runner` — testes E2E
- `refactor-cleaner` — dead code cleanup
- `doc-updater` — atualização de docs
- `architect` — design de sistemas

### superpowers plugin

- `superpowers:code-reviewer` — code review com plan alignment + quality + architecture (use via `Agent` tool)

## Quando Usar Qual

Cheatsheet centralizada em `~/.claude/rules/common/namespace-cheatsheet.md`. Resumo:

| Tarefa | Agent preferido |
|--------|-----------------|
| Frontend React/TS | `frontend-specialist` (local) |
| Backend Express/PG | `api-specialist` (local) |
| Vercel deploy | `devops-agent` (local) |
| Pesquisar lib | `research-agent` (local) |
| Code review pré-merge | `superpowers:code-reviewer` |
| TDD enforcement | ECC plugin `tdd-guide` |
| Security audit | gstack `cso` skill (mais completo que agent) |
| Build error | ECC plugin `build-error-resolver` |

## Parallel Worktrees

Agentes que **escrevem código** em paralelo: passar `isolation: "worktree"` no `Agent` tool. Detalhes em `~/.claude/rules/parallel-agents.md`.

## Imediato (não precisa user prompt)

- Feature complexa → `planner` (ECC) ou `superpowers:planning`
- Código recém-escrito → `superpowers:code-reviewer` ou ECC `code-reviewer`
- Bug fix ou nova feature → `tdd-guide` (ECC) com TDD
- Decisão arquitetural → `architect` (ECC)

*[Atualizado por: DESKTOP — 2026-05-12 — rebuild Phase 6: clarificação SoT local vs plugin agents]*
