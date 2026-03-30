# Prompt de Auto-Configuracao — Claude Code Toolkit

> **Como usar:** Copie todo o conteudo abaixo do separador `---` e cole como primeira mensagem em um Claude Code novo.
> Antes de colar, preencha os valores entre `__PLACEHOLDER__` com seus dados reais.

---

Voce vai configurar este Claude Code do zero usando meu toolkit pessoal. Siga cada passo na ordem, sem pular nenhum. Nao pergunte — execute.

## DADOS DO USUARIO (preencher antes de enviar)

```
OBSIDIAN_VAULT_PATH="__CAMINHO_DO_SEU_VAULT_OBSIDIAN__"
TESTSPRITE_API_KEY="__SUA_TESTSPRITE_API_KEY__"
N8N_API_URL="__SUA_URL_N8N__"
N8N_API_KEY="__SUA_N8N_API_KEY__"
```

## PASSO 1 — Pre-requisitos

Verifique se estao instalados (rode cada comando). Se algum faltar, instale antes de continuar:

```bash
node --version    # precisa v18+
git --version
claude --version
```

Se `n8n-mcp` nao estiver instalado globalmente:
```bash
npm install -g n8n-mcp
```

## PASSO 2 — Clonar e instalar o toolkit

```bash
git clone https://github.com/pedrormc/claude-code-toolkit.git /tmp/claude-code-toolkit
cd /tmp/claude-code-toolkit
bash install.sh --force
```

O script instala: 5 agents, 16 rules, 8 skills, scripts de notificacao, statusline, templates, teams, scheduled tasks e configs.

Verifique a saida. Se houver erros (`[ERR]`), resolva antes de continuar.

## PASSO 3 — Configurar MCP servers com os dados reais

Depois que o `install.sh` rodar, o `~/.claude/mcp.json` vai ter placeholders. Substitua pelo conteudo real.

Escreva o arquivo `~/.claude/mcp.json` com este conteudo exato (substituindo as variaveis pelos valores fornecidos acima no bloco DADOS DO USUARIO):

```json
{
  "mcpServers": {
    "obsidian": {
      "command": "npx",
      "args": [
        "@bitbonsai/mcpvault@latest",
        "${OBSIDIAN_VAULT_PATH}"
      ],
      "disabled": false
    },
    "TestSprite": {
      "command": "npx",
      "args": [
        "@testsprite/testsprite-mcp@latest"
      ],
      "env": {
        "API_KEY": "${TESTSPRITE_API_KEY}"
      },
      "disabled": false
    },
    "n8n": {
      "command": "node",
      "args": [
        "${N8N_MCP_PATH}"
      ],
      "env": {
        "MCP_MODE": "stdio",
        "N8N_API_URL": "${N8N_API_URL}",
        "N8N_API_KEY": "${N8N_API_KEY}"
      },
      "disabled": false
    }
  }
}
```

Para o `N8N_MCP_PATH`, descubra o caminho real rodando:
```bash
npm root -g
```
E concatene com `/n8n-mcp/dist/mcp/index.js`. Exemplo: se `npm root -g` retorna `/home/user/.npm-global/lib/node_modules`, o path sera `/home/user/.npm-global/lib/node_modules/n8n-mcp/dist/mcp/index.js`.

## PASSO 4 — Instalar os 4 plugins

Rode cada um. Se algum ja estiver instalado, tudo bem:

```bash
claude plugins install everything-claude-code --marketplace everything-claude-code
claude plugins install superpowers --marketplace superpowers-marketplace
claude plugins install ralph-skills --marketplace ralph-marketplace
claude plugins install ui-ux-pro-max --marketplace ui-ux-pro-max-skill
```

## PASSO 5 — Validacao completa

Rode os seguintes checks e me mostre o resultado de cada um:

### 5.1 — Agents (devem existir 5)
```bash
ls -la ~/.claude/agents/
```
Esperado: `api-specialist.md`, `devops-agent.md`, `frontend-specialist.md`, `prompt-engineer.md`, `research-agent.md`

### 5.2 — Rules (devem existir 16)
```bash
ls ~/.claude/rules/common/
ls ~/.claude/rules/typescript/
ls ~/.claude/rules/parallel-agents.md
```
Esperado: 10 em common, 5 em typescript, 1 parallel-agents

### 5.3 — Skills (devem existir 8 + learned/)
```bash
ls ~/.claude/skills/
```
Esperado: `hubspot-mcp-expert`, `n8n-code-javascript`, `n8n-code-python`, `n8n-expression-syntax`, `n8n-mcp-tools-expert`, `n8n-node-configuration`, `n8n-validation-expert`, `n8n-workflow-patterns`, `learned`

### 5.4 — Scripts
```bash
ls ~/.claude/scripts/
ls ~/.claude/scripts/ralph/
```
Esperado: `claude-notify.js`, `toast-notify.js`, pasta `ralph/`

### 5.5 — Configs
```bash
cat ~/.claude/settings.json | head -5
cat ~/.claude/settings.local.json | head -5
cat ~/.claude/mcp.json | head -5
```
Todos devem existir e ter conteudo valido (nao placeholders).

### 5.6 — Statusline e templates
```bash
ls ~/.claude/statusline.sh
ls ~/.claude/templates/
```
Esperado: `statusline.sh` existe, `templates/` tem `template-daily.md` e `template-projeto.md`

### 5.7 — Plugins instalados
```bash
claude plugins list
```
Esperado: `everything-claude-code`, `superpowers`, `ralph-skills`, `ui-ux-pro-max`

### 5.8 — MCP sem placeholders
```bash
grep -c "YOUR_" ~/.claude/mcp.json
```
Esperado: `0` (nenhum placeholder restante)

## PASSO 6 — Limpeza

```bash
rm -rf /tmp/claude-code-toolkit
```

## PASSO 7 — Resumo

Depois de tudo, me mostre um resumo no formato:

```
SETUP COMPLETO
━━━━━━━━━━━━━━━━━━━━━━━━━━━
Agents:     X/5
Rules:      X/16
Skills:     X/8
Plugins:    X/4
Scripts:    OK/FALHA
Statusline: OK/FALHA
MCP:        OK/FALHA (0 placeholders)
Templates:  X/2
━━━━━━━━━━━━━━━━━━━━━━━━━━━
Erros: [lista ou "nenhum"]
```

Se houver qualquer erro, tente resolver automaticamente. So pergunte se nao conseguir resolver sozinho.

Reinicie o Claude Code ao final para aplicar tudo.
