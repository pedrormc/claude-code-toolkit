#!/usr/bin/env node
// Claude Code Stop hook — Windows toast notification (silent)
// Uses PowerShell 5.1 WinRT [Windows.UI.Notifications] — no external deps

const { execFile } = require('child_process');

let input = '';
process.stdin.setEncoding('utf8');
process.stdin.on('data', (chunk) => { input += chunk; });
process.stdin.on('end', () => {
  let stopReason = 'completed';
  try {
    const data = JSON.parse(input);
    if (data.stop_hook_active === false) {
      // Hook not active, skip notification
      process.stdout.write(JSON.stringify({ continue: true }));
      process.exit(0);
    }
    stopReason = data.reason || 'completed';
  } catch {
    // If stdin isn't valid JSON, still show notification
  }

  const title = 'Claude Code';
  const message = `Agent ${stopReason === 'completed' ? 'concluiu a tarefa' : stopReason}`;

  const ps1 = `
[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
[Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom, ContentType = WindowsRuntime] | Out-Null

$template = @"
<toast>
  <visual>
    <binding template='ToastGeneric'>
      <text>${title}</text>
      <text>${message}</text>
    </binding>
  </visual>
  <audio silent='true'/>
</toast>
"@

$xml = New-Object Windows.Data.Xml.Dom.XmlDocument
$xml.LoadXml($template)
$toast = [Windows.UI.Notifications.ToastNotification]::new($xml)
[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier('Claude Code').Show($toast)
`;

  execFile('powershell', ['-NoProfile', '-NonInteractive', '-Command', ps1], { timeout: 8000 }, (err) => {
    if (err) {
      console.error('Toast notification failed:', err.message);
    }
    // Always return valid hook response
    process.stdout.write(JSON.stringify({ continue: true }));
    process.exit(0);
  });
});

// Handle case where stdin is already closed (no piped input)
setTimeout(() => {
  process.stdout.write(JSON.stringify({ continue: true }));
  process.exit(0);
}, 9000);
