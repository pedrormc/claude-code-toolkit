# VPS (Docker / AWS Lightsail) — Setup das 3 Abas

> **Ambiente headless máximo.** Roda automações longas, jobs agendados, integrações externas. Lê o vault Obsidian montado em volume.

## Acesso do VPS

- Vault Obsidian via Git pull periódico OU Syncthing (depende do setup atual).
- Pode escrever em `singular/operacoes/` quando for output de automação (deploy log, métricas, etc).
- Para escrever em `plano/` ou `skip/` → só com pedido explícito do Pedro.

## Fluxo VPS

Automação rodando no VPS gera output:

```
Job VPS → output → categoria padrão = singular/operacoes/
                 → cria arquivo em Pessoal/plano/singular/operacoes/<jobname>-<YYYYMMDD>.md
                 → Master Desktop sincroniza pro filesystem local
```

## Tipos de output VPS

| Output | Aba destino | Sub-pasta |
|--------|-------------|-----------|
| Deploy log Singular | singular | operacoes/deploys/ |
| Métricas de cliente | singular | clientes/<nome>/metrics/ |
| Notification de monitoring | singular ou skip (depende severidade) | operacoes/alerts/ ou skip/descarte/ |
| Insight de IA / análise | plano (se serve plano-vital) | plano/ideias/ — **PERGUNTAR antes** |

## Regras de escrita VPS

1. **Default:** `singular/operacoes/`.
2. **Plano:** Só se o Pedro autorizou explicitamente (job tem `plano: true` no config).
3. **Skip:** Só se filtro automatizado classificou explicitamente como skipável.
4. **Quando ambíguo:** Notifica Pedro via WhatsApp / vault inbox e aguarda confirmação.

## Frontmatter VPS

```yaml
---
title: "Output do job <jobname>"
aba: singular  # default
peso: 100      # default
status: gerado
created: 2026-04-26T18:30:00-03:00
created_by: vps
job: <jobname>
job_run_id: <uuid>
---
```

## Limitações VPS

- Headless: sem interação direta, depende de regra prévia do Pedro.
- Só escreve com confiança em `singular/operacoes/`.
- Para classificar `plano` ou `skip` automaticamente, precisa de critério explícito do Pedro (a definir).

*[Registrado por: DESKTOP — 2026-04-26]*
