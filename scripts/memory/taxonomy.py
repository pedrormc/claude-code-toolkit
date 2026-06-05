"""Taxonomia canonica Singular - fonte unica de verdade (SoT) dos slugs.

Centraliza as 4 dimensoes de catalogacao usadas em todo o ecossistema:
  - layer  (camada arquitetural)
  - area   (especializacao funcional)
  - entidade (entidade concreta)
  - bu     (unidade de negocio dona, Regra Soberana #4) + cross_bu

Importado por: seed_from_jsonl.py, create_collection.py, a skill /ingest e
qualquer pipeline que escreva no Singular_Memory. Em vez de hardcodar slugs e
heuristicas em cada script (que foi o gap apontado na auditoria 2026-06-05),
tudo passa por aqui.

SoT human-readable:
  - feedback_taxonomy_3d_singular.md  (layer/area/entidade)
  - feedback_bu_taxonomy_singular.md  (bu)

bu: backoffice-tech
[Registrado por: DESKTOP - 2026-06-05]
"""

# ===================== DIMENSAO 1: layer =====================
LAYERS = {
    "front-office", "middle-office", "back-office",
    "opco", "investida", "cliente",
}

# ===================== DIMENSAO 2: area =====================
AREAS = {
    "ma-captacao", "rp", "novos-negocios",
    "venture-builder", "gestao-portfolio", "bi-analytics",
    "tecnologia", "financas", "people-workspace", "juridico",
}  # None / "null" tambem e valido quando layer=opco

# ===================== DIMENSAO 3: entidade =====================
ENTIDADES = {
    "holding", "consultorio", "marketplace", "fabrica-marketing",
    "smup", "doc-n-easy", "bedran-nexoadv", "kristalo", "gecop",
    "portal-fitbox", "valora",
    "ponto-do-queijo", "lumi-estetica", "dom-parmegiana", "aurani",
    "mundo-fit", "ecomanias", "com-amor-bee", "ad-energia",
    "loe-odontologia", "powercoffee", "cafe-pix", "gloria",
}

# ===================== DIMENSAO 4: bu (Regra Soberana #4) =====================
# tipo de cada slug: bu (core) / apoio / portfolio / macro
BU_CORE = {
    "consultorio-comercial", "consultorio-operacional",
    "fabrica-marketing", "produtora-rp", "backoffice-tech",
}
BU_APOIO = {
    "apoio-financeiro", "apoio-juridico", "apoio-pessoas",
    "apoio-cs", "apoio-contabil",
}
BU_PORTFOLIO = {
    "portfolio-power-coffee", "portfolio-doc-n-easy", "portfolio-smup",
    "portfolio-kristalo", "portfolio-gecop",
}
BU_MACRO = {"holding", "generico"}
BU_SLUGS = BU_CORE | BU_APOIO | BU_PORTFOLIO | BU_MACRO

BU_DONO = {
    "consultorio-comercial": "Simon",
    "consultorio-operacional": "Arthur Trojan",
    "fabrica-marketing": "Carol",
    "produtora-rp": "Ana Luiza",
    "backoffice-tech": "Robertinho + Volpi",
    "apoio-financeiro": "Sergio",
    "apoio-juridico": "Isa",
    "apoio-pessoas": "Claudia",
    "apoio-cs": "vazio (Claudia candidata)",
    "apoio-contabil": "JPC",
}

# ===================== MAPEAMENTOS DE INFERENCIA =====================
# entidade (investida do portfolio novo "O Essencial") -> bu portfolio
_ENTIDADE_PORTFOLIO = {
    "smup": "portfolio-smup",
    "doc-n-easy": "portfolio-doc-n-easy",
    "kristalo": "portfolio-kristalo",
    "gecop": "portfolio-gecop",
    "powercoffee": "portfolio-power-coffee",
}
# investidas antigas que NAO estao no portfolio "O Essencial" -> macro holding
_ENTIDADE_FORA_PORTFOLIO = {"bedran-nexoadv", "portal-fitbox", "valora", "marketplace"}
# area do back-office -> bu de apoio/tech
_AREA_BU = {
    "tecnologia": "backoffice-tech",
    "financas": "apoio-financeiro",
    "juridico": "apoio-juridico",
    "people-workspace": "apoio-pessoas",
}


# ===================== VALIDADORES =====================
def is_valid_bu(slug):
    return slug in BU_SLUGS


def is_valid_entidade(slug):
    return slug in ENTIDADES


def validate(layer=None, area=None, entidade=None, bu=None, cross_bu=None):
    """Valida um conjunto de tags. Retorna lista de erros (vazia = ok)."""
    errs = []
    if layer is not None and layer not in LAYERS:
        errs.append("layer invalido: %r" % layer)
    if area not in (None, "null") and area not in AREAS:
        errs.append("area invalida: %r" % area)
    if entidade is not None and entidade not in ENTIDADES:
        errs.append("entidade invalida: %r" % entidade)
    if bu is not None and bu not in BU_SLUGS:
        errs.append("bu invalido: %r" % bu)
    for c in (cross_bu or []):
        if c not in BU_SLUGS:
            errs.append("cross_bu invalido: %r" % c)
    return errs


# ===================== INFERENCIA DE BU =====================
def infer_bu(layer=None, area=None, entidade=None):
    """Infere a bu primaria a partir das 3 dimensoes antigas.

    Retorna (bu, confident: bool). confident=False sinaliza chute de baixa
    confianca (o chamador deve logar/avisar, NUNCA gravar silenciosamente).
    Para artefato novo, prefira sempre bu EXPLICITO em vez de inferencia.
    """
    # 1) Cliente do Consultorio -> entrega operacional
    if layer == "cliente":
        return "consultorio-operacional", True
    # 2) Investida do portfolio novo
    if entidade in _ENTIDADE_PORTFOLIO:
        return _ENTIDADE_PORTFOLIO[entidade], True
    # 3) Investida antiga fora do portfolio / marketplace -> macro holding
    if entidade in _ENTIDADE_FORA_PORTFOLIO:
        return "holding", True
    # 4) Fabrica de Marketing (opco = bu)
    if entidade == "fabrica-marketing":
        return "fabrica-marketing", True
    # 5) Consultorio
    if entidade == "consultorio":
        if area == "novos-negocios":
            return "consultorio-comercial", True
        return "consultorio-operacional", True
    # 6) Holding / back-middle-front office: usa a area
    if area in _AREA_BU:
        return _AREA_BU[area], True
    if layer in ("front-office", "middle-office"):
        return "holding", True
    if layer == "back-office":
        return "backoffice-tech", True
    # 7) Fallback de baixa confianca
    return "backoffice-tech", False


def coerce_taxonomy(rec, infer=True):
    """A partir de um dict (doc record), retorna as 4 dimensoes normalizadas.

    Prioridade: valor EXPLICITO no rec > inferencia (se infer=True).
    Retorna (dict {layer, area, entidade, bu, cross_bu}, inferred: bool).
    """
    layer = rec.get("layer")
    area = rec.get("area")
    entidade = rec.get("entidade")
    bu = rec.get("bu")
    cross_bu = rec.get("cross_bu") or []
    inferred = False
    if not bu and infer:
        bu, confident = infer_bu(layer, area, entidade)
        inferred = not confident
    return ({"layer": layer, "area": area, "entidade": entidade,
             "bu": bu, "cross_bu": cross_bu}, inferred)
