---
name: slide
description: Cria apresentação de slides da Singular Group (capa, resumo, detalhes, comparativo, recomendação, próximos passos) a partir de texto livre ou JSON. Gera HTML standalone (1 arquivo, scroll-snap, navegação por teclado/wheel/touch, animações reveal) com identidade visual oficial da Singular — paleta cobre/aço/off-white/preto + Urbanist. Opcionalmente exporta para .pptx via python-pptx. Use quando o usuário digitar /slide, ou pedir "monta uma apresentação", "cria slides pra essa tese/pitch/proposta", "transforma esse pitch num slide deck Singular".
---

# /slide — Apresentação Singular

Converte texto livre, brain-dump, tese ou pitch num **deck de slides** com identidade visual da Singular.

- **HTML standalone** (default): 1 arquivo `.html` zero-dependência, viewport-safe, scroll-snap, navegação por teclado/wheel/touch, animações reveal sutis. Pronto pra demonstrar no navegador, fazer captura de tela, ou apresentar fullscreen.
- **PowerPoint (`.pptx`)**: exportação opcional via `python-pptx` mantendo paleta e estrutura — pra quando o cliente/sócio precisa do arquivo editável no formato corporativo.

> A skill foi extraída da metodologia validada na tese **PowerCoffee · Aporte Direto** (maio/2026, deploy Vercel).

## Quando usar

Invoque quando o usuário:
- Digitar `/slide` seguido de texto a estruturar
- Pedir "monta uma apresentação", "cria slides", "transforma em pitch deck"
- Tiver uma tese de investimento, proposta comercial, plano estratégico ou diagnóstico que precise virar deck pra apresentar
- Quiser um deck com a cara da Singular pra mandar pra cliente/sócio/investidor

**Não usar quando:**
- For documento estático em texto → `/documento`
- For ata de reunião → `/ata`
- For POP → `/pop`
- For contrato → `/contrato`
- For tese de investimento bruta (sem visualização) → `/tese-investimento`

## Identidade visual oficial Singular (não negociável)

### Paleta primária
| Nome | Hex | Uso |
|------|-----|-----|
| **COBRE** | `#E64E10` | Accent principal — eyebrows, badges, números, CTAs, highlights |
| **AÇO QUENTE** | `#5B4B48` | Texto secundário em fundo claro, divisores, bordas sutis |
| **OFF WHITE** | `#F7EEEB` | Texto sobre fundo escuro, fundo claro alternativo |
| **PRETO PROFUNDO** | `#1C1C1C` | Fundo padrão dos slides |

### Paleta secundária (com parcimônia)
| Nome | Hex | Uso |
|------|-----|-----|
| Cobre dessaturado | `#C55A48` | Variação tonal pra destaques alternativos |
| Preto puro | `#000000` | Acentos extremos, sombras |

### Tipografia
- **Principal:** Urbanist (fonte oficial Singular — usada em /pop, /ata, /documento)
- **Fallback web:** Inter, Montserrat, system-ui
- Pesos: 300, 400, 500, 600, 700, 800

### Logo
- Logo SINGULAR (LOGO PNG/SVG) em capa e fechamento
- Isotipo (variação compacta) em assinatura discreta de slides intermediários
- Assets em `assets/` da skill — **não modificar nem substituir**

## Arquivos da skill

```
~/.claude/skills/slide/
├── SKILL.md                    (este arquivo)
├── build_html.py               (gerador HTML standalone — default)
├── build_pptx.py               (exportador .pptx — opcional)
├── example-content.json        (exemplo válido do schema)
├── secrets.local.json          (config local — gitignored)
├── secrets.local.json.example  (template público)
├── .gitignore                  (exclui secrets + builds)
├── assets/
│   ├── logo-singular.png       (logo oficial pra capa)
│   ├── logo-singular.svg       (versão vetorizada)
│   └── isotipo-singular-dark.png (isotipo pra fundo escuro)
├── references/
│   └── palette.md              (referência completa da paleta + grid)
└── templates/
    └── base.html.tmpl          (esqueleto HTML com CSS Singular)
```

## Fluxo de execução (8 passos — NÃO pule etapas)

### Passo 1 — Inferir estrutura do deck

A partir do texto livre, decida quantos slides e quais tipos. Catálogo de tipos suportados:

| `type` | Para quê | Layout |
|--------|----------|--------|
| `cover` | Capa | Hero gigante + autor + data |
| `summary-cards` | Resumo executivo com 2-4 opções/pilares | Grid de cards com tag/título/corpo |
| `section-detail` | Detalhamento de uma opção/pilar | Header + 3-4 cards numerados + highlight box |
| `compare-table` | Tabela comparativa (até 4 colunas) | Header + tabela full-width |
| `text-section` | Seção de texto livre com bullets/parágrafos | Header + parágrafos + lista bullet/numbered |
| `recommendation` | Recomendação central com 4 motivos | Hero centralizado + grid 2×2 numerado |
| `next-steps` | Próximos passos / perguntas | Grid 3 cards numerados + CTA |
| `closing` | Fechamento | Mensagem central + assinatura |

**Mínimo recomendado:** 5 slides. **Máximo recomendado:** 12 slides (acima disso vira documento, não apresentação).

### Passo 2 — Aplicar norma culta do português

Antes de gravar o JSON, revise toda redação corrigindo acentuação conforme `~/.claude/skills/pop/references/accents.md`. Use aspas tipográficas (`"` `"`) e travessão (`—`).

### Passo 3 — Escrever o JSON

Schema completo em `example-content.json`. Estrutura mínima:

