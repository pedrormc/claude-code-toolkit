"""Indexa UM artefato canonico Singular no Singular_Memory, com taxonomy 4D EXPLICITA.

Esta e a ponta da skill /ingest (Fase 3 do Backoffice Pro Max). Diferente do
seed_from_jsonl em modo "drive dump" (que infere tags por heuristica de path), aqui
a taxonomy 4D e EXIGIDA e VALIDADA antes de qualquer escrita. Sem fallback silencioso:
esse fallback foi exatamente o gap apontado na auditoria 2026-06-05, quando docs
entravam no Qdrant com bu inferida errada sem ninguem perceber.

Fluxo:
  1. Le os args (file, name, path-tag, layer, area, entidade, bu, cross-bu, infer-bu).
  2. Le o conteudo do arquivo (.md / .txt).
  3. VALIDA via memory.taxonomy.validate(...). Se layer/area/entidade/bu/cross_bu
     forem invalidos, ERRO claro e sai. Se bu estiver ausente:
       - sem --infer-bu  -> ERRO (exige bu explicito).
       - com --infer-bu  -> infere via taxonomy.infer_bu e AVISA qual bu foi inferida
                            (e se a inferencia e de baixa confianca).
  4. Monta um record JSONL com a taxonomy 4D explicita ja resolvida e escreve um
     .jsonl temporario em ~/.claude/.cache/ingest-tmp/.
  5. Invoca o pipeline real (memory.seed_from_jsonl) via subprocess, com
     cwd=C:/Users/teste/.claude/scripts, que sanitiza -> chunk parent-child ->
     embed (OpenAI dense + bm42 sparse) -> upsert idempotente (UUID5).
  6. Imprime resumo (arquivo, taxonomy aplicada, bu, status).

Uso:
  py ingest_doc.py --file <path.md> --name "Ata reuniao X" \\
     --path-tag "COMERCIAL/Spoleto" \\
     --layer opco --area novos-negocios --entidade consultorio \\
     --bu consultorio-comercial [--cross-bu fabrica-marketing,produtora-rp] \\
     [--infer-bu] [--dry-run]

bu: backoffice-tech
[Registrado por: DESKTOP - 2026-06-05]
"""
import os
import sys
import json
import uuid
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

# A SoT da taxonomia mora em C:/Users/teste/.claude/scripts/memory/taxonomy.py.
# A skill /ingest roda de qualquer cwd, entao injetamos o diretorio de scripts no
# sys.path pra conseguir "import memory.taxonomy" sem depender do cwd.
SCRIPTS_DIR = Path("C:/Users/teste/.claude/scripts")
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

try:
    from memory import taxonomy  # noqa: E402
except Exception as e:  # pragma: no cover - so dispara se o ambiente quebrar
    print(f"ERRO: nao consegui importar memory.taxonomy de {SCRIPTS_DIR}: {e}")
    sys.exit(2)

TMP_DIR = Path("~/.claude/.cache/ingest-tmp").expanduser()
MAX_CONTENT_CHARS = 200000  # corte de seguranca; o seed faz o chunking de verdade


def _parse_cross_bu(raw):
    """csv -> lista de slugs limpos. None / "" -> []."""
    if not raw:
        return []
    return [s.strip() for s in raw.split(",") if s.strip()]


def _stable_file_id(name, path_tag):
    """file_id determinístico: prioriza path-tag (logico e estavel), cai pro nome.

    Usa UUID5 sobre a string canonica pra dar idempotencia: re-ingerir o mesmo
    artefato (mesmo path-tag) gera o mesmo file_id, e o seed (UUID5 por chunk)
    sobrescreve em vez de duplicar.
    """
    seed_str = (path_tag or name or "").strip().lower()
    if not seed_str:
        seed_str = "ingest-" + datetime.utcnow().isoformat()
    return "ingest:" + str(uuid.uuid5(uuid.NAMESPACE_URL, seed_str))


