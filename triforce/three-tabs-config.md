# three-tabs-config — Regra Soberana TRIFORCE

> **Fonte de verdade canônica** das 3 abas master de prioridade.
> **Aplica a:** Master Desktop, Mobile/Termux, VPS.

## Hierarquia

```
plano     [peso 99999]   ← VENCE TUDO. Plano-vital.
singular  [peso 100]     ← Trabalho Singular Group.
skip      [peso 101]     ← Descarte. Vence singular em ambiguidade.
```

## Ordem de avaliação obrigatória

Para todo input recebido (mensagem, arquivo, ideia, demanda):

1. **Cabe em `plano`?** (peso 99999) → SIM = top priority, vai pra `~/plano/plano/` (Desktop) ou repassado pra Master via Obsidian.
2. **Cabe em `singular`?** (peso 100) → SIM = trabalho Singular, vai pra `~/plano/singular/`.
3. **É `skip`?** (peso 101) → SIM = descartar / pular, vai pra `~/plano/skip/descarte/`.

## Comportamento de cada Claude

### Master Desktop (Windows 11)
- **Tem permissão total.** Processa input, categoriza, **escreve no `C:\Users\teste\plano\`**.
- Pergunta ao Pedro quando ambíguo.
- Sincroniza com Obsidian vault e propaga para Mobile/VPS via vault.

### Mobile (Termux/Poco F5)
- **Restrito.** NÃO escreve direto em `C:\Users\teste\plano\` (não tem acesso).
- **Captura input** quando o Pedro registra algo on-the-go.
- **Salva no vault Obsidian** (`Pessoal/plano/inbox/<aba>/<timestamp>.md`).
- Master Desktop puxa do inbox e move pra estrutura definitiva.

### VPS (Docker / Lightsail)
- **Máximo headless.** Roda automações e jobs.
- **Lê** o vault Obsidian montado em volume.
- **Pode escrever** em `singular/operacoes/` se for output de automação.
- Para `plano/`: só escreve se o Pedro pediu explicitamente.

## Questionamento — TODOS os Claudes

Quando duvidoso sobre categoria, **PERGUNTAR** antes de agir:

```
[PRIORIDADE] Onde isso entra?
[ ] plano (99999) — serve ao plano-vital
[ ] singular (100) — trabalho Singular Group
[ ] skip (101) — descartável / pular
```

## Triggers para esta regra

A regra dispara quando o Pedro:

- Cria nota / ideia / projeto / item nova.
- Pede algo que ainda não foi categorizado.
- Repassa demanda externa (cliente, mensagem, etc).
- Faz brainstorm sem destino claro.

NÃO dispara quando o Pedro:

- Continua tarefa já categorizada (mesma sessão).
- Faz pergunta puramente conceitual sem gerar artefato.
- Pede comando técnico isolado ("rode os testes").

## Sincronização de mudanças

Se a regra das 3 abas precisar mudar (renomear aba, ajustar pesos, adicionar 4ª aba), **TODOS** estes arquivos precisam ser atualizados em sequência:

1. `~/.claude/triforce/three-tabs-config.md` (este arquivo, fonte de verdade)
2. `~/.claude/CLAUDE.md` (cada ambiente)
3. `~/.claude/rules/common/three-tabs-priority.md`
4. `C:\Users\teste\plano\PRIORIDADE.md`
5. `C:\Users\teste\plano\INDEX.md`
6. `~/.claude/projects/C--Users-teste-plano/memory/abas_master_priority.md`
7. `Vault Obsidian: Pessoal/plano/3-abas-master.md`
8. `Vault Obsidian: CLAUDE.md` (se mencionar)

*[Registrado por: DESKTOP — 2026-04-26]*
