# Prompt para Agente Claude Code na VPS — Docker Sandbox Setup

> **Como usar:** Copie tudo abaixo do `---` e cole como primeira mensagem no Claude Code da VPS.
> Preencha os valores `__PLACEHOLDER__` antes de enviar.

---

Voce vai configurar um ambiente Docker sandbox seguro para rodar Claude Code isolado nesta VPS. Siga cada passo na ordem. Nao pergunte — execute.

## DADOS (preencher antes de enviar)

```
ANTHROPIC_API_KEY="__SUA_ANTHROPIC_API_KEY__"
```

## PASSO 1 — Pre-requisitos

Verifique que Docker e Docker Compose estao instalados:

```bash
docker --version
docker compose version
git --version
```

Se Docker nao estiver instalado:
```bash
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
# IMPORTANTE: relogue na VPS depois deste comando para o grupo ter efeito
```

Se Docker Compose v2 nao estiver disponivel:
```bash
sudo apt-get update && sudo apt-get install -y docker-compose-plugin
```

## PASSO 2 — Clonar o toolkit

```bash
git clone https://github.com/pedrormc/claude-code-toolkit.git ~/claude-code-toolkit
cd ~/claude-code-toolkit
```

## PASSO 3 — Configurar environment

```bash
cd ~/claude-code-toolkit/docker
cp .env.example .env
```

Edite o arquivo `.env` e coloque a `ANTHROPIC_API_KEY` com o valor fornecido acima no bloco DADOS. Nao coloque nenhum outro placeholder — so a API key e obrigatoria.

## PASSO 4 — Criar workspace

O workspace e o UNICO diretorio do host que o container pode acessar. Crie ele:

```bash
mkdir -p ~/claude-workspace
```

Edite o `.env` e ajuste o `WORKSPACE_PATH`:
```
WORKSPACE_PATH=/root/claude-workspace
```

(Ou o home dir correto do usuario da VPS, ex: `/home/ubuntu/claude-workspace`)

## PASSO 5 — Build da imagem

```bash
cd ~/claude-code-toolkit
docker compose -f docker/docker-compose.yml build
```

Esse build vai:
- Baixar node:20-slim
- Instalar dependencias do sistema (git, iptables, ripgrep, etc.)
- Instalar Claude Code via npm
- Copiar todo o toolkit (5 agents, 16 rules, 8 skills, scripts, statusline)
- Configurar usuario non-root `coder`

O build pode demorar uns 3-5 minutos na primeira vez.

## PASSO 6 — Testar o container

```bash
cd ~/claude-code-toolkit/docker
docker compose run --rm claude bash -c "echo 'Container OK' && whoami && claude --version"
```

Esperado:
- `Container OK`
- `coder` (nao root)
- Versao do Claude Code

## PASSO 7 — Testar o firewall

```bash
cd ~/claude-code-toolkit/docker
docker compose run --rm claude bash -c "\
  echo '=== Testing allowed ===' && \
  curl -s --max-time 5 https://api.anthropic.com/ > /dev/null && echo 'OK: Anthropic API' || echo 'FAIL: Anthropic API' && \
  curl -s --max-time 5 https://github.com/ > /dev/null && echo 'OK: GitHub' || echo 'FAIL: GitHub' && \
  echo '=== Testing blocked ===' && \
  curl -s --max-time 3 https://google.com/ > /dev/null && echo 'FAIL: Google should be blocked' || echo 'BLOCKED: Google (expected)' && \
  curl -s --max-time 3 https://facebook.com/ > /dev/null && echo 'FAIL: Facebook should be blocked' || echo 'BLOCKED: Facebook (expected)'"
```

Esperado:
- Anthropic API: OK
- GitHub: OK
- Google: BLOCKED
- Facebook: BLOCKED

Se o firewall nao ativou (mensagem "NET_ADMIN capability not available"), verifique que o docker-compose.yml tem `cap_add: NET_ADMIN` e `cap_add: NET_RAW`.

## PASSO 8 — Instalar plugins (dentro do container)

```bash
cd ~/claude-code-toolkit/docker
docker compose run --rm claude bash -c "\
  claude plugins install everything-claude-code --marketplace everything-claude-code && \
  claude plugins install superpowers --marketplace superpowers-marketplace && \
  claude plugins install ralph-skills --marketplace ralph-marketplace && \
  claude plugins install ui-ux-pro-max --marketplace ui-ux-pro-max-skill && \
  echo 'Plugins instalados:' && claude plugins list"
```

Os plugins ficam persistidos no volume `claude-code-config`.

## PASSO 9 — Rodar Claude Code interativo

```bash
cd ~/claude-code-toolkit/docker
docker compose run --rm claude
```

Dentro do container:
```bash
claude
```

Isso abre o Claude Code interativo dentro do sandbox. Ele so pode acessar `/workspace` (que e o `~/claude-workspace` do host).

## PASSO 10 — Criar aliases para uso diario

Adicione ao `~/.bashrc` ou `~/.zshrc` da VPS:

```bash
# Claude Code sandbox aliases
alias claude-sandbox='cd ~/claude-code-toolkit/docker && docker compose run --rm claude'
alias claude-shell='cd ~/claude-code-toolkit/docker && docker compose run --rm claude bash'
alias claude-headless='cd ~/claude-code-toolkit/docker && docker compose run --rm --profile headless claude-headless'
alias claude-rebuild='cd ~/claude-code-toolkit && docker compose -f docker/docker-compose.yml build --no-cache'
```

Depois: `source ~/.bashrc`

Uso:
- `claude-sandbox` — abre bash no container, rode `claude` manualmente
- `claude-shell` — mesma coisa
- `claude-headless` — roda prompt automatico (definido no .env)
- `claude-rebuild` — rebuild da imagem apos updates no toolkit

## PASSO 11 — Validacao final

Rode e me mostre a saida:

```bash
echo "=== Docker ===" && docker --version && docker compose version
echo "=== Image ===" && docker images | grep claude
echo "=== Volumes ===" && docker volume ls | grep claude
echo "=== Workspace ===" && ls -la ~/claude-workspace/
echo "=== .env (sem secrets) ===" && grep -v "API_KEY" ~/claude-code-toolkit/docker/.env
echo "=== Firewall test ===" && cd ~/claude-code-toolkit/docker && docker compose run --rm claude bash -c "curl -s --max-time 3 https://google.com/ > /dev/null 2>&1 && echo 'FIREWALL FAIL' || echo 'FIREWALL OK'"
```

## RESUMO ESPERADO

```
DOCKER SANDBOX SETUP COMPLETO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Image:       claude-sandbox (built)
User:        coder (non-root)
Workspace:   ~/claude-workspace → /workspace
Firewall:    ACTIVE (whitelist only)
Plugins:     4/4 installed
Volumes:     claude-code-config, claude-code-history
Aliases:     claude-sandbox, claude-shell, claude-headless
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Se houver qualquer erro, tente resolver automaticamente. So pergunte se nao conseguir resolver sozinho.
