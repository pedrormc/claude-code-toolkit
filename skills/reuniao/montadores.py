"""
Montadores — convertem master.json em content.json específico de cada skill base.
Cada função recebe master (dict) e devolve content (dict) no schema da skill base.
"""

# ============================================================
# ATA — 1 montador (skill base: /ata)
# ============================================================

def _normalize_participantes(participantes_raw):
    """Aceita dict {presentes:[...], ausentes:[...]} onde cada item pode ser:
      - string -> mantém
      - dict {nome, papel} -> formata 'Nome — Papel'
    Schema do /ata/build.py espera SEMPRE lista de strings (caso contrário
    python-docx itera as chaves do dict e gera 'nomepapel' literal).
    """
    def _fmt(item):
        if isinstance(item, str):
            return item
        if isinstance(item, dict):
            nome = item.get("nome", "").strip()
            papel = item.get("papel", "").strip()
            if nome and papel:
                return f"{nome} — {papel}"
            return nome or papel or ""
        return str(item)
    raw = participantes_raw or {}
    return {
        "presentes": [_fmt(p) for p in raw.get("presentes", []) if _fmt(p)],
        "ausentes": [_fmt(p) for p in raw.get("ausentes", []) if _fmt(p)],
    }


def _normalize_topicos(topicos_raw):
    """Garante: discussao SEMPRE lista de strings, decisoes SEMPRE lista de strings.
    Sem isso o build.py do /ata itera 'for para in discussao' e quando recebe
    string ele itera CHAR a CHAR, virando uma coluna de letras na ata.
    """
    out = []
    for t in (topicos_raw or []):
        novo = {"titulo": t.get("titulo", "")}
        disc = t.get("discussao", [])
        if isinstance(disc, str):
            disc = [disc] if disc.strip() else []
        novo["discussao"] = list(disc)

        decisoes = t.get("decisoes") or t.get("decisao") or []
        if isinstance(decisoes, str):
            decisoes = [decisoes] if decisoes.strip() else []
        if decisoes:
            novo["decisoes"] = list(decisoes)

        if t.get("tabelas"):
            novo["tabelas"] = t["tabelas"]
        out.append(novo)
    return out


def monta_ata_reuniao(master):
    """Converte master.json em schema de /ata/build.py.
    Schema alvo: ver §5.4.1 do spec.
    """
    meta = master["meta"]
    cliente = meta.get("cliente", {})
    encam = master.get("encaminhamentos", [])

    # Título: reuniões internas (sem cliente externo) não levam o sufixo "× cliente".
    _cli_nome = (cliente.get("nome") or "").strip()
    _tipo = meta.get("tipo_reuniao", "Alinhamento")
    if _cli_nome and _cli_nome.lower() not in ("interna", "interno", "singular"):
        _titulo = f"Reunião de {_tipo} — Singular × {_cli_nome}"
    else:
        _titulo = f"Reunião de {_tipo} — Singular"

    return {
        "titulo_curto": "ATA",
        "titulo": _titulo,
        "header_subtitle": "Ata de Reunião",
        "empresa": "Singular",
        "data": meta["data"],
        "hora_inicio": meta.get("hora_inicio", ""),
        "hora_fim": meta.get("hora_fim", ""),
        "local": meta.get("local", ""),
        "tipo_reuniao": meta.get("tipo_reuniao", ""),
        "objetivo": master.get("objetivo", ""),
        "participantes": _normalize_participantes(master.get("participantes")),
        "pauta": master.get("pauta", []),
        "topicos": _normalize_topicos(master.get("topicos", [])),
        "encaminhamentos": {
            "titulo": "Encaminhamentos",
            "linhas": [["Ação", "Responsável", "Prazo"]] + [
                [e["acao"], e["responsavel"], e.get("prazo", "sem prazo")] for e in encam
            ],
        },
        "proxima_reuniao": master.get("proxima_reuniao", {}),
        "observacoes": master.get("observacoes", ""),
        "assinaturas": master.get("assinaturas", []),
    }


