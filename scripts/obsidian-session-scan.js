#!/usr/bin/env node
// obsidian-session-scan.js
// Scans Claude Code session .jsonl files for a given date and emits JSON summary.
//
// Usage:
//   node obsidian-session-scan.js                 -> today
//   node obsidian-session-scan.js 2026-04-16      -> specific date
//   node obsidian-session-scan.js --session <id>  -> single session only
//
// Output: stdout JSON { date, sessions: [ { sessionId, cwd, ... } ] }

const fs = require('fs');
const path = require('path');
const os = require('os');
const { execSync } = require('child_process');

function parseArgs() {
  const args = process.argv.slice(2);
  let date = null;
  let sessionId = null;
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--session' && args[i + 1]) { sessionId = args[i + 1]; i++; }
    else if (/^\d{4}-\d{2}-\d{2}$/.test(args[i])) date = args[i];
  }
  if (!date) {
    const d = new Date();
    const yy = d.getFullYear();
    const mm = String(d.getMonth() + 1).padStart(2, '0');
    const dd = String(d.getDate()).padStart(2, '0');
    date = `${yy}-${mm}-${dd}`;
  }
  return { date, sessionId };
}

const PROJECTS_ROOT = path.join(os.homedir(), '.claude', 'projects');

function listJsonlForDate(date, sessionFilter) {
  const out = [];
  let dirs;
  try { dirs = fs.readdirSync(PROJECTS_ROOT, { withFileTypes: true }); }
  catch { return out; }
  for (const d of dirs) {
    if (!d.isDirectory()) continue;
    const p = path.join(PROJECTS_ROOT, d.name);
    let files;
    try { files = fs.readdirSync(p); } catch { continue; }
    for (const f of files) {
      if (!f.endsWith('.jsonl')) continue;
      const full = path.join(p, f);
      const sid = f.replace(/\.jsonl$/, '');
      if (sessionFilter && sid !== sessionFilter) continue;
      let stat;
      try { stat = fs.statSync(full); } catch { continue; }
      const mtimeDate = stat.mtime.toISOString().slice(0, 10);
      if (sessionFilter || mtimeDate === date) {
        out.push({ path: full, sessionId: sid, mtime: stat.mtime, size: stat.size, projectDir: d.name });
      }
    }
  }
  return out.sort((a, b) => a.mtime - b.mtime);
}

