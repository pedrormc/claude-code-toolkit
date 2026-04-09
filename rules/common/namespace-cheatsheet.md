# Namespace Cheatsheet — Claude Code Stack

> Quem faz o quê nos slash commands. Use isso quando houver dúvida ou colisão.

## Plugins instalados (4 ativos + 2 desabilitados)

| Plugin | Origem | Comando exemplo | Status |
|---|---|---|---|
| ECC | everything-claude-code | `/plan`, `/tdd`, `/learn-eval` | ativo |
| Superpowers | superpowers-marketplace | `/brainstorming`, `/writing-plans` | ativo |
| Gstack | garrytan/gstack | `/office-hours`, `/autoplan`, `/review`, `/ship`, `/qa`, `/cso` | ativo (36 skills) |
| UI/UX Pro Max | ui-ux-pro-max-skill | `/ui-ux-pro-max` | ativo |
| Ralph | snarktank/ralph | `/prd`, `/ralph` | **desabilitado** (substituído por RuFlo) |
| RuFlo | ruvnet/ruflo (VPS only) | n/a (workers off na Fase 1) | **desabilitado** (Phase 2) |
| Context7 | upstash/context7 | — | não instalado (fora de escopo) |

## Quando usar qual (em caso de overlap)

| Tarefa | Use |
|---|---|
| Brainstorm requisitos antes de codar | `superpowers:brainstorming` (rigoroso) |
| Escrever spec depois de brainstorm | `superpowers:writing-plans` |
| Quick plan pragmático sem spec | `gstack:/autoplan` |
| Code review focado em padrões | `superpowers:requesting-code-review` |
| Code review focado em deploy | `gstack:/review` |
| Security audit completo (OWASP+STRIDE) | `gstack:/cso` |
| Security check pre-commit | ECC `security-reviewer` agent |
| Test E2E completo via browser | `gstack:/qa` |
| Test E2E via Playwright headless | ECC `e2e-runner` agent |
| Plan de implementação multi-passo | `superpowers:writing-plans` |
| Investigação de bug | `gstack:/investigate` |
| Retro semanal | `gstack:/retro` |
| Salvar sessão | `ECC save-session` |
| Retomar sessão | `ECC resume-session` |
| Atualizar memória global (vault) | `~/.claude/scripts/memory-update.sh claude <file> <content>` |
| Reverter auto-promoção | `~/.claude/scripts/memory-revert.sh <entry-id>` |

## Agents customizados (5, do claude-code-toolkit)

| Agent | Quando |
|---|---|
| `api-specialist` | Express REST API, queries PG |
| `devops-agent` | Vercel deploy, GitHub Actions, env mgmt |
| `frontend-specialist` | React 19 + TS strict + Tailwind v4 |
| `prompt-engineer` | Otimizar CLAUDE.md, agents, skills, rules |
| `research-agent` | Avaliar libs antes de implementar |

## Regra de ouro pra escolher

1. Se o slash command **só existe num plugin**, usa esse.
2. Se existe em 2+, **prefere o mais específico ao caso de uso** (ver tabela acima).
3. Se ainda em dúvida, **prefere Superpowers** (mais rigoroso, gates explícitos).
4. Se quer velocidade > rigor, **prefere Gstack**.

## Quando matar (re-avaliar a cada 2 semanas)

Skills/agents não usados em 14 dias → candidatos a disable. Rastreamento de usage via hook `PostToolUse` virá no sub-projeto D.

*[Registrado por: DESKTOP — 2026-04-09]*
