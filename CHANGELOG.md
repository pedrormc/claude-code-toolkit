# Changelog

All notable changes to claude-code-toolkit are documented here.
Format inspired by [Keep a Changelog](https://keepachangelog.com/).

## [2026-05-25] — Sync completo: skills, scripts, config, plugins

### Added

**Skills:**
- `skills/pdf/` — Documento PDF final com identidade Singular (reportlab + Urbanist + logo). Mesmo schema do `/documento`, produz PDF imutavel. Criada 2026-05-15.
- `skills/reuniao/` — Suite generativa pos-reuniao. Orquestrador que reusa `/ata` + `/documento` + `/pop` pra gerar suite completa numa pasta Drive dedicada. Catalogo 17 tipos, `montadores.py`, `reuniao.py`, suite de testes (regression + smoke). Criada 2026-05-20.

**Scripts:**
- `scripts/memory/` — 5 scripts Python pro sistema Singular_Memory (Qdrant): `create_collection.py`, `add_doc.py`, `consolidate_jsonl.py`, `seed_from_jsonl.py`, `__init__.py`. Stack: qdrant-client + OpenAI text-embedding-3-large + fastembed bm42.

**Plugins:**
- Example Skills (anthropics/skills) — skills oficiais Anthropic: /docx, /pdf, /xlsx, /pptx, /canvas-design, /claude-api.
- Vercel (claude-plugins-official) — 20+ skills: deploy, env vars, AI SDK, Next.js, routing, middleware, Turbopack.

### Changed

**Config (settings.json):**
- `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE`: 50% → 75%
- `effortLevel`: high → xhigh
- Added `permissions.defaultMode: "auto"` e `skipAutoPermissionPrompt: true`
- Added `SessionEnd` hook (obsidian-auto-save.sh, timeout 15s)
- Added async/timeout em Stop hooks e SessionStart hooks
- Added `verify-ecc-patches.sh` sync em SessionStart (timeout 3s)
- Fixed `UserPromptSubmit` timeout: 2 → 2000 (era milissegundos truncado)
- Added `skillOverrides`: 48 entries silenciando stacks fora do dominio (~5K tokens/turn economizados)
- Added `voice`, `theme`, `skillListingMaxDescChars`
- Cleaned `disabledPlugins` (ralph-skills fix)

**Docs:**
- `docs/SKILLS_CATALOG.md` — adicionados /pdf e /reuniao, count 19 → 21
- `README.md` — plugins 4 → 6, skills 9 → 21, section Singular_Memory, config atualizado

### Removed
- `scripts/test-i4-fake-data.sh` — test artifact nao mais usado
- `scripts/toast-notify.js` — substituido por claude-notify.js

---

## [Unreleased] - 2026-05-13

### Added — Rebuild estrutural 2026-05-12

**Hooks:**
- `hooks/verify-ecc-patches.sh` — auto-reaplica patches críticos do plugin everything-claude-code se updates os sobrescreverem. Wired em SessionStart síncrono com timeout 3s.

**Scripts (Audit & Observability):**
- `scripts/audit-hooks.sh` — 13 smoke-tests cobrindo settings.json syntax, ECC patches, hooks executáveis, active.md size, stale locks, etc. Sempre exit 0, logs em `_archive/audit-hooks.log`.
- `scripts/audit-sessions.sh [--fix]` — detecta `*-session.tmp` misroteadas (scheduled-task em flat pool, interactive em scheduled/, arquivos >30 dias). Auto-fix opcional.
- `scripts/sync-triforce.sh` — propaga config Desktop → VPS via SSH (`status` / `push [--dry-run]`).

**Rules Soberanas (novo dir `rules/core/`):**
- `rules/core/identity.md` — Single Source of Truth para "3 Abas Master" (plano/singular/skip) + persona Master Desktop. Substitui as 5+ cópias divergentes que existiam.
- `rules/core/task-orchestration.md` — REGRA SOBERANA #2. Decision tree pra classificar tasks (trivial/simples/média/complexa/multi-subsistema) + tabela de 27 rotas de skill/agent + 6 estratégias de dispatch. NÃO perguntar qual skill — decidir e agir.

**Patches:**
- `patches/ecc-session-start-filter.md` — documenta o patch crítico que filtra scheduled-task summaries do "Previous session summary" injection do ECC SessionStart hook. Inclui MD5 do estado patched + procedimento manual de re-apply.

**Docs:**
- `docs/ARCHITECTURE.md` — estrutura completa pós-rebuild do `~/.claude/` (hierarquia de loading, hooks lifecycle, performance config, secrets, manutenção, follow-ups).
- `docs/specs/2026-05-12-environment-rebuild-design.md` — spec doc do rebuild (Approach C — rebuild estrutural; 8 phases; 31 findings consolidados).

### Changed

**Hooks (patched):**
- `hooks/session-end-memory-writer.sh` — awk agora **trunca** o bloco `## Últimas 3 sessões` em N=3 entries (antes inflava sem limite; estava com 50+).
- `hooks/post-edit-memory-validator.sh` — fallback **node** caso `jq` não esteja no PATH do hook env (Git Bash padrão pode não ter).
- `hooks/save-session-vault-mirror.sh` — **idempotente** via mtime check (não copia se dest é mais novo).

**Rules atualizadas:**
- `rules/common/agents.md` — reescrita pra clarificar SoT: 5 agents customizados locais (frontend/api/devops/research/prompt) vs ~17 agents do ECC plugin. Eliminada referência a "9 agents fictícios" que nunca existiram localmente.
- `rules/common/namespace-cheatsheet.md` — status real dos plugins após rebuild (ralph DESABILITADO no settings era no-op por format mismatch; designer-skills marcado DEPRECATED).
- `rules/common/performance.md` — modelo atual: **Opus 4.7** (era Opus 4.5/Sonnet 4.6).
- `rules/common/hooks.md` — vocabulary update (`permissions.defaultMode`/`skipAutoPermissionPrompt` ao invés do antigo `dangerously-skip-permissions`).

**install.sh:**
- Adicionado copy de `rules/core/*.md`
- Adicionado copy de `patches/*.md`
- Adicionado copy de `audit-hooks.sh`, `audit-sessions.sh`, `sync-triforce.sh`
- Adicionado validação dos novos arquivos no check final.

### Fixed

- **BLOCKER:** ECC SessionStart hook (`plugins/.../scripts/hooks/session-start.js`) puxava scheduled-task summaries como "Previous session summary" porque pegava o `*-session.tmp` mais novo sem filtro. Patch aplicado nas 2 cópias (cache + marketplaces) adiciona filter por `<scheduled-task name=` e `automated run of a scheduled task`. Auto-reaplicado por `verify-ecc-patches.sh`.
- Settings.json: `UserPromptSubmit` timeout era **2ms** (bug de unidade), agora 2000ms.
- Stop hooks paralelos sem `async: true` causavam risco de cygheap fork race no Git Bash Windows (`Win32 error 299`). Agora 2 Stop hooks marcados `async: true`.
- `obsidian-auto-save.sh` estava duplicado em `Stop` E `SessionEnd` (15s timeout × 2). Removido de Stop, mantido apenas em SessionEnd.
- `disabledPlugins: ["ralph-skills@1.0.0"]` no settings era no-op (format mismatch com `enabledPlugins: "ralph-skills@ralph-marketplace"`). Limpo para `[]`.

### Removed / Archived

- `_archive/scripts/toast-notify.js` — duplicate superseded por `claude-notify.js` (movido, não deletado).
- `_archive/scripts/test-i4-fake-data.sh` — dev fixture one-shot (movido).
- `_archive/shell-snapshots/*` — 107 snapshots antigos arquivados (manteve 5 mais recentes).
- `_archive/scheduled_tasks.lock.stale-pid13888-2026-05-12` — stale lock de May 3.
- `_archive/active.md.pre-truncate-2026-05-12` — backup do active.md de 551 linhas antes do truncate.

### Security

- `N8N_API_KEY` JWT removida do plaintext em `settings.json` env block. Agora carregada via Windows User environment variable (já presente). Aplicar mesmo padrão se replicar em outras máquinas via `rotate-mcp-key.ps1`.
- `N8N_API_URL` mesma coisa.

### Performance

- `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE: 50 → 75` — corta compactações pela metade em sessões longas.
- `skillOverrides`: 51 entries (`"off"` para stacks fora do domínio — perl, swift, kotlin, android, go, java, springboot, django, c++, logistics, supply chain). Economia: **~4-5K tokens/turn**.
- `skillListingMaxDescChars: 200` — corta descrições verbosas.

### Métricas pós-rebuild

| Métrica | Antes | Depois |
|---------|-------|--------|
| audit-hooks.sh smoke-tests | (não existia) | 13/13 PASS |
| `active.md` | 551 linhas | 32 linhas |
| Skills carregadas no system reminder | 280+ (~10.5K tokens) | ~230 (51 silenciadas) |
| Stop hooks | 3 (com dup) | 2 (deduped, async) |
| UserPromptSubmit timeout | 2ms (bug) | 2000ms |
| BLOCKER scheduled task | ativo | fixado + auto-healing |

---

## [v1] - 2026-05-11

- Toolkit completo + SETUP_PROMPT reescrito + install.sh atualizado + catalog
- 19 skills custom (ata, contrato, slide, documento, backgroundcheck, etc.)
- Foundation v1 (memory brain + hooks + scripts)
- 4 plugins (everything-claude-code, superpowers, ralph, ui-ux-pro-max)
- Marketplaces registrados
- TRIFORCE methodology (Desktop/Mobile/VPS)

Ver historico completo em `git log --oneline`.
