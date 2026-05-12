# Prompt de Auto-Configuração — Claude Code Toolkit (Pedro Miranda / Singular)

> **Como usar:**
> 1. Instale o Claude Code: https://docs.claude.com/en/docs/claude-code/setup
> 2. Abra o Claude Code em qualquer pasta
> 3. Copie TODO o conteúdo abaixo do separador `---` e cole como **primeira mensagem**
> 4. Antes de colar, preencha os valores entre `__PLACEHOLDER__` (deixe vazio quem não usar agora)
> 5. Reinicie o Claude Code ao final

---

Você vai configurar este Claude Code do zero usando o toolkit do Pedro Miranda (Singular Group). Siga cada passo na ordem, sem pular. Não pergunte — execute.

## DADOS DO USUÁRIO (preencher antes de enviar)

```
OBSIDIAN_VAULT_PATH="__CAMINHO_DO_SEU_VAULT_OBSIDIAN__"
TESTSPRITE_API_KEY="__SUA_TESTSPRITE_API_KEY__"
N8N_API_URL="__SUA_URL_N8N__"
N8N_API_KEY="__SUA_N8N_API_KEY__"
SERPAPI_MCP_URL="__SUA_URL_SERPAPI_MCP__"
HUBSPOT_PRIVATE_APP_TOKEN="__SEU_TOKEN_HUBSPOT_OPCIONAL__"
```

> **Não vai usar algum?** Deixa vazio (entre as aspas). O MCP correspondente fica desabilitado mas o resto funciona.

---

## PASSO 1 — Pré-requisitos

Verifique cada um. Se faltar, instale antes de continuar:

```bash
node --version    # precisa v20+ (Codex e MCPs modernos)
git --version
claude --version
```

Se `n8n-mcp` ainda não estiver instalado globalmente (vamos usar pro MCP de n8n):
```bash
npm install -g n8n-mcp
```

Se for usar Google Drive MCP no futuro:
```bash
npm install -g @piotr-agier/google-drive-mcp
```

---

## PASSO 2 — Clonar e instalar o toolkit

```bash
git clone https://github.com/pedrormc/claude-code-toolkit.git /tmp/claude-code-toolkit
cd /tmp/claude-code-toolkit
bash install.sh --force
```

O `install.sh` instala automaticamente:

