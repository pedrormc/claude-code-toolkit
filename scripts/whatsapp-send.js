#!/usr/bin/env node
// whatsapp-send.js — Evolution API wrapper pra enviar texto e mídias no WhatsApp.
//
// Uso:
//   node whatsapp-send.js text  --number 5561... --message "texto"
//   node whatsapp-send.js media --number 5561... --file /path/to/file [--caption "legenda"]
//
// Env vars obrigatórias:
//   EVOLUTION_API_URL   Base URL (ex: https://sua-evolution.exemplo.com)
//   EVOLUTION_INSTANCE  Instance name (ex: Zel2)
//   EVOLUTION_API_KEY   Header apikey

const fs = require('fs');
const path = require('path');

function parseArgs(argv) {
  const mode = argv[2];
  const args = {};
  for (let i = 3; i < argv.length; i++) {
    if (argv[i].startsWith('--')) {
      args[argv[i].slice(2)] = argv[i + 1];
      i++;
    }
  }
  return { mode, args };
}

function mimeFromExt(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  const map = {
    '.md': 'text/markdown',
    '.txt': 'text/plain',
    '.pdf': 'application/pdf',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.png': 'image/png',
    '.gif': 'image/gif',
    '.mp4': 'video/mp4',
    '.mp3': 'audio/mpeg',
    '.ogg': 'audio/ogg',
    '.json': 'application/json',
    '.csv': 'text/csv',
    '.doc': 'application/msword',
    '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    '.xls': 'application/vnd.ms-excel',
    '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    '.zip': 'application/zip',
  };
  return map[ext] || 'application/octet-stream';
}

function mediatypeFromMime(mime) {
  if (mime.startsWith('image/')) return 'image';
  if (mime.startsWith('video/')) return 'video';
  if (mime.startsWith('audio/')) return 'audio';
  return 'document';
}

async function sendText(url, instance, apikey, number, text) {
  const endpoint = `${url}/message/sendText/${instance}`;
  const res = await fetch(endpoint, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'apikey': apikey },
    body: JSON.stringify({ number, text }),
  });
  const body = await res.json().catch(() => ({}));
  return { status: res.status, body };
}

async function sendMedia(url, instance, apikey, number, filePath, caption) {
  const endpoint = `${url}/message/sendMedia/${instance}`;
  const buffer = fs.readFileSync(filePath);
  const base64 = buffer.toString('base64');
  const fileName = path.basename(filePath);
  const mimetype = mimeFromExt(filePath);
  const mediatype = mediatypeFromMime(mimetype);

  const res = await fetch(endpoint, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'apikey': apikey },
    body: JSON.stringify({
      number,
      mediatype,
      mimetype,
      caption: caption || '',
      media: base64,
      fileName,
    }),
  });
  const body = await res.json().catch(() => ({}));
  return { status: res.status, body, sizeBytes: buffer.length };
}

async function main() {
  const { mode, args } = parseArgs(process.argv);
  const url = process.env.EVOLUTION_API_URL;
  const instance = process.env.EVOLUTION_INSTANCE;
  const apikey = process.env.EVOLUTION_API_KEY;

  if (!url || !instance || !apikey) {
    console.error('Missing env vars: EVOLUTION_API_URL, EVOLUTION_INSTANCE, EVOLUTION_API_KEY');
    process.exit(1);
  }

  if (mode === 'text') {
    if (!args.number || !args.message) {
      console.error('Uso: text --number <num> --message <msg>');
      process.exit(1);
    }
    const out = await sendText(url, instance, apikey, args.number, args.message);
    console.log(JSON.stringify(out, null, 2));
    process.exit(out.status < 400 ? 0 : 1);
  }

  if (mode === 'media') {
    if (!args.number || !args.file) {
      console.error('Uso: media --number <num> --file <path> [--caption <txt>]');
      process.exit(1);
    }
    if (!fs.existsSync(args.file)) {
      console.error(`Arquivo não encontrado: ${args.file}`);
      process.exit(1);
    }
    const out = await sendMedia(url, instance, apikey, args.number, args.file, args.caption);
    console.log(JSON.stringify(out, null, 2));
    process.exit(out.status < 400 ? 0 : 1);
  }

  console.error('Modo inválido. Use: text | media');
  process.exit(1);
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
