# Claude Code Toolkit

Setup completo e tunado do Claude Code para o time de desenvolvimento. Inclui agents customizados, rules, skills, hooks, scripts de notificacao e statusline personalizada.

## Requisitos

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) v2.1+ instalado
- Node.js 18+
- Git + GitHub CLI (`gh`)
- Windows 10/11 (scripts de notificacao usam PowerShell/WinRT)

## Instalacao Rapida

```bash
git clone https://github.com/pedrormc/claude-code-toolkit.git
cd claude-code-toolkit
bash install.sh
```

O script copia tudo para `~/.claude/` e instala os plugins automaticamente.

---

## Raio-X Completo

### Ambiente

| Item | Valor |
|------|-------|
| Claude Code | v2.1.83 |
| Modelo padrao | Opus 4.6 (1M context) |
| Effort level | `high` |
| Autocompact | 50% |
| Agent Teams | habilitado |
| ECC Hook Profile | `strict` |
| Auto updates | `latest` channel |

---

### Plugins (4)

| Plugin | Versao | Repo | Descricao |
|--------|--------|------|-----------|
| **Everything Claude Code** | 1.8.0 | [affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code) | 100+ skills, agents, rules para todas as linguagens. TDD, code review, deployment patterns, continuous learning |
| **Superpowers** | 5.0.2 | [obra/superpowers-marketplace](https://github.com/obra/superpowers-marketplace) | Brainstorming, plan mode, TDD workflow, systematic debugging, parallel agents, code review, git worktrees |
| **Ralph Skills** | 1.0.0 | [snarktank/ralph](https://github.com/snarktank/ralph) | Conversao de PRDs para formato JSON do agente autonomo Ralph. Long-running agent loops |
| **UI/UX Pro Max** | 2.2.1 | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | 50+ estilos, 161 paletas, 57 font pairings, 161 product types, 99 UX guidelines, 25 chart types |

---

### Agents Customizados (5)

Todos em PT-BR, modelo Opus.

#### `api-specialist`
- **Foco:** Express.js, REST API, PostgreSQL, JWT, bcrypt
- **Regras:** Envelope `{ success, data/error }`, queries parametrizadas, SELECT explicito, rate limiting, mensagens PT-BR
- **Quando:** Novas rotas, middleware, validacao, queries, integracao backend

#### `devops-agent`
- **Foco:** Vercel, GitHub Actions, Docker, env management, monitoring
- **Regras:** Nunca expor secrets, validar env vars no startup, health check obrigatorio, rollback strategy
- **Quando:** Deploy, CI/CD workflows, Docker, monitoring, DNS/SSL

#### `frontend-specialist`
- **Foco:** React 19, TypeScript strict, Tailwind CSS v4, acessibilidade, performance
- **Regras:** Tokens `fire-*` do tema, componentes funcionais, estado imutavel, props tipadas
- **Quando:** Novos componentes, refatoracao UI, performance, acessibilidade, hooks customizados

#### `prompt-engineer`
- **Foco:** CLAUDE.md, agents, skills, rules, hooks, context window
- **Regras:** CLAUDE.md < 300 linhas, rules acionaveis, agents sem overlap, skills com triggers claros
- **Quando:** Otimizar configs, criar agents/skills, debugar hooks, resolver conflitos de rules

#### `research-agent`
- **Foco:** Avaliacao de libs, prior art, comparacao de tecnologias
- **Tools:** Read, Bash, Grep, Glob, WebFetch, WebSearch
- **Quando:** Antes de implementar features, avaliar pacotes, comparar tecnologias

---

### Skills Customizados (8)

#### HubSpot
| Skill | Arquivos | Descricao |
|-------|----------|-----------|
| `hubspot-mcp-expert` | SKILL.md, CRM_OPERATIONS.md | Guia expert para HubSpot MCP — contacts, deals, engagements, associations |

#### n8n (Workflow Automation)
| Skill | Arquivos | Descricao |
|-------|----------|-----------|
| `n8n-code-javascript` | 6 arquivos | JavaScript em Code nodes — $input/$json, HTTP requests, DateTime |
| `n8n-code-python` | 6 arquivos | Python em Code nodes — _input/_json, standard library |
| `n8n-expression-syntax` | 4 arquivos | Sintaxe `{{}}`, $json/$node, erros comuns |
| `n8n-mcp-tools-expert` | 5 arquivos | Guia de tools MCP — search, validate, templates, workflows |
| `n8n-node-configuration` | 4 arquivos | Configuracao de nodes, dependencias, campos obrigatorios |
| `n8n-validation-expert` | 4 arquivos | Erros de validacao, false positives, profiles |
| `n8n-workflow-patterns` | 7 arquivos | Padroes: webhook, HTTP API, database, AI agent, scheduled tasks |

---

### MCP Servers (2)

| Server | Pacote | Descricao |
|--------|--------|-----------|
| **n8n** | `n8n-mcp` | Gerenciamento de workflows n8n — criar, editar, validar, testar, executar |
| **TestSprite** | `@testsprite/testsprite-mcp` | Testing automation |

> Configuracao em `config/mcp.json` — substitua os placeholders pelas suas API keys.

---

### Rules (15 arquivos)

#### Globais (`rules/common/`) — 9 arquivos
| Arquivo | Foco |
|---------|------|
| `agents.md` | Orquestracao de agents, quando usar cada um, execucao paralela |
| `coding-style.md` | Imutabilidade, files pequenos, error handling, input validation |
| `development-workflow.md` | Pipeline: research > plan > TDD > code review > commit |
| `git-workflow.md` | Conventional commits, PR workflow |
| `hooks.md` | PreToolUse, PostToolUse, Stop hooks, TodoWrite best practices |
| `patterns.md` | Repository pattern, API response envelope, skeleton projects |
| `performance.md` | Model selection (Haiku/Sonnet/Opus), context window, extended thinking |
| `security.md` | Checklist pre-commit, secret management, security response protocol |
| `testing.md` | 80% coverage minimo, TDD obrigatorio, unit + integration + E2E |

#### TypeScript (`rules/typescript/`) — 5 arquivos
| Arquivo | Foco |
|---------|------|
| `coding-style.md` | Types/interfaces, avoid `any`, React props, Zod validation, no console.log |
| `hooks.md` | Prettier auto-format, tsc check, console.log warning |
| `patterns.md` | ApiResponse<T> envelope, custom hooks, Repository pattern tipado |
| `security.md` | Secret management com env vars, security-reviewer agent |
| `testing.md` | Playwright E2E, e2e-runner agent |

#### Isolamento (`rules/parallel-agents.md`)
- Regras para worktree isolation em agents paralelos
- Quando usar worktree vs. nao usar
- Merge workflow sequencial

---

### Hooks (6 eventos)

| Evento | Acao |
|--------|------|
| `Notification` | Windows toast + terminal bell + WezTerm tab state |
| `Stop` | Toast "Tarefa concluida" + bell + tab state verde |
| `PermissionRequest` | Toast urgente "Aguardando aprovacao" + double bell + tab laranja |
| `TaskCompleted` | Toast com nome da task + bell |
| `SubagentStop` | Toast com nome do agent + bell |
| `UserPromptSubmit` | Terminal title "Trabalhando..." |

#### Como funciona
- `claude-notify.js` — Script principal que gerencia todos os eventos. Detecta o tipo de hook, seta o terminal title, envia Windows toast notification via PowerShell/WinRT, e atualiza o WezTerm tab state via OSC 1337.
- `toast-notify.js` — Fallback simplificado, toast silencioso.

---

### Statusline Customizada

Script bash que mostra em tempo real:
```
Opus 4.6 | meu-projeto | [frontend-specialist] | feature/nova-pagina
░░░░░░░░░░ 23% | 1m 45s | $0.42 | #a1b2c3d4
```

- **Linha 1:** Modelo + projeto + agent ativo + branch
- **Linha 2:** Barra de progresso (contexto) + duracao + custo + session ID
- Cores: verde (<60%), amarelo (60-80%), vermelho (>80%)

---

### Scripts Extras

#### Ralph (`scripts/ralph/`)
- `ralph.sh` — Long-running AI agent loop. Executa Claude Code em modo headless com iteracoes configuraveis.
- `CLAUDE.md` — Instrucoes do agente Ralph
- `prd.json.example` — Exemplo de PRD no formato Ralph

---

## Estrutura do Repositorio

```
claude-code-toolkit/
├── README.md                    # Este arquivo
├── install.sh                   # Script de instalacao automatica
├── statusline.sh                # Statusline customizada
├── agents/                      # 5 agents customizados (PT-BR)
│   ├── api-specialist.md
│   ├── devops-agent.md
│   ├── frontend-specialist.md
│   ├── prompt-engineer.md
│   └── research-agent.md
├── config/                      # Configuracoes (sanitizadas)
│   ├── mcp.json                 # MCP servers (substituir API keys)
│   ├── settings.json            # Settings principal
│   └── settings.local.json      # Permissions locais
├── rules/                       # 15 arquivos de rules
│   ├── common/                  # Rules globais (9)
│   │   ├── agents.md
│   │   ├── coding-style.md
│   │   ├── development-workflow.md
│   │   ├── git-workflow.md
│   │   ├── hooks.md
│   │   ├── patterns.md
│   │   ├── performance.md
│   │   ├── security.md
│   │   └── testing.md
│   ├── typescript/              # Rules TypeScript (5)
│   │   ├── coding-style.md
│   │   ├── hooks.md
│   │   ├── patterns.md
│   │   ├── security.md
│   │   └── testing.md
│   └── parallel-agents.md       # Worktree isolation
├── scripts/                     # Scripts de notificacao e automacao
│   ├── claude-notify.js         # Notificacao principal (toast+bell+wezterm)
│   ├── toast-notify.js          # Toast fallback
│   └── ralph/                   # Ralph agent loop
│       ├── ralph.sh
│       ├── CLAUDE.md
│       └── prd.json.example
└── skills/                      # 8 skills customizados
    ├── hubspot-mcp-expert/
    ├── n8n-code-javascript/
    ├── n8n-code-python/
    ├── n8n-expression-syntax/
    ├── n8n-mcp-tools-expert/
    ├── n8n-node-configuration/
    ├── n8n-validation-expert/
    └── n8n-workflow-patterns/
```

---

## Instalacao Manual

Se preferir instalar manualmente:

### 1. Agents
```bash
cp agents/*.md ~/.claude/agents/
```

### 2. Rules
```bash
cp -r rules/common ~/.claude/rules/
cp -r rules/typescript ~/.claude/rules/
cp rules/parallel-agents.md ~/.claude/rules/
```

### 3. Skills
```bash
cp -r skills/* ~/.claude/skills/
```

### 4. Scripts
```bash
cp scripts/claude-notify.js ~/.claude/scripts/
cp scripts/toast-notify.js ~/.claude/scripts/
cp -r scripts/ralph ~/.claude/scripts/
```

### 5. Statusline
```bash
cp statusline.sh ~/.claude/
chmod +x ~/.claude/statusline.sh
```

### 6. Configs
```bash
# CUIDADO: faca backup antes de sobrescrever
cp ~/.claude/settings.json ~/.claude/settings.json.bak
cp config/settings.json ~/.claude/settings.json
cp config/settings.local.json ~/.claude/settings.local.json
# Edite config/mcp.json com suas API keys, depois:
cp config/mcp.json ~/.claude/mcp.json
```

### 7. Plugins
```bash
# Instale via Claude Code CLI:
claude plugins install everything-claude-code --marketplace everything-claude-code
claude plugins install superpowers --marketplace superpowers-marketplace
claude plugins install ralph-skills --marketplace ralph-marketplace
claude plugins install ui-ux-pro-max --marketplace ui-ux-pro-max-skill
```

---

## Configuracao Pos-Instalacao

### API Keys necessarias

Edite `~/.claude/mcp.json` e substitua:

| Placeholder | Onde obter |
|-------------|------------|
| `YOUR_TESTSPRITE_API_KEY_HERE` | [TestSprite Dashboard](https://testsprite.com) |
| `YOUR_N8N_INSTANCE_URL` | URL da sua instancia n8n |
| `YOUR_N8N_API_KEY_HERE` | n8n Settings > API > Create API Key |
| `PATH_TO_N8N_MCP` | `npm root -g` + `/n8n-mcp` |

### Instalar n8n-mcp globalmente
```bash
npm install -g n8n-mcp
```

---

## Filosofia do Setup

### Modelo de Agents
- **Opus** para agents que precisam de raciocinio profundo (todos os 5 customizados)
- **Haiku 4.5** para agents leves e frequentes (via ECC)
- **Sonnet 4.6** para trabalho principal de desenvolvimento

### Workflow Enforced
1. **Research** — Pesquisar antes de codificar (research-agent)
2. **Plan** — Planejar com planner agent
3. **TDD** — Testes primeiro, depois implementacao
4. **Code Review** — Review automatico pos-codigo
5. **Security** — Checklist pre-commit obrigatorio

### Principios
- Imutabilidade em tudo
- Arquivos pequenos e focados (<800 linhas)
- Error handling explicito
- Input validation com Zod
- 80%+ test coverage
- Conventional commits
- PT-BR em agents e mensagens de erro

---

## Licenca

Uso interno do time. Nao redistribuir sem autorizacao.
