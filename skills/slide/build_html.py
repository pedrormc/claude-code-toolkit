"""
build_html.py — Gera apresentacao HTML standalone com identidade Singular.

Uso:
    python build_html.py content.json saida.html

Le um content.json com lista de slides (ver SKILL.md / example-content.json),
renderiza um HTML zero-dependencia (so Google Fonts CDN), com:
- Paleta oficial Singular (cobre #E64E10, aco quente #5B4B48, off-white #F7EEEB, preto profundo #1C1C1C)
- Fonte Urbanist via Google Fonts (fallback Inter, Montserrat, system-ui)
- Scroll-snap entre slides, navegacao por teclado/wheel/touch
- Animacoes reveal (fade + slide-up), prefers-reduced-motion honrado
- Viewport-safe (clamp() em todo tamanho de fonte)
- 8 tipos de slide: cover, summary-cards, section-detail, compare-table,
  text-section, recommendation, next-steps, closing

A skill completa esta documentada em SKILL.md.
"""
from __future__ import annotations

import html
import json
import sys
from pathlib import Path

# ---------------- HTML helpers ----------------

def esc(s) -> str:
    if s is None:
        return ""
    return html.escape(str(s), quote=True)


def render_inline(s: str) -> str:
    """Permite **bold** e <strong> ja existente no texto. Escapa o resto."""
    if s is None:
        return ""
    out = esc(s)
    while "**" in out:
        out = out.replace("**", "<strong>", 1)
        if "**" in out:
            out = out.replace("**", "</strong>", 1)
        else:
            out = out.replace("<strong>", "")
            break
    out = out.replace("&lt;br&gt;", "<br/>").replace("&lt;br/&gt;", "<br/>")
    return out


# ---------------- Slide renderers ----------------

def render_cover(slide: dict, idx: int, total: int) -> str:
    eyebrow = render_inline(slide.get("eyebrow", "Apresentacao"))
    hero = render_inline(slide.get("hero", "Singular"))
    subtitle = render_inline(slide.get("subtitle", ""))
    left = render_inline(slide.get("footer_left", ""))
    right = render_inline(slide.get("footer_right", ""))
    return f"""
<section class="slide cover" data-slide="{idx}">
    <div class="cover-decor"></div>
    <div class="slide-content cover">
        <div class="cover-top reveal">
            <div class="eyebrow">{eyebrow}</div>
        </div>
        <div class="cover-mid">
            <h1 class="hero reveal delay-1">{hero}</h1>
            <div class="sub reveal delay-2">{subtitle}</div>
        </div>
        <div class="cover-bottom reveal delay-3">
            <div class="left">{left}</div>
            <div class="right">{right}</div>
        </div>
    </div>
</section>
"""


def render_summary_cards(slide: dict, idx: int, total: int) -> str:
    eyebrow = render_inline(slide.get("eyebrow", ""))
    title = render_inline(slide.get("title", ""))
    cards = slide.get("cards", [])
    footer = render_inline(slide.get("footer_note", ""))
    n = max(1, len(cards))
    cards_html_parts = []
    for i, c in enumerate(cards):
        rec = " recommended" if c.get("recommended") else ""
        cards_html_parts.append(f"""
            <div class="opt-card{rec} reveal delay-{i+1}">
                <div class="opt-tag">{render_inline(c.get('tag',''))}</div>
                <div class="opt-title">{render_inline(c.get('title',''))}</div>
                <div class="opt-body">{render_inline(c.get('body',''))}</div>
            </div>""")
    cards_html = "".join(cards_html_parts)
    footer_html = f'<div class="footer-note reveal delay-{n+1}">{footer}</div>' if footer else ""
    return f"""
<section class="slide" data-slide="{idx}">
    <div class="slide-number"><span class="current">{idx+1:02d}</span> / {total:02d}</div>
    <div class="slide-content">
        <div class="section-header reveal">
            <div class="eyebrow">{eyebrow}</div>
            <h2 class="section">{title}</h2>
        </div>
        <div class="opts-grid" style="grid-template-columns: repeat({min(n,4)}, 1fr);">{cards_html}
        </div>
        {footer_html}
    </div>
</section>
"""


