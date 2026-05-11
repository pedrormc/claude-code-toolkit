# Setup do Ecossistema Singular no Codex — Guia pro Simon

> Esse documento é pra você **copiar inteiro** e colar no Codex (chat ou terminal) **na primeira sessão**. Ele explica passo-a-passo como replicar o ambiente do Pedro (Claude Code) no Codex CLI da OpenAI.
>
> **Tempo total estimado:** 60-90 minutos (15min Codex + 20min MCPs + 30min validar).
>
> **Pré-requisitos:** uma máquina com Windows 10/11, macOS, ou Linux. Internet. Conta OpenAI (Plus ou API).

---

## 0) Antes de começar — o que é cada coisa

Simon, você é novo em IA e terminal, então vou explicar o vocabulário primeiro. **Leia essa seção até o fim antes de rodar nada.**

| Termo | O que é | Por que importa |
|---|---|---|
| **Terminal** | A "janela preta" onde você digita comandos. No Windows é o **PowerShell** ou o **Git Bash**. No Mac/Linux é o **Terminal**. | Quase tudo aqui é via terminal — Codex roda nele. |
| **CLI** | "Command Line Interface" — programa que roda no terminal (sem janelinha gráfica). | Codex, Git, npm, todos são CLIs. |
| **Codex CLI** | A "versão terminal" do ChatGPT da OpenAI. Editor de código pilotado por IA. | É o equivalente do Claude Code, mas usa GPT (não Claude). |
| **MCP (Model Context Protocol)** | Plugin que dá superpoderes pra IA (ex: ler seu Google Drive, mandar WhatsApp, etc.) | É o que diferencia o setup do Pedro de um Codex "cru". |
| **AGENTS.md** | Arquivo de instruções permanentes pro Codex (como o `CLAUDE.md` é pro Claude). | O Codex lê esse arquivo TODA sessão. Sem ele você não tem persona. |
| **Skill / Plugin** | Atalhos de comportamento que o Pedro criou (ex: `/contrato` gera um NDA). | **No Codex isso vira prompt manual** — não tem skill auto-invoke. |
| **Repo / Repositório** | Pasta de projeto versionada com Git. | Vamos clonar o repo `claude-code-toolkit` que tem tudo. |
| **.env** | Arquivo escondido que guarda suas senhas/tokens (NUNCA vai pro Git). | Toda credencial vai aí. |

### O que dá pra clonar e o que NÃO dá

| O que o Pedro tem no Claude Code | Funciona no Codex? | Solução |
|---|---|---|
| MCPs (Obsidian, n8n, Drive, etc.) | ✅ Sim | Codex 0.50+ suporta MCP. Mesma config. |
| `CLAUDE.md` (instruções permanentes) | ✅ Equivalente | Vira `AGENTS.md`. |
| Skills (`/contrato`, `/ata`, etc.) | ⚠️ Parcial | Skills viram prompts. Você cola o conteúdo da skill quando quer usar. |
| Plugins (ECC, Superpowers, Gstack) | ❌ Não | Não existe no Codex. Funcionalidade equivalente vem de prompts custom. |
| Hooks (auto-save, validação) | ⚠️ Parcial | Codex tem hooks próprios mas diferentes — vamos pular nessa primeira instalação. |
| Memory (`~/.claude/projects/`) | ⚠️ Manual | Codex não tem auto-memory. Use o `AGENTS.md` pra "memória estática". |

**Resumo:** vamos clonar **MCPs + AGENTS.md + skills como prompts**. Hooks/auto-memory ficam pra fase 2.

---

## 1) Instalar o Codex CLI

### 1.1) Instalar o Node.js (pré-requisito)

O Codex CLI precisa do Node.js v20 ou mais novo.

**Windows:**
1. Baixe o instalador em https://nodejs.org/ (versão **LTS**, botão verde)
2. Roda o `.msi`, dá Next em tudo, marca a opção "Add to PATH" (já vem marcado)
3. **Reinicia o PC** (importante pra PATH carregar)
4. Abre o **PowerShell** (Win+X → Terminal) e digita:
   ```powershell
   node --version
   npm --version
   ```
   Tem que aparecer algo tipo `v20.x.x` e `10.x.x`. Se não, repete a instalação.

