# Project Categorization

## Regra Obrigatoria

Quando detectar que o usuario esta iniciando trabalho em um NOVO projeto (que nao existe no Obsidian vault em `C:/Users/teste/Documents/obsidiano/`), ANTES de qualquer implementacao:

1. Perguntar: "Em qual caixa esse projeto se encaixa?"
2. Opcoes:
   - **Pessoal** — Projetos pessoais, estudo, side projects → pasta `Pessoal/`
   - **Paralelo** — Projetos em andamento simultaneo, sem ser o foco principal → pasta `Projetos/`
   - **Freelancer** — Projetos de clientes, trabalho avulso → pasta `Freelancer/`
   - **Singular** — Projeto principal, dedicacao full-time (Grupo Black / Singular Group) → pasta `singular/`
3. Criar nota no Obsidian vault via MCPVault MCP com frontmatter:
   ```yaml
   ---
   title: "Nome do Projeto"
   category: pessoal|paralelo|freelancer|singular
   status: active
   stack: []
   created: "YYYY-MM-DD"
   updated: "YYYY-MM-DD"
   ---
   ```
4. Registrar na memoria do projeto

## Como detectar "novo projeto"
- Usuario menciona um nome de projeto que nao existe nas pastas do vault
- Usuario pede para "criar", "iniciar", "comecar" algo novo
- O diretorio de trabalho e um repo sem nota correspondente no vault

## Nao perguntar quando
- Projeto ja tem nota no Obsidian (verificar via MCPVault search)
- E uma tarefa dentro de um projeto existente
- E uma pergunta generica, pesquisa, ou config do Claude Code
- E continuacao de trabalho ja em andamento na sessao

## Vault Path
`C:/Users/teste/Documents/obsidiano/`

## Categorias → Pastas
| Categoria | Pasta no Vault |
|-----------|---------------|
| pessoal | `Pessoal/` |
| paralelo | `Projetos/` |
| freelancer | `Freelancer/` ou `Clientes/` |
| singular | `singular/` |