def render_section_detail(slide: dict, idx: int, total: int) -> str:
    badge = render_inline(slide.get("badge", ""))
    title = render_inline(slide.get("title", ""))
    subtitle = render_inline(slide.get("subtitle", ""))
    cards = slide.get("cards", [])
    n = len(cards) if cards else 1
    cols = min(max(n, 1), 4)
    cards_html_parts = []
    for i, c in enumerate(cards):
        cards_html_parts.append(f"""
            <div class="detail-card reveal delay-{i+1}">
                <div class="label">{render_inline(c.get('label',''))}</div>
                <div class="value">{render_inline(c.get('value',''))}</div>
            </div>""")
    cards_html = "".join(cards_html_parts)
    badge_html = f'<span class="badge">{badge}</span>' if badge else ""
    subtitle_html = f'<div class="subtitle">{subtitle}</div>' if subtitle else ""
    highlight = slide.get("highlight_box")
    highlight_html = (
        f'<div class="highlight-box reveal delay-{n+1}">{render_inline(highlight)}</div>'
        if highlight else ""
    )
    return f"""
<section class="slide" data-slide="{idx}">
    <div class="slide-number"><span class="current">{idx+1:02d}</span> / {total:02d}</div>
    <div class="slide-content">
        <div class="option-header reveal">
            {badge_html}
            <h1 class="title">{title}</h1>
            {subtitle_html}
        </div>
        <div class="detail-grid" style="grid-template-columns: repeat({cols}, 1fr);">{cards_html}
        </div>
        {highlight_html}
    </div>
</section>
"""


def render_compare_table(slide: dict, idx: int, total: int) -> str:
    eyebrow = render_inline(slide.get("eyebrow", ""))
    title = render_inline(slide.get("title", ""))
    columns = slide.get("columns", [])
    rows = slide.get("rows", [])
    base_col_idx = slide.get("base_col_index", 1)

    thead_parts = []
    for i, col in enumerate(columns):
        cls = " base-col" if i == base_col_idx else ""
        thead_parts.append(f'<th class="{cls.strip()}">{render_inline(col)}</th>')
    thead = "".join(thead_parts)

    tbody_parts = []
    for row in rows:
        tds = []
        for i, cell in enumerate(row):
            classes = []
            if i == 0:
                classes.append("label-cell")
            if i == base_col_idx:
                classes.append("base-col strong")
            if isinstance(cell, dict):
                if cell.get("positive"):
                    classes.append("pos")
                if cell.get("negative"):
                    classes.append("neg")
                if cell.get("strong"):
                    classes.append("strong")
                value = render_inline(cell.get("value", ""))
            else:
                value = render_inline(cell)
            cls = (" ".join(classes)).strip()
            cls_attr = f' class="{cls}"' if cls else ""
            tds.append(f"<td{cls_attr}>{value}</td>")
        tbody_parts.append("<tr>" + "".join(tds) + "</tr>")
    tbody = "".join(tbody_parts)
    footer = render_inline(slide.get("footer_note", ""))
    footer_html = f'<div class="footer-note reveal delay-2">{footer}</div>' if footer else ""

    wrap_class = "table-wrap compare-wrap" if len(columns) >= 4 else "table-wrap"
    return f"""
<section class="slide" data-slide="{idx}">
    <div class="slide-number"><span class="current">{idx+1:02d}</span> / {total:02d}</div>
    <div class="slide-content">
        <div class="section-header reveal">
            <div class="eyebrow">{eyebrow}</div>
            <h2 class="section">{title}</h2>
        </div>
        <div class="{wrap_class} reveal delay-1">
            <table>
                <thead><tr>{thead}</tr></thead>
                <tbody>{tbody}</tbody>
            </table>
        </div>
        {footer_html}
    </div>
</section>
"""


def render_text_section(slide: dict, idx: int, total: int) -> str:
    eyebrow = render_inline(slide.get("eyebrow", ""))
    title = render_inline(slide.get("title", ""))
    subtitle = render_inline(slide.get("subtitle", ""))
    paragraphs = slide.get("paragraphs", [])
    bullets = slide.get("bullets", [])
    highlight = slide.get("highlight_box")

    para_html = "".join(
        f'<p class="reveal delay-{i+1}">{render_inline(p)}</p>'
        for i, p in enumerate(paragraphs)
    )
    bullets_html = ""
    if bullets:
        items = "".join(f"<li>{render_inline(b)}</li>" for b in bullets)
        bullets_html = f'<ul class="text-bullets reveal delay-{len(paragraphs)+1}">{items}</ul>'

    highlight_html = (
        f'<div class="highlight-box reveal delay-{len(paragraphs)+2}">{render_inline(highlight)}</div>'
        if highlight else ""
    )
    subtitle_html = f'<div class="subtitle">{subtitle}</div>' if subtitle else ""
    return f"""
<section class="slide" data-slide="{idx}">
    <div class="slide-number"><span class="current">{idx+1:02d}</span> / {total:02d}</div>
    <div class="slide-content">
        <div class="section-header reveal">
            <div class="eyebrow">{eyebrow}</div>
            <h2 class="section">{title}</h2>
            {subtitle_html}
        </div>
        <div class="text-body">
            {para_html}
            {bullets_html}
            {highlight_html}
        </div>
    </div>
</section>
"""


