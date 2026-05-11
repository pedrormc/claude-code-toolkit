# Google Drive MCP — Manual Completo de Instalação

> Esse é o setup **mais demorado** do ecossistema. Reserva **45-60 minutos** ininterruptos.
> Não pula etapa, não chuta valor. Cada passo importa.
>
> **Pré-requisitos:** Node v20+, Codex CLI instalado, conta Google ativa (de preferência a do trabalho — a mesma que tem acesso ao Drive onde estão os documentos).

---

## 0) O que é o Google Drive MCP

É o plugin que dá ao Codex acesso completo às APIs do Google Workspace:

- **Drive:** listar, criar, mover, renomear, deletar arquivos/pastas
- **Docs:** criar/editar Google Docs, formatar, find-and-replace, comentários
- **Sheets:** criar/editar planilhas, fórmulas, formatação condicional, named ranges
- **Slides:** criar/editar apresentações, shapes, imagens, layouts
- **Calendar:** criar/atualizar eventos, listar agendas, sugerir horários
- **Permissions:** compartilhar arquivos, gerenciar acesso

**Pacote:** `@piotr-agier/google-drive-mcp` (npm)

### Por que OAuth (e não API key simples)?

Diferente de HubSpot/n8n que usam um único token, o Google **força OAuth** porque:

1. **Você está acessando dados de uma conta de pessoa real**, não só endpoint público
2. O Google quer que **você autorize cada scope explicitamente** (Drive vs Calendar vs Gmail)
3. **Tokens curtos + refresh tokens** — mais seguro que API key estática

Tradução: dá mais trabalho **uma vez**, mas é o jeito certo. Depois de configurado, esquece.

---

## 1) Visão geral dos passos

```
┌─────────────────────────────────────────────────────────────┐
│ FASE 1 — Google Cloud Console (no navegador)                │
│   1.1) Criar projeto                                         │
│   1.2) Habilitar 5 APIs (Drive, Docs, Sheets, Slides, Cal)  │
│   1.3) Configurar OAuth Consent Screen                       │
│   1.4) Criar OAuth Credentials (Desktop app)                 │
│   1.5) Baixar o JSON                                         │
├─────────────────────────────────────────────────────────────┤
│ FASE 2 — Instalação local (no terminal)                     │
│   2.1) Instalar pacote npm                                   │
│   2.2) Criar pasta secrets                                   │
│   2.3) Mover JSON pra pasta correta                          │
│   2.4) Configurar no Codex                                   │
├─────────────────────────────────────────────────────────────┤
│ FASE 3 — Primeiro auth (no navegador + terminal)            │
│   3.1) Disparar primeiro uso do MCP                          │
│   3.2) Autorizar acesso no navegador                         │
│   3.3) Confirmar que o token.json foi gerado                 │
├─────────────────────────────────────────────────────────────┤
│ FASE 4 — Validação                                           │
│   4.1) Smoke test                                            │
└─────────────────────────────────────────────────────────────┘
```

---

# FASE 1 — Google Cloud Console

## 1.1) Criar projeto no Google Cloud

1. Vai em **https://console.cloud.google.com/**
2. Loga com a conta Google que tem acesso ao Drive (a mesma do email do trabalho, provavelmente)
3. No topo da página, do lado do logo "Google Cloud", tem um **dropdown de projeto**. Clica nele.
4. Clica em **"NEW PROJECT"** (canto superior direito do modal)
5. **Project name:** `codex-mcp-singular` (ou outro nome reconhecível pra você)
6. **Organization:** se aparecer, deixa como está
7. **Location:** deixa "No organization" se for a primeira vez
8. Clica **CREATE**
9. Espera ~30s, no topo aparece uma notificação quando o projeto está pronto
10. Clica no nome do projeto no dropdown pra "entrar" nele

> **Como saber se você está no projeto certo?** Olha o topo da página, do lado do logo Google Cloud — tem que aparecer `codex-mcp-singular` (ou o nome que você deu).

## 1.2) Habilitar as APIs necessárias