**macOS:**
```bash
brew install node
# Se não tiver brew: https://brew.sh
```

**Linux (Ubuntu/Debian):**
```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
```

### 1.2) Instalar o Codex CLI

No terminal:
```bash
npm install -g @openai/codex
```

Confere:
```bash
codex --version
```
Esperado: `0.50.0` ou mais novo.

### 1.3) Logar na OpenAI

```bash
codex login
```

Vai abrir o navegador. Logue com sua conta OpenAI (a mesma do ChatGPT). **Se tiver ChatGPT Plus** já está OK. Se for API-only, precisa adicionar créditos em https://platform.openai.com/billing.

Teste:
```bash
codex
```
Vai abrir o REPL. Digita `oi` e vê se responde. **Ctrl+C duas vezes** pra sair.

---

## 2) Instalar o Git e clonar o toolkit do Pedro

### 2.1) Git

**Windows:** Baixar em https://git-scm.com/download/win. Instala dando Next em tudo. Vai instalar junto o **Git Bash** — recomendo usar ele no Windows pros próximos passos (em vez do PowerShell), porque a maioria dos comandos é Linux-style.

**Mac:** `brew install git`
**Linux:** `sudo apt install git`

Confere:
```bash
git --version
```

### 2.2) Configurar Git (primeira vez)

```bash
git config --global user.name "Simon Sobrenome"
git config --global user.email "seu.email@singular.group"
```

### 2.3) Clonar o toolkit

Escolhe uma pasta pra clonar (ex: Desktop):
```bash
cd ~/Desktop          # ou onde preferir
git clone https://github.com/pedrormc/claude-code-toolkit.git
cd claude-code-toolkit
```

Agora você tem o repo localmente. Vê o que tem:
```bash
ls
```
Deve listar: `agents/`, `config/`, `hooks/`, `rules/`, `skills/`, `templates/`, `scripts/`, `README.md`, etc.

---

## 3) Configurar o AGENTS.md (o "CLAUDE.md" do Codex)

O Codex lê automaticamente um arquivo chamado **`AGENTS.md`** na raiz do projeto onde você está trabalhando. É onde você define persona, regras, atalhos. Vamos criar o seu.

### 3.1) Onde colocar o AGENTS.md

Você tem **3 níveis** de AGENTS.md (do mais geral pro mais específico):

| Caminho | Quando aplica | O que colocar |
|---|---|---|
| `~/.codex/AGENTS.md` | Toda sessão de Codex, em qualquer pasta | Sua persona global, idioma, regras universais |
| `<repo>/AGENTS.md` | Só dentro daquele repo | Convenções daquele projeto |
| `<repo>/subpasta/AGENTS.md` | Só dentro daquela subpasta | Overrides locais |

### 3.2) Criar o `~/.codex/AGENTS.md` (global)

No Git Bash (Windows) ou Terminal (Mac/Linux):
```bash
mkdir -p ~/.codex
```

Agora crie o arquivo. **Copie o bloco abaixo INTEIRO** e cole no arquivo `~/.codex/AGENTS.md`:

