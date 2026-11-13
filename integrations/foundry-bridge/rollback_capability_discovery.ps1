<#
.SYNOPSIS
  Restore first-party Acq bridge and Python MCP files from a specific upgrade backup.
.DESCRIPTION
  Dry-run by default. Checks backup checksums and that installed files still equal
  the versions recorded by the upgrade. Does not restart either service.
#>
[CmdletBinding()]
param(
  [Parameter(Mandatory=$true)][string]$BackupDirectory,
  [switch]$Apply
)
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$backup = [IO.Path]::GetFullPath($BackupDirectory)
$metaPath = Join-Path $backup "backup-manifest.json"
if (-not (Test-Path -LiteralPath $metaPath -PathType Leaf)) { throw "Backup manifest not found." }
$m = Get-Content -LiteralPath $metaPath -Raw | ConvertFrom-Json
if (-not $m.applied) { throw "Backup manifest was never marked successfully applied." }
$client = [IO.Path]::GetFullPath([string]$m.installed_client)
$mcp = [IO.Path]::GetFullPath([string]$m.installed_mcp)
if ($client -notmatch '(?i)[\\/]Data[\\/]modules[\\/]acq-foundry-bridge[\\/]scripts[\\/]acq-foundry-bridge\.js$' -or
    [IO.Path]::GetFileName($mcp) -ne "mcp_server.py") {
  throw "Backup manifest destination is outside the approved first-party scope."
}
$originalClient = Join-Path $backup "acq-foundry-bridge.js"
$originalMcp = Join-Path $backup "mcp_server.py"
foreach($p in @($originalClient,$originalMcp,$client,$mcp)) {
  if (-not (Test-Path -LiteralPath $p -PathType Leaf)) { throw "Backup or target file missing: $p" }
}
function hash([string]$p) { (Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash.ToLowerInvariant() }
if ((hash $originalClient) -ne $m.original_bridge_sha256 -or
    (hash $originalMcp) -ne $m.original_mcp_sha256) {
  throw "Immutable backup hash mismatch; refusing to restore."
}
if ((hash $client) -ne $m.new_bridge_sha256 -or
    (hash $mcp) -ne $m.new_mcp_sha256) {
  throw "Installed code changed since upgrade; do not overwrite newer changes."
}
Write-Host "Rollback precheck PASSED. Files: $client and $mcp"
if (-not $Apply) {
  Write-Host "DRY RUN. Re-run with -Apply to restore backed-up first-party files."
  return
}
# Safe replacements; originals stay in the backup directory.
$clientTmp = $client + ".rollback-" + [guid]::NewGuid().ToString("N")
$mcpTmp = $mcp + ".rollback-" + [guid]::NewGuid().ToString("N")
try {
  Copy-Item -LiteralPath $originalClient -Destination $clientTmp
  Copy-Item -LiteralPath $originalMcp -Destination $mcpTmp
  [IO.File]::Replace($clientTmp,$client,$null)
  [IO.File]::Replace($mcpTmp,$mcp,$null)
} finally {
  Remove-Item -LiteralPath $clientTmp,$mcpTmp -ErrorAction SilentlyContinue -Force
}
if ((hash $client) -ne $m.original_bridge_sha256 -or
    (hash $mcp) -ne $m.original_mcp_sha256) {
  throw "Post-restore hash verification failed. Stop and inspect backup manually."
}
Write-Host "ROLLBACK FILES VERIFIED. Restart the MCP stack and refresh Foundry only when idle."
