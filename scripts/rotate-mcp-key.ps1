# rotate-mcp-key.ps1 — Update Windows User env var with new MCP key after manual rotation
#
# USAGE:
#   .\rotate-mcp-key.ps1 -Service testsprite -NewKey "sk-user-NEW..."
#   .\rotate-mcp-key.ps1 -Service n8n -NewKey "eyJhbGc..."
#
# AFTER RUNNING:
#   - Close and reopen Claude Code / terminal so new env loads
#   - Verify with: echo $env:TESTSPRITE_API_KEY  (or N8N_API_KEY)

param(
  [Parameter(Mandatory=$true)]
  [ValidateSet("testsprite", "n8n")]
  [string]$Service,

  [Parameter(Mandatory=$true)]
  [string]$NewKey
)

$ErrorActionPreference = "Stop"

# Map service to env var name
$varName = switch ($Service) {
  "testsprite" { "TESTSPRITE_API_KEY" }
  "n8n"        { "N8N_API_KEY" }
}

# Backup old value to a one-time file (so user can revoke at provider after confirming new one works)
$backupFile = "$env:USERPROFILE\.claude\.key-rotation-backup.txt"
$oldValue = [System.Environment]::GetEnvironmentVariable($varName, "User")
$timestamp = Get-Date -Format "yyyy-MM-ddTHH:mm:ss"

if ($oldValue) {
  $oldHash = (Get-FileHash -Algorithm SHA256 -InputStream ([IO.MemoryStream]::new([Text.Encoding]::UTF8.GetBytes($oldValue)))).Hash.Substring(0,12)
  Add-Content -Path $backupFile -Value "[$timestamp] $varName old key sha256:${oldHash}... (length $($oldValue.Length))"
  Write-Host "Old key fingerprint logged to $backupFile (revoke at provider after confirming new key works)" -ForegroundColor Yellow
}

# Set new value
[System.Environment]::SetEnvironmentVariable($varName, $NewKey, "User")

$newLen = [System.Environment]::GetEnvironmentVariable($varName, "User").Length
Write-Host "$varName updated. New value length: $newLen" -ForegroundColor Green
Write-Host "Restart Claude Code / terminal to load the new value." -ForegroundColor Cyan
