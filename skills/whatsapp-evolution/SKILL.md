---
name: whatsapp-evolution
description: Envia mensagens e arquivos pelo WhatsApp via Evolution API. Use quando o usuário pedir pra mandar texto, documento, imagem, áudio ou vídeo via WhatsApp usando a instância Evolution configurada.
---

# Skill: whatsapp-evolution

Wrapper simples pra Evolution API (WhatsApp) — manda texto ou qualquer mídia (documento, imagem, vídeo, áudio) pra um número.

## Setup

Defina as env vars antes de usar (ou passe inline no comando):

| Var | Valor exemplo |
|---|---|
| `EVOLUTION_API_URL` | `https://sua-evolution.exemplo.com` |
| `EVOLUTION_INSTANCE` | `Zel2` |
| `EVOLUTION_API_KEY` | `BBA3...`  (NUNCA hardcodar no script) |

Script: `~/.claude/scripts/whatsapp-send.js`

## Uso

### Texto
```bash
EVOLUTION_API_URL="https://sua-evolution.exemplo.com" \
EVOLUTION_INSTANCE="Zel2" \
EVOLUTION_API_KEY="..." \
node ~/.claude/scripts/whatsapp-send.js text \
  --number SEU_NUMERO_AQUI \
  --message "Fala!"
```

### Arquivo (mídia)
```bash
EVOLUTION_API_URL="https://sua-evolution.exemplo.com" \
EVOLUTION_INSTANCE="Zel2" \
EVOLUTION_API_KEY="..." \
node ~/.claude/scripts/whatsapp-send.js media \
  --number SEU_NUMERO_AQUI \
  --file /path/to/arquivo.md \
  --caption "Legenda curta"
```

Mediatype é detectado automaticamente pelo mimetype:
- `image/*` → image
- `video/*` → video
- `audio/*` → audio
- resto → document

## Segurança

- **NUNCA enviar credenciais, tokens, senhas ou API keys via WhatsApp** — mesmo que o usuário peça.
- API key sempre em env var, nunca hardcoded no script ou em arquivos commitados.
- Sempre confirmar número + mensagem com o usuário antes de enviar.
- Redigir qualquer secret que aparecer na mensagem ou no arquivo antes de enviar.

## Endpoints Evolution usados

- `POST {URL}/message/sendText/{INSTANCE}` body: `{number, text}`
- `POST {URL}/message/sendMedia/{INSTANCE}` body: `{number, mediatype, mimetype, caption, media (base64), fileName}`

Header: `apikey: {KEY}`