Você precisa habilitar **5 APIs**. Vou listar e dar o link direto pra cada:

| API | Link direto (com seu projeto ativo) |
|---|---|
| Google Drive API | https://console.cloud.google.com/apis/library/drive.googleapis.com |
| Google Docs API | https://console.cloud.google.com/apis/library/docs.googleapis.com |
| Google Sheets API | https://console.cloud.google.com/apis/library/sheets.googleapis.com |
| Google Slides API | https://console.cloud.google.com/apis/library/slides.googleapis.com |
| Google Calendar API | https://console.cloud.google.com/apis/library/calendar-json.googleapis.com |

**Pra cada uma:**
1. Abre o link
2. Confere que o projeto correto está selecionado no topo
3. Clica **ENABLE**
4. Espera carregar (5-10s)
5. Volta e abre o próximo link

> **Atalho:** se você não quiser clicar 5 vezes, dá pra fazer via terminal depois (ver Apêndice A). Mas pelo console é mais visual e fica claro o que cada API faz.

**Checkpoint:** depois de habilitar todas 5, vai em **APIs & Services → Enabled APIs & services** (menu esquerdo) — deve listar as 5.

## 1.3) Configurar OAuth Consent Screen

Antes de criar credenciais, o Google exige que você diga **"quem é esse app e o que ele faz"**.

1. Menu esquerdo: **APIs & Services → OAuth consent screen**
2. **User Type:** escolhe **"External"** (a menos que você tenha Google Workspace de empresa e queira "Internal" — External é mais simples e funciona pra todo mundo)
3. Clica **CREATE**

Agora preenche o formulário:

### Tela 1 — OAuth consent screen

- **App name:** `Codex MCP - Singular` (ou outro nome que você lembre)
- **User support email:** seu email
- **App logo:** pode pular
- **Application home page / privacy policy / terms:** pode pular (pode preencher com qualquer URL pública, ex: `https://singular.group`)
- **Authorized domains:** pode pular
- **Developer contact information:** seu email
- Clica **SAVE AND CONTINUE**

### Tela 2 — Scopes

1. Clica **ADD OR REMOVE SCOPES**
2. Na busca, procura cada um e marca o checkbox:

| Scope (cola na busca) | API |
|---|---|
| `.../auth/drive` | Drive — acesso completo |
| `.../auth/documents` | Docs — leitura/escrita |
| `.../auth/spreadsheets` | Sheets — leitura/escrita |
| `.../auth/presentations` | Slides — leitura/escrita |
| `.../auth/calendar` | Calendar — leitura/escrita |
| `.../auth/calendar.events` | Calendar events |

> **Dica:** depois de marcar, role pra baixo, eles ficam listados em "Your sensitive scopes" / "Your restricted scopes". O Drive é considerado "restricted" — é normal.

3. **UPDATE** no fim do modal
4. **SAVE AND CONTINUE** na tela principal

### Tela 3 — Test users

Enquanto o app está em modo "Testing" (não publicado), só **test users autorizados** podem usar. Você precisa se adicionar.

1. Clica **ADD USERS**
2. Cola seu email Google (o mesmo que você usa pra logar no Drive)
3. **ADD**
4. **SAVE AND CONTINUE**

### Tela 4 — Summary

Revisa e clica **BACK TO DASHBOARD**.

> **Sobre "Publishing status":** vai aparecer "Testing" — está OK. Você pode usar até **100 test users** sem precisar publicar formalmente. NÃO clica em "Publish App" — isso inicia processo de review do Google que leva semanas e é desnecessário pra uso interno.

## 1.4) Criar OAuth Credentials

1. Menu esquerdo: **APIs & Services → Credentials**
2. Topo da página: **CREATE CREDENTIALS** → **OAuth client ID**
3. **Application type:** escolhe **Desktop app** (importante! não é Web nem outras)
4. **Name:** `Codex MCP Desktop Client`
5. **CREATE**

Vai aparecer um modal com **Client ID** e **Client secret**.

