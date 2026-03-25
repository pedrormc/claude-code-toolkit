# Parallel Agents — Worktree Isolation

## Regra Principal

Agents que **escrevem codigo** em paralelo DEVEM usar worktree isolado via `isolation: "worktree"` no Agent tool.

## Quando Usar Worktree

| Cenario | Worktree? | Razao |
|---------|-----------|-------|
| 2+ agents editando arquivos simultaneamente | Sim | Evitar conflitos de escrita |
| Agent de code review (read-only) | Nao | Apenas leitura, sem risco |
| Agent de research/pesquisa | Nao | Apenas leitura e web |
| Agent fazendo build/test isolado | Sim | Pode modificar node_modules/build artifacts |
| Agent unico editando | Nao | Sem concorrencia |

## Convencoes

- Worktrees sao criados automaticamente pelo Claude Code quando `isolation: "worktree"` e especificado
- Apos conclusao, worktrees sem mudancas sao limpos automaticamente
- Worktrees com mudancas retornam o path e branch para merge manual
- Main worktree permanece limpo — recebe apenas merges revisados

## Exemplo de Uso

```
// 2 agents editando em paralelo — ambos com worktree
Agent 1: frontend-specialist (isolation: "worktree") — edita src/
Agent 2: api-specialist (isolation: "worktree") — edita api/

// 1 agent editando + 1 read-only — apenas o editor precisa
Agent 1: frontend-specialist (isolation: "worktree") — edita src/
Agent 2: code-reviewer — apenas le e analisa
```

## Merge Workflow

1. Agents completam trabalho em worktrees isolados
2. Revisar mudancas de cada worktree
3. Merge sequencial para main worktree
4. Resolver conflitos se houver
5. Verificacao final (`npm run lint && npm run build`)
