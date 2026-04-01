# Identity Templates — TRIFORCE

Templates de `CLAUDE.md` para cada ambiente do ecossistema TRIFORCE.

## Como usar

Copie o template do seu ambiente para `~/.claude/CLAUDE.md`:

```bash
# Desktop
cp identity/desktop.md ~/.claude/CLAUDE.md

# Mobile (Termux)
cp identity/mobile.md ~/.claude/CLAUDE.md

# VPS (Docker)
cp identity/vps.md ~/.claude/CLAUDE.md
```

Edite os placeholders (PATH_TO_OBSIDIAN_VAULT, etc.) com seus valores reais.

## Niveis de Permissao

| Ambiente | defaultMode | Identidade | Uso |
|----------|-------------|------------|-----|
| Desktop | acceptEdits | Claude Master | Dev principal |
| Mobile | default | Claude Mobile | Consultas, emergencias |
| VPS | bypassPermissions | Claude VPS | Automacoes headless |

## Rastreabilidade

Cada ambiente identifica suas escritas:
- Desktop: `*[Registrado por: DESKTOP — YYYY-MM-DD]*`
- Mobile: `*[Registrado por: MOBILE — YYYY-MM-DD]*`
- VPS: `*[Registrado por: VPS — YYYY-MM-DD]*`

Veja mais em: [TRIFORCE](https://github.com/pedrormc/TRIFORCE)