## 1.5) Baixar o JSON

1. No modal, clica **DOWNLOAD JSON**
2. Salva o arquivo. Ele vem com nome tipo `client_secret_xxxxx.apps.googleusercontent.com.json`
3. Renomeia pra **`gcp-oauth.keys.json`** (exato esse nome)
4. Guarda em local conhecido — vamos mover ele pro lugar certo na Fase 2

**Checkpoint:** você agora tem um arquivo `gcp-oauth.keys.json` no seu Downloads (ou onde salvou). Conteúdo dele é tipo:
```json
{
  "installed": {
    "client_id": "xxxxx-xxxxx.apps.googleusercontent.com",
    "project_id": "codex-mcp-singular",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    ...
  }
}
```

> **⚠️ Esse arquivo é credencial.** Trata como senha. NÃO commita em Git, NÃO compartilha em chat público.

---

# FASE 2 — Instalação local

## 2.1) Instalar o pacote npm

No terminal:
```bash
npm install -g @piotr-agier/google-drive-mcp
```

Confere onde foi instalado:
```bash
npm root -g
```

Anota esse path — vamos usar em 2.4. Exemplos:
- **Windows:** `C:\Users\Simon\AppData\Roaming\npm\node_modules`
- **Mac:** `/usr/local/lib/node_modules` ou `/opt/homebrew/lib/node_modules`
- **Linux:** `/usr/lib/node_modules` ou `~/.npm-global/lib/node_modules`

O caminho COMPLETO do MCP fica:
```
<NPM_ROOT_GLOBAL>/@piotr-agier/google-drive-mcp/dist/index.js
```

Valida que existe:
```bash
ls "<NPM_ROOT_GLOBAL>/@piotr-agier/google-drive-mcp/dist/index.js"
```

Tem que listar o arquivo. Se der "No such file", a instalação npm falhou — repete o `npm install -g`.

## 2.2) Criar pasta de secrets

```bash
mkdir -p ~/.codex/secrets
```

Confere:
```bash
ls -la ~/.codex/secrets
```

(Vai estar vazio, sem problema.)

## 2.3) Mover o JSON pra pasta correta

Pega o `gcp-oauth.keys.json` que você baixou e move pra `~/.codex/secrets/`:

**Windows (Git Bash):**
```bash
mv ~/Downloads/gcp-oauth.keys.json ~/.codex/secrets/
```

**Mac/Linux:**
```bash
mv ~/Downloads/gcp-oauth.keys.json ~/.codex/secrets/
```

Confere:
```bash
ls -la ~/.codex/secrets/
```

Deve listar: `gcp-oauth.keys.json`.

## 2.4) Configurar no Codex

**Método A — via CLI:**
```bash
codex mcp add google-drive \
  --env GOOGLE_DRIVE_OAUTH_CREDENTIALS="$HOME/.codex/secrets/gcp-oauth.keys.json" \
  --env GOOGLE_DRIVE_MCP_TOKEN_PATH="$HOME/.codex/secrets/gcp-oauth.token.json" \
  -- node "<NPM_ROOT_GLOBAL>/@piotr-agier/google-drive-mcp/dist/index.js"
```

Substitui `<NPM_ROOT_GLOBAL>` pelo path real que você anotou em 2.1.

**Método B — via `~/.codex/config.toml`:**

Abre o arquivo e adiciona no final:

```toml
[mcp_servers.google-drive]
command = "node"
args = ["C:/Users/Simon/AppData/Roaming/npm/node_modules/@piotr-agier/google-drive-mcp/dist/index.js"]
env = { GOOGLE_DRIVE_OAUTH_CREDENTIALS = "C:/Users/Simon/.codex/secrets/gcp-oauth.keys.json", GOOGLE_DRIVE_MCP_TOKEN_PATH = "C:/Users/Simon/.codex/secrets/gcp-oauth.token.json" }
```