```markdown
# Codex Master — Simon (Singular Group)

Você é o **assistente de código do Simon**, da Singular Group. Trabalha com o Simon que é iniciante em terminal/IA — explica o que está fazendo antes de fazer, em PT-BR informal e direto.

## Identidade do usuário
- **Nome:** Simon (Singular Group)
- **Nível técnico:** iniciante em IA e terminal, intermediário em produto/negócio
- **Empresa:** Singular Group / Singular Venture
- **Estilo de comunicação:** PT-BR informal, curto, sem firula

## Regras de comunicação
- PT-BR informal, casual, direto
- Sem emojis (a menos que o Simon peça)
- Respostas curtas, vai pro ponto
- **Antes de rodar comando perigoso (rm, drop, deploy, force-push), PERGUNTA primeiro**
- Quando usar um comando de terminal, explica em 1 linha o que ele faz
- Quando criar um arquivo grande, mostra o nome e diz "criei em X, dá uma olhada"

## Stack que o Simon usa
- **OS:** [Windows / Mac / Linux — preencha você]
- **Editor:** [VS Code / Cursor / outro — preencha você]
- **Linguagens principais:** JavaScript/Node, Python (quando necessário)
- **Framework principal:** [Next.js / React / outro — preencha você]
- **Banco:** [PostgreSQL / Supabase / outro — preencha você]

## Workflow padrão
1. **Antes de codar:** entender o requisito, perguntar se algo está ambíguo
2. **Pesquisar reuso:** checar npm / GitHub antes de escrever do zero
3. **Testar:** escrever teste antes (TDD) quando o caso é claro
4. **Commit:** mensagem curta no formato `feat: descrição` ou `fix: descrição`
5. **Push:** sempre `git pull --rebase` antes de pushar

## Segurança — checklist obrigatório
- NUNCA hardcode secrets (API keys, tokens, senhas) no código
- SEMPRE usar `.env` + variáveis de ambiente
- VALIDAR input do usuário antes de qualquer SQL/HTTP/filesystem
- Mensagens de erro no UI não podem vazar dados internos

## Skills disponíveis (do toolkit do Pedro)
O Simon clonou o repo `claude-code-toolkit`. Skills disponíveis em `skills/`:

| Slug | O que faz | Como usar |
|---|---|---|
| `contrato` | Gera NDA/MOU/Prestação de Serviços em .docx | Simon pede "faz um NDA com fulano" → você lê `skills/contrato/SKILL.md` e segue |
| `ata` | Transforma notas de reunião em .docx formatado | Simon pede "monta a ata dessa reunião" → você lê `skills/ata/SKILL.md` |
| `pop` | Gera Procedimento Operacional Padrão | "monta um POP de X" → `skills/pop/SKILL.md` |
| `documento` | Documento formal genérico em .docx | "monta um documento sobre X" → `skills/documento/SKILL.md` |
| `slide` | Apresentação HTML+ scroll snap (e .pptx opcional) | "cria slides sobre X" → `skills/slide/SKILL.md` |
| `backgroundcheck` | Due diligence de pessoa física | "background check em fulano" → `skills/backgroundcheck/SKILL.md` |
| `prospect` | Prospecção comercial Asa Norte | "prospecta a quadra X" → `skills/prospect/SKILL.md` |
| `tese-investimento` | Estrutura tese de investimento | "monta uma tese de X" → `skills/tese-investimento/SKILL.md` |
| `whatsapp-evolution` | Envia mensagem WhatsApp via Evolution API | "manda WhatsApp pra X dizendo Y" → `skills/whatsapp-evolution/SKILL.md` |
| `mp4` | Converte MP4 pra MP3 (ffmpeg) | "extrai áudio desse vídeo" → `skills/mp4/SKILL.md` |
| `obsidian` | Salva resumo da sessão no vault Obsidian | "/obsidian" ou "salva no obsidian" |
| `n8n-*` (7 skills) | Helpers pra workflows n8n | Quando trabalhar com n8n |
| `hubspot-mcp-expert` | Como usar o HubSpot via MCP | Quando integrar com HubSpot |

**Como funciona:** quando o Simon pedir algo que casa com uma skill, você **lê o arquivo `SKILL.md`** da skill correspondente e segue o que está escrito lá. Não invente — siga o protocolo da skill.

## MCPs disponíveis
- `obsidian` — leitura/escrita no vault Obsidian local
- `google-drive` — CRUD em Docs, Sheets, Slides, Drive
- `n8n` — gerenciar workflows n8n
- `TestSprite` — gerar testes E2E
- `serpapi` — busca Google estruturada

Antes de usar um MCP, valida que ele está configurado com `codex mcp list`.

## Comandos perigosos — sempre perguntar antes
- `rm -rf` em qualquer pasta importante
- `git reset --hard`, `git push --force`
- `DROP TABLE`, `DELETE FROM ... WHERE` sem `LIMIT`
- Deploy em produção
- Mudança em config de ambiente (`.env`, secrets)
```

**Como criar o arquivo no Windows (Git Bash):**
```bash
nano ~/.codex/AGENTS.md
# cola o conteúdo, Ctrl+O Enter pra salvar, Ctrl+X pra sair
```

Ou use o VS Code:
```bash
code ~/.codex/AGENTS.md
```

### 3.3) AGENTS.md por projeto