# ============================================================
# POPs — 3 montadores (skill base: /pop)
# ============================================================

def monta_pop_roteiro_roleplay(master):
    """POP de role-play comercial — converte roteiro_roleplay.* em passos sequenciais."""
    rp = master.get("roteiro_roleplay", {})
    cliente = master["meta"].get("cliente", {})
    passos = [
        {
            "titulo": "Passo 1 — Abordagem inicial",
            "paragrafos": [rp.get("abordagem_inicial", "A definir")],
            "acao_final": "Iniciar conversa com sondagem aberta.",
        },
        {
            "titulo": "Passo 2 — Apresentação de valor",
            "paragrafos": [rp.get("apresentacao_valor", "A definir")],
        },
        {
            "titulo": "Passo 3 — Tratamento de objeções",
            "listas": [{"titulo": "Objeções comuns e respostas:", "itens": rp.get("objeções", rp.get("objecoes", []))}],
        },
        {
            "titulo": "Passo 4 — Fechamento",
            "paragrafos": [rp.get("fechamento", "A definir")],
            "acao_final": "Sempre confirmar próximos passos antes de encerrar.",
        },
    ]
    return {
        "titulo_curto": "POP",
        "titulo": f"Processo Operacional de Role-Play Comercial — {cliente.get('nome', '')}",
        "empresa": "Singular",
        "versao": "1.0",
        "data": master["meta"]["data"],
        "objetivo": "Padronizar abordagem comercial e fechamento de vendas.",
        "fluxo_titulo": "Fluxo em 4 Passos",
        "passos": passos,
    }


def monta_pop_stand_vendas(master):
    """POP de stand de vendas em evento."""
    sv = master.get("stand_vendas", {})
    cliente = master["meta"].get("cliente", {})
    passos = [
        {"titulo": "Passo 1 — Montagem", "paragrafos": [sv.get("montagem", "A definir")]},
        {"titulo": "Passo 2 — Recepção do visitante", "paragrafos": [sv.get("fluxo_visitante", "A definir")]},
        {"titulo": "Passo 3 — Demonstração", "paragrafos": [sv.get("demonstracao", "A definir")]},
        {"titulo": "Passo 4 — Captura de lead", "paragrafos": [sv.get("captura_lead", "A definir")], "acao_final": "Sempre coletar contato antes do visitante sair."},
        {"titulo": "Passo 5 — Desmontagem e relatório", "paragrafos": [sv.get("desmontagem", "A definir")]},
    ]
    return {
        "titulo_curto": "POP",
        "titulo": f"Processo Operacional de Stand de Vendas — {cliente.get('nome', '')}",
        "empresa": "Singular",
        "versao": "1.0",
        "data": master["meta"]["data"],
        "objetivo": f"Padronizar operação de stand em evento presencial.",
        "perfil_secao": {"titulo": "Materiais necessários", "bullets": sv.get("materiais", [])},
        "fluxo_titulo": "Fluxo em 5 Passos",
        "passos": passos,
    }


def monta_pop_evento_degustacao(master):
    """POP de evento de degustação em local específico (academia, etc.)."""
    ed = master.get("evento_degustacao", {})
    local_slug = ed.get("local_slug", "academia")
    passos = [
        {"titulo": "Passo 1 — Pré-evento (preparação)", "paragrafos": [ed.get("preparacao", "A definir")]},
        {"titulo": "Passo 2 — Setup no local", "paragrafos": [ed.get("setup", "A definir")]},
        {"titulo": "Passo 3 — Execução da degustação", "paragrafos": [ed.get("execucao", "A definir")]},
        {"titulo": "Passo 4 — Coleta de feedback + lead", "paragrafos": [ed.get("feedback", "A definir")], "acao_final": "Registrar todo feedback no CRM no fim do dia."},
        {"titulo": "Passo 5 — Pós-evento", "paragrafos": [ed.get("pos_evento", "A definir")]},
    ]
    return {
        "titulo_curto": "POP",
        "titulo": f"Processo Operacional de Evento de Degustação — {local_slug.title()}",
        "empresa": "Singular",
        "versao": "1.0",
        "data": master["meta"]["data"],
        "objetivo": "Padronizar evento físico de degustação com captura de leads.",
        "perfil_secao": {"titulo": "Perfil do público", "bullets": [ed.get("publico", "A definir")]},
        "fluxo_titulo": "Fluxo em 5 Passos",
        "passos": passos,
    }


