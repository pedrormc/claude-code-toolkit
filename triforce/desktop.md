# Desktop (Master) — Setup das 3 Abas

> **Ambiente principal do Pedro.** Tem permissão total. Single source of truth pra estrutura física do `plano/`.

## Localização

```
C:\Users\teste\plano\
├── PRIORIDADE.md
├── INDEX.md
├── plano\        [99999]
├── singular\     [100]
└── skip\         [101]
```

## Carregamento da regra

A regra é carregada via:

1. `~/.claude/CLAUDE.md` — seção "REGRA SOBERANA — 3 Abas Master" (visível em toda sessão).
2. `~/.claude/rules/common/three-tabs-priority.md` — referenciada pelas regras comuns.
3. `~/.claude/triforce/three-tabs-config.md` — fonte de verdade canônica.

## Fluxo de input

Quando o Pedro registra algo no Desktop:

```
Input → 3 crivos → categoria → escreve em C:\Users\teste\plano\<aba>\<sub>\<arquivo>.md
                            → linka no INDEX.md (se marco)
                            → atualiza memory do projeto se mudou diretiva
```

## Comandos úteis

```bash
# Ver estrutura
ls C:/Users/teste/plano/

# Adicionar item rápido em plano/ideias
echo "..." > C:/Users/teste/plano/plano/ideias/$(date +%Y%m%d-%H%M)-titulo.md

# Sync com Obsidian (manual — tem rule namespace-cheatsheet)
# Obsidian já está em C:/Users/teste/Documents/obsidiano/
```

## Sincronização com Obsidian

A pasta `C:\Users\teste\plano\` é independente do vault, mas o vault tem espelho em `Pessoal/plano/`. Após criar item importante, registrar paralelo no vault via MCPVault.

*[Registrado por: DESKTOP — 2026-04-26]*
