# Paleta Singular — Referência Oficial

Fonte: Brand Guidelines Singular (PDF oficial em `Desktop/dondon/pop/Brand Guidelines Singular (2).pdf`).

## Paleta primária

| Nome | Hex | RGB | CMYK | Uso |
|------|-----|-----|------|-----|
| **COBRE** | `#E64E10` | `230, 78, 16` | `C:2 M:79 Y:99 K:0` | Accent principal, eyebrows, badges, CTAs, números, highlights |
| **AÇO QUENTE** | `#5B4B48` | `91, 75, 72` | `C:51 M:55 Y:51 K:50` | Texto secundário em fundo claro, divisores, bordas sutis |
| **OFF WHITE** | `#F7EEEB` | `247, 238, 235` | `C:4 M:8 Y:7 K:0` | Texto sobre fundo escuro, fundo claro alternativo |
| **PRETO PROFUNDO** | `#1C1C1C` | `28, 28, 28` | `C:76 M:66 Y:60 K:81` | Fundo padrão dos slides, texto sobre fundo claro |

## Paleta secundária (com parcimônia)

| Nome | Hex | RGB | CMYK | Uso |
|------|-----|-----|------|-----|
| Cobre dessaturado | `#C55A48` | `197, 90, 72` | `C:18 M:73 Y:70 K:6` | Variação tonal pra destaques alternativos |
| Preto puro | `#000000` | `0, 0, 0` | `C:0 M:0 Y:0 K:100` | Sombras extremas, fundo high-contrast |

## Variações funcionais (derivadas)

Pra UI — não estão no brand guide mas seguem a lógica:

| Token CSS | Hex | Uso |
|-----------|-----|-----|
| `--ink` | `#1C1C1C` | Fundo principal (preto profundo) |
| `--ink-soft` | `#2A2727` | Cards, blocos elevados |
| `--paper` | `#F7EEEB` | Texto principal sobre fundo escuro (off-white) |
| `--copper` | `#E64E10` | Accent (cobre) |
| `--copper-soft` | `rgba(230, 78, 16, 0.18)` | Backgrounds de highlight |
| `--copper-line` | `rgba(230, 78, 16, 0.35)` | Bordas de cards recomendados |
| `--steel` | `#5B4B48` | Aço quente — texto secundário |
| `--muted` | `rgba(247, 238, 235, 0.55)` | Texto desbotado |
| `--muted-strong` | `rgba(247, 238, 235, 0.75)` | Subtítulos, descrições |
| `--rule` | `rgba(247, 238, 235, 0.12)` | Linhas divisórias sutis |
| `--green` | `#2E7D32` | Indicador positivo em tabelas |
| `--red` | `#B23A3A` | Indicador negativo / alerta |

## Tipografia

- **Principal:** Urbanist (oficial Singular)
- **Fallback web:** Inter, Montserrat, system-ui, -apple-system, sans-serif
- **Pesos disponíveis:** 300, 400, 500, 600, 700, 800
- **Hierarquia:**
  - Hero: 700, line-height 0.95, letter-spacing -0.025em
  - Title: 700, line-height 1.1
  - Section h2: 600, line-height 1.15
  - Body: 400, line-height 1.4-1.5
  - Eyebrow/tag: 500-600, uppercase, letter-spacing 0.18-0.22em

## Logo

- **Logo principal:** SINGULAR em horizontal — versões fundo claro (preto sobre off-white), fundo escuro (off-white sobre preto), fundo laranja (preto sobre cobre). Em `assets/logo-singular.png`.
- **Isotipo:** versão compacta com diagonais e quadrados — usar em slides intermediários como assinatura discreta. Em `assets/isotipo-singular-dark.png`.

## Pattern decorativo (opcional)

Brand guide define um pattern de diagonais cobre sobre preto. **Em apresentações usar com parcimônia**, sempre com transparência sutil (alpha ≤ 0.15) e apenas em capa ou fechamento. Não usar pattern em slides com tabelas ou texto denso.

## Regras visuais

1. **Cobre é spice, não molho.** Texto principal sempre off-white sobre preto.
2. **Nunca usar laranja-puro `#FF7F00`** ou variantes de e-commerce. A cor da Singular é COBRE — laranja queimado, terroso.
3. **Aço quente é cinza com calor.** Não substituir por cinza neutro `#888`.
4. **Off-white não é branco.** Tem 4% de magenta/amarelo — dá temperatura.
5. **Preto profundo não é preto puro.** Cinza muito escuro `#1C1C1C` pra evitar contraste agressivo.
6. **Backgrounds animados ou gradientes coloridos: NÃO.** Singular é geométrica, contida, premium-discreta.
