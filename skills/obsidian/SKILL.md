---
name: obsidian
description: |
  Salva o que foi feito no Claude Code numa daily note do vault Obsidian.
  Use quando o usuário digitar /obsidian, "salva no obsidian", "documenta o dia",
  "registra no diário", "grava no vault", "resumo do dia", ou variações.
  Duas modalidades: (a) recap rico da sessão ATUAL via análise da conversa,
  (b) consolidação de TODAS as sessões do dia via scanner determinístico.
  O objetivo é construir histórico Claude Code → Obsidian ao longo do tempo.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# /obsidian — Daily Note Sync Claude Code → Obsidian Vault

Registra o trabalho no Claude Code na daily note do dia dentro do vault Obsidian. Suporta três modos.

## Modos

| Modo | Quando usar | Fonte dos dados |
|------|-------------|-----------------|
| **current** (default) | "salva o que fizemos agora" — sessão atual | Análise manual da conversa no contexto |
| **full** | "resume o dia todo", "consolida todas as sessões" | Scanner determinístico sobre todos jsonl do dia |
| **pick** | "me mostra as sessões de hoje pra eu escolher" | Scanner lista; usuário escolhe N; detalha as escolhidas |

Se o usuário disser algo ambíguo (`/obsidian` cru), pergunte qual modo quer OU proponha o padrão apropriado:
- Se **só houve 1 sessão** ativa no dia → usa `current` direto
- Se **há 2+ sessões** do dia no disco → mostra a tabela e pergunta "resumir só esta ou consolidar as N?"

## Vault path
- Base: `C:/Users/teste/Documents/obsidiano/`
- Daily notes: `C:/Users/teste/Documents/obsidiano/Diário/YYYY-MM-DD.md`
- Atenção: a pasta é `Diário` com acento. Em paths bash use aspas duplas.

## Ferramentas disponíveis

Dois scripts em `~/.claude/scripts/`:

### `obsidian-session-scan.js`
Varre `~/.claude/projects/*/` e extrai info de `.jsonl` de uma data (ou sessão específica).

```bash
node ~/.claude/scripts/obsidian-session-scan.js                      # hoje
node ~/.claude/scripts/obsidian-session-scan.js 2026-04-15           # outra data
node ~/.claude/scripts/obsidian-session-scan.js --session <uuid>     # 1 sessão
```

Output: JSON com `sessionId`, `cwd`, `firstTs`, `lastTs`, `turnCount`, `commandNames`, `toolsUsed`, `filesEdited`, `bashCommandsSample`, `userPromptSamples`, `gitOrigin`, `gitBranch`.

### `obsidian-session-format.js`
Formata a saída do scanner em markdown pronto pra colar na daily note.

```bash
node ~/.claude/scripts/obsidian-session-format.js --list             # tabela resumida
node ~/.claude/scripts/obsidian-session-format.js --full             # recap multi-sessão
node ~/.claude/scripts/obsidian-session-format.js --auto <uuid>      # seção compacta de 1 sessão
```

## Workflow por modo

### MODO: current (rico, análise manual)

1. `date +%Y-%m-%d` pra data e `date +%H:%M` pra hora
2. Verifica se `Diário/YYYY-MM-DD.md` já existe
3. Olhe pra trás na conversa ATUAL e extraia:
   - **Tarefas concluídas** — o que foi pedido e entregue
   - **Arquivos criados/modificados** — só os relevantes
   - **Comandos importantes** — installs, deploys, migrations, SSH remotos
   - **Decisões** — escolhas técnicas e rationale
   - **Problemas encontrados** — bugs, erros e resolução
   - **Pendências** — o que ficou pra depois
4. Agrupa por **projeto/categoria**, não por ordem cronológica
5. Escreve no formato da **Seção rica** (abaixo)
6. Se já existe a daily note → APPEND (nunca sobrescrever)
7. Se não existe → cria com header `# YYYY-MM-DD — Recap do dia`

### MODO: full (consolidação automática)

1. Roda `node ~/.claude/scripts/obsidian-session-scan.js <date>` pra pegar JSON completo
2. Mostra ao usuário uma **tabela resumo** (use `--list`) com quantas sessões foram detectadas
3. Confirma: "Detectei N sessões do dia, consolido todas?"
4. Se sim, roda `--full` e appenda o resultado na daily note
5. Para as sessões que casam com projetos conhecidos no vault, adiciona `[[Projetos/X]]` se identificável pelo CWD
6. Inclui Session IDs curtos (8 primeiros chars) e links GitHub quando `gitOrigin` existe

### MODO: pick (usuário escolhe)

1. Roda `--list` e mostra a tabela ao usuário
2. Pergunta: "quais quer detalhar? (números separados por vírgula, ou 'todas')"
3. Para cada escolhida, roda `--auto <sessionId>` e concatena as seções
4. Appenda o bloco na daily note

## Seção rica (modo current)

