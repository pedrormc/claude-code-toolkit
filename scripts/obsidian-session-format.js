#!/usr/bin/env node
// obsidian-session-format.js
// Formats session data (from obsidian-session-scan.js) into markdown recap sections.
//
// Modes:
//   --auto <sessionId>   : compact auto-saved section (headless hook use)
//   --full [date]        : full multi-session daily recap (from /obsidian skill)
//   --list [date]        : markdown table listing all sessions of the day (for selection)

const path = require('path');
const { execSync } = require('child_process');
const os = require('os');

const SCANNER = path.join(os.homedir(), '.claude', 'scripts', 'obsidian-session-scan.js');

function runScanner(args) {
  const cmd = ['node', JSON.stringify(SCANNER), ...args].join(' ');
  try {
    const out = execSync(cmd, { encoding: 'utf-8', timeout: 30000 });
    return JSON.parse(out);
  } catch (e) {
    process.stderr.write('scanner failed: ' + e.message + '\n');
    return null;
  }
}

function envTag() {
  return process.env.CLAUDE_ENV_TAG || 'DESKTOP';
}

function hhmm(ts) {
  if (!ts) return '??:??';
  const d = new Date(ts);
  return String(d.getHours()).padStart(2, '0') + ':' + String(d.getMinutes()).padStart(2, '0');
}

function shortPath(p) {
  if (!p) return '?';
  return p
    .replace(/^C:\\Users\\teste\\/, '~/')
    .replace(/^C:\\Users\\teste/, '~')
    .replace(/\\/g, '/');
}

function formatAutoSection(session, date) {
  const time = hhmm(session.lastTs || session.firstTs);
  const lines = [];
  lines.push(`## 🤖 Claude Code — ${time} (auto)`);
  lines.push('');
  lines.push(`**Sessão:** \`${session.sessionId}\``);
  lines.push(`**Diretório:** \`${shortPath(session.cwd)}\``);
  if (session.gitOrigin) lines.push(`**Repo:** ${session.gitOrigin}${session.gitBranch ? ' (`' + session.gitBranch + '`)' : ''}`);
  lines.push(`**Turnos:** ${session.turnCount}`);
  lines.push('');

  if (session.commandNames && session.commandNames.length) {
    lines.push('### Slash commands');
    for (const c of session.commandNames) lines.push(`- \`${c}\``);
    lines.push('');
  }

  if (session.toolsUsed && session.toolsUsed.length) {
    const top = session.toolsUsed.slice(0, 6).map(t => `${t.name}×${t.count}`).join(', ');
    lines.push(`### Ferramentas`);
    lines.push(top);
    lines.push('');
  }

  if (session.userPromptSamples && session.userPromptSamples.length) {
    lines.push('### Pedidos do usuário (amostra)');
    for (const p of session.userPromptSamples.slice(0, 3)) {
      const one = p.replace(/\n+/g, ' ').slice(0, 180);
      lines.push(`- ${one}`);
    }
    lines.push('');
  }

  if (session.filesEdited && session.filesEdited.length) {
    lines.push('### Arquivos tocados');
    for (const f of session.filesEdited.slice(0, 10)) lines.push(`- \`${shortPath(f)}\``);
    if (session.filesEdited.length > 10) lines.push(`- _(+${session.filesEdited.length - 10} outros)_`);
    lines.push('');
  }

  lines.push(`*[Registrado por: ${envTag()} — ${date} ${time} — auto-save]*`);
  return lines.join('\n');
}

function formatListTable(data) {
  const lines = [];
  lines.push(`# Sessões Claude Code — ${data.date}`);
  lines.push('');
  lines.push(`Total: **${data.total}**`);
  lines.push('');
  lines.push('| # | Hora | Sessão | Diretório | Turnos | Git |');
  lines.push('|---|------|--------|-----------|--------|-----|');
  data.sessions.forEach((s, i) => {
    const time = `${hhmm(s.firstTs)}–${hhmm(s.lastTs)}`;
    const dir = shortPath(s.cwd);
    const git = s.gitOrigin ? '✓' : '—';
    lines.push(`| ${i + 1} | ${time} | \`${s.sessionId.slice(0, 8)}\` | ${dir} | ${s.turnCount} | ${git} |`);
  });
  lines.push('');
  return lines.join('\n');
}

function formatFullDaily(data) {
  const lines = [];
  lines.push(`# ${data.date} — Recap do dia`);
  lines.push('');
  lines.push(`_Consolidado automático de **${data.total}** sessões Claude Code do dia._`);
  lines.push('');

  for (const s of data.sessions) {
    const time = `${hhmm(s.firstTs)}–${hhmm(s.lastTs)}`;
    lines.push(`## 🤖 Claude Code — ${time}`);
    lines.push('');
    lines.push(`- **Sessão:** \`${s.sessionId}\``);
    lines.push(`- **Diretório:** \`${shortPath(s.cwd)}\``);
    if (s.gitOrigin) lines.push(`- **Repo:** ${s.gitOrigin}${s.gitBranch ? ' (`' + s.gitBranch + '`)' : ''}`);
    lines.push(`- **Turnos:** ${s.turnCount}`);
    if (s.commandNames && s.commandNames.length) {
      lines.push(`- **Slash:** ${s.commandNames.map(c => '`' + c + '`').join(', ')}`);
    }
    if (s.toolsUsed && s.toolsUsed.length) {
      const top = s.toolsUsed.slice(0, 5).map(t => `${t.name}×${t.count}`).join(', ');
      lines.push(`- **Tools:** ${top}`);
    }
    lines.push('');

    if (s.userPromptSamples && s.userPromptSamples.length) {
      lines.push('**Pedidos principais:**');
      for (const p of s.userPromptSamples.slice(0, 3)) {
        const one = p.replace(/\n+/g, ' ').slice(0, 180);
        lines.push(`- ${one}`);
      }
      lines.push('');
    }

    if (s.filesEdited && s.filesEdited.length) {
      lines.push('**Arquivos tocados:**');
      for (const f of s.filesEdited.slice(0, 8)) lines.push(`- \`${shortPath(f)}\``);
      if (s.filesEdited.length > 8) lines.push(`- _(+${s.filesEdited.length - 8} outros)_`);
      lines.push('');
    }
    lines.push('');
  }

  lines.push(`*[Registrado por: ${envTag()} — ${data.date} — consolidado]*`);
  return lines.join('\n');
}

function main() {
  const args = process.argv.slice(2);
  let mode = null;
  let sessionId = null;
  let date = null;
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--auto' && args[i + 1]) { mode = 'auto'; sessionId = args[i + 1]; i++; }
    else if (args[i] === '--full') mode = 'full';
    else if (args[i] === '--list') mode = 'list';
    else if (/^\d{4}-\d{2}-\d{2}$/.test(args[i])) date = args[i];
  }

  if (!mode) {
    process.stderr.write('usage: obsidian-session-format.js --auto <sessionId> | --full [date] | --list [date]\n');
    process.exit(2);
  }

  if (mode === 'auto') {
    const data = runScanner(['--session', sessionId]);
    if (!data || !data.sessions || !data.sessions.length) process.exit(0);
    const s = data.sessions[0];
    const d = (s.firstTs || '').slice(0, 10) || new Date().toISOString().slice(0, 10);
    process.stdout.write(formatAutoSection(s, d));
  } else {
    const scanArgs = date ? [date] : [];
    const data = runScanner(scanArgs);
    if (!data) process.exit(1);
    if (mode === 'list') process.stdout.write(formatListTable(data));
    else process.stdout.write(formatFullDaily(data));
  }
}

main();