def render_recommendation(slide: dict, idx: int, total: int) -> str:
    eyebrow = render_inline(slide.get("eyebrow", "Nossa recomendacao"))
    headline = render_inline(slide.get("headline", ""))
    accent = render_inline(slide.get("accent", ""))
    sub = render_inline(slide.get("sub", ""))
    items = slide.get("items", [])
    footer = render_inline(slide.get("footer_note", ""))

    accent_html = f'<span class="accent">{accent}</span>' if accent else ""
    items_html_parts = []
    for i, it in enumerate(items):
        items_html_parts.append(f"""
            <div class="recommend-item reveal delay-{i+3}">
                <div class="num">{i+1:02d}</div>
                <div class="body">
                    <strong>{render_inline(it.get('title',''))}</strong>
                    <span>{render_inline(it.get('body',''))}</span>
                </div>
            </div>""")
    items_html = "".join(items_html_parts)
    footer_html = (
        f'<div class="recommend-footer reveal delay-{len(items)+3}">{footer}</div>'
        if footer else ""
    )
    return f"""
<section class="slide" data-slide="{idx}">
    <div class="slide-number"><span class="current">{idx+1:02d}</span> / {total:02d}</div>
    <div class="cover-decor"></div>
    <div class="slide-content recommend">
        <div class="recommend-eyebrow reveal">{eyebrow}</div>
        <h1 class="recommend-headline reveal delay-1">{headline} {accent_html}</h1>
        <div class="recommend-sub reveal delay-2">{sub}</div>
        <div class="recommend-list">{items_html}
        </div>
        {footer_html}
    </div>
</section>
"""


def render_next_steps(slide: dict, idx: int, total: int) -> str:
    eyebrow = render_inline(slide.get("eyebrow", "Proximos passos"))
    title = render_inline(slide.get("title", ""))
    cards = slide.get("cards", [])
    cta = render_inline(slide.get("cta", ""))
    n = max(1, len(cards))

    cards_html_parts = []
    for i, c in enumerate(cards):
        opts = render_inline(c.get("options", ""))
        opts_html = f'<div class="options">{opts}</div>' if opts else ""
        cards_html_parts.append(f"""
            <div class="next-card reveal delay-{i+1}">
                <div class="step">{i+1:02d}</div>
                <div class="head">{render_inline(c.get('head',''))}</div>
                <div class="q">{render_inline(c.get('question',''))}</div>
                {opts_html}
            </div>""")
    cards_html = "".join(cards_html_parts)
    cta_html = f'<div class="cta reveal delay-{n+1}">{cta}</div>' if cta else ""
    return f"""
<section class="slide" data-slide="{idx}">
    <div class="slide-number"><span class="current">{idx+1:02d}</span> / {total:02d}</div>
    <div class="slide-content">
        <div class="section-header reveal">
            <div class="eyebrow">{eyebrow}</div>
            <h2 class="section">{title}</h2>
        </div>
        <div class="next-grid" style="grid-template-columns: repeat({min(n,4)}, 1fr);">{cards_html}
        </div>
        {cta_html}
    </div>
</section>
"""


def render_closing(slide: dict, idx: int, total: int) -> str:
    headline = render_inline(slide.get("headline", "Obrigado."))
    sub = render_inline(slide.get("sub", ""))
    brand = render_inline(slide.get("brand", "Singular Group"))
    return f"""
<section class="slide" data-slide="{idx}">
    <div class="slide-number"><span class="current">{idx+1:02d}</span> / {total:02d}</div>
    <div class="cover-decor"></div>
    <div class="slide-content recommend">
        <h1 class="recommend-headline reveal">{headline}</h1>
        <div class="recommend-sub reveal delay-1">{sub}</div>
    </div>
    <div class="singular-mark">{brand}</div>
</section>
"""


RENDERERS = {
    "cover": render_cover,
    "summary-cards": render_summary_cards,
    "section-detail": render_section_detail,
    "compare-table": render_compare_table,
    "text-section": render_text_section,
    "recommendation": render_recommendation,
    "next-steps": render_next_steps,
    "closing": render_closing,
}


# ---------------- CSS + JS shell ----------------

