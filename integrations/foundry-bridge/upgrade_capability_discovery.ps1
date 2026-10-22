<#
.SYNOPSIS
  Guarded, additive Acq 3D capability-discovery upgrade (first-party files only).
.DESCRIPTION
  Dry-run by default. Backup and exact installed-bridge SHA gate before -Apply.
  Does not restart the Foundry GM client, alter vendor modules, or change scenes.
  Supports -McpServerPath if process discovery cannot identify the running service.
#>
[CmdletBinding()]
param(
  [switch]$Apply,
  [string]$FoundryUserData = "",
  [string]$McpServerPath = ""
)
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$ExpectedBridgeHash = "842e858751b50d765ac86c90665c29eaa59fd15b7562339fc2c67658615fa951"
$ScriptRoot = $PSScriptRoot
$CandidateClient = Join-Path $ScriptRoot "module\acq-foundry-bridge\scripts\acq-foundry-bridge.js"
$CandidateAnchor = Join-Path $ScriptRoot "module\acq-foundry-bridge\scripts\fps-camera-anchor.mjs"
$CandidateMcp = Join-Path $ScriptRoot "agent\mcp_server.py"
foreach ($p in @($CandidateClient, $CandidateAnchor, $CandidateMcp)) {
  if (-not (Test-Path -LiteralPath $p -PathType Leaf)) { throw "Missing upgrade input: $p" }
}

if (-not $FoundryUserData) {
  foreach ($candidate in @((Join-Path $env:LOCALAPPDATA "FoundryVTT"), (Join-Path $env:APPDATA "FoundryVTT"))) {
    if (Test-Path -LiteralPath (Join-Path $candidate "Data\modules\acq-foundry-bridge\scripts\acq-foundry-bridge.js") -PathType Leaf) {
      $FoundryUserData = $candidate
      break
    }
  }
}
if (-not $FoundryUserData) { throw "Cannot locate Foundry user data. Supply -FoundryUserData explicitly." }
$InstalledModule = Join-Path $FoundryUserData "Data\modules\acq-foundry-bridge"
$InstalledClient = Join-Path $InstalledModule "scripts\acq-foundry-bridge.js"
$InstalledAnchor = Join-Path $InstalledModule "scripts\fps-camera-anchor.mjs"
$InstalledManifest = Join-Path $InstalledModule "module.json"
foreach ($p in @($InstalledClient, $InstalledAnchor, $InstalledManifest)) {
  if (-not (Test-Path -LiteralPath $p -PathType Leaf)) { throw "Missing installed first-party file: $p" }
}
$ActualBridgeHash = (Get-FileHash -LiteralPath $InstalledClient -Algorithm SHA256).Hash.ToLowerInvariant()
if ($ActualBridgeHash -ne $ExpectedBridgeHash) {
  throw "Installed bridge changed since live preflight. Expected $ExpectedBridgeHash; actual $ActualBridgeHash. Stop; do not overwrite."
}
$manifest = Get-Content -LiteralPath $InstalledManifest -Raw | ConvertFrom-Json
if ($manifest.id -ne "acq-foundry-bridge" -or $manifest.version -ne "0.2.8") {
  throw "Installed bridge identity/version differs from verified 0.2.8. Stop."
}
$installedText = Get-Content -LiteralPath $InstalledClient -Raw
$upgradeText = Get-Content -LiteralPath $CandidateClient -Raw
if (-not $installedText.StartsWith('import "./fps-camera-anchor.mjs";')) {
  throw "Protected first-person camera import is missing or moved; stop for reinspection."
}
if (-not $upgradeText.StartsWith('import "./fps-camera-anchor.mjs";') -or
    -not $upgradeText.Contains('function inspect3dCapabilities(') -or
    -not $upgradeText.Contains('type === "inspect_3d_capabilities"')) {
  throw "Proposed client is not the expected additive capability-discovery build."
}
$anchorCurrent = (Get-FileHash -LiteralPath $InstalledAnchor -Algorithm SHA256).Hash.ToLowerInvariant()
$anchorCandidate = (Get-FileHash -LiteralPath $CandidateAnchor -Algorithm SHA256).Hash.ToLowerInvariant()
if ($anchorCurrent -ne $anchorCandidate) {
  throw "Installed first-person stabilization file differs from candidate. Stop; preserve customized code."
}