```json
{
  "meta": {
    "title": "PowerCoffee — Tese de Investimento",
    "subtitle": "Aporte Direto · Investidor PF",
    "author": "Pedro Roberto Miranda · Singular Group",
    "date": "01 de maio de 2026",
    "footer_brand": "Singular Group"
  },
  "slides": [
    {
      "type": "cover",
      "eyebrow": "Dossiê de Tese de Investimento",
      "hero": "PowerCoffee",
      "subtitle": "Aporte Direto · Investidor PF"
    },
    {
      "type": "summary-cards",
      "eyebrow": "Resumo executivo",
      "title": "Existem 3 caminhos para os R$ 30k.",
      "cards": [
        { "tag": "Opção A", "title": "Royalty estruturado", "body": "R$ 3,00 por unidade vendida...", "recommended": true },
        { "tag": "Opção B", "title": "Aporte em estoque", "body": "..." },
        { "tag": "Opção C", "title": "Tier de entrada", "body": "..." }
      ],
      "footer_note": "Spoiler: chegamos no slide 8 com uma recomendação clara."
    }
  ]
}
```

**Regras críticas:**
- NUNCA invente nomes, números, datas ou afirmações factuais
- Resumir e estruturar — não inflar nem inventar
- Use `recommended: true` em **no máximo 1 card** por slide `summary-cards`
- `highlight_box` é o callout cobre — use pra frase-chave do slide, **1 por slide no máximo**
- Tabelas: até 4 colunas, até 6 linhas (acima disso fica ilegível em projetor)

### Passo 4 — Gerar HTML

```bash
python ~/.claude/skills/slide/build_html.py content.json apresentacao.html
```

**Alternativas de invocação:**
- Windows bash: `python /c/Users/teste/.claude/skills/slide/build_html.py content.json apresentacao.html`
- PowerShell: `python "$env:USERPROFILE\.claude\skills\slide\build_html.py" content.json apresentacao.html`

O HTML é zero-dependência (apenas CDN do Google Fonts) e roda em qualquer browser moderno.

### Passo 5 — (Opcional) Exportar para PowerPoint

```bash
python ~/.claude/skills/slide/build_pptx.py content.json apresentacao.pptx
```

**Dependência:** `python-pptx` (`pip install python-pptx`).

O `.pptx` mantém paleta e estrutura mas é uma renderização simplificada — **HTML é a fonte de verdade visual**, PPTX é pra clientes/contextos onde precisa formato editável.

### Passo 6 — Validar

- [ ] Arquivo `.html` criado, > 30KB
- [ ] Abre no browser sem erro de console
- [ ] Capa renderiza com logo
- [ ] Navegação por teclado (`←/→/espaço`) funciona
- [ ] Sem campos `[A definir]` não-sinalizados ao usuário

### Passo 7 — (Opcional) Upload Drive + WhatsApp

Mesma sequência que `/documento` (passos 6 e 7 daquela skill):

1. Ler `~/.claude/skills/slide/secrets.local.json` (drive + whatsapp)
2. Upload `.html` (e `.pptx` se gerado) na pasta Zel via `mcp__google-drive__uploadFile`
3. `mcp__google-drive__shareFile` com `auto_share_email` (writer)
4. Disparar WhatsApp via Evolution API com link

**Mensagem padrão:**
```
🎤 <título do deck>
<link Drive>

(<N> slides · HTML+PPTX)
```

### Passo 8 — Entregar ao usuário no chat

Resposta curta:
1. Caminho absoluto do `.html` gerado (e `.pptx` se gerado)
2. Quantidade e tipos de slides
3. **Link Drive** (se uploadado)
4. Status WhatsApp (se enviado)
5. Comando pra abrir local: `start apresentacao.html` (Windows) / `open apresentacao.html` (mac)

## Diretrizes de design (regras de ouro)

1. **Hierarquia visual:** 1 hero por slide, no máximo. Resto é suporte.
2. **Espaço em branco é luxo:** não encha o slide. Se não couber confortável em 1080p, divide em 2 slides.
3. **Cobre é spice, não molho:** use cobre pra eyebrows, números, callouts. Texto principal sempre off-white sobre preto.
4. **Tabelas comparativas têm 1 coluna destacada:** a "base case" / coluna recomendada vem com background cobre 9% e texto bold.
5. **Animações são sutis:** apenas reveal (fade + slide up 18px) com `prefers-reduced-motion: reduce` honrado.
6. **Capa segue padrão Singular:** eyebrow pequeno em cobre, hero gigante em off-white, autor + data no rodapé separado por linha cobre.
7. **Slide de recomendação é centralizado:** "Opção X" com X em cobre itálico, 4 motivos em grid 2×2.
8. **Nunca use sombras pesadas.** Singular é geométrica e direta.

## Diferença das skills irmãs

| Skill | Output | Quando |
|-------|--------|--------|
| `/documento` | .docx | Texto longo, leitura linear |
| `/ata` | .docx | Reunião com decisões |
| `/pop` | .docx | Processo executável |
| `/contrato` | .docx | Documento jurídico |
| `/tese-investimento` | .docx + checklist | Análise estruturada de tese |
| **`/slide`** | **.html + .pptx** | **Pitch / apresentação visual** |

## Referência

- Exemplo completo: `example-content.json` (8 slides cobrindo todos os tipos)
- Paleta detalhada: `references/palette.md`
- Acentuação: `~/.claude/skills/pop/references/accents.md`
- Origem da metodologia: `C:\Users\teste\plano\singular\investimentos\powercoff-aporte-amigo-2026-04\apresentacao-powercoff.html` (10 slides, deploy https://powercoffee-tese.vercel.app)
