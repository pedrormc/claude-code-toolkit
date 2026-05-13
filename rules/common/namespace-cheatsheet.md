# Namespace Cheatsheet — Claude Code Stack

> Quem faz o quê nos slash commands. Use isso quando houver dúvida ou colisão.
> **Atualizado 2026-05-12 [DESKTOP]** após rebuild estrutural.

## Plugins instalados (status real após rebuild)

| Plugin | Origem | Status | Comando exemplo |
|---|---|---|---|
| everything-claude-code | affaan-m/everything-claude-code | **ATIVO** v1.8.0 (~50 skills ocultas via skillOverrides) | `/plan`, `/tdd`, `/learn-eval` |
| superpowers | obra/superpowers-marketplace | **ATIVO** v5.0.2 | `/brainstorming`, `/writing-plans` |
| ralph-skills | snarktank/ralph | **ATIVO** v1.0.0 (disabledPlugins limpo no rebuild) | `/ralph`, `/prd` |
| ui-ux-pro-max | nextlevelbuilder/ui-ux-pro-max-skill | ATIVO v2.2.1 | `/ui-ux-pro-max` |
| example-skills | anthropics/skills | ATIVO (commit f458cee) | `/docx`, `/pdf`, `/algorithmic-art` |
| vercel | claude-plugins-official | ATIVO v0.42.1 | `/vercel:deploy`, `/vercel:bootstrap` |
| designer-skills | Owl-Listener/designer-skills | **DEPRECATED** 2026-05-12 — marketplace registered mas zero plugins ativos | — |
| RuFlo | ruvnet/ruflo (VPS only) | DESABILITADO Phase 1 | — |

## Skills ECC silenciadas via skillOverrides (rebuild Phase 2)

~50 skills de stacks fora do domínio (perl, swift, kotlin, android, go, java, springboot, django, c++, logistics, supply chain etc) estão com `"off"` ou `"user-invocable-only"` em `settings.json > skillOverrides`. Economia: **~4-5K tokens/turn**.

Pra ver listagem completa: `jq '.skillOverrides' ~/.claude/settings.json`.

## Quando usar qual (em caso de overlap)

| Tarefa | Use |
|---|---|
| Brainstorm requisitos antes de codar | `superpowers:brainstorming` (rigoroso, gates explícitos) |
| Escrever spec depois de brainstorm | `superpowers:writing-plans` |
| Quick plan pragmático sem spec formal | gstack `/autoplan` |
| Code review focado em padrões | `superpowers:requesting-code-review` |
| Code review focado em deploy | gstack `/review` |
| Security audit completo (OWASP+STRIDE) | gstack `/cso` |
| Security check pre-commit | ECC `security-reviewer` agent |
| Test E2E completo via browser | gstack `/qa` |
| Test E2E via Playwright headless | ECC `e2e-runner` agent |
| Investigação de bug | gstack `/investigate` (sistemático) |
| Retro semanal | gstack `/retro` |
| Salvar sessão | ECC `save-session` |
| Retomar sessão | ECC `resume-session` |
| Atualizar memória global (vault) | `~/.claude/scripts/memory-update.sh` |
| Reverter auto-promoção | `~/.claude/scripts/memory-revert.sh` |
| Health check de hooks | `~/.claude/scripts/audit-hooks.sh` (criado no rebuild) |
| Sync TRIFORCE | `~/.claude/scripts/sync-triforce.sh` |

## Agents customizados (5, em `~/.claude/agents/`)

| Agent | Quando |
|---|---|
| `api-specialist` | Express REST API, queries PG |
| `devops-agent` | Vercel deploy, GitHub Actions, env mgmt |
| `frontend-specialist` | React 19 + TS strict + Tailwind v4 |
| `prompt-engineer` | Otimizar CLAUDE.md, agents, skills, rules |
| `research-agent` | Avaliar libs antes de implementar |

Detalhes em `~/.claude/rules/common/agents.md`.

## Regra de ouro pra escolher

1. Se o slash command **só existe num plugin**, usa esse.
2. Se existe em 2+, **prefere o mais específico ao caso de uso** (ver tabela acima).
3. Se ainda em dúvida, **prefere Superpowers** (mais rigoroso, gates explícitos).
4. Se quer velocidade > rigor, **prefere Gstack**.
5. Pra meta-trabalho no próprio Claude Code (config, hooks, rules), **prefere agente customizado** `prompt-engineer`.

## Manutenção

Skills/agents não usados em 14 dias → candidatos a `skillOverrides: "off"`. Rastreamento via `audit-hooks.sh` (criado em rebuild Phase 5).

*[Atualizado por: DESKTOP — 2026-05-12 — rebuild Phase 6: status real após cleanup]*
