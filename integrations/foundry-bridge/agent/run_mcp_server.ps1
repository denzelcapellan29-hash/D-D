param(
    [string]$Python = "python",
    [int]$Port = 18748
)

$ErrorActionPreference = "Stop"
$env:ACQ_3D_MCP_HOST = "127.0.0.1"
$env:ACQ_3D_MCP_PORT = "$Port"

& $Python "$PSScriptRoot\mcp_server.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
