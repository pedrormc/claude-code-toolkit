# Claude Code Sandbox — Docker

Container isolado e seguro para rodar Claude Code sem acesso ao host.

## Seguranca

| Camada | O que faz |
|--------|-----------|
| **Filesystem** | Apenas `/workspace` montado — nenhum outro dir do host acessivel |
| **Network firewall** | iptables whitelist: so Anthropic API, npm, GitHub, DNS |
| **Capabilities** | `cap_drop: ALL` + apenas NET_ADMIN/NET_RAW para firewall |
| **User** | Roda como `coder` (uid 1000), nunca root |
| **no-new-privileges** | Container nao pode escalar privilegios |
| **Resource limits** | Max 4 CPUs, 8GB RAM |
| **tmpfs** | `/tmp` em memoria, nao persiste |

## Quick Start

```bash
# 1. Clone o toolkit
git clone https://github.com/pedrormc/claude-code-toolkit.git
cd claude-code-toolkit/docker

# 2. Configure
cp .env.example .env
nano .env  # coloque sua ANTHROPIC_API_KEY

# 3. Crie o workspace
mkdir -p ../workspace

# 4. Build e rode
docker compose build
docker compose run --rm claude
```

## Modos de Uso

### Interativo (padrao)
```bash
# Abre um bash — rode claude manualmente
docker compose run --rm claude

# Dentro do container:
claude
```

### Interativo direto
```bash
docker compose run --rm --profile interactive claude-interactive
```

### Headless (automacao)
```bash
CLAUDE_PROMPT="Review the code for security issues" \
docker compose run --rm --profile headless claude-headless
```

### Projeto especifico
```bash
WORKSPACE_PATH=/home/user/meu-projeto \
docker compose run --rm claude
```

## Persistencia

| Volume | Conteudo | Persiste? |
|--------|----------|-----------|
| `claude-code-config` | ~/.claude/ (config, credenciais, memoria) | Sim |
| `claude-code-history` | Historico de bash | Sim |
| Workspace bind mount | Seu codigo | Sim (host) |

Resetar config: `docker volume rm claude-code-config`
Resetar tudo: `docker compose down -v`

## Verificar Firewall

Dentro do container:
```bash
# Deve funcionar
curl -s https://api.anthropic.com/ && echo "OK: Anthropic API"
curl -s https://github.com/ > /dev/null && echo "OK: GitHub"

# Deve ser bloqueado
curl -s --max-time 3 https://google.com/ || echo "BLOCKED (expected)"
```

## Instalar Plugins (primeira vez)

```bash
docker compose run --rm claude bash -c "\
  claude plugins install everything-claude-code --marketplace everything-claude-code && \
  claude plugins install superpowers --marketplace superpowers-marketplace && \
  claude plugins install ralph-skills --marketplace ralph-marketplace && \
  claude plugins install ui-ux-pro-max --marketplace ui-ux-pro-max-skill"
```

Plugins ficam salvos no volume `claude-code-config`.
