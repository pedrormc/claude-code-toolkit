# Prompt de Auto-Configuracao — Claude Code Toolkit (Pedro Miranda / Singular)

> **Como usar:**
> 1. Instale o Claude Code: https://docs.claude.com/en/docs/claude-code/setup
> 2. Abra o Claude Code em qualquer pasta
> 3. Copie TODO o conteudo abaixo do separador `---` e cole como **primeira mensagem**
> 4. Antes de colar, preencha os valores entre `__PLACEHOLDER__` (deixe vazio quem nao usar agora)
> 5. Reinicie o Claude Code ao final

---

Voce vai configurar este Claude Code do zero usando o toolkit do Pedro Miranda (Singular Group). Siga cada passo na ordem, sem pular. Nao pergunte — execute.

## DADOS DO USUARIO (preencher antes de enviar)

```
OBSIDIAN_VAULT_PATH="__CAMINHO_DO_SEU_VAULT_OBSIDIAN__"
TESTSPRITE_API_KEY="__SUA_TESTSPRITE_API_KEY__"
N8N_API_URL="__SUA_URL_N8N__"
N8N_API_KEY="__SUA_N8N_API_KEY__"
SERPAPI_MCP_URL="__SUA_URL_SERPAPI_MCP__"
HUBSPOT_PRIVATE_APP_TOKEN="__SEU_TOKEN_HUBSPOT_OPCIONAL__"
QDRANT_URL="__URL_DO_SEU_QDRANT_OPCIONAL__"
OPENAI_API_KEY="__SUA_OPENAI_API_KEY_OPCIONAL__"
```

> **Nao vai usar algum?** Deixa vazio (entre as aspas). O MCP/servico correspondente fica desabilitado mas o resto funciona.

---

## PASSO 1 — Pre-requisitos

Verifique cada um. Se faltar, instale antes de continuar:

```bash
node --version    # precisa v20+ (MCPs modernos exigem)
git --version
gh --version      # GitHub CLI (pra plugins e push)
claude --version  # Claude Code CLI
python3 --version # precisa 3.10+ (skills de doc e Singular_Memory)
```

Dependencias Python (skills de documentos e Singular_Memory):
```bash
pip install python-docx python-pptx reportlab Pillow qdrant-client openai fastembed
```

Se `n8n-mcp` ainda nao estiver instalado globalmente:
```bash
npm install -g n8n-mcp
```

Se for usar Google Drive MCP:
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

