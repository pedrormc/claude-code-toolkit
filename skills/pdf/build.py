#!/usr/bin/env python3
"""
/pdf — gerador de PDF formal com identidade visual da Singular.

Lê um content.json (mesmo schema da skill /documento) e gera um PDF
profissional, pronto para apresentar a cliente/sócio/fornecedor.

Identidade visual (não negociável):
  - Logo Singular centralizada no topo de cada página
  - Fonte Urbanist (registrada de assets/fonts/)
  - Paleta: preto #1C1C1C sobre branco, callouts em cinza #F2F2F2
  - Cabeçalho de tabela preto com texto branco, linhas alternadas em cinza claro
  - Numeração de página no rodapé com linha divisória superior

Uso:
    python ~/.claude/skills/pdf/build.py content.json saida.pdf

Dependência única: reportlab (pip install reportlab).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    ListFlowable,
    ListItem,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

# ---- Paths and theme ----

SKILL_DIR = Path(__file__).parent
ASSETS = SKILL_DIR / "assets"
LOGO = ASSETS / "logo-singular.png"
FONT_DIR = ASSETS / "fonts"

# Singular palette
BLACK = colors.HexColor("#1C1C1C")
WHITE = colors.white
GREY_BG = colors.HexColor("#F2F2F2")
GREY_BORDER = colors.HexColor("#D9D9D9")
GREY_TEXT = colors.HexColor("#666666")

# Page geometry (A4 portrait)
PAGE_W, PAGE_H = A4
MARGIN_X = 2.2 * cm
MARGIN_TOP = 3.5 * cm  # espaço para logo
MARGIN_BOTTOM = 2.2 * cm
LOGO_W = 3.5 * cm  # ~ equivalente às 1.8" do template .docx, adaptado a A4
LOGO_RATIO = 1314 / 4854  # altura/largura do PNG oficial


# ---- Font registration ----

def _register_fonts() -> tuple[str, str]:
    """Registra Urbanist como fonte principal; cai para Helvetica se ausente."""
    urbanist = FONT_DIR / "Urbanist-Regular.ttf"
    if urbanist.exists():
        pdfmetrics.registerFont(TTFont("Urbanist", str(urbanist)))
        # Urbanist é variable font — usamos o mesmo arquivo para "bold" lógico;
        # hierarquia vem por tamanho/cor, não por peso real
        pdfmetrics.registerFont(TTFont("Urbanist-Bold", str(urbanist)))
        return "Urbanist", "Urbanist-Bold"
    return "Helvetica", "Helvetica-Bold"


FONT, FONT_BOLD = _register_fonts()


# ---- Styles ----

def _styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    s: dict[str, ParagraphStyle] = {}
    s["label"] = ParagraphStyle(
        "label", parent=base["Normal"], fontName=FONT_BOLD, fontSize=8.5,
        textColor=GREY_TEXT, leading=11, spaceAfter=2, alignment=TA_LEFT,
    )
    s["title"] = ParagraphStyle(
        "title", parent=base["Title"], fontName=FONT_BOLD, fontSize=24,
        textColor=BLACK, leading=28, spaceAfter=4, alignment=TA_LEFT,
    )
    s["subtitle"] = ParagraphStyle(
        "subtitle", parent=base["Normal"], fontName=FONT, fontSize=12,
        textColor=GREY_TEXT, leading=15, spaceAfter=14, alignment=TA_LEFT,
    )
    s["meta"] = ParagraphStyle(
        "meta", parent=base["Normal"], fontName=FONT, fontSize=9,
        textColor=GREY_TEXT, leading=12, spaceAfter=2, alignment=TA_LEFT,
    )
    s["tldr_label"] = ParagraphStyle(
        "tldr_label", parent=base["Normal"], fontName=FONT_BOLD, fontSize=8.5,
        textColor=BLACK, leading=11, spaceAfter=2, alignment=TA_LEFT,
    )
    s["h2"] = ParagraphStyle(
        "h2", parent=base["Heading2"], fontName=FONT_BOLD, fontSize=14,
        textColor=BLACK, leading=18, spaceBefore=16, spaceAfter=8, alignment=TA_LEFT,
    )
    s["h3"] = ParagraphStyle(
        "h3", parent=base["Heading3"], fontName=FONT_BOLD, fontSize=11,
        textColor=BLACK, leading=14, spaceBefore=10, spaceAfter=6, alignment=TA_LEFT,
    )
    s["body"] = ParagraphStyle(
        "body", parent=base["Normal"], fontName=FONT, fontSize=10,
        textColor=BLACK, leading=15, spaceAfter=6, alignment=TA_JUSTIFY,
    )
    s["bullet"] = ParagraphStyle(
        "bullet", parent=base["Normal"], fontName=FONT, fontSize=10,
        textColor=BLACK, leading=14, alignment=TA_LEFT,
    )
    s["destaque"] = ParagraphStyle(
        "destaque", parent=base["Normal"], fontName=FONT, fontSize=10,
        textColor=BLACK, leading=14, alignment=TA_LEFT,
    )
    s["footer_rod"] = ParagraphStyle(
        "footer_rod", parent=base["Normal"], fontName=FONT, fontSize=8.5,
        textColor=GREY_TEXT, leading=11, alignment=TA_CENTER,
    )
    return s


STYLES = _styles()


# ---- Page chrome ----

def _draw_page_chrome(c, doc) -> None:
    """Logo no topo + linha divisória + número de página."""
    c.saveState()
    if LOGO.exists():
        logo_h = LOGO_W * LOGO_RATIO
        x = (PAGE_W - LOGO_W) / 2
        y_top = PAGE_H - 2.0 * cm
        c.drawImage(
            str(LOGO), x, y_top - logo_h + 0.6 * cm,
            width=LOGO_W, height=logo_h, mask="auto", preserveAspectRatio=True,
        )
    c.setFont(FONT, 8)
    c.setFillColor(GREY_TEXT)
    c.drawCentredString(PAGE_W / 2, 1.2 * cm, f"Página {doc.page}")
    c.setStrokeColor(GREY_BORDER)
    c.setLineWidth(0.4)
    c.line(MARGIN_X, 1.7 * cm, PAGE_W - MARGIN_X, 1.7 * cm)
    c.restoreState()


# ---- Building blocks ----

def _callout(text: str) -> Table:
    para = Paragraph(text, STYLES["destaque"])
    t = Table([[para]], colWidths=[PAGE_W - 2 * MARGIN_X])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), GREY_BG),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LINEBEFORE", (0, 0), (0, -1), 2, BLACK),
    ]))
    return t


def _table(colunas: list[str], linhas: list[list]) -> Table:
    th_style = ParagraphStyle(
        "th", fontName=FONT_BOLD, fontSize=9.5, textColor=WHITE, leading=12,
    )
    td_style = ParagraphStyle(
        "td", fontName=FONT, fontSize=9.5, textColor=BLACK, leading=12,
    )
    head = [Paragraph(f"<b>{c}</b>", th_style) for c in colunas]
    body = [[Paragraph(str(cell), td_style) for cell in row] for row in linhas]
    data = [head] + body
    avail = PAGE_W - 2 * MARGIN_X
    col_widths = [avail / len(colunas)] * len(colunas)
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), BLACK),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, -1), FONT),
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("GRID", (0, 1), (-1, -1), 0.4, GREY_BORDER),
        ("LINEBELOW", (0, 0), (-1, 0), 0, WHITE),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style.append(("BACKGROUND", (0, i), (-1, i), GREY_BG))
    t.setStyle(TableStyle(style))
    return t


def _bullets(itens: list[str], numbered: bool = False) -> ListFlowable:
    style = STYLES["bullet"]
    items = [ListItem(Paragraph(it, style), leftIndent=6) for it in itens]
    return ListFlowable(
        items,
        bulletType="1" if numbered else "bullet",
        bulletFontName=FONT,
        bulletFontSize=10,
        bulletColor=BLACK,
        leftIndent=18,
        bulletDedent=10,
        spaceBefore=2,
        spaceAfter=6,
    )


def _render_secao(secao: dict, story: list) -> None:
    if titulo := secao.get("titulo"):
        story.append(Paragraph(titulo, STYLES["h2"]))
    for p in secao.get("paragrafos", []) or []:
        story.append(Paragraph(p, STYLES["body"]))
    for lst in secao.get("listas", []) or []:
        numbered = lst.get("tipo") == "numbered"
        story.append(_bullets(lst["itens"], numbered=numbered))
    for tb in secao.get("tabelas", []) or []:
        story.append(Spacer(1, 4))
        story.append(_table(tb["colunas"], tb["linhas"]))
        story.append(Spacer(1, 6))
    if d := secao.get("destaque"):
        story.append(Spacer(1, 4))
        story.append(_callout(d))
        story.append(Spacer(1, 6))
    for sub in secao.get("subsecoes", []) or []:
        story.append(Paragraph(sub.get("titulo", ""), STYLES["h3"]))
        for p in sub.get("paragrafos", []) or []:
            story.append(Paragraph(p, STYLES["body"]))


# ---- Public entry point ----

def build(content_path: Path, output_path: Path) -> None:
    data = json.loads(content_path.read_text(encoding="utf-8"))

    if "titulo" not in data or "secoes" not in data:
        raise ValueError("content.json precisa ter ao menos 'titulo' e 'secoes'.")

    doc = BaseDocTemplate(
        str(output_path), pagesize=A4,
        leftMargin=MARGIN_X, rightMargin=MARGIN_X,
        topMargin=MARGIN_TOP, bottomMargin=MARGIN_BOTTOM,
        title=data.get("titulo", "Documento Singular"),
        author=data.get("autor", "Singular Group"),
    )
    frame = Frame(
        MARGIN_X, MARGIN_BOTTOM,
        PAGE_W - 2 * MARGIN_X, PAGE_H - MARGIN_TOP - MARGIN_BOTTOM,
        id="normal", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
    )
    doc.addPageTemplates([
        PageTemplate(id="main", frames=[frame], onPage=_draw_page_chrome),
    ])

    story: list = []
    if label := data.get("titulo_curto"):
        story.append(Paragraph(label, STYLES["label"]))
    story.append(Paragraph(data["titulo"], STYLES["title"]))
    if sub := data.get("subtitulo"):
        story.append(Paragraph(sub, STYLES["subtitle"]))

    meta_bits: list[str] = []
    if a := data.get("autor"):
        meta_bits.append(f"<b>Autor:</b> {a}")
    if d := data.get("destinatario"):
        meta_bits.append(f"<b>Destinatário:</b> {d}")
    if dt := data.get("data"):
        meta_bits.append(f"<b>Data:</b> {dt}")
    if meta_bits:
        story.append(Paragraph(" &nbsp;·&nbsp; ".join(meta_bits), STYLES["meta"]))
    story.append(Spacer(1, 10))

    if tldr := data.get("tldr"):
        story.append(Paragraph("RESUMO EXECUTIVO", STYLES["tldr_label"]))
        story.append(_callout(tldr))
        story.append(Spacer(1, 6))

    for secao in data.get("secoes", []):
        _render_secao(secao, story)

    if conc := data.get("conclusao"):
        story.append(Paragraph("Conclusão", STYLES["h2"]))
        story.append(Paragraph(conc, STYLES["body"]))

    if pp := data.get("proximos_passos"):
        story.append(Paragraph("Próximos passos", STYLES["h2"]))
        story.append(_bullets(pp))

    if refs := data.get("referencias"):
        story.append(Paragraph("Referências", STYLES["h2"]))
        story.append(_bullets(refs))

    if rod := data.get("autor_rodape"):
        story.append(Spacer(1, 16))
        story.append(Paragraph(rod, STYLES["footer_rod"]))

    doc.build(story)
    print(f"Gerado: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("Uso: python build.py <content.json> <saida.pdf>")
    build(Path(sys.argv[1]), Path(sys.argv[2]))