# Locate the exact running Python MCP file, not any arbitrary .py under a user folder.
if (-not $McpServerPath) {
  $possible = @()
  $regex = '[A-Za-z]:[\\/](?:(?![A-Za-z]:[\\/])[^"''\r\n])*?mcp_server\.py'
  foreach ($proc in @(Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match 'mcp_server\.py' })) {
    $hits = [regex]::Matches([string]$proc.CommandLine, $regex)
    foreach ($hit in $hits) {
      $resolved = [string]$hit.Value
      if (Test-Path -LiteralPath $resolved -PathType Leaf) { $possible += $resolved }
    }
  }
  $possible = @($possible | Sort-Object -Unique)
  if ($possible.Count -ne 1) {
    throw "Cannot uniquely identify running MCP server. Supply -McpServerPath with its absolute mcp_server.py path."
  }
  $McpServerPath = $possible[0]
}
$McpServerPath = [IO.Path]::GetFullPath($McpServerPath)
if ([IO.Path]::GetFileName($McpServerPath) -ne "mcp_server.py" -or
    -not (Test-Path -LiteralPath $McpServerPath -PathType Leaf)) {
  throw "Invalid MCP server path: $McpServerPath"
}
$mcpCurrent = Get-Content -LiteralPath $McpServerPath -Raw
$mcpCandidate = Get-Content -LiteralPath $CandidateMcp -Raw
if (-not $mcpCurrent.Contains('def inspect_3d_scene(') -or
    -not $mcpCurrent.Contains('def _rpc(') -or
    -not $mcpCandidate.Contains('def inspect_3d_capabilities(')) {
  throw "Python MCP source identity cannot be verified."
}
if ($mcpCurrent.Contains('def inspect_3d_capabilities(')) {
  throw "Running MCP file already includes the new tool. Stop and inspect before double-patching."
}
# Patch the existing Python server additively, preserving any installed-only tools.
$pyNl = $mcpCurrent.Replace("`r`n", "`n")
$pyAnchor = "@mcp.tool()`ndef search_3d_assets("
if (-not $pyNl.Contains($pyAnchor)) {
  throw "Installed Python MCP server lacks expected discovery insertion anchor."
}
$pyAddition = @'
@mcp.tool()
def inspect_3d_capabilities(scene_id: str | None = None) -> dict[str, Any]:
    """Read-only 3D Canvas discovery: installed module versions, camera state, available runtime methods, and safe registered settings. Method availability is not proof of tested behavior."""
    return _operation(_rpc([{"op": "inspect_3d_capabilities"}], scene_id=scene_id))


'@
$patchedMcp = $pyNl.Replace($pyAnchor, ($pyAddition + "`n" + $pyAnchor))
if (-not $patchedMcp.Contains('def inspect_3d_capabilities(')) {
  throw "Python MCP additive patch failed."
}

$node = Get-Command "node" -ErrorAction SilentlyContinue
if ($node) {
  & $node.Source --check $CandidateClient
  if ($LASTEXITCODE -ne 0) { throw "Client JavaScript syntax validation failed." }
  & $node.Source --check $CandidateAnchor
  if ($LASTEXITCODE -ne 0) { throw "First-person anchor JavaScript syntax validation failed." }
}
$py = Get-Command "python" -ErrorAction SilentlyContinue
if ($py) {
  & $py.Source -c "import ast,sys;ast.parse(open(sys.argv[1],encoding='utf-8').read())" $CandidateMcp
  if ($LASTEXITCODE -ne 0) { throw "Python MCP syntax validation failed." }
}

Write-Host "PRECHECK PASS: Foundry 0.2.8 bridge identity, protected FPS anchor, and MCP server discovered."
Write-Host "Installed bridge SHA256: $ActualBridgeHash"
Write-Host "Foundry module: $InstalledModule"
Write-Host "Running MCP source: $McpServerPath"
if (-not $Apply) {
  Write-Host "DRY RUN ONLY. Re-run with -Apply to back up and stage both first-party updates."
  return
}

