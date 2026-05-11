---
name: mp4
description: Converte arquivo MP4 (ou outros videos) em MP3. Abre file picker do Windows pro usuario escolher o video, extrai audio via ffmpeg e salva em C:/Users/teste/Desktop/transcricao/. Use quando o usuario digitar /mp4 ou pedir "converte mp4 em mp3", "extrai audio de video".
---

# Skill: /mp4 — MP4 -> MP3

Converte qualquer video em MP3 e salva no Desktop/transcricao.

## Workflow

1. Rodar o script Python que abre file picker do Windows:
   ```bash
   python "C:/Users/teste/.claude/skills/mp4/convert.py"
   ```
2. O script:
   - Abre dialogo do Windows pro usuario escolher o .mp4
   - Extrai audio via ffmpeg bundled (imageio-ffmpeg, libmp3lame 192kbps, 44.1kHz)
   - Cria pasta `C:/Users/teste/Desktop/transcricao/` se nao existir
   - Salva como `<nome-original>.mp3` la dentro
   - Se ja existir arquivo com mesmo nome, adiciona timestamp pra nao sobrescrever
   - Mostra popup de confirmacao no fim
3. (Opcional, default ON quando o mp3 e um output final pro Robertin) Upload pra raiz da pasta **Zel** no Drive via MCP `google-drive`:
   - Tool: `mcp__google-drive__uploadFile`
   - Args: `localPath` = path absoluto do .mp3, `parentFolderId: "10ARKUMWyFzVkdaPEWLYC9OXWqm0ywS6e"` (raiz Zel), `convertToGoogleFormat: false`
   - **Skipar upload** quando o mp3 e claramente arquivo intermediario que vai ser transcrito em seguida (ex.: o usuario pediu so a conversao porque ele mesmo vai usar localmente). Em duvida, perguntar.

## Nao faca

- Nao tente rodar ffmpeg direto no shell — nao esta no PATH global, use sempre o script (que usa imageio-ffmpeg bundled)
- Nao assuma caminho do arquivo — deixa o usuario escolher via picker
- Nao mude a pasta de destino sem o usuario pedir (Desktop/transcricao e fixo por design)

## Dependencias

- Python 3.13+ (ja instalado)
- `imageio-ffmpeg` (ja instalado via pip — traz ffmpeg bundled)
- `tkinter` (stdlib, ja disponivel)

## Troubleshooting

- **"imageio-ffmpeg nao instalado"**: `pip install imageio-ffmpeg`
- **Nada acontece ao chamar /mp4**: janela do tkinter pode ter aberto atras de outras. Olhar taskbar.
- **Erro de conversao**: rodar o script no terminal pra ver log do ffmpeg.