# ============================================================
# DOCUMENTOS — 13 montadores (skill base: /documento)
# ============================================================

def _autor_rodape(master):
    return f"Singular Group · {master['meta']['data']}"


def monta_doc_tarefas_completas(master):
    encam = master.get("encaminhamentos", [])
    por_resp = {}
    for e in encam:
        por_resp.setdefault(e["responsavel"], []).append(e)
    secoes = []
    for resp, tarefas in por_resp.items():
        secoes.append({
            "titulo": resp,
            "tabelas": [{
                "colunas": ["Ação", "Prazo"],
                "linhas": [[t["acao"], t.get("prazo", "sem prazo")] for t in tarefas],
            }],
        })
    if not secoes:
        secoes = [{"titulo": "Sem ações registradas", "paragrafos": ["A definir — reunião sem encaminhamentos claros."]}]
    return {
        "titulo_curto": "TAREFAS",
        "titulo": "Tarefas Consolidadas",
        "empresa": "Singular",
        "data": master["meta"]["data"],
        "tldr": f"{len(encam)} ações consolidadas por responsável.",
        "secoes": secoes,
        "autor_rodape": _autor_rodape(master),
    }


def monta_doc_plano_comercial(master):
    pc = master.get("plano_comercial", {})
    cliente = master["meta"].get("cliente", {})
    return {
        "titulo_curto": "PLANO",
        "titulo": f"Plano Comercial — {cliente.get('nome', '')}",
        "subtitulo": cliente.get("vertical", ""),
        "empresa": "Singular",
        "data": master["meta"]["data"],
        "tldr": pc.get("tldr", ""),
        "secoes": [
            {"titulo": "1. Metas comerciais", "listas": [{"itens": pc.get("metas", ["A definir"])}]},
            {"titulo": "2. Abordagem", "paragrafos": [pc.get("abordagem", "A definir")]},
            {"titulo": "3. Ticket médio alvo", "destaque": pc.get("ticket_medio", "A definir")},
            {"titulo": "4. Funil e conversão", "paragrafos": [pc.get("funil", "A definir")]},
        ],
        "autor_rodape": _autor_rodape(master),
    }


def monta_doc_proposta_comercial(master):
    p = master.get("proposta_comercial", {})
    cliente = master["meta"].get("cliente", {})
    return {
        "titulo_curto": "PROPOSTA",
        "titulo": f"Proposta Comercial — {cliente.get('nome', '')}",
        "empresa": "Singular",
        "destinatario": cliente.get("nome", ""),
        "data": master["meta"]["data"],
        "tldr": p.get("tldr", ""),
        "secoes": [
            {"titulo": "1. Escopo", "paragrafos": [p.get("escopo", "A definir")]},
            {"titulo": "2. Valor", "destaque": p.get("valor", "A definir")},
            {"titulo": "3. Prazo de entrega", "paragrafos": [p.get("prazo", "A definir")]},
            {"titulo": "4. Termos comerciais", "listas": [{"itens": p.get("termos", ["A definir"])}]},
        ],
        "proximos_passos": p.get("proximos_passos", []),
        "autor_rodape": _autor_rodape(master),
    }