Quando você for trabalhar em um projeto específico (ex: o site da Singular), cria um `AGENTS.md` na raiz do projeto com as convenções dele. O Codex automaticamente **mescla** o global com o local.

---

## 4) Instalar e configurar os MCPs

### 4.1) Listar MCPs atuais

```bash
codex mcp list
```

Provavelmente vai estar vazio na primeira vez.

### 4.2) Pré-instalar dependências dos MCPs

Alguns MCPs precisam ser instalados como pacotes globais antes:

```bash
npm install -g n8n-mcp
npm install -g @piotr-agier/google-drive-mcp
```

> **Por que `-g`?** Instala globalmente, fica disponível em qualquer pasta. Sem `-g`, só funciona dentro daquele projeto.

### 4.3) Adicionar cada MCP no Codex

O Codex aceita MCPs via `codex mcp add` (linha de comando) **OU** editando `~/.codex/config.toml`. Vou mostrar os dois jeitos.

#### Jeito 1: Via CLI (mais simples pra começar)

**Obsidian MCP (substitua `<PATH_VAULT>` pelo caminho do seu vault local):**
```bash
codex mcp add obsidian -- npx @bitbonsai/mcpvault@latest "<PATH_VAULT>"
```
Exemplo no Windows: `"C:/Users/Simon/Documents/MeuVault"`
Exemplo no Mac: `"/Users/simon/Documents/MeuVault"`

> **Se você não usa Obsidian ainda**, pula esse MCP. Pode adicionar depois.

**TestSprite MCP:**
Primeiro pega a API key em https://testsprite.com → Dashboard → API Keys. Aí:
```bash
codex mcp add TestSprite --env API_KEY=SUA_CHAVE_AQUI -- npx @testsprite/testsprite-mcp@latest
```

**n8n MCP** (só se você tem n8n self-hosted):
```bash
codex mcp add n8n \
  --env MCP_MODE=stdio \
  --env N8N_API_URL=https://seu-n8n.exemplo.com \
  --env N8N_API_KEY=SUA_N8N_API_KEY \
  -- node "<CAMINHO_GLOBAL_NODE_MODULES>/n8n-mcp/dist/mcp/index.js"
```

Pra descobrir o `<CAMINHO_GLOBAL_NODE_MODULES>`:
```bash
npm root -g
```

**SerpAPI MCP:**
Pega URL completa em https://serpapi.com/dashboard → Manage MCP Server (formato `https://mcp.serpapi.com/<TOKEN>/mcp`):
```bash
codex mcp add serpapi --url "https://mcp.serpapi.com/SEU_TOKEN/mcp"
```

**Google Drive MCP** (mais complexo — requer OAuth, ver §4.4):
```bash
codex mcp add google-drive \
  --env GOOGLE_DRIVE_OAUTH_CREDENTIALS=~/.codex/secrets/gcp-oauth.keys.json \
  --env GOOGLE_DRIVE_MCP_TOKEN_PATH=~/.codex/secrets/gcp-oauth.token.json \
  -- node "<CAMINHO_GLOBAL_NODE_MODULES>/@piotr-agier/google-drive-mcp/dist/index.js"
```

#### Jeito 2: Via arquivo `~/.codex/config.toml`

Se preferir editar arquivo direto, abra `~/.codex/config.toml` (cria se não existir) e cola:

```toml
[mcp_servers.obsidian]
command = "npx"
args = ["@bitbonsai/mcpvault@latest", "PATH_DO_SEU_VAULT"]

[mcp_servers.TestSprite]
command = "npx"
args = ["@testsprite/testsprite-mcp@latest"]
env = { API_KEY = "${TESTSPRITE_API_KEY}" }

[mcp_servers.n8n]
command = "node"
args = ["PATH_DO_n8n-mcp/dist/mcp/index.js"]
env = { MCP_MODE = "stdio", N8N_API_URL = "${N8N_API_URL}", N8N_API_KEY = "${N8N_API_KEY}" }

[mcp_servers.serpapi]
url = "${SERPAPI_MCP_URL}"

[mcp_servers.google-drive]
command = "node"
args = ["PATH_DO_google-drive-mcp/dist/index.js"]
env = { GOOGLE_DRIVE_OAUTH_CREDENTIALS = "${HOME}/.codex/secrets/gcp-oauth.keys.json", GOOGLE_DRIVE_MCP_TOKEN_PATH = "${HOME}/.codex/secrets/gcp-oauth.token.json" }
```

