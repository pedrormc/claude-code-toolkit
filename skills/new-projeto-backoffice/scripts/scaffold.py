"""scaffold.py - Cria a estrutura de um projeto Singular novo seguindo o
padrao de arquitetura obrigatorio (feedback_architecture_memory_pattern),
ja com a 4a dimensao de taxonomia (bu) carimbada.

Standalone (so stdlib). NAO acessa rede. Idempotente: nao sobrescreve
PROJETO.md nem project_<slug>.md se ja existirem (apenas avisa).

Cria em disco (passos 1 a 3 do padrao de 6 passos):
  1. C:/Users/teste/plano/singular/_bu/<bu>/<slug>/            (raiz do projeto)
  2. <slug>/PROJETO.md                                         (doc canonical)
  3. <slug>/memory/ + MEMORY.md (indice) + project_<slug>.md   (memoria tipada)

Depois imprime o CHECKLIST MANUAL dos passos que envolvem rede / git e que o
script NAO executa (passos 4 a 6 do padrao): nota Obsidian, /ingest no
Singular_Memory, git init/add/commit.

Uso:
  py -3 scaffold.py --nome "Nome Legivel" --slug nome-kebab --bu backoffice-tech \
      [--cross-bu apoio-financeiro,apoio-juridico] [--categoria singular]

bu: backoffice-tech
[Registrado por: DESKTOP - 2026-06-05]
"""

import argparse
import os
import sys

# --- importa a taxonomia canonica (SoT dos slugs de bu) -----------------
# scripts/memory/taxonomy.py exporta BU_SLUGS, BU_DONO, is_valid_bu, validate.
_MEMORY_DIR = r"C:/Users/teste/.claude/scripts"
if _MEMORY_DIR not in sys.path:
    sys.path.insert(0, _MEMORY_DIR)

try:
    from memory import taxonomy  # noqa: E402
except Exception as exc:  # pragma: no cover - so falha se a SoT sumir
    sys.stderr.write(
        "ERRO: nao consegui importar a taxonomia canonica de %s\n"
        "  (esperado memory/taxonomy.py). Detalhe: %r\n" % (_MEMORY_DIR, exc)
    )
    sys.exit(2)

DATA = "2026-06-05"
SINGULAR_ROOT = r"C:/Users/teste/plano/singular/_bu"


# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------
def _is_kebab(slug):
    """slug kebab valido: minusculas, digitos e hifen; nao comeca/termina com hifen."""
    if not slug:
        return False
    if slug[0] == "-" or slug[-1] == "-":
        return False
    return all(c.islower() or c.isdigit() or c == "-" for c in slug)


def _parse_cross_bu(raw):
    """'a,b , c' -> ['a', 'b', 'c'] (sem vazios)."""
    if not raw:
        return []
    return [s.strip() for s in raw.split(",") if s.strip()]


def _write_if_absent(path, content):
    """Escreve content em path so se nao existir. Retorna (escreveu, motivo)."""
    if os.path.exists(path):
        return False, "ja existe (preservado, nao sobrescrevi)"
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(content)
    return True, "criado"


def _cross_bu_yaml(cross_bu):
    """Renderiza a lista cross_bu pra YAML inline: [] ou [a, b]."""
    if not cross_bu:
        return "[]"
    return "[" + ", ".join(cross_bu) + "]"