def monta_doc_decisao(master):
    d = master.get("decisao_adr", {})
    return {
        "titulo_curto": "DECISÃO",
        "titulo": d.get("titulo", "Decisão Singular"),
        "empresa": "Singular",
        "data": master["meta"]["data"],
        "tldr": d.get("decisao", "A definir"),
        "secoes": [
            {"titulo": "1. Contexto", "paragrafos": [d.get("contexto", "A definir")]},
            {"titulo": "2. Decisão", "destaque": d.get("decisao", "A definir")},
            {"titulo": "3. Alternativas consideradas", "listas": [{"itens": d.get("alternativas", ["A definir"])}]},
            {"titulo": "4. Consequências", "listas": [{"itens": d.get("consequencias", ["A definir"])}]},
        ],
        "autor_rodape": _autor_rodape(master),
    }


def monta_doc_briefing_posicionamento(master):
    bp = master.get("briefing_posicionamento", {})
    cliente = master["meta"].get("cliente", {})
    return {
        "titulo_curto": "BRIEFING",
        "titulo": f"Briefing de Posicionamento — {cliente.get('nome', 'Singular')}",
        "subtitulo": cliente.get("vertical", ""),
        "empresa": "Singular",
        "data": master["meta"]["data"],
        "tldr": bp.get("tldr", ""),
        "secoes": [
            {"titulo": "1. Público-alvo", "paragrafos": [bp.get("publico_alvo", "A definir")]},
            {"titulo": "2. Tom de voz", "paragrafos": [bp.get("tom_voz", "A definir")]},
            {"titulo": "3. Posicionamento", "paragrafos": [bp.get("posicionamento", "A definir")]},
            {"titulo": "4. Diferenciação", "paragrafos": [bp.get("diferenciacao", "A definir")]},
            {"titulo": "5. Mensagem-chave", "destaque": bp.get("mensagem_chave", "A definir")},
        ],
        "autor_rodape": _autor_rodape(master),
    }


def monta_doc_cronograma_editorial(master):
    ce = master.get("cronograma_editorial", {})
    return {
        "titulo_curto": "CRONOGRAMA",
        "titulo": "Cronograma Editorial",
        "empresa": "Singular",
        "data": master["meta"]["data"],
        "tldr": f"Frequência: {ce.get('frequencia', 'A definir')}",
        "secoes": [
            {"titulo": "1. Frequência", "paragrafos": [ce.get("frequencia", "A definir")]},
            {"titulo": "2. Canais", "listas": [{"itens": ce.get("canais", ["A definir"])}]},
            {"titulo": "3. Temas e pautas", "listas": [{"itens": ce.get("temas", ["A definir"])}]},
        ],
        "autor_rodape": _autor_rodape(master),
    }


def monta_doc_estrategia_canal(master):
    ec = master.get("estrategia_canal", {})
    return {
        "titulo_curto": "ESTRATÉGIA",
        "titulo": f"Estratégia de Canal — {ec.get('canal_principal', 'Digital')}",
        "empresa": "Singular",
        "data": master["meta"]["data"],
        "tldr": ec.get("tldr", ""),
        "secoes": [
            {"titulo": "1. Canal principal", "destaque": ec.get("canal_principal", "A definir")},
            {"titulo": "2. Objetivos", "listas": [{"itens": ec.get("objetivos", ["A definir"])}]},
            {"titulo": "3. KPIs", "listas": [{"itens": ec.get("kpis", ["A definir"])}]},
        ],
        "autor_rodape": _autor_rodape(master),
    }


def monta_doc_fabrica_marketing(master):
    fm = master.get("fabrica_marketing", {})
    return {
        "titulo_curto": "OPERAÇÃO",
        "titulo": "Fábrica de Marketing — Pipeline de Produção",
        "empresa": "Singular",
        "data": master["meta"]["data"],
        "tldr": fm.get("tldr", ""),
        "secoes": [
            {"titulo": "1. Pipeline de produção", "listas": [{"itens": fm.get("pipeline", ["A definir"])}]},
            {"titulo": "2. Responsáveis", "listas": [{"itens": fm.get("responsaveis", ["A definir"])}]},
        ],
        "autor_rodape": _autor_rodape(master),
    }


