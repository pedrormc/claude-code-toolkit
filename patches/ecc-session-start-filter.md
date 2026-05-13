# ECC session-start.js — Scheduled-Task Filter Patch

**Aplicado:** 2026-05-12 por DESKTOP
**Target:** `everything-claude-code@1.8.0`
**Arquivos patched:**
- `~/.claude/plugins/marketplaces/everything-claude-code/scripts/hooks/session-start.js`
- `~/.claude/plugins/cache/everything-claude-code/everything-claude-code/1.8.0/scripts/hooks/session-start.js`

**MD5 original (sem patch):** `a0ea9788770c39d798cedc965386b530`

## Motivo

O hook original lia o `*-session.tmp` mais novo de `~/.claude/sessions/` sem distinguir interactive vs scheduled-task. Quando um scheduled task (ex: `daily-sync-obsidian`) escrevia um session summary recente, ele virava o "Previous session summary" injetado, sobrescrevendo a conversa real do usuário.

## Patch

Adicionado filter após `findFiles` que descarta sessões cujo conteúdo contém:
- `<scheduled-task name=` (marker literal do summary automatizado)
- `automated run of a scheduled task` (frase usada pelo runner)

```js
const allRecent = findFiles(sessionsDir, '*-session.tmp', { maxAge: 7 });
const recentSessions = allRecent.filter(s => {
  const c = readFile(s.path) || '';
  return !c.includes('<scheduled-task name=') &&
         !c.includes('automated run of a scheduled task');
});
```

## Verificação contínua

Hook `~/.claude/hooks/verify-ecc-patches.sh` (síncrono em SessionStart) checa se o patch ainda está aplicado. Se ECC update sobrescreveu, re-aplica automaticamente OU avisa via log.

## Como re-aplicar manualmente se quebrar

```bash
# 1. Backup do estado atual
cp ~/.claude/plugins/marketplaces/everything-claude-code/scripts/hooks/session-start.js{,.pre-rebuild-patch}

# 2. Aplicar (procurar pela string `const recentSessions = findFiles(sessionsDir`):
# Substituir o bloco original pelo bloco patched acima.

# 3. Mesma coisa no cache:
cp ~/.claude/plugins/cache/everything-claude-code/everything-claude-code/1.8.0/scripts/hooks/session-start.js{,.pre-rebuild-patch}
# ... aplicar mesmo patch
```

## Follow-up

- Considerar PR upstream em `affaan-m/everything-claude-code` com esse filter.
- Migrar long-term pra arquitetura `sessions/{interactive,scheduled}/` (Phase 5 do rebuild) que isola na escrita.

*[Registrado por: DESKTOP — 2026-05-12]*
