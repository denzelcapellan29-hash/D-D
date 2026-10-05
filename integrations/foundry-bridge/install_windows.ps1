param(
  [string]$FoundryUserData = "",
  [string]$BridgeFolder = ""
)

$ErrorActionPreference = "Stop"

if (-not $FoundryUserData) {
  $FoundryUserData = Read-Host "Foundry User Data folder (the folder containing Data)"
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
Start-Process -FilePath `$Py -ArgumentList @('$escapedAgent','--transport','$escapedBridge') -WindowStyle Minimized
Start-Sleep -Seconds 1
& `$Py '$escapedMcp'
"@ | Set-Content -Path $StackLauncher -Encoding UTF8

Write-Host "Installed Acq Foundry Bridge + Acq 3D MCP files."
Write-Host "Restart Foundry, enable the module, then run:"
Write-Host "  $StackLauncher"
