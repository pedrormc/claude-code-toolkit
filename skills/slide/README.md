# /slide — Apresentação Singular

Skill do Claude Code que transforma texto livre, brain-dump, tese ou pitch num **deck de slides** com identidade visual da Singular Group — paleta cobre/aço/off-white/preto + fonte Urbanist.

- **HTML standalone** (default): 1 arquivo `.html` zero-dependência, viewport-safe, scroll-snap, navegação por teclado/wheel/touch, animações reveal sutis. Pronto pra apresentar fullscreen.
- **PowerPoint (`.pptx`)**: exportação opcional via `python-pptx` mantendo paleta e estrutura — pra quando precisar do arquivo editável no formato corporativo.

Metodologia validada na tese **PowerCoffee · Aporte Direto** (deploy [powercoffee-tese.vercel.app](https://powercoffee-tese.vercel.app), maio/2026).

## O que essa skill faz

1. **Analisa** texto livre e infere a estrutura ideal do deck (5-12 slides).
2. **Aplica norma culta do português** (acentuação, smart quotes, travessões).
3. **Gera HTML standalone** com paleta Singular oficial e navegação completa.
4. **(Opcional) Exporta `.pptx`** via `python-pptx` pra distribuição.
5. **(Opcional) Sobe no Google Drive** numa pasta configurada e auto-compartilha.
6. **(Opcional) Manda o link via WhatsApp** usando uma instância Evolution.

## Estrutura

```
skills/slide/
├── README.md                    (este arquivo — para humanos)
├── SKILL.md                     (instruções para o Claude Code — fluxo de 8 passos)
├── build_html.py                (gerador HTML standalone — default)
├── build_pptx.py                (exportador .pptx — opcional)
├── example-content.json         (exemplo válido do schema, 8 slides)
├── secrets.local.json.example   (template de config local)
├── .gitignore                   (exclui secrets e builds)
├── assets/
│   ├── logo-singular.png        (logo oficial)
│   ├── logo-singular.svg        (versão vetorizada)
│   └── isotipo-singular-dark.png (isotipo pra fundo escuro)
└── references/
    └── palette.md               (paleta completa + diretrizes visuais)
```

## Tipos de slide suportados (8)

| `type` | Para quê | Layout |
|--------|----------|--------|
| `cover` | Capa | Hero gigante + autor + data |
| `summary-cards` | Resumo executivo com 2-4 opções/pilares | Grid de cards com tag/título/corpo |
| `section-detail` | Detalhamento de uma opção/pilar | Header + 3-4 cards numerados + highlight box |
| `compare-table` | Tabela comparativa (até 4 colunas) | Header + tabela full-width com coluna base destacada |
| `text-section` | Seção de texto livre com bullets/parágrafos | Header + parágrafos + lista bullet/numbered |
| `recommendation` | Recomendação central com 4 motivos | Hero centralizado + grid 2×2 numerado |
| `next-steps` | Próximos passos / perguntas | Grid 3 cards numerados + CTA |
| `closing` | Fechamento | Mensagem central + assinatura |

## Identidade visual aplicada

### Paleta primária Singular

| Nome | Hex | Uso |
|------|-----|-----|
| **COBRE** | `#E64E10` | Accent principal — eyebrows, badges, números, CTAs |
| **AÇO QUENTE** | `#5B4B48` | Texto secundário, divisores |
| **OFF WHITE** | `#F7EEEB` | Texto sobre fundo escuro |
| **PRETO PROFUNDO** | `#1C1C1C` | Fundo padrão dos slides |

### Tipografia
- Principal: **Urbanist** (oficial Singular)
- Fallback web: Inter, Montserrat, system-ui

> ⚠️ Não edite os arquivos em `assets/` nem substitua a logo. Mudanças quebram a identidade compartilhada das skills `/pop`, `/ata`, `/documento`, `/slide`.

## Dependências

- **Python 3.10+**
- **`python-pptx`** (`pip install python-pptx`) — só pra exportação `.pptx`. HTML não precisa.
- **MCP `google-drive`** configurado (opcional, para upload).
- **Node.js + script `whatsapp-send.js`** (incluso no toolkit) e instância Evolution API (opcional, para WhatsApp).

## Setup

### 1. Instalar a skill
Copie `skills/slide/` para `~/.claude/skills/slide/`. Se você usa o `install.sh` deste toolkit, ele já cuida disso.

### 2. (Opcional) Configurar credenciais

```bash
cp ~/.claude/skills/slide/secrets.local.json.example ~/.claude/skills/slide/secrets.local.json
```

Edite `secrets.local.json` e preencha `drive.zel_folder_id`, `drive.auto_share_email`, e os campos `whatsapp.*`. **Nunca** commite o `secrets.local.json`.

### 3. Pronto

No Claude Code:

```
/slide

<cola aqui a tese, pitch, brain-dump ou estrutura que você quer transformar em deck>
```

A skill:
- Infere estrutura ideal (5-12 slides)
- Gera `apresentacao.html` zero-dependência (e `.pptx` se pedir)
- Sobe no Drive na pasta configurada (se config presente)
- Manda o link no WhatsApp (se config presente)
- Devolve no chat o caminho local + link Drive

Sem `secrets.local.json`, a skill ainda funciona: gera os arquivos localmente e pula upload/WhatsApp.

## Uso direto (sem Claude)

```bash
# HTML
python ~/.claude/skills/slide/build_html.py meu-content.json apresentacao.html

# PPTX
python ~/.claude/skills/slide/build_pptx.py meu-content.json apresentacao.pptx
```

Veja `example-content.json` pra um JSON completo (8 slides cobrindo todos os tipos).

## Schema do `content.json` (resumo)

Campos obrigatórios:
- `meta.title`
- `slides` (lista com pelo menos 1 slide)

Cada slide precisa de `type` (um dos 8 tipos suportados) + os campos específicos do tipo.

Veja schema completo em `SKILL.md` ou exemplo funcional em `example-content.json`.

## Segurança

- `secrets.local.json` nunca vai pro git (`.gitignore` da skill bloqueia).
- API keys nunca aparecem em logs ou no chat — passadas só por env var.
- Antes de mandar conteúdo sensível por WhatsApp, a skill confirma com você.
- O Claude (rodando a skill) não tem permissão de editar `secrets.local.json` — só lê.

## Diferença das skills irmãs

| Skill | Output | Quando usar |
|-------|--------|-------------|
| `/ata` | .docx | Reunião com decisões |
| `/pop` | .docx | Processo executável |
| `/documento` | .docx | Estratégia, memo, briefing, RFC |
| `/contrato` | .docx | Documento jurídico |
| `/tese-investimento` | .docx + checklist | Análise estruturada de tese |
| **`/slide`** | **.html + .pptx** | **Pitch / apresentação visual** |

## Licença

Mesma do toolkit (ver `LICENSE` na raiz).

## Autoria

Singular Group — Pedro Roberto Miranda (CEO)
