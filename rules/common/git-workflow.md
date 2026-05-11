# Git Workflow

## Pull → Commit → Push (OBRIGATÓRIO)

**Sempre que for commitar, execute a sequência completa pull → commit → push.** Nunca apenas commitar local.

Razão: o ambiente TRIFORCE (Desktop + Mobile + VPS) escreve no mesmo repo em paralelo. Commits locais sem push acumulam, divergem do remote, e na hora do próximo push o git inicia rebase automático que pode travar no meio — já aconteceu em 2026-04-16 com o vault Obsidian (19 commits em rebase interativo parado, requeriu recovery manual).

### Sequência padrão

```bash
# 1. PULL (antes de commitar, traz mudanças do remote)
git pull --rebase --autostash origin <branch>

# 2. COMMIT (apenas mudanças intencionais, nunca git add -A)
git add <arquivos-específicos>
git commit -m "<type>: <description>"

# 3. PUSH (imediato após commit, não deixa acumular)
git push origin <branch>
```

### Exceções (quando pular a regra)

- Commits em sequência dentro do MESMO turno da conversa — faz pull+commit na primeira vez, depois apenas commits subsequentes, e UM push no final agrupando tudo
- Branch local sem upstream configurado — criar com `git push -u origin <branch>` na primeira vez
- Repo sem remote (totalmente local) — só `git commit`, sem push/pull
- Usuário pediu explicitamente pra NÃO pushar ("só commita por enquanto")

### Se o pull der conflito

1. Resolver no ato, não deixar rebase travado
2. Se for conflito complexo que precisa decisão, PARAR e perguntar ao usuário antes de commitar
3. Nunca usar `git push --force` sem aprovação explícita

## Commit Message Format
```
<type>: <description>

<optional body>
```

Types: feat, fix, refactor, docs, test, chore, perf, ci

Note: Attribution disabled globally via ~/.claude/settings.json.

## Pull Request Workflow

When creating PRs:
1. Analyze full commit history (not just latest commit)
2. Use `git diff [base-branch]...HEAD` to see all changes
3. Draft comprehensive PR summary
4. Include test plan with TODOs
5. Push with `-u` flag if new branch

> For the full development process (planning, TDD, code review) before git operations,
> see [development-workflow.md](./development-workflow.md).
