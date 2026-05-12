# Three Tabs Priority — Regra Soberana

> **Decretada em:** 2026-04-26
> **Escopo:** TODOS os Claudes (Master Desktop / Mobile / VPS), TODOS os contextos, TODOS os projetos.
> **Override:** APENAS o próprio Pedro pode revogar/alterar esta regra.

## A Hierarquia

| Ordem | Aba | Peso | Significado |
|-------|------|------|-------------|
| 1 | **plano** | 99999 | Plano-vital. Vence tudo. |
| 2 | **singular** | 100 | Trabalho / Singular Group. |
| 3 | **skip** | 101 | Descarte / pular. Vence singular em ambiguidade. |

## A Regra de Ouro

Todo input do Pedro **DEVE** ser categorizado nas 3 abas, **NESTA ORDEM**, antes de qualquer ação:

1. **Isso serve ao plano-vital?** (peso 99999) → `C:\Users\teste\plano\plano\`
2. **Isso é Singular Group?** (peso 100) → `C:\Users\teste\plano\singular\`
3. **Isso é skipável?** (peso 101) → `C:\Users\teste\plano\skip\descarte\`

> **Pesos numéricos:** quanto maior, mais prioritário no ranking. `plano` (99999) sempre vence. `skip` (101) vence `singular` (100) em caso de ambiguidade — quando algo poderia ser singular mas também poderia ser pulado, a flag de skip ganha.

## Questionamento Obrigatório

Quando o Claude **NÃO TIVER 100% de certeza** da categoria, **DEVE PERGUNTAR** antes de qualquer ação:

```
[PRIORIDADE] Onde isso entra?
[ ] plano (99999) — serve ao plano-vital
[ ] singular (100) — trabalho Singular Group
[ ] skip (101) — descartável / pular
```

## Aplicação

- **Antes de iniciar QUALQUER tarefa** que o Pedro pedir → aplicar mentalmente os 3 crivos.
- **Se categoria for óbvia** → seguir.
- **Se categoria for ambígua** → perguntar com o formato acima.
- **Sempre referenciar** `C:\Users\teste\plano\PRIORIDADE.md` em qualquer dúvida.

## O que conta como "input do Pedro"

- Mensagens diretas no Claude Code (qualquer ambiente TRIFORCE).
- Arquivos novos que o Pedro cria.
- Ideias soltas ("seria legal se...").
- Demandas de cliente (passa pelo crivo: plano? singular? skip?).
- Mensagens em outros canais (WhatsApp, Slack) repassadas pra Claude.

## O que NÃO precisa de classificação

- Comandos puramente técnicos isolados ("rode os testes", "instale isto").
- Continuação de uma tarefa já categorizada.
- Perguntas conceituais que não geram artefato (ex: "o que é X?").

## Sincronização

Esta regra é replicada em:
- `~/.claude/CLAUDE.md` (persona Master Desktop)
- `~/.claude/triforce/three-tabs-config.md` (sync TRIFORCE)
- `C:\Users\teste\plano\PRIORIDADE.md` (manifesto raiz do projeto)
- `~/.claude/projects/C--Users-teste-plano/memory/abas_master_priority.md` (memória)
- `Vault Obsidian: Pessoal/plano/3-abas-master.md`

Mudanças nesta regra **DEVEM** ser propagadas para TODOS os 5 lugares acima.

*[Registrado por: DESKTOP — 2026-04-26]*