# Immutable timestamped backups outside Foundry's module directory.
$backupRoot = Join-Path $env:LOCALAPPDATA "AcqBridgeBackups"
$stamp = (Get-Date).ToUniversalTime().ToString("yyyyMMddTHHmmssZ")
$backup = Join-Path $backupRoot ("capability-discovery-" + $stamp)
if (Test-Path -LiteralPath $backup) { throw "Backup directory already exists: $backup" }
New-Item -ItemType Directory -Path $backup -Force | Out-Null
$backupClient = Join-Path $backup "acq-foundry-bridge.js"
$backupMcp = Join-Path $backup "mcp_server.py"
Copy-Item -LiteralPath $InstalledClient -Destination $backupClient -ErrorAction Stop
Copy-Item -LiteralPath $McpServerPath -Destination $backupMcp -ErrorAction Stop
Copy-Item -LiteralPath $InstalledAnchor -Destination (Join-Path $backup "fps-camera-anchor.mjs") -ErrorAction Stop
Copy-Item -LiteralPath $InstalledManifest -Destination (Join-Path $backup "module.json") -ErrorAction Stop

$manifestData = [ordered]@{
  created_utc = (Get-Date).ToUniversalTime().ToString("o")
  installed_client = $InstalledClient
  installed_mcp = $McpServerPath
  original_bridge_sha256 = $ActualBridgeHash
  original_mcp_sha256 = (Get-FileHash -LiteralPath $backupMcp -Algorithm SHA256).Hash.ToLowerInvariant()
  first_person_anchor_sha256 = $anchorCurrent
  applied = $false
}
$manifestPath = Join-Path $backup "backup-manifest.json"
$manifestData | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $manifestPath -Encoding UTF8

# Files on disk change; the active GM client and Python service are NOT restarted.
$clientTmp = $InstalledClient + ".acq-validated-" + [guid]::NewGuid().ToString("N")
$mcpTmp = $McpServerPath + ".acq-validated-" + [guid]::NewGuid().ToString("N")
try {
  [IO.File]::WriteAllText($clientTmp, $upgradeText, (New-Object System.Text.UTF8Encoding($false)))
  [IO.File]::WriteAllText($mcpTmp, $patchedMcp, (New-Object System.Text.UTF8Encoding($false)))
  [IO.File]::Replace($clientTmp, $InstalledClient, $null)
  [IO.File]::Replace($mcpTmp, $McpServerPath, $null)
  $clientNew = (Get-FileHash -LiteralPath $InstalledClient -Algorithm SHA256).Hash.ToLowerInvariant()
  $mcpNew = (Get-FileHash -LiteralPath $McpServerPath -Algorithm SHA256).Hash.ToLowerInvariant()
  if ($clientNew -eq $ActualBridgeHash) { throw "3D capability source did not change." }
  if (-not (Get-Content -LiteralPath $McpServerPath -Raw).Contains('def inspect_3d_capabilities(')) { throw 'Post-write MCP tool validation failed.' }
  if (-not (Get-Content -LiteralPath $InstalledClient -Raw).Contains('function inspect3dCapabilities(')) {
    throw "Post-write discovery endpoint validation failed."
  }
  $manifestData.applied = $true
  $manifestData.new_bridge_sha256 = $clientNew
  $manifestData.new_mcp_sha256 = $mcpNew
  $manifestData | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $manifestPath -Encoding UTF8
} catch {
  Write-Warning "Deployment failed; restoring both first-party files from verified backup."
  Copy-Item -LiteralPath $backupClient -Destination $InstalledClient -Force
  Copy-Item -LiteralPath $backupMcp -Destination $McpServerPath -Force
  throw
} finally {
  Remove-Item -LiteralPath $clientTmp,$mcpTmp -Force -ErrorAction SilentlyContinue
}

Write-Host "FILES STAGED: no live services restarted and no scene writes performed."
Write-Host "Rollback backup: $backup"
Write-Host "When gameplay is idle, restart the Acq MCP stack and refresh the Foundry GM client."
Write-Host "Recheck the MCP tool list for inspect_3d_capabilities and compare active Scene revision."
