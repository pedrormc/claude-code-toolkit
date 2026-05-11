# brainstorm-up.ps1 — Solução definitiva para Windows
#
# Inicia o servidor de visual companion do plugin superpowers/brainstorming
# desacoplado do bash do Claude Code. Resolve o problema crônico de o server
# ser killed pelo "owner detection" quando o subshell que iniciou ele morre.
#
# Como funciona:
#   - Mata servers antigos no projeto (lê .server.pid de cada session)
#   - Spawna `node server.js` via Start-Process -WindowStyle Hidden
#   - Define BRAINSTORM_OWNER_PID = explorer.exe → server fica vivo enquanto
#     o usuário estiver logado (não morre quando o bash do Claude termina)
#   - Aguarda .server-info aparecer e imprime o JSON
#
# Uso:
#   pwsh -File brainstorm-up.ps1 <project-dir>
#
# Saída: JSON com { type, port, host, url_host, url, screen_dir }

param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$ProjectDir
)

$ErrorActionPreference = 'Stop'

$ScriptDir = "C:\Users\teste\.claude\plugins\cache\superpowers-marketplace\superpowers\5.0.2\skills\brainstorming\scripts"

if (-not (Test-Path (Join-Path $ScriptDir "server.js"))) {
    Write-Error "server.js nao encontrado em: $ScriptDir"
    exit 1
}

$BrainstormRoot = Join-Path $ProjectDir ".superpowers\brainstorm"
New-Item -ItemType Directory -Force -Path $BrainstormRoot | Out-Null

# Mata servers antigos do mesmo projeto
Get-ChildItem -Path $BrainstormRoot -Directory -ErrorAction SilentlyContinue | ForEach-Object {
    $pidFile = Join-Path $_.FullName ".server.pid"
    if (Test-Path $pidFile) {
        $oldPid = (Get-Content $pidFile -Raw).Trim()
        if ($oldPid -match '^\d+$') {
            $proc = Get-Process -Id ([int]$oldPid) -ErrorAction SilentlyContinue
            if ($proc -and $proc.ProcessName -eq 'node') {
                Stop-Process -Id ([int]$oldPid) -Force -ErrorAction SilentlyContinue
            }
        }
    }
    # Marca a session antiga como parada
    $stoppedFile = Join-Path $_.FullName ".server-stopped"
    if (-not (Test-Path $stoppedFile)) {
        '{"reason":"replaced by new session"}' | Out-File -FilePath $stoppedFile -Encoding ascii -NoNewline
    }
}

# Sessao nova
$timestamp = [int][double]::Parse((Get-Date -UFormat %s))
$sessionId = "$pid-$timestamp"
$ScreenDir = Join-Path $BrainstormRoot $sessionId
New-Item -ItemType Directory -Force -Path $ScreenDir | Out-Null

# Owner = explorer.exe (sessao de usuario, persiste enquanto logado)
$ExplorerProc = Get-Process explorer -ErrorAction SilentlyContinue | Select-Object -First 1
$OwnerPid = if ($ExplorerProc) { $ExplorerProc.Id } else { $pid }

$LogFile = Join-Path $ScreenDir ".server.log"
$ErrFile = Join-Path $ScreenDir ".server.err"
$PidFile = Join-Path $ScreenDir ".server.pid"

# Prepara env vars
$env:BRAINSTORM_DIR = $ScreenDir
$env:BRAINSTORM_HOST = "127.0.0.1"
$env:BRAINSTORM_URL_HOST = "localhost"
$env:BRAINSTORM_OWNER_PID = "$OwnerPid"

# Spawna node detached
$Proc = Start-Process -FilePath "node" `
    -ArgumentList "server.js" `
    -WorkingDirectory $ScriptDir `
    -RedirectStandardOutput $LogFile `
    -RedirectStandardError $ErrFile `
    -PassThru `
    -WindowStyle Hidden

"$($Proc.Id)" | Out-File -FilePath $PidFile -Encoding ascii -NoNewline

# Aguarda .server-info aparecer (timeout 5s)
$InfoFile = Join-Path $ScreenDir ".server-info"
$Found = $false
for ($i = 0; $i -lt 50; $i++) {
    if (Test-Path $InfoFile) {
        $Content = (Get-Content $InfoFile -Raw).Trim()
        if ($Content -match 'server-started') {
            # Verifica que processo ainda esta vivo
            $StillAlive = Get-Process -Id $Proc.Id -ErrorAction SilentlyContinue
            if (-not $StillAlive) {
                Write-Error "Server iniciou mas morreu logo apos. Log: $LogFile"
                if (Test-Path $LogFile) { Get-Content $LogFile | Write-Error }
                exit 2
            }
            Write-Output $Content
            $Found = $true
            break
        }
    }
    Start-Sleep -Milliseconds 100
}

if (-not $Found) {
    Write-Error "Server nao iniciou em 5s. Log: $LogFile"
    if (Test-Path $LogFile) { Get-Content $LogFile | Write-Error }
    if (Test-Path $ErrFile) { Get-Content $ErrFile | Write-Error }
    exit 1
}
