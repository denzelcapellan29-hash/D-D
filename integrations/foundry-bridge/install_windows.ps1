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
$ModuleSource = Join-Path $Here "foundry-module\acq-foundry-bridge"
$ModuleTarget = Join-Path $FoundryUserData "Data\modules\acq-foundry-bridge"

New-Item -ItemType Directory -Force -Path $ModuleTarget | Out-Null
Copy-Item -Path (Join-Path $ModuleSource "*") -Destination $ModuleTarget -Recurse -Force

$Launcher = Join-Path $Here "run_bridge_agent.ps1"
$AgentPath = Join-Path $Here "agent\acq_bridge_agent.py"
$escapedBridge = $BridgeFolder.Replace("'", "''")
$escapedAgent = $AgentPath.Replace("'", "''")
@"
python '$escapedAgent' --transport '$escapedBridge'
"@ | Set-Content -Path $Launcher -Encoding UTF8

Write-Host "Installed Acq Foundry Bridge."
Write-Host "Restart Foundry, enable the module, then run: $Launcher"