def main():
    ap = argparse.ArgumentParser(
        description="Ingesta de 1 artefato canonico Singular no Singular_Memory (taxonomy 4D obrigatoria).")
    ap.add_argument("--file", required=True, help="Caminho do .md / .txt a indexar")
    ap.add_argument("--name", required=True, help="Titulo legivel do artefato")
    ap.add_argument("--path-tag", required=True,
                    help="Path logico (ex: COMERCIAL/Spoleto). Vira drive_path + file_id estavel.")
    ap.add_argument("--layer", required=True, help="Dimensao 1: layer")
    ap.add_argument("--area", default=None,
                    help="Dimensao 2: area (use 'null' ou omita quando layer=opco)")
    ap.add_argument("--entidade", required=True, help="Dimensao 3: entidade")
    ap.add_argument("--bu", default=None,
                    help="Dimensao 4: bu (Regra Soberana #4). Obrigatoria, salvo --infer-bu.")
    ap.add_argument("--cross-bu", default=None,
                    help="csv de bus adicionais quando o artefato serve 2+ frentes")
    ap.add_argument("--infer-bu", action="store_true",
                    help="Permite inferir bu via taxonomy.infer_bu quando --bu nao for dado (com aviso explicito).")
    ap.add_argument("--dry-run", action="store_true",
                    help="Valida + monta o JSONL e mostra o tagging, sem embed/upsert (passa --dry-run pro seed).")
    args = ap.parse_args()

    # ---------- 1) Le o arquivo ----------
    src = Path(args.file).expanduser()
    if not src.exists() or not src.is_file():
        print(f"ERRO: arquivo nao encontrado: {src}")
        return 1
    content = src.read_text(encoding="utf-8", errors="replace")
    if not content or len(content.strip()) < 20:
        print(f"ERRO: arquivo vazio ou curto demais pra indexar: {src} ({len(content)} chars)")
        return 1
    if len(content) > MAX_CONTENT_CHARS:
        content = content[:MAX_CONTENT_CHARS]

    # ---------- 2) Normaliza area / cross_bu ----------
    area = args.area
    if area in ("null", "none", "None", ""):
        area = None
    cross_bu = _parse_cross_bu(args.cross_bu)

    # ---------- 3) Resolve bu (explicito > inferido com --infer-bu) ----------
    bu = args.bu
    inferred_note = None
    if not bu:
        if not args.infer_bu:
            print("ERRO: --bu ausente e --infer-bu nao foi passado.")
            print("      Taxonomy 4D (Regra Soberana #4) exige bu EXPLICITO pra artefato canonico.")
            print("      Rode /bu pra classificar, ou passe --infer-bu pra aceitar inferencia (com aviso).")
            print(f"      Slugs validos: {sorted(taxonomy.BU_SLUGS)}")
            return 1
        bu, confident = taxonomy.infer_bu(layer=args.layer, area=area, entidade=args.entidade)
        if confident:
            inferred_note = f"bu inferida (alta confianca): {bu}"
        else:
            inferred_note = (f"bu inferida (BAIXA confianca): {bu} -- revise; "
                             f"o ideal e passar --bu explicito ou rodar /bu")
        print(f"[infer-bu] {inferred_note}")

    # ---------- 4) VALIDA a taxonomy 4D (sem fallback silencioso) ----------
    errs = taxonomy.validate(layer=args.layer, area=area, entidade=args.entidade,
                             bu=bu, cross_bu=cross_bu)
    if errs:
        print("ERRO de validacao de taxonomy 4D (nada foi indexado):")
        for e in errs:
            print(f"  - {e}")
        print()
        print(f"  layers validos:    {sorted(taxonomy.LAYERS)}")
        print(f"  areas validas:     {sorted(taxonomy.AREAS)} (ou null)")
        print(f"  entidades validas: {sorted(taxonomy.ENTIDADES)}")
        print(f"  bus validos:       {sorted(taxonomy.BU_SLUGS)}")
        return 1

    # ---------- 5) Monta o record JSONL com a taxonomy explicita ----------
    file_id = _stable_file_id(args.name, args.path_tag)
    record = {
        "file_id": file_id,
        "name": args.name,
        "path": args.path_tag,
        "mime_type": "text/markdown" if src.suffix.lower() == ".md" else "text/plain",
        "content": content,
        # taxonomy 4D EXPLICITA -> o seed estendido grava direto no payload,
        # sem cair na heuristica tag_from_path.
        "layer": args.layer,
        "area": area,
        "entidade": args.entidade,
        "bu": bu,
        "cross_bu": cross_bu,
    }

    TMP_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    tmp_jsonl = TMP_DIR / f"ingest-{stamp}-{uuid.uuid4().hex[:8]}.jsonl"
    tmp_jsonl.write_text(json.dumps(record, ensure_ascii=False) + "\n", encoding="utf-8")

    print("[ingest] artefato validado e enfileirado:")
    print(f"  arquivo:   {src}")
    print(f"  name:      {args.name}")
    print(f"  path-tag:  {args.path_tag}")
    print(f"  layer:     {args.layer}")
    print(f"  area:      {area}")
    print(f"  entidade:  {args.entidade}")
    print(f"  bu:        {bu}  (dono: {taxonomy.BU_DONO.get(bu, 'n/a')})")
    print(f"  cross_bu:  {cross_bu or 'nenhum'}")
    print(f"  chars:     {len(content)}")
    print(f"  jsonl tmp: {tmp_jsonl}")

    # ---------- 6) Chama o pipeline real (seed_from_jsonl) ----------
    cmd = [sys.executable, "-m", "memory.seed_from_jsonl", "--jsonl", str(tmp_jsonl)]
    if args.dry_run:
        cmd.append("--dry-run")
    print(f"[ingest] rodando: {' '.join(cmd)}  (cwd={SCRIPTS_DIR})")
    try:
        proc = subprocess.run(cmd, cwd=str(SCRIPTS_DIR))
    except FileNotFoundError:
        print("ERRO: nao consegui executar o interpretador Python pro seed_from_jsonl.")
        print(f"      Tente manualmente: cd {SCRIPTS_DIR} && py -3 -m memory.seed_from_jsonl --jsonl {tmp_jsonl}")
        return 1

    if proc.returncode != 0:
        print(f"[ingest] FALHA no seed (returncode={proc.returncode}). JSONL preservado em {tmp_jsonl}")
        return proc.returncode

    # Limpa o tmp em caso de sucesso real (mantem em dry-run pra inspecao)
    if not args.dry_run:
        try:
            tmp_jsonl.unlink()
        except OSError:
            pass

    print()
    print("=== /ingest OK ===")
    print(f"Artefato: {args.name}")
    print(f"Taxonomy 4D: layer={args.layer} area={area} entidade={args.entidade} "
          f"bu={bu} cross_bu={cross_bu or '[]'}")
    if inferred_note:
        print(f"Nota: {inferred_note}")
    print("Collection: Singular_Memory")
    return 0


if __name__ == "__main__":
    sys.exit(main())
