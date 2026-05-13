---
name: claude-code-environment-rebuild
description: Approach C — rebuild estrutural do ambiente Claude Code Desktop após auditoria com 6 agentes paralelos
status: in-progress
started: 2026-05-12T18:45 UTC-3
owner: Pedro Roberto (Desktop)
environments: TRIFORCE (este: Desktop; Mobile/VPS via sync-triforce.sh em Phase 5)
---

# Claude Code Environment Rebuild — Design Doc

## Contexto

Auditoria com 6 agentes paralelos revelou 31 findings (1 BLOCKER, 10 HIGH, 10 MEDIUM, 10 LOW). Trigger inicial: SessionStart hook puxando scheduled task `daily-sync-obsidian` ao invés de conversa interativa anterior.

Approach escolhido: **C — Rebuild estrutural** (cobre 31/31 findings).

## Backup

Antes de qualquer mudança: `~/.claude/.backup-2026-05-12-rebuild/` (431KB, exclui plugins cache/sessions runtime/shell-snapshots).

## Princípios

1. **Single Source of Truth** por conceito (3 abas, agents, rules, secrets).
2. **Carregamento condicional** de rules (corta tokens/turn).
3. **Observabilidade by default** (last_run.json, audit-hooks.sh).
4. **Async no Windows** pra hooks de side-effect (evitar cygheap fork race).
5. **Smoke-testable** (audit-hooks.sh roda <30s).
6. **Never delete** — move pra `_archive/`. Respeita feedback memory "Nunca deletar configs".

## Findings consolidados

### BLOCKER
1. ECC SessionStart hook (`session-start.js:34-47`) pega `*-session.tmp` mais novo sem filtrar scheduled tasks.

### HIGH (10)
2. `active.md` log infinito (awk no writer não trunca).
3. SessionStart loader síncrono → risco cygwin fork race.
4. 3 Stop hooks paralelos sem async.
5. `rules/common/agents.md` declara 9 agents fictícios.
6. Ralph disable broken (format mismatch `@1.0.0` vs `@ralph-marketplace`).
7. **N8N_API_KEY plaintext** em settings.json.
8. `obsidian-auto-save.sh` duplicado Stop+SessionEnd.
9. `namespace-cheatsheet.md` stale.
10. `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE: 50` agressivo.
11. 280+ skills carregadas = ~10.5K tokens/turn.

### MEDIUM (10) + LOW (10)
(ver findings completos no histórico da sessão c8d06464)

## Phases

- **Phase 0** ✅ Backup + spec doc + scaffolding (`sessions/{interactive,scheduled,_archive}`, `_archive/`, `patches/`, `hooks/lib/`, `specs/`)
- **Phase 1** BLOCKER fix (ECC patch + migration sessions + stale lock)
- **Phase 2** Performance tuning (autocompact 50→75, effortLevel xhigh→high, skillOverrides ~80, async flags)
- **Phase 3** Hook hygiene (active.md truncation, dup removal, jq→node, timeouts)
- **Phase 4** Cleanup órfãos pra `_archive/` (toast-notify.js, ralph/, shell-snapshots antigos)
- **Phase 5** Observabilidade nova (audit-hooks.sh, audit-sessions.sh, sync-triforce.sh, verify-ecc-patches.sh, session-save-router.sh, last_run.json)
- **Phase 6** Rules restructure (core/language/domain, SoT 3 abas, fix agents.md, merge typescript/*)
- **Phase 7** Agents corretos (criar code-reviewer, tdd-guide, security-reviewer, build-error-resolver, e2e-runner, refactor-cleaner, doc-updater, planner, architect)
- **Phase 8** Docs (ARCHITECTURE.md, update CLAUDE.md, update MEMORY.md)

## Smoke-Test

`~/.claude/scripts/audit-hooks.sh` roda 12+ smoke-tests após Phase 5. Phase 8 inclui verificação final em paralelo.

## Rollback

Cada phase é reversível pela cópia em `~/.claude/.backup-2026-05-12-rebuild/`. ECC patches versionados em `~/.claude/patches/`.

*[Registrado por: DESKTOP — 2026-05-12]*