function cleanUserText(raw) {
  if (typeof raw !== 'string') return null;
  // skip obvious tool/hook noise
  if (/^<local-command-caveat>/.test(raw)) return null;
  if (/<local-command-stdout>/.test(raw)) return null;
  if (/hook_success/.test(raw)) return null;
  if (/^\[Request interrupted/.test(raw)) return null;
  return raw.trim();
}

// Redact strings that look like secrets. Conservative: false positives are fine
// (we only redact "sensitive-looking" strings), false negatives are NOT (a leaked
// key on disk is unacceptable). Each entry is [regex, replacer].
const SECRET_RULES = [
  // Private keys (any kind)
  [/-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY-----[\s\S]+?-----END[^-]+-----/g,
    () => '[REDACTED PRIVATE KEY]'],

  // Well-known prefixed keys/tokens
  [/\bsk-[A-Za-z0-9_\-]{20,}\b/g,               () => '[REDACTED]'],   // OpenAI
  [/\bsk_live_[A-Za-z0-9]{20,}\b/gi,            () => '[REDACTED]'],   // Stripe live
  [/\bsk_test_[A-Za-z0-9]{20,}\b/gi,            () => '[REDACTED]'],   // Stripe test
  [/\bxox[baprs]-[A-Za-z0-9-]{10,}\b/g,         () => '[REDACTED]'],   // Slack
  [/\bghp_[A-Za-z0-9]{30,}\b/g,                 () => '[REDACTED]'],   // GitHub PAT
  [/\bgho_[A-Za-z0-9]{30,}\b/g,                 () => '[REDACTED]'],
  [/\bghs_[A-Za-z0-9]{30,}\b/g,                 () => '[REDACTED]'],
  [/\bghu_[A-Za-z0-9]{30,}\b/g,                 () => '[REDACTED]'],
  [/\bAKIA[0-9A-Z]{16}\b/g,                     () => '[REDACTED]'],   // AWS
  [/\bASIA[0-9A-Z]{16}\b/g,                     () => '[REDACTED]'],
  [/\bAIza[0-9A-Za-z_\-]{30,}\b/g,              () => '[REDACTED]'],   // Google
  [/\beyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{5,}\b/g,
    () => '[REDACTED JWT]'],

  // URL basic auth for any scheme: postgres://user:pass@host, redis://:pass@host, etc.
  [/\b([a-z][a-z0-9+\-.]*:\/\/)([^:@\s/]*):([^@\s/]+)@/gi,
    (_m, proto, user) => `${proto}${user}:[REDACTED]@`],

  // "api_key: X", "token=X", "password = X", etc
  [/((?:api[_\- ]?key|api[_\- ]?token|access[_\- ]?token|auth[_\- ]?token|bearer|secret|password|credential|client[_\- ]?secret)\s*[:=]\s*)["']?([^\s"',<>]{6,})["']?/gi,
    (_m, prefix) => `${prefix}[REDACTED]`],

  // ENV_LIKE=value when the variable name contains a sensitive word
  [/\b([A-Z][A-Z0-9_]*(?:PASSWORD|SECRET|TOKEN|APIKEY|API_KEY|PRIVATE|CREDENTIAL|AUTH|PWD)[A-Z0-9_]*)\s*=\s*([^\s"'`]{4,})/g,
    (_m, varName) => `${varName}=[REDACTED]`],

  // High-entropy blobs (run LAST so specific rules match first)
  [/\b[0-9a-f]{40,}\b/gi,                       () => '[REDACTED]'],   // long hex
  [/\b[A-Za-z0-9+/]{50,}={0,2}\b/g,             () => '[REDACTED]'],   // long base64
];

function redactSecrets(text) {
  if (!text) return text;
  let out = String(text);
  for (const [pat, repl] of SECRET_RULES) {
    out = out.replace(pat, repl);
  }
  return out;
}

function extractCommandName(raw) {
  const m = raw && raw.match(/<command-name>([^<]+)<\/command-name>/);
  return m ? m[1] : null;
}

function analyzeSession(filePath) {
  const info = {
    sessionId: path.basename(filePath, '.jsonl'),
    path: filePath,
    cwd: null,
    firstTs: null,
    lastTs: null,
    summary: null,
    turnCount: 0,
    userPromptSamples: [],
    commandNames: [],
    toolsUsed: [],
    filesEdited: [],
    bashCommandsSample: [],
    gitOrigin: null,
    gitBranch: null,
    gitRemoteUrl: null,
  };
  const tools = new Map();
  const cmds = new Set();
  const edits = new Set();
  const bashes = [];
  const prompts = [];

  let raw;
  try { raw = fs.readFileSync(filePath, 'utf-8'); }
  catch { return info; }

  const lines = raw.split('\n');
  for (const ln of lines) {
    if (!ln.trim()) continue;
    let obj;
    try { obj = JSON.parse(ln); } catch { continue; }

    if (obj.cwd && !info.cwd) info.cwd = obj.cwd;
    if (obj.timestamp) {
      if (!info.firstTs) info.firstTs = obj.timestamp;
      info.lastTs = obj.timestamp;
    }
    if (obj.type === 'summary' && obj.summary) info.summary = obj.summary;

    if (obj.type === 'user' && obj.message) {
      const content = obj.message.content;
      if (typeof content === 'string') {
        const cmd = extractCommandName(content);
        if (cmd) { cmds.add(cmd); continue; }
        const clean = cleanUserText(content);
        if (clean) {
          info.turnCount++;
          prompts.push(redactSecrets(clean).slice(0, 500));
        }
      }
    }

    if (obj.type === 'assistant' && obj.message && Array.isArray(obj.message.content)) {
      for (const block of obj.message.content) {
        if (block.type === 'tool_use' && block.name) {
          tools.set(block.name, (tools.get(block.name) || 0) + 1);
          if (block.name === 'Edit' || block.name === 'Write') {
            const fp = block.input && block.input.file_path;
            if (fp) edits.add(fp);
          }
          if (block.name === 'Bash') {
            const cmd = block.input && block.input.command;
            if (cmd && bashes.length < 5) bashes.push(redactSecrets(String(cmd)).slice(0, 140));
          }
        }
      }
    }
  }

  info.commandNames = [...cmds];
  info.toolsUsed = [...tools.entries()].map(([name, count]) => ({ name, count }))
    .sort((a, b) => b.count - a.count);
  info.filesEdited = [...edits];
  info.bashCommandsSample = bashes;
  info.userPromptSamples = prompts.slice(0, 3).concat(prompts.slice(-1)).filter((v, i, a) => a.indexOf(v) === i).slice(0, 4);

  // git info (best-effort, silent fail)
  if (info.cwd) {
    try {
      const origin = execSync('git -C "' + info.cwd.replace(/"/g, '\\"') + '" config --get remote.origin.url',
        { encoding: 'utf-8', stdio: ['ignore', 'pipe', 'ignore'], timeout: 3000 }).trim();
      if (origin) {
        info.gitRemoteUrl = origin;
        // GitHub https or ssh → canonical https link
        let m = origin.match(/github\.com[:/](.+?)(?:\.git)?$/);
        if (m) info.gitOrigin = 'https://github.com/' + m[1];
      }
      const branch = execSync('git -C "' + info.cwd.replace(/"/g, '\\"') + '" rev-parse --abbrev-ref HEAD',
        { encoding: 'utf-8', stdio: ['ignore', 'pipe', 'ignore'], timeout: 3000 }).trim();
      if (branch && branch !== 'HEAD') info.gitBranch = branch;
    } catch { /* not a repo or git absent */ }
  }

  return info;
}

function main() {
  const { date, sessionId } = parseArgs();
  const files = listJsonlForDate(date, sessionId);
  const sessions = files.map(f => {
    const info = analyzeSession(f.path);
    info.mtime = f.mtime.toISOString();
    info.sizeBytes = f.size;
    info.projectDir = f.projectDir;
    return info;
  }).filter(s => s.turnCount > 0 || s.summary);

  process.stdout.write(JSON.stringify({ date, total: sessions.length, sessions }, null, 2));
}

main();
