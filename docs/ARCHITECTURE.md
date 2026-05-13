# Claude Code Architecture — Master Desktop (Pedro)

> Documenta o ambiente Claude Code do Pedro após o rebuild de 2026-05-12.
> Source of Truth pra futuras sessões e pra setup em novos ambientes TRIFORCE.

## Estado pós-rebuild (2026-05-12)

### Trigger
Auditoria com 6 agentes paralelos identificou 31 findings após user reportar que SessionStart estava carregando scheduled task `daily-sync-obsidian` ao invés da conversa interativa anterior.

### Resultado
- **BLOCKER fixado:** ECC SessionStart hook agora filtra `<scheduled-task name=` summaries.
- **31/31 findings endereçados** ou documentados como follow-up.
- **audit-hooks.sh:** 13/13 PASS final.
- **Backup completo:** `~/.claude/.backup-2026-05-12-rebuild/` (431KB).
- **Spec rastreável:** `~/.claude/specs/2026-05-12-environment-rebuild-design.md`.

---

## Hierarquia de Carregamento

Claude Code carrega contexto nesta ordem (ver `using-superpowers` skill):
1. **User instructions** (CLAUDE.md, GEMINI.md, AGENTS.md, mensagens diretas) — **maior prioridade**
2. **Superpowers skills** — override default
3. **Default system prompt** — menor prioridade

## Estrutura de Diretórios

```
~/.claude/
├── CLAUDE.md                    # Persona Master Desktop (identidade + 3 Abas Master) — duplicação consciente com identity.md
├── ARCHITECTURE.md              # ESTE arquivo
├── settings.json                # Config global (51 skillOverrides, 75 autocompact, async Stop hooks)
├── settings.local.json          # Permissões (387 allows acumulados — limpar em Phase 6.5 futuro)
├── statusline.sh                # Status line bash + jq
│
├── rules/
│   ├── core/
│   │   └── identity.md          # SoT 3 Abas Master + Master Desktop (rebuild 2026-05-12)
│   ├── common/                  # rules globais antigas (compatibilidade)
│   │   ├── agents.md            # CORRIGIDO: clarifica local (5) vs plugin (ECC)
│   │   ├── namespace-cheatsheet.md  # CORRIGIDO: status real plugins
│   │   ├── performance.md       # CORRIGIDO: Opus 4.7
│   │   ├── hooks.md             # CORRIGIDO: vocab settings.json moderno
│   │   ├── git-workflow.md
│   │   ├── coding-style.md
│   │   ├── development-workflow.md
│   │   ├── patterns.md
│   │   ├── security.md
│   │   ├── testing.md
│   │   ├── three-tabs-priority.md  # cópia legada (manter; SoT é core/identity.md)
│   │   └── project-categorization.md
│   ├── typescript/              # 5 arquivos — carregamento atual incondicional (~3K tokens overhead)
│   ├── language/                # NOVO, vazio — placeholder pra conditional loading futuro
│   ├── domain/                  # NOVO, vazio — placeholder pra rules por projeto (singular/plano)
│   └── parallel-agents.md       # Worktree isolation
│
├── agents/                      # 5 agents customizados Singular
│   ├── api-specialist.md
│   ├── devops-agent.md
│   ├── frontend-specialist.md
│   ├── prompt-engineer.md
│   └── research-agent.md
│
├── hooks/                       # Lifecycle handlers
│   ├── verify-ecc-patches.sh    # NOVO 2026-05-12: re-aplica ECC patches se update sobrescreve
│   ├── session-start-memory-loader.sh
│   ├── session-end-memory-writer.sh  # PATCHED: truncate keep=3
│   ├── obsidian-auto-save.sh
│   ├── post-edit-memory-validator.sh  # PATCHED: jq→node fallback
│   ├── save-session-vault-mirror.sh   # PATCHED: idempotent (mtime check)
│   └── lib/                     # placeholder para funções compartilhadas
│
├── scripts/                     # Utilities
│   ├── audit-hooks.sh           # NOVO 2026-05-12: smoke-test 13 hooks (rode após mudanças)
│   ├── audit-sessions.sh        # NOVO 2026-05-12: detecta sessions misroteadas (--fix opcional)
│   ├── sync-triforce.sh         # NOVO 2026-05-12: propaga p/ VPS via SSH
│   ├── claude-notify.js         # Toast + terminal title
│   ├── memory-update.sh
│   ├── memory-revert.sh
│   ├── memory-index-rebuild.sh
│   ├── memory-auto-promote.sh   # Unix cron (não roda no Windows — registrar via schtasks pra ativar)
│   ├── obsidian-session-format.js
│   ├── whatsapp-send.js
│   ├── brainstorm-up.ps1
│   ├── rotate-mcp-key.ps1
│   └── foundation-{smoke,validate,uninstall}.sh
│
├── patches/                     # NOVO 2026-05-12
│   └── ecc-session-start-filter.md  # Documenta patch crítico
│
├── sessions/                    # Pool ativo: 113 .tmp interactive flat
│   ├── scheduled/               # Quarentena: 10 .tmp polluídas com scheduled-task
│   ├── _archive/                # 43 .tmp >30 dias arquivadas
│   └── interactive/             # vazio (preparado pra isolamento write-side futuro)
│
├── specs/
│   └── 2026-05-12-environment-rebuild-design.md  # Esta intervenção
│
├── _archive/                    # NOVO 2026-05-12: backups + órfãos preservados (não deletados)
│   ├── scripts/                 # toast-notify.js, test-i4-fake-data.sh
│   ├── shell-snapshots/         # 107 snapshots antigos
│   ├── active.md.pre-truncate-2026-05-12
│   ├── scheduled_tasks.lock.stale-pid13888-2026-05-12
│   ├── audit-hooks.log          # log do auditor
│   ├── audit-sessions.log
│   └── verify-ecc-patches.log
│
├── .backup-2026-05-12-rebuild/  # Backup completo pré-rebuild (431KB)
│
├── plugins/                     # Gerenciado pelo Claude Code (155MB)
│   └── ...
├── projects/                    # Auto-memory + sessions JSONL
│   └── C--Users-teste/memory/MEMORY.md  # 27/27 entries
├── scheduled-tasks/
│   └── daily-sync-obsidian/
│       ├── SKILL.md
│       └── last_run.json        # NOVO 2026-05-12: observabilidade
├── secrets/                     # OAuth keys (NTFS-restricted)
├── shell-snapshots/             # 5 mais recentes (107 movidos pra _archive)
└── triforce/                    # TRIFORCE config
```

