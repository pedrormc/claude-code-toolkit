"""Converte MP4 em MP3 via ffmpeg bundled (imageio-ffmpeg).
Abre file picker do Windows, salva em C:/Users/teste/Desktop/transcricao.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from tkinter import Tk, filedialog, messagebox

try:
    import imageio_ffmpeg
except ImportError:
    print("ERRO: imageio-ffmpeg nao instalado. Rode: pip install imageio-ffmpeg", file=sys.stderr)
    sys.exit(1)


DESKTOP = Path.home() / "Desktop"
OUTPUT_DIR = DESKTOP / "transcricao"


def pick_mp4() -> Path | None:
    root = Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    path = filedialog.askopenfilename(
        title="Escolha um arquivo MP4 para converter",
        filetypes=[("Video MP4", "*.mp4"), ("Todos videos", "*.mp4 *.mov *.mkv *.avi *.webm"), ("Todos arquivos", "*.*")],
        initialdir=str(Path.home()),
    )
    root.destroy()
    return Path(path) if path else None


def convert(src: Path, dst: Path) -> None:
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    cmd = [
        ffmpeg,
        "-y",
        "-i", str(src),
        "-vn",
        "-acodec", "libmp3lame",
        "-ab", "192k",
        "-ar", "44100",
        str(dst),
    ]
    subprocess.run(cmd, check=True)


def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    src = pick_mp4()
    if not src:
        print("Cancelado: nenhum arquivo selecionado.")
        return 1
    if not src.exists():
        print(f"ERRO: arquivo nao existe: {src}", file=sys.stderr)
        return 2

    dst = OUTPUT_DIR / (src.stem + ".mp3")
    if dst.exists():
        dst = OUTPUT_DIR / f"{src.stem}_{int(Path(src).stat().st_mtime)}.mp3"

    print(f"Convertendo: {src.name}")
    print(f"Destino:     {dst}")
    try:
        convert(src, dst)
    except subprocess.CalledProcessError as e:
        print(f"ERRO na conversao (exit {e.returncode})", file=sys.stderr)
        return 3

    print(f"OK: {dst}")
    try:
        root = Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        messagebox.showinfo("MP4 -> MP3", f"Pronto!\n\nSalvo em:\n{dst}")
        root.destroy()
    except Exception:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
