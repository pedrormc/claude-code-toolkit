"""
search.py — Busca multi-fonte de processos judiciais e presença pública por nome.

Uso:
    python search.py "NOME COMPLETO" [--cpf 000.000.000-00] [--out resultado.json]

Saída: JSON estruturado com:
- identidade (nome normalizado, slug, cpf opcional)
- fontes_consultadas: lista de fontes com {nome, url_consulta, status, resultados, observacao}
- links_diretos: URLs pre-formatadas pra busca manual (tribunais que exigem JS/captcha)
- bruto: HTML/JSON cru de quem retornou algo (limitado a 5KB por fonte)

Não persiste credenciais. Usa apenas endpoints públicos.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import unicodedata
import urllib.parse
from dataclasses import dataclass, field, asdict
from typing import Any

import requests
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
}

TIMEOUT = 15


def normalize(name: str) -> str:
    name = re.sub(r"\s+", " ", name.strip())
    return name


def to_slug(name: str) -> str:
    nfkd = unicodedata.normalize("NFKD", name)
    only_ascii = "".join(c for c in nfkd if not unicodedata.combining(c))
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", only_ascii).strip("-").lower()
    return slug


@dataclass
class Resultado:
    fonte: str
    url_consulta: str
    status: str  # "ok" | "links-only" | "erro" | "vazio"
    achados: list[dict] = field(default_factory=list)
    observacao: str = ""


def safe_get(url: str, **kwargs) -> requests.Response | None:
    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT, **kwargs)
        if r.status_code >= 500:
            return None
        return r
    except requests.RequestException:
        return None


def safe_post(url: str, json_body=None, **kwargs) -> requests.Response | None:
    try:
        r = requests.post(
            url, headers=HEADERS, json=json_body, timeout=TIMEOUT, **kwargs
        )
        if r.status_code >= 500:
            return None
        return r
    except requests.RequestException:
        return None


# ---------- ESCAVADOR ----------
def search_escavador(name: str) -> Resultado:
    q = urllib.parse.quote_plus(name)
    url = f"https://www.escavador.com/busca?q={q}"
    res = Resultado(fonte="Escavador", url_consulta=url, status="links-only")
    r = safe_get(url)
    if r is None or r.status_code != 200:
        res.observacao = f"http {r.status_code if r else 'timeout'} — abrir manualmente"
        return res
    soup = BeautifulSoup(r.text, "html.parser")
    achados = []
    for a in soup.select("a[href*='/sobre/']")[:10]:
        href = a.get("href", "")
        if not href.startswith("http"):
            href = "https://www.escavador.com" + href
        title = a.get_text(strip=True)
        if title:
            achados.append({"titulo": title, "url": href})
    if achados:
        res.status = "ok"
        res.achados = achados
    else:
        res.observacao = "sem matches públicos no HTML — abrir o link"
    return res


# ---------- DATAJUD CNJ ----------
# IMPORTANTE: A API pública do DataJud NÃO expõe nomes de partes (restrição LGPD).
# Os _source disponíveis são apenas metadados (numeroProcesso, classe, movimentos,
# assuntos, orgaoJulgador). Busca por nome só funciona via UI dos tribunais ou
# agregadores tipo Escavador. Mantemos referência aqui pra busca futura por NÚMERO.
DATAJUD_INFO_URL = "https://datajud-wiki.cnj.jus.br/api-publica/"


def link_datajud_info(name: str) -> Resultado:
    return Resultado(
        fonte="DataJud CNJ — API pública (info)",
        url_consulta=DATAJUD_INFO_URL,
        status="links-only",
        observacao="API pública NÃO permite busca por nome (LGPD). Use só com nº de processo conhecido.",
    )


# ---------- TRIBUNAIS COM BUSCA POR NOME (links-only, JS-heavy) ----------
def link_tst_pje(name: str) -> Resultado:
    q = urllib.parse.quote(name)
    url = f"https://pje.tst.jus.br/consultaprocessual/pages/consultas/ConsultaProcessual.seam?nomeParte={q}"
    return Resultado(
        fonte="TST/PJe — Justiça do Trabalho",
        url_consulta=url,
        status="links-only",
        observacao="Portal único do TST + TRTs. Busca por nome funciona via UI. CAPTCHA pode aparecer.",
    )


def link_stf(name: str) -> Resultado:
    q = urllib.parse.quote(name)
    url = f"https://portal.stf.jus.br/processos/listarProcessos.asp?classe=&numProcesso=&parte={q}"
    return Resultado(
        fonte="STF — Supremo Tribunal Federal",
        url_consulta=url,
        status="links-only",
        observacao="Busca por parte funciona — abrir e filtrar.",
    )


def link_stj(name: str) -> Resultado:
    q = urllib.parse.quote(name)
    url = f"https://processo.stj.jus.br/processo/pesquisa/?aplicacao=processos.ea&tipoPesquisa=tipoPesquisaGenerica&termo={q}"
    return Resultado(
        fonte="STJ — Superior Tribunal de Justiça",
        url_consulta=url,
        status="links-only",
        observacao="Pesquisa genérica aceita nome.",
    )


def link_tjdft_consulta(name: str) -> Resultado:
    q = urllib.parse.quote(name)
    url = (
        "https://pje-consulta-publica.tjdft.jus.br/consulta-publica/?"
        f"nomeDaParte={q}"
    )
    return Resultado(
        fonte="TJDFT — Tribunal de Justiça do DF",
        url_consulta=url,
        status="links-only",
        observacao="Pós-LGPD: pode exigir CPF além do nome no formulário.",
    )


def link_tjsp_esaj(name: str) -> Resultado:
    q = urllib.parse.quote(name)
    url = f"https://esaj.tjsp.jus.br/cpopg/search.do?conversationId=&cbPesquisa=NMPARTE&dadosConsulta.valorConsulta={q}"
    return Resultado(
        fonte="TJSP e-SAJ — São Paulo",
        url_consulta=url,
        status="links-only",
        observacao="Busca por nome de parte (1º grau).",
    )


def link_cnj_codex(name: str) -> Resultado:
    q = urllib.parse.quote(name)
    url = f"https://corporativo.cnj.jus.br/consultapublica/?nomeParte={q}"
    return Resultado(
        fonte="CNJ — Consulta Pública Unificada",
        url_consulta=url,
        status="links-only",
        observacao="Agregador de processos públicos. Disponibilidade varia.",
    )


def link_receita_pj_check(name: str) -> Resultado:
    q = urllib.parse.quote_plus(name)
    url = f"https://www.google.com/search?q=%22{q}%22+site%3Areceita.fazenda.gov.br+OR+site%3Acnpj.biz"
    return Resultado(
        fonte="Vínculo societário (PJ) — pesquisa indireta",
        url_consulta=url,
        status="links-only",
        observacao="Sem CPF, busca por nome em CNPJ.biz e RFB indica vínculos societários.",
    )


# ---------- GOOGLE / WEB ABERTA (links-only) ----------
def link_google_dorks(name: str) -> list[Resultado]:
    q = urllib.parse.quote_plus(f'"{name}"')
    dorks = [
        ("Mídia geral", f'https://www.google.com/search?q={q}'),
        ("LinkedIn", f'https://www.google.com/search?q={q}+site%3Alinkedin.com'),
        ("Notícias", f'https://www.google.com/search?q={q}&tbm=nws'),
        ("Diário Oficial / .gov.br", f'https://www.google.com/search?q={q}+site%3Agov.br'),
        ("Acadêmico", f'https://scholar.google.com/scholar?q={q}'),
        ("Imprensa Nacional (DOU)", f'https://www.google.com/search?q={q}+site%3Ain.gov.br'),
        ("Conselhos profissionais (CRM/OAB/CRO/CRC)", f'https://www.google.com/search?q={q}+%28OAB+OR+CRM+OR+CRO+OR+CRC+OR+CRP%29'),
        ("Mercado financeiro (CVM/B3)", f'https://www.google.com/search?q={q}+site%3Acvm.gov.br+OR+site%3Ab3.com.br'),
        ("Sanções (CGU/CEIS/CNEP)", f'https://portaldatransparencia.gov.br/sancoes/ceis?paginacaoSimples=true&termo={urllib.parse.quote(name)}'),
        ("TCU — Lista de inelegíveis", f'https://contas.tcu.gov.br/ords/f?p=INABILITADO:5'),
    ]
    return [
        Resultado(fonte=f"Google — {label}", url_consulta=u, status="links-only")
        for label, u in dorks
    ]


# ---------- ORQUESTRAÇÃO ----------
def run(name: str, cpf: str | None = None) -> dict[str, Any]:
    name = normalize(name)
    out = {
        "identidade": {
            "nome": name,
            "slug": to_slug(name),
            "cpf": cpf,
            "consultado_em": time.strftime("%Y-%m-%d %H:%M:%S"),
        },
        "fontes_consultadas": [],
    }

    fontes: list[Resultado] = []

    # ativas (com hit HTTP real)
    fontes.append(search_escavador(name))

    # links-only (JS-heavy, captcha, ou restrição LGPD)
    fontes.extend([
        link_tst_pje(name),
        link_stf(name),
        link_stj(name),
        link_tjdft_consulta(name),
        link_tjsp_esaj(name),
        link_cnj_codex(name),
        link_datajud_info(name),
        link_receita_pj_check(name),
    ])
    fontes.extend(link_google_dorks(name))

    out["fontes_consultadas"] = [asdict(f) for f in fontes]

    # resumo
    total_achados = sum(len(f.achados) for f in fontes)
    out["resumo"] = {
        "total_fontes": len(fontes),
        "fontes_com_match": sum(1 for f in fontes if f.achados),
        "total_achados": total_achados,
    }

    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("nome", help="Nome completo da pessoa")
    ap.add_argument("--cpf", default=None, help="CPF (opcional)")
    ap.add_argument("--out", default=None, help="Arquivo JSON de saída")
    args = ap.parse_args()

    result = run(args.nome, cpf=args.cpf)
    payload = json.dumps(result, ensure_ascii=False, indent=2)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(payload)
        print(f"[ok] salvo em {args.out} — {result['resumo']}")
    else:
        print(payload)


if __name__ == "__main__":
    main()