# ----------------------------------------------------------------------
# Templates
# ----------------------------------------------------------------------
def projeto_md(nome, slug, bu, cross_bu, categoria, dono):
    cb = _cross_bu_yaml(cross_bu)
    return """---
title: "%s"
slug: %s
categoria: %s
bu: %s
cross_bu: %s
layer: TODO        # front-office / middle-office / back-office / opco / investida / cliente
area: TODO         # 1 dos valores de AREAS (ou null se layer=opco)
entidade: TODO     # holding / consultorio / fabrica-marketing / ...
status: active
created: "%s"
updated: "%s"
---

# %s

> Documento canonical (PROJETO.md) do projeto. Fonte de verdade humana viva.
> BU dona: **%s** (dono: %s). Cross-BU: %s.

## Visao geral

TODO: descrever em 1 a 3 frases o que e este projeto, qual dor resolve e por
que ele existe dentro da Singular. Preencher os placeholders de taxonomia no
frontmatter (layer / area / entidade) assim que estiverem definidos: a skill
`/bu` ajuda a carimbar.

## Arquitetura

TODO: descrever a arquitetura. Este projeto segue o padrao de arquitetura
obrigatorio Singular (memory + MEMORY.md indice + doc canonical + Qdrant
Singular_Memory + Obsidian mirror + Git). Listar componentes, integracoes,
stack e fluxos principais aqui conforme forem definidos.

## Pendencias

- [ ] Preencher layer / area / entidade no frontmatter (usar `/bu` se precisar).
- [ ] Criar nota espelho no Obsidian vault.
- [ ] Ingerir PROJETO.md no Singular_Memory (`/ingest`).
- [ ] `git init` / primeiro commit (se este projeto virar repo proprio).
- [ ] Detalhar Visao geral e Arquitetura.

*[Registrado por: DESKTOP - %s]*
""" % (nome, slug, categoria, bu, cb, DATA, DATA, nome, bu, dono, cb, DATA)


def memory_index_md(nome, slug, bu):
    return """# Memory Index - %s

> Indice da memoria do projeto **%s** (bu: %s). Cada entrada aponta pra um
> arquivo de memoria tipado nesta pasta. Mantenha este indice atualizado a
> cada nova memoria adicionada.

## Project
- [project_%s](project_%s.md) - memoria raiz do projeto: contexto, decisoes, estado.

## Feedback
- (vazio) - adicionar aprendizados e correcoes de rumo aqui conforme surgirem.

## Reference
- (vazio) - adicionar referencias tecnicas e fontes externas aqui.

*[Registrado por: DESKTOP - %s]*
""" % (nome, nome, bu, slug, slug, DATA)


