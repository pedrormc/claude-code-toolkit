# Mobile (Termux/Poco F5) — Setup das 3 Abas

> **Ambiente restrito.** Captura input do Pedro on-the-go, NÃO escreve direto na estrutura física do Desktop. Usa vault Obsidian como inbox.

## Por que Mobile não escreve direto

- O `C:\Users\teste\plano\` mora no Desktop Windows. O Mobile (Linux/Termux/Poco F5) não tem acesso ao filesystem do Desktop.
- A sincronização acontece via **vault Obsidian** (Obsidian Sync ou Git, dependendo do setup atual do Pedro).

## Fluxo Mobile

Quando o Pedro registra algo no celular:

```
Input → Mobile aplica os 3 crivos → categoria
                                  → cria nota no vault em:
                                    Pessoal/plano/inbox/<aba>/<YYYYMMDD-HHMM>-titulo.md
                                  → notifica Pedro via reply
```

## Estrutura do inbox no vault

Criar quando a primeira nota mobile chegar:

```
Vault Obsidian: Pessoal/plano/inbox/
├── plano/        ← itens classificados como plano (peso 99999)
├── singular/     ← itens classificados como singular (peso 100)
├── skip/         ← itens classificados como skip (peso 101)
└── _ambiguous/   ← itens onde Mobile não conseguiu decidir e marcou pra revisão
```

## Frontmatter padrão Mobile

```yaml
---
title: "Título curto"
aba: plano | singular | skip | ambiguous
peso: 99999 | 100 | 101 | null
status: inbox
created: 2026-04-26T18:30:00-03:00
created_by: mobile
needs_review: true | false
---
```

## Master Desktop pulls inbox

O Master Desktop deve, periodicamente:

1. Ler `Pessoal/plano/inbox/<aba>/`.
2. Mover cada nota pra `C:\Users\teste\plano\<aba>\<sub>\` apropriado.
3. Atualizar status: `inbox → arquivado-no-master`.
4. Linkar no `INDEX.md` se marco importante.

## Limitações Mobile

- Sem acesso a tools pesadas (Bash full, npm, deploys).
- Foco em: captura, classificação rápida, consultas ao vault.
- Quando duvidoso, marca `needs_review: true` e o Master decide depois.

*[Registrado por: DESKTOP — 2026-04-26]*