| Componente | Qtd | O que e |
|---|---|---|
| **Agents** | 5 | api-specialist, devops-agent, frontend-specialist, prompt-engineer, research-agent |
| **Rules** | 20 | 12 common + 2 core (identity, task-orchestration) + 5 typescript + 1 parallel-agents |
| **Skills custom** | 21 | Ata, Documento, Slide, PDF, POP, Reuniao, Contrato, Backgroundcheck, Prospect, Tese-investimento, WhatsApp, MP4, Obsidian, HubSpot, 7x n8n-helpers |
| **Skills Gstack** | 36+ | Clona `garrytan/gstack` → `/qa`, `/ship`, `/cso`, `/office-hours`, `/investigate`, etc. |
| **Plugins** | 6 | everything-claude-code, superpowers, ralph-skills, ui-ux-pro-max, example-skills, vercel |
| **Hooks** | 6 | session-start memory loader, verify-ecc-patches, session-end memory writer, obsidian-auto-save, post-edit validator, save-session-mirror |
| **Scripts** | 24 | memory-* (4), memory/ Python (5), foundation-* (3), audit-* (2), obsidian-* (2), claude-notify, whatsapp-send, brainstorm-up, rotate-mcp-key, sync-triforce, ralph/* (3) |
| **Configs** | 4 | settings.json, settings.local.json, mcp.json, auto-promote.yaml |
| **Templates** | 2 | daily note, projeto note (Obsidian) |
| **Identity** | 4 | Desktop/Mobile/VPS/README (perfis TRIFORCE) |
| **Triforce** | 5 | desktop/mobile/vps/README + three-tabs-config |
| **Teams** | 1 | default (com inbox spec-reviewer) |
| **Scheduled tasks** | 1 | daily-sync-obsidian |

Se aparecer `[ERR]`, resolva antes de prosseguir.

### O que o settings.json configura automaticamente

| Config | Valor | Por que |
|---|---|---|
| Effort level | `xhigh` | Raciocinio profundo Opus 4.7 |
| Autocompact | 75% | Context window otimizado |
| Permissions | `auto` + `skipAutoPermissionPrompt` | Master persona — acoes sem prompt |
| Agent Teams | habilitado | Comunicacao entre agents |
| Skill overrides | 48 entries `"off"` | Silencia stacks fora do dominio (Go/Swift/Kotlin/Perl/Java/C++/Django/logistics/supply chain) — economia ~5K tokens/turn |
| Voice | hold mode | Input de voz por push-to-talk |
| Theme | light | Tema claro |
| Auto-updates | `latest` channel | Sempre na ultima versao |
| ECC Hook Profile | `strict` | Hooks do plugin ECC no modo rigoroso |

---

## PASSO 3 — Configurar MCP servers

Depois do `install.sh`, o `~/.claude/mcp.json` vem com placeholders. Sobrescreva com este conteudo (substituindo as variaveis do bloco DADOS DO USUARIO):

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

> **Importante:** se algum placeholder ficou vazio (nao vai usar agora), comente o bloco inteiro daquele MCP no JSON, OU adicione `"disabled": true`.

**Google Drive MCP:** OAuth e setup separado, longo. Veja [`docs/GOOGLE_DRIVE_MCP_SETUP.md`](docs/GOOGLE_DRIVE_MCP_SETUP.md) (45 min de Cloud Console + auth flow).

### Cloud connectors (conectar manualmente no Claude Code)

Alem dos MCPs locais acima, conecte estes na UI do Claude Code (Settings > MCP > Cloud):

| Connector | O que faz |
|---|---|
| **Excalidraw** | Diagramas hand-drawn style |
| **Gmail** | Buscar, ler threads, criar drafts, labels |
| **Google Calendar** | Criar eventos, encontrar horarios, listar calendarios |
| **Google Drive** | Buscar e ler Google Docs/Sheets/Slides diretamente |
| **HubSpot** | MCP oficial Anthropic — CRM objects, search, manage |

---

## PASSO 4 — Identidade (CLAUDE.md)

O toolkit instalou 3 templates em `~/.claude/identity/`. Escolha o seu ambiente e copie:

```bash
# Desktop (default, Windows/macOS/Linux com permissoes totais):
cp ~/.claude/identity/desktop.md ~/.claude/CLAUDE.md

# Ou Mobile (Termux/Android, restrito):
cp ~/.claude/identity/mobile.md ~/.claude/CLAUDE.md

# Ou VPS (cloud, automacoes headless):
cp ~/.claude/identity/vps.md ~/.claude/CLAUDE.md
```

Edite o `~/.claude/CLAUDE.md` resultante e personalize com **seu nome** e ambiente.

### Regras Soberanas (ja incluidas nas rules)

O toolkit inclui 3 regras soberanas que governam o comportamento do Claude:

| # | Nome | O que faz | Arquivo |
|---|---|---|---|
| 1 | **3 Abas Master** | Todo input categorizado: plano (99999) > singular (100) > skip (101) | `rules/core/identity.md` |
| 2 | **Task Orchestration** | Toda task classificada + dispatch automatico de agents+skills | `rules/core/task-orchestration.md` |
| 3 | **Catalogacao Singular** | Recall/ingest automatico no Qdrant Singular_Memory | `rules/core/identity.md` |

Se nao for Singular Group, pode remover ou adaptar os arquivos em `rules/core/`.

---

## PASSO 5 — Singular_Memory (opcional)

Se for usar o sistema de memoria permanente da Singular (Qdrant):

```bash
# 1. Verificar que os scripts existem
ls ~/.claude/scripts/memory/*.py
# Esperado: __init__.py, add_doc.py, consolidate_jsonl.py, create_collection.py, seed_from_jsonl.py

# 2. Criar a collection (precisa do Qdrant rodando)
python3 ~/.claude/scripts/memory/create_collection.py \
  --url "${QDRANT_URL}" \
  --collection "Singular_Memory"

# 3. Seed inicial (opcional — se tiver dados pre-processados)
python3 ~/.claude/scripts/memory/seed_from_jsonl.py \
  --url "${QDRANT_URL}" \
  --input "seus-dados.jsonl" \
  --collection "Singular_Memory"
```

Documentacao completa: [`docs/SINGULAR_MEMORY.md`](docs/SINGULAR_MEMORY.md)

> Se nao for usar Qdrant, pule este passo. As skills funcionam sem ele — so perde o recall/ingest automatico pra contexto Singular.

---

## PASSO 6 — Validacao completa

Rode todos os checks abaixo e me mostre o resultado de cada um:

### 6.1 — Agents (devem existir 5)
```bash
ls ~/.claude/agents/
```
Esperado: `api-specialist.md`, `devops-agent.md`, `frontend-specialist.md`, `prompt-engineer.md`, `research-agent.md`

### 6.2 — Rules (devem existir 20)
```bash
echo "Common:"; ls ~/.claude/rules/common/ | wc -l      # 12
echo "Core:"; ls ~/.claude/rules/core/ | wc -l           # 2
echo "TypeScript:"; ls ~/.claude/rules/typescript/ | wc -l # 5
echo "Root:"; ls ~/.claude/rules/parallel-agents.md       # 1
```

### 6.3 — Skills custom (devem existir 21+)
```bash
ls -d ~/.claude/skills/*/ | wc -l
ls -d ~/.claude/skills/*/
```
Skills obrigatorias: `ata`, `backgroundcheck`, `contrato`, `documento`, `hubspot-mcp-expert`, `mp4`, `n8n-code-javascript`, `n8n-code-python`, `n8n-expression-syntax`, `n8n-mcp-tools-expert`, `n8n-node-configuration`, `n8n-validation-expert`, `n8n-workflow-patterns`, `obsidian`, `pdf`, `pop`, `prospect`, `reuniao`, `slide`, `tese-investimento`, `whatsapp-evolution`

Gstack (clone separado):
```bash
ls ~/.claude/skills/gstack 2>/dev/null && echo "Gstack OK" || echo "Gstack faltou — clone manual: git clone https://github.com/garrytan/gstack.git ~/.claude/skills/gstack"
```

### 6.4 — Hooks (devem existir 6)
```bash
ls ~/.claude/hooks/*.sh
```
Esperado: `obsidian-auto-save.sh`, `post-edit-memory-validator.sh`, `save-session-vault-mirror.sh`, `session-end-memory-writer.sh`, `session-start-memory-loader.sh`, `verify-ecc-patches.sh`

### 6.5 — Scripts (24 arquivos)
```bash
find ~/.claude/scripts -type f ! -path '*__pycache__*' | sort
```
Esperado:
- `audit-hooks.sh`, `audit-sessions.sh` — auditoria
- `brainstorm-up.ps1`, `rotate-mcp-key.ps1` — utilidades PowerShell
- `claude-notify.js` — notificacoes
- `foundation-smoke.sh`, `foundation-uninstall.sh`, `foundation-validate.sh` — Foundation v1
- `memory/__init__.py`, `memory/add_doc.py`, `memory/consolidate_jsonl.py`, `memory/create_collection.py`, `memory/seed_from_jsonl.py` — Singular_Memory (Qdrant)
- `memory-auto-promote.sh`, `memory-index-rebuild.sh`, `memory-revert.sh`, `memory-update.sh` — memoria auto
- `obsidian-session-format.js`, `obsidian-session-scan.js` — Obsidian sync
- `ralph/CLAUDE.md`, `ralph/prd.json.example`, `ralph/ralph.sh` — Ralph agent loop
- `sync-triforce.sh` — sync Desktop/Mobile/VPS
- `whatsapp-send.js` — WhatsApp via Evolution API

### 6.6 — Configs
```bash
cat ~/.claude/settings.json | python3 -c "import json,sys; d=json.load(sys.stdin); print('effortLevel:', d.get('effortLevel')); print('plugins:', len(d.get('enabledPlugins',{}))); print('skillOverrides:', len(d.get('skillOverrides',{})))"
cat ~/.claude/mcp.json | head -3
ls ~/.claude/settings.local.json
```
Esperado: `effortLevel: xhigh`, `plugins: 6`, `skillOverrides: 48`, mcp.json sem `__PLACEHOLDER__`

### 6.7 — Statusline + templates + identity + triforce
```bash
ls ~/.claude/statusline.sh
ls ~/.claude/templates/        # template-daily.md, template-projeto.md
ls ~/.claude/identity/          # desktop.md, mobile.md, vps.md, README.md
ls ~/.claude/triforce/          # desktop.md, mobile.md, vps.md, three-tabs-config.md, README.md
ls ~/.claude/CLAUDE.md          # criado no Passo 4
```

### 6.8 — Plugins (devem existir 6)
```bash
claude plugins list
```
Esperado: `everything-claude-code`, `superpowers`, `ralph-skills`, `ui-ux-pro-max`, `example-skills`, `vercel`

### 6.9 — Teams + scheduled tasks
```bash
ls ~/.claude/teams/default/
ls ~/.claude/scheduled-tasks/
```

### 6.10 — MCP sem placeholders
```bash
grep -c '__' ~/.claude/mcp.json
```
Esperado: `0`

### 6.11 — Audit de saude (rodavel a qualquer momento)
```bash
bash ~/.claude/scripts/audit-hooks.sh
```
Esperado: 13 smoke-tests passando, exit 0.

---

## PASSO 7 — Limpeza

```bash
rm -rf /tmp/claude-code-toolkit
```

---

## PASSO 8 — Resumo final

Depois de tudo, mostre um resumo no formato:

```
SETUP COMPLETO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Agents:         X/5
Rules:          X/20 (12 common + 2 core + 5 ts + 1 root)
Skills custom:  X/21
Skills Gstack:  X/36+
Plugins:        X/6
Hooks:          X/6
Scripts:        X/24
Configs:        OK/FALHA (effortLevel, plugins, overrides)
Statusline:     OK/FALHA
MCP:            OK/FALHA (0 placeholders)
Templates:      X/2
Identity:       X/4
Triforce:       X/5
Teams:          X/1
Tasks:          X/1
CLAUDE.md:      OK/FALHA
Audit:          OK/FALHA (13 smoke-tests)
Singular_Memory: OK/SKIP (Qdrant)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Erros: [lista ou "nenhum"]
```

Se houver erro, tente resolver automaticamente. So pergunte se travar mesmo.

**Reinicie o Claude Code ao final** para aplicar tudo (especialmente hooks e plugins).

---

## Catalogo de skills (referencia rapida)

Pasta no GitHub: **https://github.com/pedrormc/claude-code-toolkit/tree/master/skills**
Catalogo completo: **[`docs/SKILLS_CATALOG.md`](docs/SKILLS_CATALOG.md)**

### Documentos Singular (.docx / .pdf)

| Slug | O que faz |
|---|---|
| `/ata` | Transforma notas de reuniao em Ata .docx Singular |
| `/documento` | Documento formal generico em .docx (briefing, memo, RFC, plano) |
| `/pop` | Procedimento Operacional Padrao em .docx |
| `/slide` | Apresentacao HTML scroll-snap + .pptx opcional |
| `/pdf` | Documento PDF final com identidade Singular (reportlab) |
| `/reuniao` | Suite completa pos-reuniao: orquestra /ata + /documento + /pop numa pasta Drive |

### Operacoes comerciais / inteligencia

| Slug | O que faz |
|---|---|
| `/contrato` | Gera NDA/MOU/Prestacao/Representacao/Embaixador em .docx (c/ Qdrant Nexo_Adv) |
| `/backgroundcheck` | Due diligence reputacional de PF (processos, midia, socios, sancoes) |
| `/prospect` | Prospeccao comercial porta-a-porta Asa Norte |
| `/tese-investimento` | Estrutura tese de investimento + 5 personas criticas |

### Comunicacao & utilidades

| Slug | O que faz |
|---|---|
| `/whatsapp-evolution` | Envia texto/docs/imagem/audio/video via WhatsApp (Evolution API) |
| `/mp4` | Converte video MP4 → MP3 (ffmpeg) |
| `/obsidian` | Salva recap da sessao no vault Obsidian |

### n8n workflow automation (7 skills)

| Slug | O que faz |
|---|---|
| `/n8n-code-javascript` | JS no Code node — $input/$json, HTTP, DateTime |
| `/n8n-code-python` | Python no Code node — _input/_json, stdlib |
| `/n8n-expression-syntax` | Sintaxe `{{ }}`, erros comuns |
| `/n8n-mcp-tools-expert` | Tools do n8n-mcp (search, validate, templates) |
| `/n8n-node-configuration` | Config por operation, deps, campos obrigatorios |
| `/n8n-validation-expert` | Validar workflows, false positives |
| `/n8n-workflow-patterns` | Padroes: webhook, HTTP API, DB, AI agent, scheduled |

### HubSpot CRM

| Slug | O que faz |
|---|---|
| `/hubspot-mcp-expert` | Guia expert HubSpot MCP — contacts, deals, engagements, associations |

Cada skill e **uma pasta** em `skills/<nome>/` com `SKILL.md` (instrucoes), scripts, templates e exemplos.

---

## Plugins que ficam disponiveis apos install

| Plugin | Source | Slash commands principais |
|---|---|---|
| **everything-claude-code** | [affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code) | `/plan`, `/tdd`, `/learn-eval`, `/resume-session`, `/skill-create`, `/claw` |
| **superpowers** | [obra/superpowers-marketplace](https://github.com/obra/superpowers-marketplace) | `/brainstorming`, `/writing-plans`, `/test-driven-development`, `/systematic-debugging`, `/code-review` |
| **ralph-skills** | [snarktank/ralph](https://github.com/snarktank/ralph) | `/ralph`, `/prd` |
| **ui-ux-pro-max** | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | `/ui-ux-pro-max` (50+ design styles, 161 paletas, 57 fonts, 99 UX guidelines) |
| **example-skills** | [anthropics/skills](https://github.com/anthropics/skills) | `/docx`, `/pdf`, `/pptx`, `/xlsx`, `/canvas-design`, `/claude-api`, `/mcp-builder` |
| **vercel** | [claude-plugins-official](https://github.com/anthropics/claude-code-plugins) | `/vercel:deploy`, `/vercel:env`, `/vercel:bootstrap`, `/vercel:ai-sdk`, `/vercel:nextjs` |
| **gstack** (clone, nao-marketplace) | [garrytan/gstack](https://github.com/garrytan/gstack) | `/qa`, `/ship`, `/cso`, `/office-hours`, `/investigate`, `/retro`, `/health`, `/design-*`, `/plan-*` |

### Skill overrides (stacks silenciados)

O `settings.json` silencia **48 skills** de stacks fora do dominio pra economizar ~5K tokens/turn:
- **Off:** C++, Perl, Swift, Kotlin, Android, Go, Java, SpringBoot, Django, ClickHouse, supply chain, logistics, visa, plankton, nutrient, investor-outreach, etc.
- **User-invocable-only:** Python testing/patterns/review (disponivel via `/python-review` mas nao carrega automaticamente)

Pra ver a lista completa: `jq '.skillOverrides' ~/.claude/settings.json`

---

## Agents customizados (5)

Todos em PT-BR, modelo Opus 4.7. Definidos em `agents/`:

| Agent | Foco | Tools | Quando usar |
|---|---|---|---|
| `api-specialist` | Express.js, REST API, PostgreSQL, JWT | Read, Write, Edit, Bash, Grep, Glob | Backend: rotas, middleware, queries |
| `devops-agent` | Vercel, GitHub Actions, Docker, env | Read, Write, Edit, Bash, Grep, Glob | Deploy, CI/CD, Docker, infra |
| `frontend-specialist` | React 19, TS strict, Tailwind v4, a11y | Read, Write, Edit, Bash, Grep, Glob | UI: componentes, performance, hooks |
| `prompt-engineer` | CLAUDE.md, agents, skills, rules, hooks | Read, Write, Edit, Grep, Glob | Meta: otimizar Claude Code config |
| `research-agent` | Avaliar libs, prior art, comparar tech | Read, Bash, Grep, Glob, WebFetch, WebSearch | Antes de implementar: pesquisar opcoes |

---

## Hooks lifecycle

| Evento | Hook | O que faz | Async | Timeout |
|---|---|---|---|---|
| **SessionStart** | `verify-ecc-patches.sh` | Re-aplica patches criticos do ECC se updates sobrescreveram | Nao | 3s |
| **SessionStart** | `session-start-memory-loader.sh` | Carrega vault + auto-memory unificada | Sim | 10s |
| **SessionStart** | `any-buddy apply` | Aplica any-buddy changes | Sim | 30s |
| **Stop** | `session-end-memory-writer.sh` | Atualiza active.md + trigger INDEX rebuild | Sim | 10s |
| **SessionEnd** | `obsidian-auto-save.sh` | Auto-salva sessao no vault Obsidian | Nao | 15s |
| **PostToolUse** (Edit/Write) | `post-edit-memory-validator.sh` | Valida consistencia de edits em memoria | Nao | — |
| **PostToolUse** (Write) | `save-session-vault-mirror.sh` | Espelha saves no vault (idempotente via mtime) | Nao | — |
| **Notification/Permission/TaskCompleted/SubagentStop** | `claude-notify.js` | Toast notification Windows (WinRT + bell) | — | 10s |
| **UserPromptSubmit** | Terminal title | Atualiza titulo do terminal | Nao | 2s |

---

## Scripts de manutencao

```bash
# Health check (13 smoke-tests dos hooks + settings)
bash ~/.claude/scripts/audit-hooks.sh

# Detectar sessions misroteadas
bash ~/.claude/scripts/audit-sessions.sh [--fix]

# Propagar config Desktop → VPS via SSH
bash ~/.claude/scripts/sync-triforce.sh status
bash ~/.claude/scripts/sync-triforce.sh push [--dry-run]

# Rotacionar chave MCP
pwsh ~/.claude/scripts/rotate-mcp-key.ps1

# Memory: atualizar/reverter/rebuild index
bash ~/.claude/scripts/memory-update.sh
bash ~/.claude/scripts/memory-revert.sh
bash ~/.claude/scripts/memory-index-rebuild.sh
```

---

## Troubleshooting

| Problema | Solucao |
|---|---|
| `install.sh` falha no clone Gstack | `git clone https://github.com/garrytan/gstack.git ~/.claude/skills/gstack` manual |
| Plugin nao aparece apos install | Reinicie o Claude Code (`Ctrl+C Ctrl+C` e reabra) |
| Hooks nao executam | Verifique `chmod +x ~/.claude/hooks/*.sh` |
| ECC patches sobrescritos por update | `bash ~/.claude/scripts/verify-ecc-patches.sh` ou `bash ~/.claude/scripts/audit-hooks.sh` |
| SessionStart lento (>10s) | Hooks com `async: true` ja configurados; se persistir, cheque `session-start-memory-loader.sh` |
| `skill not found` apos install | Verifique se a pasta existe em `~/.claude/skills/` e tem `SKILL.md` |
| MCP connection refused | Verifique se o servico (n8n, Qdrant, etc.) esta rodando e a URL/porta estao corretas |
| `__PLACEHOLDER__` no mcp.json | Edite `~/.claude/mcp.json` e substitua todos os placeholders ou adicione `"disabled": true` |
| Python deps faltando | `pip install python-docx python-pptx reportlab Pillow` (skills de doc) |
| Qdrant connection error | Verifique `QDRANT_URL` e se a porta 6333 esta aberta |

---

*[Toolkit: github.com/pedrormc/claude-code-toolkit]*
*[Mantenedor: Pedro Roberto (pedrormc) — CTO @ Singular Group]*
*[Ultima atualizacao: 2026-05-25]*
