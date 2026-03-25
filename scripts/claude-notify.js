#!/usr/bin/env node
// Claude Code hook — Terminal title + bell + Windows toast + WezTerm tab state
// Hooks: Notification, Stop, PermissionRequest, TaskCompleted, SubagentStop
//
// States:
//   permission (orange) — awaiting human approval
//   done (green)        — task finished
//   working (blue)      — reset on new prompt (via UserPromptSubmit bash hook)

const fs = require('fs');
const { execFile } = require('child_process');

let input = '';
process.stdin.setEncoding('utf8');
process.stdin.on('data', (chunk) => { input += chunk; });
process.stdin.on('end', () => {
  let data = {};
  try {
    data = JSON.parse(input);
  } catch {}

  // Skip if explicitly disabled
  if (data.stop_hook_active === false) {
    respond();
    return;
  }

  const hookEvent = data.hook_event_name || 'Stop';
  const notificationType = data.notification_type || '';
  const reason = data.reason || 'completed';

  let state = null;
  let message = '';
  let title = '';
  let soundEvent = 'Notification.Default';

  // ── Determine state based on hook event ──

  if (hookEvent === 'PermissionRequest' || notificationType === 'permission_prompt' || notificationType === 'elicitation_dialog') {
    state = 'permission';
    message = 'Aguardando aprovacao';
    title = '[!!] Claude - AGUARDANDO APROVACAO';
    soundEvent = 'Notification.Reminder';

  } else if (hookEvent === 'TaskCompleted') {
    state = 'done';
    const taskName = data.task_name || data.agent_name || 'Task';
    message = taskName + ' concluida';
    title = '[OK] Claude - ' + taskName + ' concluida';
    soundEvent = 'Notification.IM';

  } else if (hookEvent === 'SubagentStop') {
    state = 'done';
    const agentName = data.agent_name || 'Subagent';
    message = agentName + ' finalizou';
    title = '[OK] Claude - ' + agentName + ' finalizou';
    soundEvent = 'Notification.IM';

  } else if (hookEvent === 'Stop') {
    state = 'done';
    message = reason === 'completed'
      ? 'Tarefa concluida'
      : 'Agent parou: ' + reason;
    title = reason === 'completed'
      ? '[OK] Claude - Concluido'
      : '[!] Claude - Parou: ' + reason;
    soundEvent = 'Notification.Default';

  } else if (notificationType === 'idle_prompt') {
    state = 'done';
    message = 'Claude aguardando novo comando';
    title = '[..] Claude - Aguardando';

  } else {
    // auth_success, etc. — no state change
    respond();
    return;
  }

  if (!state) {
    respond();
    return;
  }

  // ── Build terminal sequences ──

  // OSC 1337 SetUserVar for WezTerm tab coloring
  const stateB64 = Buffer.from(state).toString('base64');
  const oscUserVar = '\x1b]1337;SetUserVar=CLAUDE_STATE=' + stateB64 + '\x07';

  // OSC 0 — set terminal title (works in Windows Terminal, WezTerm, etc.)
  const oscTitle = '\x1b]0;' + title + '\x07';

  // BEL character (terminal bell)
  const bell = '\x07';

  // Write all sequences to terminal
  try {
    const fd = fs.openSync('/dev/tty', 'w');
    fs.writeSync(fd, oscUserVar);
    fs.writeSync(fd, oscTitle);
    fs.writeSync(fd, bell);
    // Double bell for permission (more urgent)
    if (state === 'permission') {
      fs.writeSync(fd, bell);
    }
    fs.closeSync(fd);
  } catch {
    try {
      process.stderr.write(oscUserVar);
      process.stderr.write(oscTitle);
      process.stderr.write(bell);
    } catch {}
  }

  // Windows toast notification with sound
  sendToast('Claude Code', message, soundEvent);
});

function respond() {
  try {
    process.stdout.write(JSON.stringify({ continue: true }));
  } catch {}
  process.exit(0);
}

function sendToast(title, message, soundEvent) {
  const safeTitle = title.replace(/'/g, "''").replace(/`/g, '``');
  const safeMsg = message.replace(/'/g, "''").replace(/`/g, '``');
  const safeSoundEvent = soundEvent || 'Notification.Default';

  const ps1 = `
[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
[Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom, ContentType = WindowsRuntime] | Out-Null

$template = @"
<toast>
  <visual>
    <binding template='ToastGeneric'>
      <text>${safeTitle}</text>
      <text>${safeMsg}</text>
    </binding>
  </visual>
  <audio src='ms-winsoundevent:${safeSoundEvent}'/>
</toast>
"@

$xml = New-Object Windows.Data.Xml.Dom.XmlDocument
$xml.LoadXml($template)
$toast = [Windows.UI.Notifications.ToastNotification]::new($xml)
[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier('Claude Code').Show($toast)
`;

  execFile('powershell', ['-NoProfile', '-NonInteractive', '-Command', ps1], { timeout: 8000 }, () => {
    respond();
  });
}

// Safety timeout — always respond
setTimeout(() => {
  respond();
}, 9000);
