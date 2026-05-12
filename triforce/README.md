# TRIFORCE — Sync de Prioridade entre os 3 Claudes

> **Decretado em 2026-04-26.** Esta pasta consolida a regra das 3 Abas Master pros 3 ambientes Claude do Pedro.

## Os 3 ambientes

| Ambiente | Plataforma | Permissão | Papel |
|----------|------------|-----------|-------|
| **Desktop (Master)** | Windows 11 | Total | Dev principal, decisões arquiteturais |
| **Mobile** | Termux / Poco F5 | Restrita | Consultas leves, captura de ideias on-the-go |
| **VPS** | Docker / AWS Lightsail | Máxima headless | Automações, jobs longos, agendados |

## Arquivos nesta pasta

| Arquivo | Propósito |
|---------|-----------|
| [three-tabs-config.md](./three-tabs-config.md) | **REGRA SOBERANA das 3 abas — fonte de verdade.** |
| [desktop.md](./desktop.md) | Setup específico do Master Desktop. |
| [mobile.md](./mobile.md) | Setup específico do Mobile / Termux. |
| [vps.md](./vps.md) | Setup específico da VPS. |

## Como sincronizar

Todos os ambientes carregam `three-tabs-config.md` na inicialização da sessão. Mudanças nessa regra **DEVEM** ser propagadas pra:

- `~/.claude/CLAUDE.md` em cada ambiente
- `~/.claude/rules/common/three-tabs-priority.md`
- `C:\Users\teste\plano\PRIORIDADE.md` (Desktop)
- `Vault Obsidian: Pessoal/plano/3-abas-master.md`
- `~/.claude/projects/C--Users-teste-plano/memory/abas_master_priority.md`

## Princípio

**Plano (99999) > Singular (100), Skip (101) vence Singular em ambiguidade.**

*[Registrado por: DESKTOP — 2026-04-26]*