```markdown
## 🤖 Claude Code — HH:MM

### O que foi feito
- **<Projeto/Categoria>** — <descrição curta>
  - <detalhe 1>
  - <detalhe 2>

### Arquivos tocados
- `caminho/arquivo.md` — <o que mudou>

### 🛠 Ações remotas / infra
- `<comando>` — <resultado>

### Decisões
- **<Decisão>** — <rationale>

### 📅 Pendências
- [ ] <item>

*[Registrado por: DESKTOP — YYYY-MM-DD HH:MM]*
```

Se for criar a daily note do zero, prefixe com:

```markdown
# YYYY-MM-DD — Recap do dia
```

## Seção compacta (modo full/pick/auto)

Gerada pelos scripts. Inclui:
- Sessão ID (curto e completo)
- Diretório de trabalho
- Repo + branch (quando for git)
- Contagem de turnos
- Slash commands usados
- Top tools com contagem
- Amostra de pedidos do usuário (até 3)
- Arquivos tocados (até 10)

Exemplo:
```markdown
## 🤖 Claude Code — 14:32 (auto)

**Sessão:** `77a3f3db-699a-46be-8132-b90b70dff5e6`
**Diretório:** `~/Desktop/singular/onboarding`
**Repo:** https://github.com/pedrormc/onboarding (`main`)
**Turnos:** 12

### Slash commands
- `/ship`

### Ferramentas
Edit×24, Bash×18, Read×11, TaskUpdate×6
...
```

## Modo automático via hook

O hook `~/.claude/hooks/obsidian-auto-save.sh` é chamado em `SessionEnd` (e `Stop` com `reason=exit|logout`). Ele:

- Extrai `session_id` do payload recebido via stdin
- Roda `obsidian-session-format.js --auto <id>` pra gerar a seção compacta
- Appenda na daily note do dia (cria se não existe)
- Marca um arquivo marker pra não duplicar no caso de re-firing
- É silencioso (nunca imprime em stdout/stderr)

**Não invoque esse fluxo manualmente pela skill** — ele é para o exit. Quando usuário digita `/obsidian`, use os modos acima (current/full/pick), que geram recap mais rico.

## Regras de segurança (CRÍTICAS)

- **NUNCA** copie valores de secrets (API keys, tokens, senhas, .env, credentials).
- Pode descrever que `<serviço> foi configurado com credenciais X` — sem o valor.
- Se encontrar secret na conversa (modo `current`), registre como `[credencial registrada — ver env local]`.

### Sanitização automática (modos full/pick/auto)

O scanner aplica **redação de secrets** antes de emitir dados:

| Padrão | Cobertura |
|--------|-----------|
| Private keys (PEM) | `-----BEGIN ... PRIVATE KEY-----` blocks |
| Prefixos conhecidos | `sk-`, `sk_live_`, `sk_test_`, `xoxb-`, `ghp_`, `AKIA…`, `AIza…`, JWT `eyJ…` |
| Keyword contexts | `api_key/token/password/secret/credential/bearer = VALOR` |
| ENV patterns | `*_PASSWORD`, `*_SECRET`, `*_TOKEN`, `*_APIKEY`, `*_PRIVATE`, `*_CREDENTIAL`, `*_AUTH`, `*_PWD` = `VALOR` |
| URL basic auth | `scheme://user:pass@host` → `scheme://user:[REDACTED]@host` |
| Blobs de alta entropia | hex >= 40 chars, base64 >= 50 chars |

Os scripts só acessam **metadados**: nomes de tools, paths de arquivos, comandos bash (truncados), e amostras de prompts do usuário (com redação). **Não copiam outputs de tools** — isso garante que secrets em respostas de API/env nunca entram na nota.

Se identificar um padrão que escapou da redação, atualize `SECRET_RULES` em `~/.claude/scripts/obsidian-session-scan.js`.

## Confirmação antes de escrever

- Sessão longa (>10 turnos) ou complexa → mostre preview da seção e peça "posso gravar?"
- Sessão trivial (3-5 turnos) → pode escrever direto
- Modo `full` ou `pick` → sempre confirmar antes (envolve múltiplas sessões)

## Estilo

- PT-BR informal, direto, casual (segue standing orders do vault)
- Sem emojis exceto os do padrão (`🤖`, `✅`, `📅`, `🔗`, `🛠`)
- Linguagem de engenheiro, não de diário pessoal
- Curto e objetivo, agrupando por projeto

## Quando NÃO registrar (modo current)

- Sessão só tem perguntas triviais sem ação executada
- Usuário cancelou/rejeitou as ações propostas
- Conversa é exploração/research sem artefatos gerados

Nesses casos, pergunte: "A sessão teve pouco trabalho concreto — registrar mesmo assim ou pular hoje?"

Se o usuário ainda assim quiser, ofereça o modo `full`/`pick` que pega contexto de outras sessões do dia.

## Output ao final

Depois de escrever, responda ao usuário com:
1. Path do arquivo salvo
2. Se foi criado novo ou appended
3. Resumo de 1 linha do que entrou
4. Em modo `full`/`pick`: quantas sessões foram incluídas

## Exemplo real

Ver `C:/Users/teste/Documents/obsidiano/Diário/2026-04-15.md` pro formato rico e `C:/Users/teste/Documents/obsidiano/Diário/2026-04-07.md` pro padrão original do vault.
