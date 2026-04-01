# Claude Code Toolkit

Setup completo e tunado do Claude Code para o time de desenvolvimento. Inclui agents customizados, rules, skills, hooks, scripts de notificacao, statusline personalizada, teams, scheduled tasks e templates.

> **Parte do ecossistema [TRIFORCE](https://github.com/pedrormc/TRIFORCE)** — metodologia multi-ambiente Claude Code (Desktop/Mobile/VPS). Este repo e a **caixa de ferramentas** que cada ambiente instala. O TRIFORCE documenta **como montar** os ambientes do zero.

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

### Plugins (4) — Onde moram os 255 skills, 64 agents e 141 rules

> **IMPORTANTE:** Os plugins sao a fonte de ~95% dos skills/agents. Sem eles, voce so tem os 5 agents e 8 skills customizados. O `install.sh` instala todos automaticamente, mas se precisar instalar manualmente, siga as instrucoes abaixo.

| Plugin | Marketplace ID | GitHub Repo | O que traz |
|--------|---------------|-------------|------------|
| **Everything Claude Code** | `everything-claude-code` | [affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code) | 217 skills, 17 agents, 125+ rules para 7 linguagens |
| **Superpowers** | `superpowers` | [obra/superpowers-marketplace](https://github.com/obra/superpowers-marketplace) | 14 skills, 1 agent — brainstorming, plan mode, TDD, debugging, parallel agents |
| **Ralph Skills** | `ralph-skills` | [snarktank/ralph](https://github.com/snarktank/ralph) | 2 skills — PRD generator e conversor para formato Ralph |
| **UI/UX Pro Max** | `ui-ux-pro-max` | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | 14 skills — 50+ estilos, 161 paletas, 57 fonts, 99 UX guidelines |

#### Como instalar os plugins manualmente

Cada plugin vem de um **marketplace** (repo GitHub que o Claude Code sabe baixar). Para instalar:

```bash
# 1. Primeiro, registre os marketplaces (o settings.json ja faz isso automaticamente)
#    Se o settings.json nao foi copiado, adicione manualmente em ~/.claude/settings.json:
#    "extraKnownMarketplaces": { ... }

# 2. Instale cada plugin (requer Claude Code logado):
claude plugins install everything-claude-code --marketplace everything-claude-code
claude plugins install superpowers --marketplace superpowers-marketplace
claude plugins install ralph-skills --marketplace ralph-marketplace
claude plugins install ui-ux-pro-max --marketplace ui-ux-pro-max-skill

# 3. Verifique a instalacao:
claude plugins list
```

#### Marketplaces (configurados no settings.json)

Os marketplaces sao repos GitHub que servem como fonte de plugins:

```json
{
  "extraKnownMarketplaces": {
    "everything-claude-code": {
      "source": { "source": "github", "repo": "affaan-m/everything-claude-code" }
    },
    "superpowers-marketplace": {
      "source": { "source": "github", "repo": "obra/superpowers-marketplace" }
    },
    "ralph-marketplace": {
      "source": { "source": "github", "repo": "snarktank/ralph" }
    },
    "ui-ux-pro-max-skill": {
      "source": { "source": "github", "repo": "nextlevelbuilder/ui-ux-pro-max-skill" }
    }
  }
}
```

> Quando voce copia o `settings.json` deste repo, os marketplaces ja ficam registrados. Basta rodar os comandos `claude plugins install` acima.

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

### Skills/Agents dos Plugins (Inventario Completo)

> Quando voce digita `/` no Claude Code, a lista e montada combinando seus skills customizados + todos os skills dos plugins abaixo. Por isso voce ve muito mais que 8 skills.

#### Everything Claude Code (ECC) — 20 skills + 9 agents
| Tipo | Nome | Descricao |
|------|------|-----------|
| skill | `plan` | Criar planos de implementacao |
| skill | `tdd` | Test-driven development workflow |
| skill | `e2e` | E2E testing com Playwright |
| skill | `claw` | NanoClaw REPL |
| skill | `evolve` | Analise e evolucao de instincts |
| skill | `go-build` | Fix Go build errors |
| skill | `go-review` | Go code review |
| skill | `go-test` | Go TDD workflow |
| skill | `gradle-build` | Fix Gradle build errors |
| skill | `learn-eval` | Extrair patterns reutilizaveis |
| skill | `save-session` / `resume-session` | Persistir/retomar sessoes |
| skill | `skill-create` | Gerar SKILL.md a partir de git history |
| skill | `instinct-status` / `export` / `import` / `promote` | Gestao de instincts |
| skill | `projects` | Listar projetos conhecidos |
| skill | `python-review` | Python code review |
| agent | `planner` | Planejamento de implementacao |
| agent | `architect` | Decisoes de arquitetura |
| agent | `tdd-guide` | Guia TDD |
| agent | `code-reviewer` | Code review |
| agent | `security-reviewer` | Analise de seguranca |
| agent | `build-error-resolver` | Fix build errors |
| agent | `e2e-runner` | E2E testing |
| agent | `refactor-cleaner` | Limpeza de dead code |
| agent | `doc-updater` | Atualizacao de docs |

Alem disso, ECC traz **130+ rules** para 7 linguagens (TypeScript, Python, Go, Kotlin, Perl, PHP, Swift) cobrindo coding-style, patterns, security, testing e hooks.

#### Superpowers — 18 skills + 1 agent
| Tipo | Nome | Descricao |
|------|------|-----------|
| skill | `using-superpowers` | Bootstrap de sessao — detecta skills aplicaveis |
| skill | `brainstorming` | Explorar intent e requisitos antes de implementar |
| skill | `writing-plans` | Escrever planos de implementacao |
| skill | `executing-plans` | Executar planos com checkpoints |
| skill | `test-driven-development` | TDD workflow |
| skill | `systematic-debugging` | Debugging estruturado |
| skill | `dispatching-parallel-agents` | Despachar agents em paralelo |
| skill | `subagent-driven-development` | Desenvolvimento com subagents |
| skill | `requesting-code-review` | Solicitar code review |
| skill | `receiving-code-review` | Receber e processar code review |
| skill | `using-git-worktrees` | Isolamento com git worktrees |
| skill | `finishing-a-development-branch` | Finalizar branch (merge/PR/cleanup) |
| skill | `verification-before-completion` | Verificar antes de declarar pronto |
| skill | `writing-skills` | Criar e editar skills |
| skill | `brainstorm` | (deprecated, usa brainstorming) |
| skill | `write-plan` / `execute-plan` | (deprecated, usa writing-plans/executing-plans) |
| agent | `code-reviewer` | Code review com alinhamento ao plano |

#### Ralph — 2 skills
| Tipo | Nome | Descricao |
|------|------|-----------|
| skill | `ralph` | Converter PRD para prd.json (formato Ralph) |
| skill | `prd` | Gerar PRD de feature do zero |

#### UI/UX Pro Max — 1 skill (2 versoes)
| Tipo | Nome | Descricao |
|------|------|-----------|
| skill | `ui-ux-pro-max` | Design intelligence: 50+ estilos, 161 paletas, 57 fonts, 99 UX guidelines |

---

### MCP Servers — Completo (3 locais + 7 cloud)

#### Locais (configurados em `mcp.json`)

Instalados via npm, configurados em `~/.claude/mcp.json`:

| Server | Pacote | Como instalar | Descricao |
|--------|--------|---------------|-----------|
| **Obsidian** | `@bitbonsai/mcpvault` | `npx @bitbonsai/mcpvault@latest PATH_VAULT` | Vault MCP para leitura/escrita de notas Obsidian |
| **n8n** | `n8n-mcp` | `npm install -g n8n-mcp` | Gerenciamento de workflows n8n — criar, editar, validar, testar, executar |
| **TestSprite** | `@testsprite/testsprite-mcp` | `npx @testsprite/testsprite-mcp@latest` | Testing automation |

```bash
# Instalar n8n-mcp globalmente:
npm install -g n8n-mcp

# Obsidian e TestSprite usam npx (nao precisam instalar previamente)
# Basta configurar as API keys no mcp.json
```

#### User MCP Connectors (conectados via Claude Code)
| Connector | Status | Descricao |
|-----------|--------|-----------|
| **HubSpot** | connected | CRM — contacts, companies, deals, engagements, batch operations, workflows |
| **n8n-mcp** | connected | Duplica o local para acesso via Claude Code UI |

#### Cloud Connectors (claudeai — gerenciados via OAuth)
| Connector | Status | Descricao |
|-----------|--------|-----------|
| **Excalidraw** | connected | Criar diagramas hand-drawn style |
| **Gmail** | connected | Buscar, ler, criar drafts, listar labels |
| **Google Calendar** | connected | Criar eventos, encontrar horarios, listar calendarios |
| **Google Drive** | connected | Buscar e ler documentos Google Docs |
| **HubSpot** (cloud) | connected | MCP oficial Anthropic — CRM objects, search, manage |

#### Como configurar MCP em outro dispositivo

```bash
# 1. Copie o mcp.json (ja feito pelo install.sh)
cp config/mcp.json ~/.claude/mcp.json

# 2. Edite com suas API keys:
#    - PATH_TO_YOUR_OBSIDIAN_VAULT -> caminho do seu vault
#    - YOUR_TESTSPRITE_API_KEY_HERE -> sua API key do TestSprite
#    - YOUR_N8N_INSTANCE_URL -> URL da sua instancia n8n
#    - YOUR_N8N_API_KEY_HERE -> n8n Settings > API > Create API Key

# 3. Cloud connectors: conecte manualmente no Claude Code
#    Abra Claude Code > /mcp > Installed > conecte cada servico via OAuth:
#    - Gmail, Google Calendar, Google Drive, HubSpot, Excalidraw
#    Cada dispositivo precisa autenticar individualmente.
```

---

### Rules (16 arquivos)

#### Globais (`rules/common/`) — 10 arquivos
| Arquivo | Foco |
|---------|------|
| `agents.md` | Orquestracao de agents, quando usar cada um, execucao paralela |
| `coding-style.md` | Imutabilidade, files pequenos, error handling, input validation |
| `development-workflow.md` | Pipeline: research > plan > TDD > code review > commit |
| `git-workflow.md` | Conventional commits, PR workflow |
| `hooks.md` | PreToolUse, PostToolUse, Stop hooks, TodoWrite best practices |
| `patterns.md` | Repository pattern, API response envelope, skeleton projects |
| `performance.md` | Model selection (Haiku/Sonnet/Opus), context window, extended thinking |
| `project-categorization.md` | Categorizacao automatica de projetos no Obsidian (Pessoal/Paralelo/Freelancer/Singular) |
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

### Teams (1 team)

| Team | Inbox | Descricao |
|------|-------|-----------|
| `default` | `spec-reviewer` | Inbox para revisao de specs — recebe mensagens de team-lead para re-review |

---

### Scheduled Tasks (1 task)

| Task | Schedule | Descricao |
|------|----------|-----------|
| `daily-sync-obsidian` | Diario | Sync Calendar + Gmail + HubSpot para daily note no Obsidian vault |

A task puxa:
- **Google Calendar**: Eventos do dia
- **Gmail**: Emails nao lidos (top 10)
- **HubSpot**: Deals ativos (top 5 por valor)
- Cria daily note em `Diario/YYYY-MM-DD.md` no Obsidian vault

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

> **PORTABILIDADE:** Os paths dos hooks usam `$HOME/.claude/` (nao hardcoded). Funcionam em qualquer dispositivo apos rodar `install.sh`.

---

### Hooks do ECC Plugin (20 hooks automaticos)

Alem dos 6 hooks customizados acima, o plugin **Everything Claude Code** traz **20 hooks automaticos** que sao ativados pela env var `ECC_HOOK_PROFILE=strict` no `settings.json`.

Esses hooks vem com o plugin — nao precisam ser configurados manualmente. Basta instalar o plugin e ter `ECC_HOOK_PROFILE=strict` no env.

#### PreToolUse (rodam ANTES de cada tool)
| Hook | Matcher | O que faz |
|------|---------|-----------|
| Auto-tmux dev server | `Bash` | Bloqueia `npm run dev` fora de tmux |
| Tmux reminder | `Bash` | Sugere tmux para comandos longos (npm test, cargo build, docker) |
| Git push reminder | `Bash` | Lembra de revisar antes de `git push` |
| Doc file warning | `Write` | Avisa sobre arquivos .md nao-padrao |
| Strategic compact | `Edit\|Write` | Sugere `/compact` a cada ~50 tool calls |
| Continuous learning observer | `*` | Captura observacoes para aprendizado continuo |
| InsAIts security (opt-in) | `Bash\|Write\|Edit` | Scan de seguranca (requer `ECC_ENABLE_INSAITS=1`) |

#### PostToolUse (rodam DEPOIS de cada tool)
| Hook | Matcher | O que faz |
|------|---------|-----------|
| PR logger | `Bash` | Loga URL do PR apos `gh pr create` |
| Build analysis | `Bash` | Analise async apos build commands |
| Quality gate | `Edit\|Write` | Checks de qualidade apos edits |
| Prettier/Biome format | `Edit` | Auto-format JS/TS apos edits |
| TypeScript check | `Edit` | `tsc --noEmit` apos editar .ts/.tsx |
| console.log warning | `Edit` | Avisa sobre console.log em edits |
| Continuous learning result | `*` | Captura resultados para aprendizado |

#### Lifecycle
| Hook | Evento | O que faz |
|------|--------|-----------|
| Session start | `SessionStart` | Carrega contexto anterior, detecta package manager |
| Pre-compact | `PreCompact` | Salva estado antes de compactacao |
| Console.log audit | `Stop` | Checa console.log em todos os arquivos modificados |
| Session summary | `Stop` | Persiste estado da sessao |
| Pattern extraction | `Stop` | Avalia sessao para patterns reutilizaveis |
| Cost tracker | `Stop` | Metricas de custo por sessao |
| Session end marker | `SessionEnd` | Lifecycle marker |

#### Como funciona o ECC_HOOK_PROFILE

```
ECC_HOOK_PROFILE=strict   -> TODOS os hooks ativos (recomendado)
ECC_HOOK_PROFILE=standard -> Maioria dos hooks (sem tmux blocker)
ECC_HOOK_PROFILE=minimal  -> Apenas lifecycle hooks (session start/end)
```

O profile `strict` ja esta configurado no `settings.json` deste repo.

---

### Regras de Execucao — Superpowers (CRITICO)

O plugin **Superpowers** e o cerebro que governa COMO o Claude Code trabalha. Ele impoe um modelo de execucao disciplinado com skills obrigatorios em cada fase do trabalho.

#### Skill `using-superpowers` (auto-ativa em toda sessao)

Este skill carrega automaticamente no inicio de cada sessao e forca o Claude a:

1. **Verificar skills ANTES de qualquer resposta** — mesmo perguntas simples
2. **Invocar skills aplicaveis obrigatoriamente** — mesmo com 1% de chance de relevancia
3. **Bloquear racionalizacoes** — "e so uma pergunta simples" nao e desculpa

#### Cadeia de Execucao Superpowers

```
Mensagem do usuario
  |
  v
[using-superpowers] Verifica se algum skill se aplica
  |
  v (se sim)
[Skill invocado] -> brainstorming / writing-plans / tdd / debugging / etc.
  |
  v
[Skill seguido] Execucao conforme o skill manda
  |
  v
[verification-before-completion] Verifica antes de declarar pronto
```

#### Skills de Execucao do Superpowers

| Skill | Quando ativa | O que forca |
|-------|-------------|-------------|
| `brainstorming` | Antes de QUALQUER trabalho criativo | Explorar intent, requisitos e design antes de codificar |
| `writing-plans` | Antes de implementacao multi-step | Plano escrito com steps numerados |
| `executing-plans` | Ao executar um plano existente | Checkpoints de review entre steps |
| `test-driven-development` | Qualquer feature ou bugfix | Testes PRIMEIRO, depois implementacao |
| `systematic-debugging` | Qualquer bug ou falha | Root cause analysis antes de fix |
| `dispatching-parallel-agents` | 2+ tasks independentes | Paralelizar com agents isolados |
| `subagent-driven-development` | Implementacao com tasks independentes | Delegar para subagents |
| `requesting-code-review` | Apos completar feature/task | Review automatico |
| `receiving-code-review` | Ao receber feedback de review | Verificar antes de aceitar cegamente |
| `using-git-worktrees` | Feature que precisa isolamento | Worktree isolado para cada agent |
| `finishing-a-development-branch` | Implementacao completa | Merge / PR / cleanup estruturado |
| `verification-before-completion` | Antes de declarar "pronto" | Rodar verificacao, evidencia antes de afirmar |
| `writing-skills` | Criar ou editar skills | Seguir formato e testar antes de deploy |

#### Red Flags — Pensamentos que o Superpowers bloqueia

Se o Claude pensa qualquer um destes, o Superpowers forca parar e verificar:

| Pensamento bloqueado | Realidade |
|---------------------|-----------|
| "E so uma pergunta simples" | Perguntas sao tasks. Verificar skills. |
| "Preciso de mais contexto primeiro" | Skill check vem ANTES de perguntas. |
| "Deixa eu explorar o codebase" | Skills dizem COMO explorar. Check primeiro. |
| "Vou so fazer essa coisinha rapido" | Check ANTES de fazer qualquer coisa. |
| "O skill e overkill" | Coisas simples viram complexas. Usar. |
| "Eu sei o que isso significa" | Saber o conceito ≠ usar o skill. Invocar. |

#### Garantia: Superpowers funciona em outro dispositivo?

**SIM, se o plugin estiver instalado.** O Superpowers e um plugin — quando instalado via `claude plugins install superpowers --marketplace superpowers-marketplace`, TODOS os skills de execucao acima sao baixados automaticamente para `~/.claude/plugins/cache/superpowers-marketplace/`.

O `settings.json` deste repo ja tem:
- `"superpowers@superpowers-marketplace": true` em `enabledPlugins`
- `"superpowers-marketplace"` em `extraKnownMarketplaces` apontando para `obra/superpowers-marketplace`

---

### Statusline Customizada

Script bash que mostra em tempo real:
```
Opus 4.6 | meu-projeto | [frontend-specialist] | feature/nova-pagina
 23% | 1m 45s | $0.42 | #a1b2c3d4
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

### Obsidian Templates (2)

| Template | Descricao |
|----------|-----------|
| `template-daily.md` | Template de daily note com secoes: Agenda, Emails, HubSpot, Tasks, Notas |
| `template-projeto.md` | Template de nota de projeto com frontmatter category/status/stack |

---

### Plugin Blocklist

`plugins/blocklist.json` — Lista de plugins bloqueados (testados e rejeitados). Previne reinstalacao acidental.

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
├── plugins/                     # Plugin configs
│   └── blocklist.json           # Plugins bloqueados
├── rules/                       # 16 arquivos de rules
│   ├── common/                  # Rules globais (10)
│   │   ├── agents.md
│   │   ├── coding-style.md
│   │   ├── development-workflow.md
│   │   ├── git-workflow.md
│   │   ├── hooks.md
│   │   ├── patterns.md
│   │   ├── performance.md
│   │   ├── project-categorization.md
│   │   ├── security.md
│   │   └── testing.md
│   ├── typescript/              # Rules TypeScript (5)
│   │   ├── coding-style.md
│   │   ├── hooks.md
│   │   ├── patterns.md
│   │   ├── security.md
│   │   └── testing.md
│   └── parallel-agents.md       # Worktree isolation
├── scheduled-tasks/             # Tarefas agendadas
│   └── daily-sync-obsidian/
│       └── SKILL.md             # Sync diario Calendar+Gmail+HubSpot -> Obsidian
├── scripts/                     # Scripts de notificacao e automacao
│   ├── claude-notify.js         # Notificacao principal (toast+bell+wezterm)
│   ├── toast-notify.js          # Toast fallback
│   └── ralph/                   # Ralph agent loop
│       ├── ralph.sh
│       ├── CLAUDE.md
│       └── prd.json.example
├── skills/                      # 8 skills customizados
│   ├── hubspot-mcp-expert/
│   ├── n8n-code-javascript/
│   ├── n8n-code-python/
│   ├── n8n-expression-syntax/
│   ├── n8n-mcp-tools-expert/
│   ├── n8n-node-configuration/
│   ├── n8n-validation-expert/
│   └── n8n-workflow-patterns/
├── teams/                       # Agent teams config
│   └── default/
│       └── inboxes/
│           └── spec-reviewer.json
└── templates/                   # Templates Obsidian
    ├── template-daily.md
    └── template-projeto.md
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

### 7. Teams
```bash
mkdir -p ~/.claude/teams/default/inboxes
cp teams/default/inboxes/spec-reviewer.json ~/.claude/teams/default/inboxes/
```

### 8. Scheduled Tasks
```bash
mkdir -p ~/.claude/scheduled-tasks/daily-sync-obsidian
cp scheduled-tasks/daily-sync-obsidian/SKILL.md ~/.claude/scheduled-tasks/daily-sync-obsidian/
```

### 9. Templates
```bash
mkdir -p ~/.claude/templates
cp templates/*.md ~/.claude/templates/
```

### 10. Plugin Blocklist
```bash
cp plugins/blocklist.json ~/.claude/plugins/
```

### 11. Plugins (OBRIGATORIO — traz 247 skills + 59 agents + 125 rules)
```bash
# PASSO 1: Certifique-se de que o settings.json foi copiado (contem os marketplaces)
# O settings.json registra os repos GitHub de cada marketplace

# PASSO 2: Instale cada plugin (requer Claude Code logado):
claude plugins install everything-claude-code --marketplace everything-claude-code
claude plugins install superpowers --marketplace superpowers-marketplace
claude plugins install ralph-skills --marketplace ralph-marketplace
claude plugins install ui-ux-pro-max --marketplace ui-ux-pro-max-skill

# PASSO 3: Verifique:
claude plugins list
# Deve mostrar 4 plugins enabled

# Se algum falhar, tente instalar manualmente via /plugins no Claude Code
```

**Repos dos plugins (para referencia):**
| Plugin | GitHub |
|--------|--------|
| Everything Claude Code | https://github.com/affaan-m/everything-claude-code |
| Superpowers | https://github.com/obra/superpowers-marketplace |
| Ralph Skills | https://github.com/snarktank/ralph |
| UI/UX Pro Max | https://github.com/nextlevelbuilder/ui-ux-pro-max-skill |

### 12. MCP Servers locais
```bash
# Instalar n8n-mcp globalmente:
npm install -g n8n-mcp

# Editar mcp.json com suas API keys:
nano ~/.claude/mcp.json
# Substituir: PATH_TO_YOUR_OBSIDIAN_VAULT, YOUR_TESTSPRITE_API_KEY_HERE,
#             YOUR_N8N_INSTANCE_URL, YOUR_N8N_API_KEY_HERE, PATH_TO_N8N_MCP
```

### 13. Cloud Connectors (OAuth — manual por dispositivo)
```bash
# Abra o Claude Code e conecte via OAuth:
# /mcp > procure cada servico e clique "Connect":
#   - Gmail
#   - Google Calendar
#   - Google Drive
#   - HubSpot
#   - Excalidraw
# Cada dispositivo precisa autenticar individualmente.
```

---

## Configuracao Pos-Instalacao

### Checklist completo para novo dispositivo

```
[ ] 1. git clone https://github.com/pedrormc/claude-code-toolkit.git
[ ] 2. cd claude-code-toolkit && bash install.sh
[ ] 3. Verificar que 4 plugins foram instalados: claude plugins list
[ ] 4. Se algum plugin falhou: reinstalar manualmente (ver secao 11)
[ ] 5. Instalar n8n-mcp: npm install -g n8n-mcp
[ ] 6. Editar ~/.claude/mcp.json com suas API keys
[ ] 7. Conectar cloud MCPs via OAuth: Gmail, Calendar, Drive, HubSpot, Excalidraw
[ ] 8. Reiniciar Claude Code
[ ] 9. Testar: digitar / e verificar que os skills aparecem (~255 total)
```

### API Keys necessarias

Edite `~/.claude/mcp.json` e substitua:

| Placeholder | Onde obter |
|-------------|------------|
| `PATH_TO_YOUR_OBSIDIAN_VAULT` | Caminho para seu vault Obsidian (ex: `C:/Users/user/Documents/obsidiano`) |
| `YOUR_TESTSPRITE_API_KEY_HERE` | [TestSprite Dashboard](https://testsprite.com) |
| `YOUR_N8N_INSTANCE_URL` | URL da sua instancia n8n (ex: `https://n8n.seudominio.com`) |
| `YOUR_N8N_API_KEY_HERE` | n8n > Settings > API > Create API Key |
| `PATH_TO_N8N_MCP` | Rode `npm root -g` e adicione `/n8n-mcp` ao final |

---

## Arquitetura: Como as Camadas Funcionam

Quando voce digita `/` no Claude Code, ele monta a lista combinando **4 camadas**:

```
~/.claude/
├── agents/          <- CAMADA 1: Agents customizados (5 neste repo)
├── skills/          <- CAMADA 2: Skills customizados (8 neste repo)
├── rules/           <- CAMADA 2: Rules customizadas (16 neste repo)
├── plugins/cache/   <- CAMADA 3: Skills/agents dos plugins (42 skills + 10 agents)
│   ├── everything-claude-code/  -> 20 skills, 9 agents, 130+ rules
│   ├── superpowers-marketplace/ -> 18 skills, 1 agent
│   ├── ralph-marketplace/       -> 2 skills
│   └── ui-ux-pro-max-skill/     -> 1 skill
├── teams/           <- CAMADA 2: Agent teams e inboxes
├── scheduled-tasks/ <- CAMADA 2: Tarefas agendadas (cron-like)
└── [Cloud MCPs]     <- CAMADA 4: Connectors OAuth (Gmail, Calendar, Drive, HubSpot, Excalidraw)
```

**Prioridade de resolucao:**
1. Configs de PROJETO (`.claude/` dentro do repo) > configs globais (`~/.claude/`)
2. Rules de projeto > rules globais > rules de plugins
3. Skills customizados e skills de plugins coexistem (sem override)

**Para os devs:** Este repo contem as camadas 1 e 2 (customizacoes). A camada 3 (plugins) e instalada via `install.sh`. A camada 4 (cloud connectors) requer configuracao individual via OAuth.

### Cloud Connectors — Configuracao Manual

Cada dev precisa conectar individualmente:
1. No Claude Code, acesse as configuracoes de connectors
2. Conecte os servicos que usa:
   - **Gmail** — para buscar/ler/rascunhar emails
   - **Google Calendar** — para gerenciar eventos
   - **Google Drive** — para buscar/ler Google Docs
   - **HubSpot** — para CRM (contacts, deals, tickets)
   - **Excalidraw** — para diagramas

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