> **Importantíssimo:** no Windows, os paths usam **barra normal `/`** (não invertida `\`) no `config.toml`. Mac/Linux também usa `/`.
>
> Substitui `Simon` pelo nome de usuário real do seu Windows. Pra descobrir: `echo $HOME` no Git Bash, ou `echo $env:USERPROFILE` no PowerShell.

### Validar config

```bash
codex mcp list
```

Deve aparecer `google-drive` na lista. Se não aparecer, releia 2.4 — geralmente é typo no path.

---

# FASE 3 — Primeiro auth (gera o token.json)

## 3.1) Disparar o primeiro uso

```bash
codex
```

Dentro do REPL:

```
> Liste os 5 arquivos mais recentes do meu Google Drive.
```

Na primeira execução, o MCP vai detectar que **não tem token.json ainda**, e vai abrir um link no terminal/navegador.

Pode aparecer algo tipo:
```
[google-drive] Authorize this app by visiting this url:
https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=...
```

## 3.2) Autorizar no navegador

1. **Copia o link** completo do terminal
2. **Cola no navegador** (importante: navegador onde você está logado com a conta Google certa)
3. Vai aparecer "Choose an account" — escolhe a sua
4. **Tela de aviso:** "Google hasn't verified this app" → clica em **Advanced** → **Go to Codex MCP - Singular (unsafe)**
   > Isso é normal porque o app está em modo "Testing". Como você é test user, pode prosseguir.
5. Tela de permissões: lista tudo que o app vai acessar (Drive, Docs, Sheets, Slides, Calendar). Clica **Continue** / **Allow** em tudo.
6. Vai redirecionar pra uma página tipo `localhost:8080/?code=4/0AS...` ou similar — **isso é esperado**, significa que funcionou.
7. Volta pro terminal. O MCP detecta o callback e grava o token automaticamente.

## 3.3) Confirmar que o token foi gerado

Em um terminal separado:
```bash
ls -la ~/.codex/secrets/
```

Agora tem que aparecer **dois arquivos**:
- `gcp-oauth.keys.json` (você baixou)
- `gcp-oauth.token.json` (o MCP gerou agora)

Se só tem o `.keys.json`, o auth flow falhou. Repete 3.1.

---

# FASE 4 — Validação

## 4.1) Smoke tests

Dentro do `codex`:

```
> Lista 5 arquivos do meu Google Drive.
```

```
> Cria um Google Doc chamado "Teste Codex MCP" com o texto "funcionou!".
```

```
> Lista meus calendários no Google Calendar.
```

```
> Cria uma planilha "Teste Sheet" com colunas A=Nome, B=Email, C=Telefone.
```

Se todos retornam resposta coerente, **você está 100% configurado**. 🎯

---

# 5) Troubleshooting

### Erro `redirect_uri_mismatch` no navegador
- O OAuth client é tipo "Web" em vez de "Desktop". Volta no §1.4 e recria como Desktop.

### "Access blocked: Codex MCP - Singular has not completed verification"
- Você não está como test user. Volta no §1.3 (tela "Test users") e adiciona seu email.
- Espera 5 minutos pro Google propagar a mudança.

### "invalid_grant" ou "Token has been expired or revoked"
- O refresh token quebrou. Deleta o token e refaz o auth:
  ```bash
  rm ~/.codex/secrets/gcp-oauth.token.json
  ```
- Repete §3.1.

### MCP aparece em `codex mcp list` mas nada funciona
- Olha o log: `codex mcp logs google-drive`
- 90% é path errado no `config.toml`. Confere com `ls` no path exato.

### "Cannot find module" ao rodar o MCP
- O npm install global falhou. Reinstala:
  ```bash
  npm uninstall -g @piotr-agier/google-drive-mcp
  npm install -g @piotr-agier/google-drive-mcp
  ```

### Windows: paths com backslash `\` quebram
- `config.toml` requer `/` em vez de `\`. Mesmo no Windows.

### "Insufficient Permission" ao tentar criar/editar
- Você não habilitou todas as 5 APIs no §1.2. Vai em **APIs & Services → Enabled APIs** e confere.
- OU você não marcou todos os scopes em §1.3 (tela 2). Refaz o consent screen e re-autoriza (apaga o token e refaz auth).

### Token expira sempre depois de 7 dias
- Isso é o **comportamento default** do Google quando o app está em modo "Testing". Refresh tokens em apps não publicados expiram em 7 dias.
- **Soluções:**
  - **A (recomendada):** convive — toda semana você roda o auth flow de novo (5 min).
  - **B:** publica o app no console (sem submeter pra review). Vai em **OAuth consent screen → PUBLISH APP → CONFIRM**. Aviso: vai dizer que precisa de verification, mas você pode ignorar e funciona — só com aviso "Google hasn't verified". Refresh tokens passam a durar **6 meses**.

---

# 6) Segurança — checklist

- [ ] `gcp-oauth.keys.json` e `gcp-oauth.token.json` **NÃO** estão em pasta com Git
- [ ] Você não compartilhou esses arquivos com ninguém
- [ ] Se o laptop sumir: vai em **https://console.cloud.google.com/apis/credentials**, acha o OAuth client e clica **RESET SECRET** (gera novo, invalida o atual)
- [ ] Se vazar suspeita de uso indevido: vai em **https://myaccount.google.com/permissions** e revoga o acesso do app "Codex MCP - Singular"

---

# 7) Próximo passo

Se HubSpot e Google Drive funcionam, você tem **acesso ao núcleo do ecossistema**. Daqui pra frente:

- **Evolution API (WhatsApp):** Pedro vai te mandar credenciais separadamente. Setup tá em `skills/whatsapp-evolution/SKILL.md`.
- **n8n:** se você for usar workflows, pede credenciais.
- **SerpAPI:** se for usar busca Google, pede URL.
- **TestSprite:** opcional, pra geração automática de testes E2E.

---

# Apêndice A — Habilitar APIs via gcloud CLI (opcional)

Se você instalou `gcloud` CLI, dá pra habilitar todas as APIs de uma vez:

```bash
gcloud config set project codex-mcp-singular

gcloud services enable \
  drive.googleapis.com \
  docs.googleapis.com \
  sheets.googleapis.com \
  slides.googleapis.com \
  calendar-json.googleapis.com
```

Mas isso requer ter o gcloud instalado — se você não tem, vale mais a pena fazer pelo console mesmo.

---

# Apêndice B — Arquitetura do auth flow (pra quem quiser entender)

```
┌──────────┐                ┌──────────────┐              ┌────────────┐
│  Codex   │────A──────────▶│ google-drive │              │   Google   │
│   REPL   │                │     MCP      │              │    Auth    │
└──────────┘                └──────────────┘              └────────────┘
                                   │                              ▲
                                   │ B: lê keys.json              │
                                   │                              │
                                   │ C: gera URL OAuth ───────────┘
                                   │
                                   ▼
                            ┌──────────────┐              ┌────────────┐
                            │  Terminal    │              │ Navegador  │
                            │  (cola URL)  │──D──────────▶│   (você    │
                            └──────────────┘              │  autoriza) │
                                   ▲                      └────────────┘
                                   │                              │
                                   │ F: token gravado             │
                                   │    em token.json             │ E: redirect com code
                                   │                              ▼
                            ┌──────────────┐              ┌────────────┐
                            │ token.json   │◀─────────────│ localhost  │
                            └──────────────┘              │   :8080    │
                                                          └────────────┘
```

Resumindo:
- **A:** Codex pede algo ao MCP
- **B:** MCP carrega credentials
- **C:** Gera URL de auth (primeira vez)
- **D:** Você copia URL → cola no browser
- **E:** Browser autoriza → redireciona pro localhost
- **F:** MCP escuta o callback → grava token

Depois de F, próximas requests usam o token direto. Token expira → MCP usa refresh token automaticamente. Refresh token expira → você refaz tudo a partir de C.

---

*[Documento — Singular Group / Toolkit]*
*[Versão: 1.0 / 2026-05-11]*
