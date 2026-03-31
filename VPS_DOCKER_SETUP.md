# Prompt para Agente Claude Code na VPS — Docker Sandbox Setup

> **Como usar:** Copie tudo abaixo do `---` e cole como primeira mensagem no Claude Code da VPS.

---

Voce vai configurar um Docker sandbox seguro para rodar Claude Code isolado nesta VPS. Siga cada passo na ordem. Nao pergunte — execute.

## PASSO 1 — Pre-requisitos

Verifique que Docker e Docker Compose estao instalados:

```bash
docker --version
docker compose version
```

Se Docker nao estiver instalado:
```bash
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
newgrp docker
```

Se Docker Compose v2 nao estiver disponivel:
```bash
sudo apt-get update && sudo apt-get install -y docker-compose-plugin
```

## PASSO 2 — Verificar o toolkit

O repo ja esta clonado em `~/claude/claude-code-toolkit`. Verifique:

```bash
ls ~/claude/claude-code-toolkit/docker/
```

Esperado: Dockerfile, docker-compose.yml, entrypoint.sh, init-firewall.sh, .env.example, README.md

Se nao existir, clone:
```bash
gh repo clone pedrormc/claude-code-toolkit ~/claude/claude-code-toolkit
```

## PASSO 3 — Configurar environment

```bash
cd ~/claude/claude-code-toolkit/docker
cp .env.example .env
```

Edite o `.env` e configure:
- Deixe `ANTHROPIC_API_KEY=` vazio (vamos usar OAuth com Claude Max)
- Ajuste `WORKSPACE_PATH=/home/admin/claude`

## PASSO 4 — Build da imagem

```bash
cd ~/claude/claude-code-toolkit
docker compose -f docker/docker-compose.yml build
```

Se der erro de permissao Docker: `sudo usermod -aG docker admin && newgrp docker` e tente de novo.

O build vai demorar 3-5 minutos na primeira vez.

## PASSO 5 — Testar o container

```bash
cd ~/claude/claude-code-toolkit/docker
docker compose run --rm claude bash -c "echo 'Container OK' && whoami && claude --version"
```

Esperado: Container OK, user coder, versao do Claude Code.

## PASSO 6 — Autenticar com Claude Max

Entre no container e faca login:

```bash
cd ~/claude/claude-code-toolkit/docker
docker compose run --rm claude bash
```

Dentro do container rode:
```bash
claude login
```

Vai aparecer um link e um codigo. Mostre o link e o codigo para eu abrir no navegador e autorizar. Depois que eu confirmar, o login fica salvo no volume Docker e persiste entre sessoes.

IMPORTANTE: Espere eu confirmar que autorizei antes de continuar.

## PASSO 7 — Testar firewall

```bash
cd ~/claude/claude-code-toolkit/docker
docker compose run --rm claude bash -c "\
  echo '=== Allowed ===' && \
  curl -s --max-time 5 https://api.anthropic.com/ > /dev/null && echo 'OK: Anthropic API' || echo 'FAIL: Anthropic' && \
  curl -s --max-time 5 https://github.com/ > /dev/null && echo 'OK: GitHub' || echo 'FAIL: GitHub' && \
  echo '=== Blocked ===' && \
  curl -s --max-time 3 https://google.com/ > /dev/null && echo 'FAIL: Google nao bloqueado' || echo 'BLOCKED: Google (correto)'"
```

## PASSO 8 — Instalar plugins

```bash
cd ~/claude/claude-code-toolkit/docker
docker compose run --rm claude bash -c "\
  claude plugins install everything-claude-code --marketplace everything-claude-code && \
  claude plugins install superpowers --marketplace superpowers-marketplace && \
  claude plugins install ralph-skills --marketplace ralph-marketplace && \
  claude plugins install ui-ux-pro-max --marketplace ui-ux-pro-max-skill"
```

## PASSO 9 — Criar aliases

Adicione ao ~/.bashrc do usuario admin:

```bash
cat >> ~/.bashrc << 'ALIASES'

# Claude Code sandbox
alias claude-sandbox='cd ~/claude/claude-code-toolkit/docker && docker compose run --rm claude'
alias claude-shell='cd ~/claude/claude-code-toolkit/docker && docker compose run --rm claude bash'
alias claude-rebuild='cd ~/claude/claude-code-toolkit && docker compose -f docker/docker-compose.yml build --no-cache'
ALIASES
source ~/.bashrc
```

## PASSO 10 — Validacao final

```bash
echo "=== Docker ===" && docker --version
echo "=== Image ===" && docker images | grep claude
echo "=== Volumes ===" && docker volume ls | grep claude
echo "=== Firewall ===" && cd ~/claude/claude-code-toolkit/docker && docker compose run --rm claude bash -c "curl -s --max-time 3 https://google.com/ > /dev/null 2>&1 && echo 'FIREWALL FAIL' || echo 'FIREWALL OK'"
```

Mostre o resumo:
```
DOCKER SANDBOX SETUP
━━━━━━━━━━━━━━━━━━━━
Image:     OK/FALHA
Auth:      OAuth Claude Max
Firewall:  OK/FALHA
Plugins:   X/4
Aliases:   OK/FALHA
━━━━━━━━━━━━━━━━━━━━
```

Se houver erro, resolva automaticamente. So pergunte se nao conseguir.
