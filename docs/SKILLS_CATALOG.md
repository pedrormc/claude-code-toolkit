# Catálogo de Skills — claude-code-toolkit

> Todas as **skills custom** (criadas pelo Pedro) que o toolkit instala em `~/.claude/skills/`.
>
> **Pasta no GitHub:** https://github.com/pedrormc/claude-code-toolkit/tree/master/skills
>
> Cada skill é uma subpasta com `SKILL.md` (instruções + protocolo) e arquivos auxiliares (scripts Python/JS, templates `.md`/`.docx`, exemplos JSON, references).
>
> **Total: 19 skills custom + Gstack (36+ via clone do `garrytan/gstack`).**

---

## 1) Documentos Singular (.docx com identidade visual)

### `/ata`
**Folder:** [`skills/ata/`](../skills/ata)
Transforma transcrição/notas de reunião em **Ata** formatada como `.docx` espelhando o template oficial Singular (Urbanist, header/footer com logo, paleta preto/branco). Organiza em decisões, encaminhamentos (responsável + prazo), próxima reunião. Aplica norma culta do PT.

**Como invocar:** "monta a ata dessa reunião" / "/ata <transcrição>"
**Deps:** python-docx, Pillow.

### `/documento`
**Folder:** [`skills/documento/`](../skills/documento)
Transforma texto livre (brain-dump, conversa de WhatsApp, draft) em **documento formal** `.docx` Singular. Schema flexível: estratégia, briefing, memo, plano, decisão, RFC, one-pager.

**Como invocar:** "organiza isso num doc" / "/documento <texto>"
**Deps:** python-docx, Pillow.

### `/pop`
**Folder:** [`skills/pop/`](../skills/pop)
Gera **Procedimento Operacional Padrão** (POP) em `.docx` Singular, com norma culta e estrutura formal de processo (objetivo, escopo, responsabilidades, fluxo, controles).

**Como invocar:** "monta o POP de <processo>"
**Deps:** python-docx.

### `/slide`
**Folder:** [`skills/slide/`](../skills/slide)
Cria **apresentação Singular** (capa, resumo, detalhes, comparativo, recomendação, próximos passos) em HTML standalone (1 arquivo, scroll-snap, navegação teclado/wheel/touch, animações reveal) com paleta cobre/aço/off-white/preto. Opcionalmente exporta `.pptx` via python-pptx.

**Como invocar:** "monta uma apresentação sobre X"
**Deps:** python-pptx (opcional).

---

## 2) Operações comerciais / inteligência

### `/contrato`
**Folder:** [`skills/contrato/`](../skills/contrato)
Gera contratos Singular (**NDA-PF, NDA-PJ, MOU, Prestação de Serviços, Representação Comercial, Embaixador**) em `.docx`, com upload automático pro Google Drive (pasta Zel). Consulta Qdrant Nexo_Adv (25k+ chunks de doutrina jurídica) pra fundamentar cláusulas e detectar ilegalidades.

**Como invocar:** "faz um NDA com fulano" / "/contrato <tipo> <partes>"
**Deps:** python-docx, requests, OpenAI SDK (embeddings).
**Env vars:** `QDRANT_URL`, `QDRANT_API_KEY`, `OPENAI_API_KEY`.

### `/backgroundcheck`
**Folder:** [`skills/backgroundcheck/`](../skills/backgroundcheck)
**Due diligence reputacional de pessoa física** a partir do nome completo. Consulta processos judiciais (STF, STJ, TST, TJDFT, TJSP, Escavador, CNJ), mídia, redes sociais, conselhos profissionais, sanções (CGU/CEIS, TCU). Gera dossiê em `.docx` com identidade Singular, links de cada fonte e análise de risco. Inclui varredura societária obrigatória (consultasocio + minhareceita).

**Como invocar:** "background check em <nome>" / "due diligence de <pessoa>"
**Deps:** requests, beautifulsoup4, python-docx.

### `/prospect`
**Folder:** [`skills/prospect/`](../skills/prospect)
**Prospecção comercial porta-a-porta** — analisa presença digital de todas as empresas de uma quadra da Asa Norte e gera relatórios com oportunidades de venda pra Singular.

**Como invocar:** "/prospect <quadra>"
**Repo dedicado:** github.com/pedrormc/ROTA-RUA

### `/tese-investimento`
**Folder:** [`skills/tese-investimento/`](../skills/tese-investimento)
Estrutura **teses de investimento** (operações equity ou aplicações conservadoras) com checklist + 5 personas críticas (arrojado, conservador, devil-advocate, family-office, operador) + prompts pra slides.

**Como invocar:** "estrutura tese de investimento em X" / "compara essas aplicações"

---

## 3) Comunicação & utilidades

### `/whatsapp-evolution`
**Folder:** [`skills/whatsapp-evolution/`](../skills/whatsapp-evolution)
Envia **texto, documento, imagem, áudio ou vídeo via WhatsApp** usando Evolution API self-hosted (instância configurável).

**Como invocar:** "manda WhatsApp pro fulano dizendo X" / "envia esse arquivo no zap pro Y"
**Env vars:** `EVOLUTION_API_URL`, `EVOLUTION_INSTANCE`, `EVOLUTION_API_KEY`.
**Script:** `~/.claude/scripts/whatsapp-send.js`