CSS = r"""
:root {
    --ink: #1C1C1C;
    --ink-soft: #2A2727;
    --paper: #F7EEEB;
    --paper-dim: #E8DCD7;
    --white: #FFFFFF;
    --copper: #E64E10;
    --copper-soft: rgba(230, 78, 16, 0.18);
    --copper-line: rgba(230, 78, 16, 0.35);
    --copper-bg: rgba(230, 78, 16, 0.07);
    --copper-table: rgba(230, 78, 16, 0.09);
    --steel: #5B4B48;
    --copper-dim: #C55A48;
    --green: #2E7D32;
    --red: #B23A3A;
    --muted: rgba(247, 238, 235, 0.55);
    --muted-strong: rgba(247, 238, 235, 0.75);
    --rule: rgba(247, 238, 235, 0.12);

    /* Tipografia Singular: Urbanist principal, fallback Inter/Montserrat */
    --serif: 'Urbanist', 'Inter', 'Montserrat', system-ui, sans-serif;
    --sans: 'Urbanist', 'Inter', 'Montserrat', system-ui, -apple-system, sans-serif;

    --title-size: clamp(1.5rem, 5vw, 4rem);
    --hero-size: clamp(3rem, 11vw, 9rem);
    --h2-size: clamp(1.4rem, 3.2vw, 2.4rem);
    --h3-size: clamp(1rem, 1.7vw, 1.4rem);
    --body-size: clamp(0.78rem, 1.05vw, 1rem);
    --small-size: clamp(0.65rem, 0.85vw, 0.8rem);
    --micro-size: clamp(0.6rem, 0.7vw, 0.7rem);

    --slide-padding: clamp(1.5rem, 4vw, 4rem);
    --content-gap: clamp(0.75rem, 2vw, 2rem);
    --element-gap: clamp(0.4rem, 1vw, 1rem);
}

* { box-sizing: border-box; margin: 0; padding: 0; }

html, body {
    height: 100%;
    overflow-x: hidden;
    background: var(--ink);
    color: var(--paper);
    font-family: var(--sans);
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

html { scroll-snap-type: y mandatory; scroll-behavior: smooth; }

.slide {
    width: 100vw; height: 100vh; height: 100dvh;
    overflow: hidden;
    scroll-snap-align: start;
    display: flex; flex-direction: column;
    position: relative;
    background: var(--ink);
}

.slide-content {
    flex: 1;
    display: flex; flex-direction: column;
    justify-content: center;
    max-height: 100%; overflow: hidden;
    padding: var(--slide-padding);
    position: relative; z-index: 2;
}

.slide::before {
    content: ''; position: absolute; inset: 0;
    background-image: radial-gradient(circle at 1px 1px, rgba(247,238,235,0.015) 1px, transparent 0);
    background-size: 4px 4px;
    pointer-events: none; z-index: 1;
}

.eyebrow {
    font-family: var(--sans);
    font-size: var(--small-size); font-weight: 500;
    letter-spacing: 0.22em; text-transform: uppercase;
    color: var(--copper);
    margin-bottom: clamp(0.75rem, 1.5vw, 1.5rem);
}

h1.hero {
    font-family: var(--serif); font-weight: 800;
    font-size: var(--hero-size); line-height: 0.95;
    letter-spacing: -0.025em; color: var(--paper);
}

h1.title {
    font-family: var(--serif); font-weight: 700;
    font-size: clamp(1.8rem, 3.5vw, 2.8rem);
    line-height: 1.1; letter-spacing: -0.015em;
    color: var(--paper);
    margin-bottom: clamp(0.4rem, 1vw, 0.8rem);
}

h2.section {
    font-family: var(--serif); font-weight: 700;
    font-size: var(--h2-size); line-height: 1.15;
    letter-spacing: -0.01em; color: var(--paper);
}

.subtitle {
    font-family: var(--sans);
    font-size: clamp(0.9rem, 1.3vw, 1.15rem); font-weight: 400;
    line-height: 1.4; color: var(--muted-strong);
    max-width: 60ch;
}

/* Cover */
.cover { align-items: flex-start; justify-content: space-between;
    padding-top: clamp(2rem, 6vw, 5rem); padding-bottom: clamp(2rem, 6vw, 5rem); }
.cover-top { width: 100%; }
.cover-mid { display: flex; flex-direction: column; gap: clamp(0.5rem, 1.2vw, 1rem); }
.cover-mid .sub { font-size: clamp(1rem, 1.6vw, 1.4rem); color: var(--muted-strong); letter-spacing: 0.02em; }
.cover-bottom {
    display: flex; justify-content: space-between; align-items: flex-end; width: 100%;
    border-top: 1px solid var(--rule);
    padding-top: clamp(1rem, 1.5vw, 1.5rem);
    font-size: var(--body-size); color: var(--muted-strong); letter-spacing: 0.04em;
}
.cover-bottom .right { color: var(--copper); font-weight: 500; }

.cover-decor {
    position: absolute;
    right: calc(-1 * clamp(4rem, 12vw, 12rem));
    top: 50%; transform: translateY(-50%);
    width: clamp(20rem, 45vw, 50rem);
    height: clamp(20rem, 45vw, 50rem);
    background: radial-gradient(circle at center, var(--copper-soft) 0%, transparent 65%);
    pointer-events: none; z-index: 1;
}

/* summary-cards */
.opts-grid {
    display: grid;
    gap: clamp(0.75rem, 1.5vw, 1.5rem);
    margin-top: clamp(1.5rem, 3vw, 3rem);
}
.opt-card {
    background: var(--ink-soft);
    border: 1px solid var(--rule);
    border-radius: 4px;
    padding: clamp(1rem, 2vw, 2rem);
    display: flex; flex-direction: column;
    gap: clamp(0.5rem, 1vw, 1rem);
    position: relative;
}
.opt-card .opt-tag {
    font-family: var(--sans);
    font-size: var(--small-size); font-weight: 600;
    letter-spacing: 0.18em; text-transform: uppercase;
    color: var(--copper);
}
.opt-card .opt-title {
    font-family: var(--serif);
    font-size: clamp(1.1rem, 1.6vw, 1.5rem); font-weight: 600;
    line-height: 1.2; color: var(--paper);
}
.opt-card .opt-body { font-size: var(--body-size); line-height: 1.5; color: var(--muted-strong); }
.opt-card.recommended {
    border-color: var(--copper-line);
    background: linear-gradient(180deg, var(--copper-bg) 0%, var(--ink-soft) 100%);
}

.section-header { display: flex; flex-direction: column; gap: 0.4rem; margin-bottom: clamp(0.5rem, 1vw, 1rem); }
.footer-note { margin-top: clamp(1rem, 2vw, 2rem); font-size: var(--small-size); color: var(--muted); letter-spacing: 0.02em; font-style: italic; }

/* section-detail */
.option-header { margin-bottom: clamp(1rem, 2vw, 2rem); }
.option-header .badge {
    display: inline-block;
    background: var(--copper); color: var(--ink);
    padding: 0.3rem 0.7rem;
    font-size: var(--small-size); font-weight: 700;
    letter-spacing: 0.15em; text-transform: uppercase;
    border-radius: 2px; margin-bottom: 0.75rem;
}
.detail-grid {
    display: grid; gap: clamp(0.75rem, 1.5vw, 1.5rem);
}
.detail-card {
    background: var(--ink-soft); border: 1px solid var(--rule);
    padding: clamp(1rem, 1.8vw, 1.75rem);
    display: flex; flex-direction: column; gap: 0.6rem;
}
.detail-card .label {
    font-family: var(--sans);
    font-size: var(--small-size); font-weight: 600;
    letter-spacing: 0.2em; text-transform: uppercase;
    color: var(--copper);
}
.detail-card .value { font-size: var(--body-size); line-height: 1.5; color: var(--paper); }

.highlight-box {
    margin-top: clamp(1rem, 2vw, 1.75rem);
    background: linear-gradient(135deg, var(--copper-soft) 0%, rgba(230,78,16,0.06) 100%);
    border: 1px solid var(--copper-line);
    padding: clamp(0.85rem, 1.6vw, 1.4rem) clamp(1rem, 2vw, 1.75rem);
    border-radius: 3px;
    font-family: var(--serif);
    font-size: clamp(1rem, 1.5vw, 1.3rem); font-weight: 500;
    color: var(--paper); line-height: 1.35;
}
.highlight-box strong { color: var(--copper); font-weight: 700; }

/* text-section */
.text-body { display: flex; flex-direction: column; gap: clamp(0.6rem, 1vw, 0.9rem); }
.text-body p { font-size: clamp(0.95rem, 1.3vw, 1.1rem); line-height: 1.55; color: var(--paper); }
.text-bullets { list-style: none; padding: 0; margin-top: clamp(0.5rem, 1vw, 1rem); display: flex; flex-direction: column; gap: clamp(0.4rem, 0.7vw, 0.7rem); }
.text-bullets li {
    font-size: var(--body-size); color: var(--paper); line-height: 1.5;
    padding-left: 1.4rem; position: relative;
}
.text-bullets li::before {
    content: ''; position: absolute; left: 0; top: 0.65rem;
    width: 0.6rem; height: 1px; background: var(--copper);
}

/* tables */
.table-wrap { margin-top: clamp(1rem, 2vw, 1.75rem); }
table { width: 100%; border-collapse: collapse; font-size: var(--body-size); }
table th, table td {
    padding: clamp(0.5rem, 1vw, 0.85rem) clamp(0.6rem, 1.2vw, 1rem);
    text-align: left; border-bottom: 1px solid var(--rule);
}
table th {
    font-family: var(--sans);
    font-size: var(--small-size); font-weight: 600;
    letter-spacing: 0.12em; text-transform: uppercase;
    color: var(--muted-strong);
    border-bottom: 1px solid var(--copper-line);
}
table th.base-col, table td.base-col { background: var(--copper-table); color: var(--paper); }
table th.base-col { color: var(--copper); }
table td.label-cell { font-weight: 500; color: var(--muted-strong); }
table td.strong { font-weight: 600; color: var(--paper); }
table .pos { color: var(--green); font-weight: 600; }
table .neg { color: var(--red); }

.compare-wrap table th, .compare-wrap table td {
    padding: clamp(0.45rem, 0.9vw, 0.75rem) clamp(0.5rem, 1vw, 0.9rem);
    font-size: clamp(0.72rem, 0.95vw, 0.92rem);
    line-height: 1.35;
}
.compare-wrap table th:first-child, .compare-wrap table td:first-child {
    color: var(--muted-strong); font-weight: 500; width: 22%;
}

/* recommendation */
.recommend { align-items: center; text-align: center; justify-content: center; }
.recommend-eyebrow {
    font-family: var(--sans);
    font-size: var(--small-size); font-weight: 500;
    letter-spacing: 0.3em; text-transform: uppercase;
    color: var(--copper);
    margin-bottom: clamp(0.75rem, 1.5vw, 1.5rem);
}
.recommend-headline {
    font-family: var(--serif); font-weight: 800;
    font-size: clamp(2.5rem, 7vw, 6rem);
    line-height: 1; letter-spacing: -0.02em;
    margin-bottom: clamp(0.75rem, 1.5vw, 1.25rem);
    color: var(--paper);
}
.recommend-headline .accent { color: var(--copper); font-style: italic; }
.recommend-sub {
    font-size: clamp(1rem, 1.6vw, 1.35rem);
    color: var(--muted-strong);
    margin-bottom: clamp(1.5rem, 3vw, 3rem);
    max-width: 50ch;
}
.recommend-list {
    display: grid; grid-template-columns: repeat(2, 1fr);
    gap: clamp(0.85rem, 1.6vw, 1.5rem);
    text-align: left;
    max-width: min(85vw, 950px); width: 100%;
}
.recommend-item {
    display: flex; gap: clamp(0.75rem, 1.2vw, 1rem);
    padding: clamp(0.75rem, 1.2vw, 1rem);
    border-left: 2px solid var(--copper);
    background: var(--copper-bg);
}
.recommend-item .num {
    font-family: var(--serif);
    font-size: clamp(1.3rem, 2.2vw, 1.9rem); font-weight: 700;
    color: var(--copper); line-height: 1; flex-shrink: 0;
}
.recommend-item .body { font-size: var(--body-size); line-height: 1.4; }
.recommend-item .body strong {
    color: var(--paper); font-weight: 600;
    display: block; margin-bottom: 0.2rem;
    font-family: var(--serif);
    font-size: clamp(0.95rem, 1.3vw, 1.1rem);
}
.recommend-item .body span { color: var(--muted-strong); }
.recommend-footer {
    margin-top: clamp(1.25rem, 2.5vw, 2.25rem);
    font-size: var(--body-size); color: var(--copper);
    font-style: italic; max-width: 60ch;
}

/* next-steps */
.next-grid {
    display: grid; gap: clamp(0.75rem, 1.5vw, 1.5rem);
    margin-top: clamp(1.25rem, 2.5vw, 2.25rem);
}
.next-card {
    background: var(--ink-soft); border: 1px solid var(--rule);
    padding: clamp(1rem, 1.8vw, 1.75rem);
    display: flex; flex-direction: column; gap: 0.75rem;
    min-height: clamp(11rem, 22vh, 16rem);
}
.next-card .step {
    font-family: var(--serif);
    font-size: clamp(1.6rem, 3vw, 2.4rem); font-weight: 700;
    color: var(--copper); line-height: 1;
}
.next-card .head {
    font-family: var(--serif);
    font-size: clamp(1rem, 1.5vw, 1.3rem); font-weight: 600;
    color: var(--paper); text-transform: uppercase; letter-spacing: 0.06em;
}
.next-card .q { font-size: var(--body-size); line-height: 1.4; color: var(--muted-strong); }
.next-card .options {
    margin-top: auto;
    font-size: var(--small-size);
    color: var(--copper); font-family: var(--sans); letter-spacing: 0.04em;
}
.cta {
    margin-top: clamp(1.25rem, 2.5vw, 2.25rem);
    text-align: center;
    background: var(--copper); color: var(--ink);
    padding: clamp(0.9rem, 1.5vw, 1.4rem) clamp(1.5rem, 3vw, 3rem);
    font-family: var(--serif);
    font-size: clamp(1.05rem, 1.7vw, 1.5rem); font-weight: 700;
    border-radius: 2px; letter-spacing: 0.01em;
}

.singular-mark {
    position: absolute; bottom: clamp(0.75rem, 1.5vw, 1.5rem);
    right: clamp(0.75rem, 1.5vw, 1.5rem);
    font-family: var(--serif); font-style: italic;
    font-size: var(--small-size); color: var(--muted);
    letter-spacing: 0.05em; z-index: 3;
}

.slide-number {
    position: absolute; top: clamp(1rem, 2vw, 2rem); right: clamp(1rem, 2vw, 2rem);
    font-family: var(--sans);
    font-size: var(--small-size); font-weight: 500;
    letter-spacing: 0.18em; color: var(--muted); z-index: 3;
}
.slide-number .current { color: var(--copper); font-weight: 600; }

/* nav dots */
.nav-dots {
    position: fixed; right: clamp(1rem, 1.8vw, 2rem);
    top: 50%; transform: translateY(-50%);
    display: flex; flex-direction: column;
    gap: clamp(0.4rem, 0.8vw, 0.7rem); z-index: 100;
}
.nav-dot {
    width: 7px; height: 7px; border-radius: 50%;
    background: rgba(247, 238, 235, 0.18);
    border: none; cursor: pointer;
    transition: all 0.3s ease; padding: 0;
}
.nav-dot:hover { background: var(--muted-strong); }
.nav-dot.active { background: var(--copper); transform: scale(1.4); }

/* reveal */
.reveal {
    opacity: 0; transform: translateY(18px);
    transition: opacity 0.7s cubic-bezier(0.2, 0.65, 0.3, 1),
                transform 0.7s cubic-bezier(0.2, 0.65, 0.3, 1);
}
.reveal.visible { opacity: 1; transform: translateY(0); }
.reveal.delay-1 { transition-delay: 0.1s; }
.reveal.delay-2 { transition-delay: 0.22s; }
.reveal.delay-3 { transition-delay: 0.34s; }
.reveal.delay-4 { transition-delay: 0.46s; }
.reveal.delay-5 { transition-delay: 0.58s; }
.reveal.delay-6 { transition-delay: 0.7s; }
.reveal.delay-7 { transition-delay: 0.82s; }

.keyboard-hint {
    position: fixed; bottom: clamp(0.75rem, 1.2vw, 1.2rem);
    left: clamp(0.75rem, 1.2vw, 1.2rem);
    font-family: var(--sans);
    font-size: var(--micro-size);
    color: var(--muted);
    letter-spacing: 0.15em; text-transform: uppercase;
    opacity: 0.5; z-index: 100; pointer-events: none;
}

@media (max-height: 800px) {
    .opt-card, .detail-card, .next-card { padding: clamp(0.75rem, 1.4vw, 1.2rem); }
    .recommend-list { gap: 0.6rem; }
    .recommend-item { padding: 0.6rem 0.85rem; }
}
@media (max-height: 700px) {
    :root {
        --slide-padding: clamp(1rem, 3vw, 2.5rem);
        --content-gap: clamp(0.5rem, 1.5vw, 1rem);
        --hero-size: clamp(2.5rem, 9vw, 6rem);
    }
}
@media (max-height: 600px) {
    :root { --slide-padding: clamp(0.75rem, 2.5vw, 1.75rem); --hero-size: clamp(2rem, 7vw, 4rem); }
    .nav-dots, .keyboard-hint { display: none; }
}
@media (max-width: 800px) {
    .opts-grid, .detail-grid, .next-grid, .recommend-list { grid-template-columns: 1fr !important; }
    .compare-wrap { font-size: 0.75rem; }
    .compare-wrap table th, .compare-wrap table td { padding: 0.4rem 0.5rem; }
}
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        transition-duration: 0.2s !important;
    }
    html { scroll-behavior: auto; }
    .reveal { opacity: 1; transform: none; }
}
"""