def monta_doc_marketplace(master):
    mp = master.get("marketplace", {})
    return {
        "titulo_curto": "ESTRATÉGIA",
        "titulo": "Estratégia de Marketplace",
        "empresa": "Singular",
        "data": master["meta"]["data"],
        "tldr": mp.get("estrategia", "")[:200] if mp.get("estrategia") else "",
        "secoes": [
            {"titulo": "1. Plataformas", "listas": [{"itens": mp.get("plataformas", ["A definir"])}]},
            {"titulo": "2. Estratégia geral", "paragrafos": [mp.get("estrategia", "A definir")]},
        ],
        "autor_rodape": _autor_rodape(master),
    }


def monta_doc_memo_ficha_tecnica(master):
    m = master.get("memo_ficha_tecnica", {})
    return {
        "titulo_curto": "MEMO",
        "titulo": f"Memo / Ficha Técnica — {m.get('produto', 'Produto')}",
        "empresa": "Singular",
        "data": master["meta"]["data"],
        "tldr": m.get("tldr", ""),
        "secoes": [
            {"titulo": "1. Produto", "destaque": m.get("produto", "A definir")},
            {"titulo": "2. Atributos", "listas": [{"itens": m.get("atributos", ["A definir"])}]},
            {"titulo": "3. Diferenciais", "listas": [{"itens": m.get("diferenciais", ["A definir"])}]},
        ],
        "autor_rodape": _autor_rodape(master),
    }


def monta_doc_organizacao(master):
    o = master.get("organizacao", {})
    return {
        "titulo_curto": "ORG",
        "titulo": "Organização Singular — Estrutura e Donos",
        "empresa": "Singular",
        "data": master["meta"]["data"],
        "tldr": o.get("tldr", ""),
        "secoes": [
            {"titulo": "1. Células", "listas": [{"itens": o.get("celulas", ["A definir"])}]},
            {"titulo": "2. Donos", "listas": [{"itens": o.get("donos", ["A definir"])}]},
        ],
        "autor_rodape": _autor_rodape(master),
    }


def monta_doc_plano_embaixadores(master):
    pe = master.get("plano_embaixadores", {})
    return {
        "titulo_curto": "PLANO",
        "titulo": "Plano de Embaixadores",
        "empresa": "Singular",
        "data": master["meta"]["data"],
        "tldr": pe.get("tldr", ""),
        "secoes": [
            {"titulo": "1. Perfil do embaixador", "paragrafos": [pe.get("perfil", "A definir")]},
            {"titulo": "2. Remuneração", "destaque": pe.get("remuneracao", "A definir")},
            {"titulo": "3. Ativos disponíveis", "listas": [{"itens": pe.get("ativos", ["A definir"])}]},
        ],
        "autor_rodape": _autor_rodape(master),
    }


def monta_doc_leadgen(master):
    lg = master.get("leadgen", {})
    return {
        "titulo_curto": "ESTRATÉGIA",
        "titulo": "Lead Generation — Plug + Rank",
        "empresa": "Singular",
        "data": master["meta"]["data"],
        "tldr": lg.get("tldr", ""),
        "secoes": [
            {"titulo": "1. Canais de captação", "listas": [{"itens": lg.get("canais", ["A definir"])}]},
            {"titulo": "2. CPL alvo", "destaque": lg.get("cpl_alvo", "A definir")},
            {"titulo": "3. Estratégia de ranqueamento", "paragrafos": [lg.get("ranqueamento", "A definir")]},
        ],
        "autor_rodape": _autor_rodape(master),
    }

# ============================================================
# GENÉRICOS — montadores p/ tipos NOVOS brainstormados (auto-improve)
# Não ficam no MONTADORES (precisam de `spec`). Despachados em reuniao.py
# quando o catálogo traz spec["montador"] == "generico" | "generico_pop".
# ============================================================