def project_memory_md(nome, slug, bu, cross_bu, dono):
    cb = _cross_bu_yaml(cross_bu)
    return """---
title: "%s"
node_type: memory
type: project
slug: %s
bu: %s
cross_bu: %s
created: "%s"
updated: "%s"
---

# %s - memoria raiz

> Memoria tipada raiz do projeto. Resumo vivo do estado, decisoes e contexto.
> BU dona: **%s** (dono: %s).

## Estado atual

TODO: descrever o estado atual do projeto (recem-criado via scaffold em %s).

## Decisoes

TODO: registrar decisoes relevantes conforme forem tomadas (o que / por que / quando).

## Contexto

TODO: contexto necessario pra retomar o projeto sem perda. Apontar pro
PROJETO.md (doc canonical) e pra qualquer fonte externa (Drive, Qdrant, repo).

*[Registrado por: DESKTOP - %s]*
""" % (nome, slug, bu, cb, DATA, DATA, nome, bu, dono, DATA, DATA)


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------
def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Scaffold de projeto Singular novo (padrao 6 passos) ja com bu.",
    )
    parser.add_argument("--nome", required=True, help="Nome legivel do projeto.")
    parser.add_argument("--slug", required=True, help="Slug kebab-case (pasta).")
    parser.add_argument("--bu", required=True, help="BU primaria (slug). Validado pela taxonomia.")
    parser.add_argument("--cross-bu", default="", help="BUs secundarias, separadas por virgula.")
    parser.add_argument("--categoria", default="singular", help="Categoria de projeto (default: singular).")
    args = parser.parse_args(argv)

    nome = args.nome.strip()
    slug = args.slug.strip()
    bu = args.bu.strip()
    cross_bu = _parse_cross_bu(args.cross_bu)
    categoria = args.categoria.strip()

    # --- validacao de entrada -----------------------------------------
    errs = []
    if not _is_kebab(slug):
        errs.append("--slug %r nao e kebab-case valido (minusculas, digitos, hifen)." % slug)
    if not taxonomy.is_valid_bu(bu):
        errs.append(
            "--bu %r invalido. Slugs validos: %s"
            % (bu, ", ".join(sorted(taxonomy.BU_SLUGS)))
        )
    # valida cross_bu (e que nao repita a primaria) via taxonomy.validate
    for verr in taxonomy.validate(bu=bu, cross_bu=cross_bu):
        errs.append(verr)
    if bu in cross_bu:
        errs.append("--cross-bu nao pode conter a propria bu primaria %r." % bu)

    if errs:
        sys.stderr.write("Falha de validacao:\n")
        for e in errs:
            sys.stderr.write("  - %s\n" % e)
        return 1

    dono = taxonomy.BU_DONO.get(bu, "-")

    # --- passo 1: arvore ----------------------------------------------
    bu_dir = os.path.join(SINGULAR_ROOT, bu)
    proj_dir = os.path.join(bu_dir, slug)
    mem_dir = os.path.join(proj_dir, "memory")
    os.makedirs(mem_dir, exist_ok=True)  # cria proj_dir e memory de uma vez

    print("[scaffold] projeto: %s" % nome)
    print("[scaffold] bu primaria: %s (dono: %s) | cross_bu: %s"
          % (bu, dono, cross_bu or "nenhum"))
    print("[scaffold] raiz: %s" % proj_dir)
    print()

    # --- passo 2: PROJETO.md (canonical, idempotente) -----------------
    projeto_path = os.path.join(proj_dir, "PROJETO.md")
    wrote, why = _write_if_absent(projeto_path, projeto_md(nome, slug, bu, cross_bu, categoria, dono))
    print("  [%s] PROJETO.md (%s)" % ("OK" if wrote else "SKIP", why))

    # --- passo 3: memory/ + MEMORY.md + project_<slug>.md (idempotente) -
    mem_index_path = os.path.join(mem_dir, "MEMORY.md")
    wrote, why = _write_if_absent(mem_index_path, memory_index_md(nome, slug, bu))
    print("  [%s] memory/MEMORY.md (%s)" % ("OK" if wrote else "SKIP", why))

    proj_mem_path = os.path.join(mem_dir, "project_%s.md" % slug)
    wrote, why = _write_if_absent(proj_mem_path, project_memory_md(nome, slug, bu, cross_bu, dono))
    print("  [%s] memory/project_%s.md (%s)" % ("OK" if wrote else "SKIP", slug, why))

    # --- passos 4 a 6: checklist manual (NAO executados aqui) ----------
    obsidian = r"C:/Users/teste/Documents/obsidiano/singular/%s.md" % slug
    print()
    print("=" * 64)
    print("CHECKLIST MANUAL (passos 4-6 do padrao - este script NAO faz rede/git):")
    print("=" * 64)
    print()
    print("[ ] 4. Obsidian mirror")
    print("       Criar nota espelho no vault (marcar origem Desktop):")
    print("         %s" % obsidian)
    print("       frontmatter: title / category: %s / bu: %s / status: active /" % (categoria, bu))
    print("                    created+updated: %s" % DATA)
    print()
    print("[ ] 5. Ingest Singular_Memory")
    print("       Indexar PROJETO.md no Qdrant (collection Singular_Memory,")
    print("       http://3.237.66.68:6333) com payload {layer, area, entidade,")
    print("       bu: %s, cross_bu: %s}." % (bu, cross_bu or "[]"))
    print("       Rodar a skill /ingest, ou o pipeline manual a partir de")
    print("       C:/Users/teste/.claude/scripts/:")
    print("         py -3 -m memory.seed_from_jsonl --jsonl <dump.jsonl> --dry-run")
    print("       (cada linha do JSONL leva bu/cross_bu explicitos no record).")
    print()
    print("[ ] 6. Git")
    print("       Se o projeto virar repo proprio:")
    print("         git init")
    print("         git add PROJETO.md memory/")
    print('         git commit -m "chore: scaffold projeto %s (bu: %s)"' % (slug, bu))
    print("       Seguir a regra pull -> commit -> push se houver remote.")
    print()
    print("Lembrete: preencher os placeholders layer/area/entidade no frontmatter")
    print("do PROJETO.md e do project_%s.md (use /bu pra carimbar)." % slug)
    print()
    print("*[Registrado por: DESKTOP - %s]*" % DATA)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