## Critical Hooks (settings.json)

| Event | Hook | Async | Timeout | Status |
|-------|------|-------|---------|--------|
| SessionStart | `verify-ecc-patches.sh` | sync | 3000ms | Garante patches ECC presentes |
| SessionStart | `session-start-memory-loader.sh` | async | 10000ms | Carrega memory |
| SessionStart | `any-buddy apply --silent` | async | 30000ms | Plugin |
| UserPromptSubmit | inline `printf` | sync | 2000ms | Atualiza title TUI |
| Stop | `claude-notify.js` | async | 10000ms | Toast |
| Stop | `session-end-memory-writer.sh` | async | 10000ms | Atualiza active.md (truncate=3) |
| SessionEnd | `obsidian-auto-save.sh` | sync | 15000ms | Salva no vault |
| PostToolUse(Edit\|Write) | `post-edit-memory-validator.sh` | sync | default | Valida YAML frontmatter |
| PostToolUse(Write) | `save-session-vault-mirror.sh` | sync | default | Mirror idempotente |
| Notification/PermissionRequest/TaskCompleted/SubagentStop | `claude-notify.js` | sync | 10000ms | Toast |

## Performance Configurations Aplicadas

| Setting | Antes | Depois | Justificativa |
|---------|-------|--------|---------------|
| `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` | 50 | 75 | Corta compactações pela metade |
| `effortLevel` | xhigh | xhigh (mantido) | Arquitetura/raciocínio profundo |
| `skillOverrides` | (vazio) | 51 entries off/user-invocable-only | Corta ~4-5K tokens/turn |
| `skillListingMaxDescChars` | (default 1536) | 200 | Reduz overhead descrições verbosas |
| `N8N_API_KEY` em settings env | plaintext | removido (vem do Windows User env) | Segurança |
| `N8N_API_URL` em settings env | plaintext | removido | Mesma razão |