### `/mp4`
**Folder:** [`skills/mp4/`](../skills/mp4)
Converte **MP4** (ou outros vídeos) em **MP3**. Abre file picker do Windows pro user escolher o vídeo, extrai áudio via ffmpeg.

**Como invocar:** "/mp4" / "extrai áudio desse vídeo"
**Deps:** ffmpeg (no PATH).

### `/obsidian`
**Folder:** [`skills/obsidian/`](../skills/obsidian)
Salva **recap da sessão Claude Code numa daily note do vault Obsidian**. Duas modalidades: (a) recap rico da sessão atual via análise da conversa, (b) consolidação de todas as sessões do dia via scanner determinístico. Constrói histórico Claude Code → Obsidian ao longo do tempo.

**Como invocar:** "/obsidian" / "salva no obsidian" / "documenta o dia"
**MCP:** obsidian (via `@bitbonsai/mcpvault`).

---

## 4) n8n helpers (7 skills)

Conjunto de skills pra **trabalhar com n8n** (build workflows, debug, validação) via o MCP `n8n-mcp`.

### `/n8n-code-javascript`
**Folder:** [`skills/n8n-code-javascript/`](../skills/n8n-code-javascript)
Escrever JS em **Code node** do n8n: sintaxe `$input/$json/$node`, HTTP via `$helpers`, DateTime, troubleshooting.

### `/n8n-code-python`
**Folder:** [`skills/n8n-code-python/`](../skills/n8n-code-python)
Escrever Python em **Code node** do n8n: `_input/_json/_node`, stdlib, limitações.

### `/n8n-expression-syntax`
**Folder:** [`skills/n8n-expression-syntax/`](../skills/n8n-expression-syntax)
Validar/corrigir sintaxe de expressões `{{ }}` do n8n, acesso a `$json/$node`, troubleshooting de webhook data.

### `/n8n-mcp-tools-expert`
**Folder:** [`skills/n8n-mcp-tools-expert/`](../skills/n8n-mcp-tools-expert)
Guia das tools do MCP `n8n-mcp`: buscar nós, validar configs, templates, gerenciar workflows.

### `/n8n-node-configuration`
**Folder:** [`skills/n8n-node-configuration/`](../skills/n8n-node-configuration)
Config por operation: dependências de properties, campos obrigatórios, padrões comuns por tipo de node.

### `/n8n-validation-expert`
**Folder:** [`skills/n8n-validation-expert/`](../skills/n8n-validation-expert)
Interpretar erros de validação, fixes, falsos positivos, profiles de validação.

### `/n8n-workflow-patterns`
**Folder:** [`skills/n8n-workflow-patterns/`](../skills/n8n-workflow-patterns)
Padrões arquiteturais de workflows reais: webhooks, HTTP API, DB, AI agents, scheduled tasks.

---

## 5) HubSpot

### `/hubspot-mcp-expert`
**Folder:** [`skills/hubspot-mcp-expert/`](../skills/hubspot-mcp-expert)
Guia pra usar **MCP HubSpot** (`@hubspot/mcp-server`): contacts, companies, deals, leads, engagements (calls/emails/meetings/notes/tasks), associations, communications, properties, schemas.

**MCP:** `hubspot-singular` ou `hubspot-smup` no `mcp.json`.
**Setup HubSpot completo:** entregue separadamente (contém credenciais privadas).

---

## 6) Meta-skill

### `/learned`
**Folder:** [`skills/learned/`](../skills/learned)
Pasta onde o Claude armazena learnings continuamente (via plugin everything-claude-code `/learn-eval`). Não é uma skill invocável — é um diretório de aprendizado contínuo.

---

## Como instalar

Tudo é instalado automaticamente pelo `install.sh`:

```bash
git clone https://github.com/pedrormc/claude-code-toolkit.git /tmp/claude-code-toolkit
cd /tmp/claude-code-toolkit
bash install.sh --force
```

Skills viram disponíveis após reiniciar o Claude Code (`Ctrl+C Ctrl+C` e abrir de novo).

---

## Como criar uma nova skill

1. `mkdir ~/.claude/skills/<nome-da-skill>`
2. Crie `SKILL.md` com frontmatter:
   ```yaml
   ---
   name: nome-da-skill
   description: O que faz, quando usar, gatilhos em PT-BR.
   ---
   ```
3. Adicione scripts/templates conforme necessário
4. Use o plugin `everything-claude-code` → `/skill-create` pra um wizard guiado

---

## Pasta Gstack (instalada por clone)

[`~/.claude/skills/gstack/`](https://github.com/garrytan/gstack) — Clonado pelo `install.sh` do repo público `garrytan/gstack`. Traz ~36 slash commands adicionais (`/qa`, `/ship`, `/cso`, `/office-hours`, `/investigate`, `/retro`, `/health`, `/checkpoint`, design-*, plan-*, etc.).

Não está duplicado neste toolkit pra evitar fork desnecessário — sempre puxa a versão mais nova do repo original.

---

*[Catálogo atualizado: 2026-05-11]*
*[Toolkit: github.com/pedrormc/claude-code-toolkit]*