def _plan_field(master, spec):
    """Chave em master.json onde mora o plano de conteúdo do doc brainstormado.
    Default: spec['master_field'], senão key com hífens→underscores.
    """
    field = spec.get("master_field") or spec["key"].replace("-", "_")
    return master.get(field, {}) or {}


def monta_doc_generico(master, spec):
    """Montador genérico p/ QUALQUER documento brainstormado (skill base: /documento).
    O plano de conteúdo (titulo/tldr/secoes/...) vem inteiro do master.json, montado
    pelo Claude no passo de brainstorm. Schema-alvo idêntico ao /documento/build.py.

    Plano esperado em master[<master_field>]:
      {titulo, titulo_curto?, subtitulo?, tldr?, destinatario?,
       secoes: [{titulo, paragrafos?|listas?|destaque?|tabelas?}], proximos_passos?}
    """
    plan = _plan_field(master, spec)
    cliente = master["meta"].get("cliente", {})
    secoes = plan.get("secoes") or [{"titulo": "Conteúdo", "paragrafos": ["A definir"]}]
    return {
        "titulo_curto": plan.get("titulo_curto", "DOC"),
        "titulo": plan.get("titulo") or spec.get("label") or "Documento",
        "subtitulo": plan.get("subtitulo", cliente.get("vertical", "")),
        "empresa": "Singular",
        "destinatario": plan.get("destinatario", ""),
        "data": master["meta"]["data"],
        "tldr": plan.get("tldr", ""),
        "secoes": secoes,
        "proximos_passos": plan.get("proximos_passos", []),
        "autor_rodape": _autor_rodape(master),
    }


def monta_pop_generico(master, spec):
    """Montador genérico p/ QUALQUER POP brainstormado (skill base: /pop).
    Plano esperado em master[<master_field>]:
      {titulo, objetivo?, versao?, fluxo_titulo?, perfil_secao?,
       passos: [{titulo, paragrafos?|listas?|acao_final?}]}
    """
    plan = _plan_field(master, spec)
    passos = plan.get("passos") or [{"titulo": "Passo 1", "paragrafos": ["A definir"]}]
    out = {
        "titulo_curto": "POP",
        "titulo": plan.get("titulo") or spec.get("label") or "Processo Operacional",
        "empresa": "Singular",
        "versao": plan.get("versao", "1.0"),
        "data": master["meta"]["data"],
        "objetivo": plan.get("objetivo", "A definir"),
        "fluxo_titulo": plan.get("fluxo_titulo", f"Fluxo em {len(passos)} Passos"),
        "passos": passos,
    }
    if plan.get("perfil_secao"):
        out["perfil_secao"] = plan["perfil_secao"]
    return out


GENERIC_MONTADORES = {
    "generico": monta_doc_generico,
    "generico_pop": monta_pop_generico,
}


# ============================================================
# REGISTRY — atualizado em cada chunk
# ============================================================

MONTADORES = {
    "ata-reuniao": monta_ata_reuniao,
    "doc-tarefas-completas": monta_doc_tarefas_completas,
    "doc-plano-comercial": monta_doc_plano_comercial,
    "doc-proposta-comercial": monta_doc_proposta_comercial,
    "doc-decisao": monta_doc_decisao,
    "doc-briefing-posicionamento": monta_doc_briefing_posicionamento,
    "doc-cronograma-editorial": monta_doc_cronograma_editorial,
    "doc-estrategia-canal": monta_doc_estrategia_canal,
    "doc-fabrica-marketing": monta_doc_fabrica_marketing,
    "doc-marketplace": monta_doc_marketplace,
    "doc-memo-ficha-tecnica": monta_doc_memo_ficha_tecnica,
    "doc-organizacao": monta_doc_organizacao,
    "doc-plano-embaixadores": monta_doc_plano_embaixadores,
    "doc-leadgen": monta_doc_leadgen,
    "pop-roteiro-roleplay": monta_pop_roteiro_roleplay,
    "pop-stand-vendas": monta_pop_stand_vendas,
    "pop-evento-degustacao": monta_pop_evento_degustacao,
}