## Secrets

Todos os secrets estão em **Windows User Environment Variables** (não em settings.json):
- `N8N_API_KEY` ✅ verificado presente
- `N8N_API_URL` ✅ verificado presente
- `TESTSPRITE_API_KEY` ✅ verificado presente
- `EVOLUTION_API_KEY` (via env nos scripts)
- `SERPAPI` (token na URL do MCP — TODO: migrar pra header em Phase futura)

OAuth keys: `~/.claude/secrets/gcp-oauth.keys.json` e `gcp-oauth.token.json` (permissões NTFS).

## Rotinas de Manutenção

### On-demand
- `~/.claude/scripts/audit-hooks.sh` — roda 13 smoke-tests, output em `_archive/audit-hooks.log`
- `~/.claude/scripts/audit-sessions.sh [--fix]` — checa misclassificação de sessions
- `~/.claude/scripts/sync-triforce.sh status|push` — sync Desktop → Mobile/VPS

### Auto (via hooks)
- Stop → notify + truncate active.md (async)
- SessionEnd → obsidian-auto-save (write daily-note se reason=exit)
- SessionStart → verify-ecc-patches (sync, 3s) + memory-loader (async) + any-buddy (async)

### Recomendadas (não automatizadas ainda)
- Diário: `audit-sessions.sh --fix` (Windows Task Scheduler)
- Semanal: `audit-hooks.sh` + review failing tests
- Mensal: clean `_archive/shell-snapshots/` se > 1GB

## TRIFORCE Sync

- **Desktop (este):** SoT — todas as mudanças começam aqui.
- **VPS (`vps`, `vps-claude`):** sync via `sync-triforce.sh push` (precisa SSH config; `vps` alias atualmente não resolvendo — TODO config).
- **Mobile (Termux):** sem SSH push; sync via `git pull` no `pedrormc/claude-code-toolkit` (toolkit é segundo SoT para Mobile/VPS).

## ECC Patches Críticos

`~/.claude/patches/ecc-session-start-filter.md` documenta o patch que filtra scheduled-task summaries. Re-aplicado automaticamente via `verify-ecc-patches.sh` em todo SessionStart.

Se ECC update sobrescrever:
1. `verify-ecc-patches.sh` detecta e re-aplica via Python regex replace.
2. Log em `~/.claude/_archive/verify-ecc-patches.log`.
3. Smoke-test confirma via `audit-hooks.sh`.

## Memory Architecture

- `~/.claude/projects/C--Users-teste/memory/MEMORY.md` — 27 entries, índice.
- Cada entry aponta pra `<slug>.md` no mesmo dir.
- Tipos: user, feedback, project, reference.
- `feedback_*.md` são mais importantes — comportamentos a manter/evitar.
- Update via `~/.claude/scripts/memory-update.sh` (não Edit direto).

## Follow-ups (não feitos neste rebuild)

1. **Migrar `memory-auto-promote.sh` pra Windows Task Scheduler** (atualmente desenhado pra cron Unix, nunca roda).
2. **Configurar SSH alias `vps`** pra Lightsail (`vps-claude` já funciona).
3. **Consolidar 6 cópias 3 Abas Master** via script `sync-rules.sh` (SoT em `core/identity.md`).
4. **Conditional loading pra `rules/typescript/`** (pasta `language/` criada, vazia, pronta).
5. **PR upstream `affaan-m/everything-claude-code`** com o patch filter (sustainability).
6. **Migrar SerpAPI** de URL com token pra header authorization.
7. **Limpar `settings.local.json`** (387 lines acumuladas de permissions, muitas obsoletas).
8. **Decidir designer-skills marketplace** (atualmente renomeado `_DEPRECATED_`, considerar remover).

## Como recuperar se algo quebrar

1. `cd ~/.claude/.backup-2026-05-12-rebuild/` → tem tudo (settings, rules, hooks, scripts, agents, triforce, memory).
2. `cp -r .backup-2026-05-12-rebuild/* ~/.claude/` → restaura.
3. `audit-hooks.sh` pra verificar.

*[Registrado por: DESKTOP — 2026-05-12 — rebuild Phase 8]*