JS = r"""
class PresentationController {
    constructor() {
        this.slides = document.querySelectorAll('.slide');
        this.dots = document.querySelectorAll('.nav-dot');
        this.currentSlide = 0;
        this.isScrolling = false;
        this.bindKeyboard();
        this.bindWheel();
        this.bindTouch();
        this.bindDots();
        this.bindObserver();
    }
    bindKeyboard() {
        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowDown' || e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {
                e.preventDefault(); this.next();
            } else if (e.key === 'ArrowUp' || e.key === 'ArrowLeft' || e.key === 'PageUp') {
                e.preventDefault(); this.prev();
            } else if (e.key === 'Home') { e.preventDefault(); this.go(0); }
            else if (e.key === 'End') { e.preventDefault(); this.go(this.slides.length - 1); }
        });
    }
    bindWheel() {
        let acc = 0; let last = 0;
        document.addEventListener('wheel', (e) => {
            const now = Date.now();
            if (now - last < 80) return;
            last = now;
            acc += e.deltaY;
            if (Math.abs(acc) > 50) {
                if (acc > 0) this.next(); else this.prev();
                acc = 0;
            }
        }, { passive: true });
    }
    bindTouch() {
        let startY = 0;
        document.addEventListener('touchstart', (e) => { startY = e.touches[0].clientY; }, { passive: true });
        document.addEventListener('touchend', (e) => {
            const diff = startY - e.changedTouches[0].clientY;
            if (Math.abs(diff) > 50) { if (diff > 0) this.next(); else this.prev(); }
        }, { passive: true });
    }
    bindDots() {
        this.dots.forEach((d, i) => d.addEventListener('click', () => this.go(i)));
    }
    bindObserver() {
        const io = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    const idx = parseInt(entry.target.dataset.slide, 10);
                    if (!isNaN(idx)) {
                        this.currentSlide = idx;
                        this.dots.forEach((d, i) => d.classList.toggle('active', i === idx));
                        entry.target.querySelectorAll('.reveal').forEach((el) => el.classList.add('visible'));
                    }
                }
            });
        }, { threshold: 0.5 });
        this.slides.forEach((s) => io.observe(s));
    }
    next() { this.go(Math.min(this.currentSlide + 1, this.slides.length - 1)); }
    prev() { this.go(Math.max(this.currentSlide - 1, 0)); }
    go(i) {
        if (i < 0 || i >= this.slides.length) return;
        this.slides[i].scrollIntoView({ behavior: 'smooth' });
    }
}
document.addEventListener('DOMContentLoaded', () => { new PresentationController(); });
"""