E exporta os env vars em `~/.bashrc` (Mac/Linux) ou `$PROFILE` (Windows PowerShell):
```bash
export TESTSPRITE_API_KEY="sua_chave"
export N8N_API_URL="https://seu-n8n.exemplo.com"
export N8N_API_KEY="sua_n8n_key"
export SERPAPI_MCP_URL="https://mcp.serpapi.com/SEU_TOKEN/mcp"
```

### 4.4) Setup do Google Drive MCP (OAuth)

Esse é o mais chato. Pula se não for usar Drive na primeira semana.

1. Vai em https://console.cloud.google.com/
2. Cria um projeto novo (ou usa um existente)
3. APIs & Services → **Enable APIs** → habilita: Google Drive API, Google Docs API, Google Sheets API, Google Slides API, Google Calendar API
4. APIs & Services → **Credentials** → **Create Credentials** → **OAuth client ID** → **Desktop app**
5. Baixa o JSON. Renomeia pra `gcp-oauth.keys.json`
6. Move pra:
   - Mac/Linux: `~/.codex/secrets/gcp-oauth.keys.json`
   - Windows (Git Bash): `~/.codex/secrets/gcp-oauth.keys.json` (que é `C:\Users\Simon\.codex\secrets\`)
7. Cria a pasta secrets se não existir: `mkdir -p ~/.codex/secrets`
8. Na primeira execução do MCP ele vai abrir um navegador pedindo permissão — autoriza, e ele gera o `gcp-oauth.token.json` automaticamente

### 4.5) Validar MCPs

```bash
codex mcp list
```

Roda o Codex e testa:
```bash
codex
# dentro do REPL:
```
Digita: `lista meus MCPs disponíveis e diz quais estão funcionando`

---

## 5) Replicar as skills do Pedro (modo manual)

No Claude Code, skills são auto-invocadas (você digita `/contrato` e o Claude executa). No **Codex isso não existe nativo**. Workaround: você fala em linguagem natural e o Codex lê a skill do disco.

### 5.1) Como usar uma skill no Codex

Exemplo, você quer gerar um NDA:

```
Simon (no Codex): "Lê o arquivo skills/contrato/SKILL.md desse repo e segue o protocolo dele pra gerar um NDA entre Singular Group e Fulano da Silva, CPF 000.000.000-00, consultor autônomo."
```

O Codex vai:
1. Ler `SKILL.md`
2. Seguir o passo-a-passo descrito lá
3. Gerar o `.docx` no path que a skill define

### 5.2) Atalhos no Codex (custom prompts)

Pra evitar reescrever toda vez, cria atalhos em `~/.codex/prompts/`:

```bash
mkdir -p ~/.codex/prompts
```

Cria `~/.codex/prompts/contrato.md`:
```markdown
Lê e segue exatamente o protocolo de `skills/contrato/SKILL.md` do toolkit clonado em ~/Desktop/claude-code-toolkit.

Tipo de contrato: $1
Partes: $2
Detalhes: $3
```

Aí no Codex você usa: `/contrato NDA "Singular x Fulano" "consultoria mensal"`

> **Nota:** sintaxe de prompts custom muda por versão do Codex. Veja `codex prompts --help` na sua instalação.

### 5.3) Skills que precisam de secrets adicionais

| Skill | Secret necessário | Como configurar |
|---|---|---|
| `contrato` | Qdrant + OpenAI API key | `cp config/.env.example skills/contrato/.env` e preenche |
| `whatsapp-evolution` | Evolution API URL + key | mesmo padrão, `cp config/.env.example .env` |
| `backgroundcheck` | Nada (usa só APIs públicas) | OK |

---

## 6) Setup do `.env` (suas credenciais)

```bash
cd ~/Desktop/claude-code-toolkit
cp config/.env.example .env
```

Abre `.env` no editor:
```bash
code .env       # ou: nano .env
```

Preenche TODOS os campos que você for usar. **Salva**. Esse arquivo **NUNCA** vai pro Git (já está no `.gitignore`).

Pra carregar essas vars no terminal automaticamente:

**Bash/Zsh (Mac, Linux, Git Bash):** adiciona no `~/.bashrc` ou `~/.zshrc`:
```bash
set -a; source ~/Desktop/claude-code-toolkit/.env; set +a
```

**PowerShell:** adiciona no `$PROFILE`:
```powershell
Get-Content "$HOME\Desktop\claude-code-toolkit\.env" | ForEach-Object {
  if ($_ -match '^\s*([^#=]+)=(.*)$') {
    $env:($matches[1].Trim()) = $matches[2].Trim()
  }
}
```

Reabre o terminal pra carregar.

---

## 7) Checklist final — está tudo funcionando?

Roda esses comandos um por um e verifica:

```bash
# 1. Codex instalado e logado
codex --version              # deve mostrar 0.50+
codex whoami                 # deve mostrar seu email OpenAI

# 2. Toolkit clonado
ls ~/Desktop/claude-code-toolkit/skills/   # deve listar dezenas de skills

# 3. AGENTS.md global existe
cat ~/.codex/AGENTS.md | head -5

# 4. MCPs listados
codex mcp list

# 5. Env vars carregadas (exemplo)
echo $N8N_API_URL            # deve printar sua URL (não vazio)

# 6. Smoke test no Codex
codex
> "Lista as skills disponíveis em ~/Desktop/claude-code-toolkit/skills/ e me diz o que cada uma faz"
```

Se TUDO acima funciona, **você está clonado**. 🎯

---

## 8) Troubleshooting comum

### "command not found: codex"
- Você instalou Node? `node --version` funciona?
- Você instalou Codex global? `npm install -g @openai/codex`
- Windows: reiniciou após instalar Node?
- Mac: rodou `brew link node`?

### "codex login" não abre o navegador
- Tenta `codex login --headless` e cola a URL manualmente no navegador
- Verifica se tem firewall bloqueando localhost

### MCP não aparece em `codex mcp list`
- Verifica o caminho exato no `~/.codex/config.toml`
- Pra n8n/google-drive, valida que o pacote npm foi instalado: `npm list -g n8n-mcp`
- Reinicia o Codex (sair com Ctrl+C duas vezes e reabrir)

### "Cannot find module"
- Você instalou o pacote npm global? `npm root -g` → confere se o pacote está nessa pasta
- Path no config tem que ser absoluto. Windows usa `C:/Users/...` (barra normal, não invertida)

### Skill `contrato` não gera o .docx
- Instalou Python? `python --version` ou `python3 --version`
- Instalou as deps Python? `cd skills/contrato && pip install -r requirements.txt`
- Tem `python-docx` instalado? `pip show python-docx`

### Evolution API (WhatsApp) retorna 401
- API key errada no `.env`. Pega de novo no painel Evolution.
- Instance não existe. Cria no painel ou via API.

### Geral
- Sempre olha o erro completo (não só a primeira linha)
- Copia o erro inteiro e cola pro Codex perguntando "o que tá errado aqui?"

---

## 9) Próximos passos depois de instalar

1. **Estuda o `README.md`** do toolkit (raiz do repo) — explica a metodologia TRIFORCE do Pedro
2. **Lê 2 ou 3 skills** que você acha que vai usar mais (ex: `contrato/`, `ata/`, `documento/`)
3. **Cria um projeto teste** e fala com o Codex em PT-BR: "monta um app simples de TODO list em Next.js"
4. **Quando bater dúvida:** copia esse arquivo e o erro pro Codex, ele te ajuda
5. **Daqui 1 semana:** se quiser auto-memory tipo Pedro tem, agenda um pareamento com ele pra setar hooks customizados

---

## 10) Como pedir ajuda pro Pedro

Se travar em algum passo, manda no WhatsApp:

```
Pedro, travei em [seção X] do SETUP_PROMPT_SIMON_CODEX.

O que tentei: [colar comando]
O erro: [colar erro completo]
Sistema: [Windows/Mac/Linux]
```

**Pronto Simon. Bora codar.** 🚀

---

*[Documento gerado automaticamente — versão 1.0 / 2026-05-11]*
*[Toolkit: github.com/pedrormc/claude-code-toolkit]*
