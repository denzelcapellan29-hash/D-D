param(
  [string]$FoundryUserData = "",
  [string]$BridgeFolder = ""
)

$ErrorActionPreference = "Stop"

if (-not $FoundryUserData) {
  $candidates = @(
    (Join-Path $env:LOCALAPPDATA "FoundryVTT"),
    (Join-Path $env:APPDATA "FoundryVTT")
  )
  foreach ($candidate in $candidates) {
    if (Test-Path (Join-Path $candidate "Data")) {
      $FoundryUserData = $candidate
      break
    }
  }
}
if (-not $FoundryUserData) {
  $FoundryUserData = Read-Host "Foundry User Data folder (the folder containing Data)"
}

if (-not $BridgeFolder) {
  $knownBridge = "G:\My Drive\D&D\Foundry Bridge"
  if (Test-Path $knownBridge) { $BridgeFolder = $knownBridge }
}
if (-not $BridgeFolder) {
  $BridgeFolder = Read-Host "Local Google Drive-synced D&D\Foundry Bridge folder"
}

$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
$ModuleSource = Join-Path $Here "module\acq-foundry-bridge"
$ModuleTarget = Join-Path $FoundryUserData "Data\modules\acq-foundry-bridge"

if (-not (Test-Path $ModuleSource)) {
  throw "Module source not found: $ModuleSource"
}

New-Item -ItemType Directory -Force -Path $ModuleTarget | Out-Null
Copy-Item -Path (Join-Path $ModuleSource "*") -Destination $ModuleTarget -Recurse -Force

$AgentPath = Join-Path $Here "agent\acq_bridge_agent.py"
$McpPath = Join-Path $Here "agent\mcp_server.py"
$ReqPath = Join-Path $Here "agent\requirements-mcp.txt"
$Venv = Join-Path $Here "agent\.venv"

$escapedBridge = $BridgeFolder.Replace("'", "''")
$escapedAgent = $AgentPath.Replace("'", "''")
$escapedMcp = $McpPath.Replace("'", "''")
$escapedReq = $ReqPath.Replace("'", "''")
$escapedVenv = $Venv.Replace("'", "''")

$AgentLauncher = Join-Path $Here "run_bridge_agent.ps1"
@"
python '$escapedAgent' --transport '$escapedBridge'
"@ | Set-Content -Path $AgentLauncher -Encoding UTF8

$StackLauncher = Join-Path $Here "run_acq_3d_stack.ps1"
@"
`$ErrorActionPreference = "Stop"
if (-not (Test-Path '$escapedVenv')) {
  python -m venv '$escapedVenv'
}
`$Py = Join-Path '$escapedVenv' 'Scripts\python.exe'
& `$Py -m pip install --disable-pip-version-check -r '$escapedReq'

`$LogDir = Join-Path $PSScriptRoot "logs"
New-Item -ItemType Directory -Force -Path `$LogDir | Out-Null
`$AgentOut = Join-Path `$LogDir "bridge-agent.out.log"
`$AgentErr = Join-Path `$LogDir "bridge-agent.err.log"
Remove-Item `$AgentOut, `$AgentErr -ErrorAction SilentlyContinue

`$AgentProc = Start-Process -FilePath `$Py -ArgumentList @('$escapedAgent','--transport','$escapedBridge') -PassThru -RedirectStandardOutput `$AgentOut -RedirectStandardError `$AgentErr

`$healthy = `$false
for (`$i = 0; `$i -lt 20; `$i++) {
  Start-Sleep -Milliseconds 500
  if (`$AgentProc.HasExited) { break }
  try {
    `$h = Invoke-RestMethod -Uri "http://127.0.0.1:18747/health" -TimeoutSec 2
    if (`$h.ok) { `$healthy = `$true; break }
  } catch {}
}

if (-not `$healthy) {
  Write-Host ""
  Write-Host "Acq Bridge Agent failed to become healthy." -ForegroundColor Red
  if (Test-Path `$AgentErr) { Get-Content `$AgentErr -Tail 80 }
  if (Test-Path `$AgentOut) { Get-Content `$AgentOut -Tail 80 }
  throw "Bridge agent startup failed. See logs in `$LogDir"
}

Write-Host "Acq Bridge Agent healthy on http://127.0.0.1:18747" -ForegroundColor Green
Write-Host "Starting Acq 3D MCP on http://127.0.0.1:18748/mcp" -ForegroundColor Green
& `$Py '$escapedMcp'
"@ | Set-Content -Path $StackLauncher -Encoding UTF8

$StackCmd = Join-Path $Here "run_acq_3d_stack.cmd"
@'
@echo off
setlocal
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0run_acq_3d_stack.ps1"
exit /b %ERRORLEVEL%
'@ | Set-Content -Path $StackCmd -Encoding ASCII

Write-Host "Installed Acq Foundry Bridge + Acq 3D MCP files."
Write-Host "Restart Foundry, enable the module, then run:"
Write-Host "  $StackLauncher"