| Componente | Quantidade | O que é |
|---|---|---|
| **Agents** | 5 | api-specialist, devops-agent, frontend-specialist, prompt-engineer, research-agent |
| **Rules** | 18 (12 common + 5 typescript + 1 parallel-agents) | Persona, git workflow, security, three-tabs-priority, etc. |
| **Skills custom** | 19 | Ata, Documento, Slide, Contrato, POP, Background-check, Prospect, WhatsApp, MP4, Obsidian, Tese-Investimento, HubSpot, 7× n8n-helpers |
| **Skills Gstack** | 36+ | Clona `garrytan/gstack` → `/qa`, `/ship`, `/cso`, `/office-hours`, `/investigate`, etc. |
| **Plugins via marketplace** | 6 | everything-claude-code, superpowers, ralph-skills (disabled), ui-ux-pro-max, example-skills, vercel |
| **Hooks** | 5 | session-start/end memory, post-edit validator, save-session-mirror, obsidian-auto-save |
| **Scripts** | 15+ | memory-*, foundation-*, whatsapp-send, obsidian-session, brainstorm-up, ralph/* |
| **Configs** | 4 | settings, settings.local, mcp, auto-promote |
| **Templates** | 2 | daily, projeto |
| **Identity** | 4 | Desktop/Mobile/VPS/README (TRIFORCE) |
| **Triforce** | 5 | desktop/mobile/vps/README + three-tabs-config |
| **Teams** | 1 | default (com inboxes) |
| **Scheduled tasks** | 1 | daily-sync-obsidian |

Se aparecer `[ERR]`, resolva antes de prosseguir.

---

## PASSO 3 — Configurar MCP servers

Depois do `install.sh`, o `~/.claude/mcp.json` vem com placeholders. Sobrescreva com este conteúdo (substituindo as variáveis do bloco DADOS DO USUÁRIO):

```bash
N8N_MCP_PATH=$(npm root -g)/n8n-mcp/dist/mcp/index.js
GDRIVE_MCP_PATH=$(npm root -g)/@piotr-agier/google-drive-mcp/dist/index.js
```

Escreva `~/.claude/mcp.json` com este JSON (preenchendo os valores acima):

```json
{
  "mcpServers": {
    "obsidian": {
      "command": "npx",
      "args": ["@bitbonsai/mcpvault@latest", "${OBSIDIAN_VAULT_PATH}"],
      "disabled": false
    },
    "TestSprite": {
      "command": "npx",
      "args": ["@testsprite/testsprite-mcp@latest"],
      "env": { "API_KEY": "${TESTSPRITE_API_KEY}" },
      "disabled": false
    },
    "n8n": {
      "command": "node",
      "args": ["${N8N_MCP_PATH}"],
      "env": {
        "MCP_MODE": "stdio",
        "N8N_API_URL": "${N8N_API_URL}",
        "N8N_API_KEY": "${N8N_API_KEY}"
      },
      "disabled": false
    },
    "serpapi": {
      "url": "${SERPAPI_MCP_URL}"
    },
    "google-drive": {
      "command": "node",
      "args": ["${GDRIVE_MCP_PATH}"],
      "env": {
        "GOOGLE_DRIVE_OAUTH_CREDENTIALS": "${HOME}/.claude/secrets/gcp-oauth.keys.json",
        "GOOGLE_DRIVE_MCP_TOKEN_PATH": "${HOME}/.claude/secrets/gcp-oauth.token.json"
      },
      "disabled": false
    },
    "hubspot-singular": {
      "command": "npx",
      "args": ["-y", "@hubspot/mcp-server"],
      "env": { "PRIVATE_APP_ACCESS_TOKEN": "${HUBSPOT_PRIVATE_APP_TOKEN}" },
      "disabled": false
    }
  }
}
```

> **Importante:** se algum placeholder ficou vazio (não vai usar agora), comente o bloco inteiro daquele MCP no JSON, OU adicione `"disabled": true`.

**Google Drive MCP:** OAuth é setup separado, longo. Veja [`docs/GOOGLE_DRIVE_MCP_SETUP.md`](docs/GOOGLE_DRIVE_MCP_SETUP.md) (45 min de Cloud Console + auth flow).

---

## PASSO 4 — Identidade (CLAUDE.md)

O toolkit instalou 3 templates em `~/.claude/identity/`. Escolha o seu ambiente e copie:

```bash
# Desktop (default, Windows/macOS/Linux com permissões totais):
cp ~/.claude/identity/desktop.md ~/.claude/CLAUDE.md

# Ou Mobile (Termux/Android, restrito):
cp ~/.claude/identity/mobile.md ~/.claude/CLAUDE.md

# Ou VPS (cloud, automações headless):
cp ~/.claude/identity/vps.md ~/.claude/CLAUDE.md
```

Edite o `~/.claude/CLAUDE.md` resultante e personalize com **seu nome** e ambiente.

---

## PASSO 5 — Validação completa

Rode todos os checks abaixo e me mostre o resultado de cada um:

### 5.1 — Agents (devem existir 5)
```bash
ls ~/.claude/agents/
```
Esperado: `api-specialist.md`, `devops-agent.md`, `frontend-specialist.md`, `prompt-engineer.md`, `research-agent.md`

### 5.2 — Rules (devem existir 18)
```bash
ls ~/.claude/rules/common/    # 12
ls ~/.claude/rules/typescript/  # 5
ls ~/.claude/rules/parallel-agents.md  # 1
```

### 5.3 — Skills custom (devem existir 19) + Gstack
```bash
ls ~/.claude/skills/ | grep -E "^(ata|documento|slide|contrato|pop|backgroundcheck|prospect|whatsapp-evolution|mp4|obsidian|tese-investimento|hubspot-mcp-expert|n8n-)" | wc -l
# Esperado: ~19

ls ~/.claude/skills/gstack 2>/dev/null && echo "Gstack OK" || echo "Gstack faltou — clone manual: git clone https://github.com/garrytan/gstack.git ~/.claude/skills/gstack"
```

### 5.4 — Hooks (devem existir 5)
```bash
ls ~/.claude/hooks/*.sh
```
Esperado: `session-start-memory-loader.sh`, `session-end-memory-writer.sh`, `post-edit-memory-validator.sh`, `save-session-vault-mirror.sh`, `obsidian-auto-save.sh`

### 5.5 — Scripts (15+)
```bash
ls ~/.claude/scripts/
```
Esperado: `claude-notify.js`, `toast-notify.js`, `whatsapp-send.js`, `obsidian-session-format.js`, `obsidian-session-scan.js`, `memory-*.sh` (4), `foundation-*.sh` (3), `test-i4-fake-data.sh`, `brainstorm-up.ps1`, `rotate-mcp-key.ps1`, `ralph/`

### 5.6 — Configs
```bash
cat ~/.claude/settings.json | head -3
cat ~/.claude/settings.local.json | head -3
cat ~/.claude/mcp.json | head -3
ls ~/.claude/config/auto-promote.yaml
```
Todos devem existir e ter conteúdo válido (sem `__PLACEHOLDER__` restante no mcp.json).

### 5.7 — Statusline + templates + identity + triforce
```bash
ls ~/.claude/statusline.sh
ls ~/.claude/templates/  # template-daily.md, template-projeto.md
ls ~/.claude/identity/   # desktop.md, mobile.md, vps.md, README.md
ls ~/.claude/triforce/   # desktop.md, mobile.md, vps.md, three-tabs-config.md, README.md
ls ~/.claude/CLAUDE.md   # criado no Passo 4
```

### 5.8 — Plugins (devem existir 6)
```bash
claude plugins list
```
Esperado: `everything-claude-code`, `superpowers`, `ralph-skills` (pode estar disabled), `ui-ux-pro-max`, `example-skills`, `vercel`

### 5.9 — Teams + scheduled tasks
```bash
ls ~/.claude/teams/default/
ls ~/.claude/scheduled-tasks/
```

### 5.10 — MCP sem placeholders
```bash
grep -c '__' ~/.claude/mcp.json
```
Esperado: `0`

---

## PASSO 6 — Limpeza

```bash
rm -rf /tmp/claude-code-toolkit
```

---

## PASSO 7 — Resumo final

Depois de tudo, mostre um resumo no formato:

```
SETUP COMPLETO
━━━━━━━━━━━━━━━━━━━━━━━━━━━
Agents:     X/5
Rules:      X/18
Skills:     X/19 custom + Gstack (Y/36)
Plugins:    X/6
Hooks:      X/5
Scripts:    X/15
Statusline: OK/FALHA
MCP:        OK/FALHA (0 placeholders)
Templates:  X/2
Identity:   X/4
Triforce:   X/5
Teams:      X
Tasks:      X
CLAUDE.md:  OK/FALHA
━━━━━━━━━━━━━━━━━━━━━━━━━━━
Erros: [lista ou "nenhum"]
```

Se houver erro, tente resolver automaticamente. Só pergunte se travar mesmo.

**Reinicie o Claude Code ao final** para aplicar tudo (especialmente hooks e plugins).

---

## Skills disponíveis (catálogo rápido)

Pasta no GitHub: **https://github.com/pedrormc/claude-code-toolkit/tree/master/skills**

| Slug | O que faz |
|---|---|
| `/ata` | Transforma notas de reunião em .docx Singular |
| `/documento` | Documento formal genérico em .docx |
| `/slide` | Apresentação HTML scroll-snap + .pptx opcional |
| `/contrato` | Gera NDA/MOU/Prestação/Embaixador em .docx |
| `/pop` | Procedimento Operacional Padrão em .docx |
| `/backgroundcheck` | Due diligence reputacional de PF |
| `/prospect` | Prospecção comercial Asa Norte |
| `/tese-investimento` | Estrutura tese + personas críticas |
| `/whatsapp-evolution` | Envia mensagens via Evolution API |
| `/mp4` | Converte vídeo MP4 → MP3 (ffmpeg) |
| `/obsidian` | Salva recap da sessão no vault Obsidian |
| `/hubspot-mcp-expert` | Guia HubSpot MCP (CRM ops) |
| `/n8n-code-javascript` | JS no Code node do n8n |
| `/n8n-code-python` | Python no Code node do n8n |
| `/n8n-expression-syntax` | Sintaxe `{{ }}` do n8n |
| `/n8n-mcp-tools-expert` | Tools do n8n-mcp |
| `/n8n-node-configuration` | Config por operation |
| `/n8n-validation-expert` | Validar workflows n8n |
| `/n8n-workflow-patterns` | Padrões de workflow |

Cada skill é **uma pasta** em `skills/<nome>/` com `SKILL.md` (instruções), scripts, templates e exemplos.

## Plugins que ficam disponíveis após install

| Plugin | Source | Slash commands principais |
|---|---|---|
| **everything-claude-code** | affaan-m/everything-claude-code | `/plan`, `/tdd`, `/learn-eval`, `/resume-session`, `/skill-create` |
| **superpowers** | obra/superpowers-marketplace | `/brainstorming`, `/writing-plans`, `/test-driven-development`, `/code-reviewer` |
| **ui-ux-pro-max** | nextlevelbuilder/ui-ux-pro-max-skill | `/ui-ux-pro-max` (50+ design styles) |
| **example-skills** | anthropics/skills | `/docx`, `/pdf`, `/pptx`, `/xlsx`, `/canvas-design` |
| **vercel** | anthropics/claude-plugins-official | `/vercel:deploy`, `/vercel:env`, `/vercel:bootstrap` |
| **gstack** (não-marketplace) | garrytan/gstack | `/qa`, `/ship`, `/cso`, `/office-hours`, `/investigate`, `/retro` |

---

*[Toolkit: github.com/pedrormc/claude-code-toolkit]*
*[Mantenedor: Pedro Roberto (pedrormc) — CTO @ Singular Group]*
*[Última atualização: 2026-05-11]*