# ---------------- Main ----------------

def build(content: dict) -> str:
    meta = content.get("meta", {})
    slides = content.get("slides", [])
    total = len(slides)
    if total == 0:
        raise SystemExit("content.json: lista de slides vazia.")

    title = esc(meta.get("title", "Apresentacao Singular"))
    description = esc(meta.get("subtitle", ""))

    slides_html_parts = []
    for idx, slide in enumerate(slides):
        stype = slide.get("type")
        if stype not in RENDERERS:
            raise SystemExit(f"Slide {idx}: tipo desconhecido '{stype}'. Tipos validos: {sorted(RENDERERS)}")
        slides_html_parts.append(RENDERERS[stype](slide, idx, total))
    slides_html = "".join(slides_html_parts)

    nav_dots = "\n".join(
        f'    <button class="nav-dot{" active" if i == 0 else ""}" data-slide="{i}" aria-label="Slide {i+1}"></button>'
        for i in range(total)
    )

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{title}</title>
<meta name="description" content="{description}" />
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Urbanist:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>

<nav class="nav-dots" aria-label="Navegacao">
{nav_dots}
</nav>

<div class="keyboard-hint">Setas / Espaco / Wheel / Swipe</div>

<main>
{slides_html}
</main>

<script>
{JS}
</script>
</body>
</html>
"""


def main():
    if len(sys.argv) < 3:
        print("Uso: python build_html.py content.json saida.html", file=sys.stderr)
        sys.exit(1)
    content_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    if not content_path.exists():
        print(f"Erro: nao encontrei {content_path}", file=sys.stderr)
        sys.exit(2)
    with content_path.open("r", encoding="utf-8") as f:
        content = json.load(f)
    output_path.write_text(build(content), encoding="utf-8")
    size_kb = output_path.stat().st_size / 1024
    n_slides = len(content.get("slides", []))
    print(f"Gerado: {output_path} ({size_kb:.1f}KB, {n_slides} slides)")


if __name__ == "__main__":
    main()
