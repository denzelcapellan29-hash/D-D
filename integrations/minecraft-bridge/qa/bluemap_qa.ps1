param(
  [Parameter(Mandatory=$true)][string]$WorldPath,
  [string]$WorkDir = "$PSScriptRoot\bluemap",
  [string]$ResourcePack = "",
  [switch]$AcceptMojangDownloads,
  [switch]$Serve
)
$ErrorActionPreference = "Stop"
$Version = "5.28"
$Jar = Join-Path $WorkDir "bluemap-$Version-cli.jar"
$Config = Join-Path $WorkDir "config"
$MapDir = Join-Path $Config "maps"
$PackDir = Join-Path $Config "packs"
New-Item -Force -ItemType Directory $WorkDir,$Config,$MapDir,$PackDir | Out-Null

$javaVersionText = (& java -version 2>&1 | Select-Object -First 1)
if ($javaVersionText -notmatch 'version "(\d+)') { throw "Could not determine Java version: $javaVersionText" }
$javaMajor = [int]$Matches[1]
if ($javaMajor -lt 25) { throw "BlueMap 5.28 targets Java 25. Found Java $javaMajor." }

if (!(Test-Path $Jar)) {
  $url = "https://github.com/BlueMap-Minecraft/BlueMap/releases/download/v$Version/bluemap-$Version-cli.jar"
  Write-Host "Downloading BlueMap $Version CLI..."
  Invoke-WebRequest -Uri $url -OutFile $Jar
}

$core = Join-Path $Config "core.conf"
if (!(Test-Path $core)) {
  Push-Location $WorkDir
  try { & java -jar $Jar -c $Config | Out-Host } finally { Pop-Location }
}

if ($AcceptMojangDownloads) {
  $txt = Get-Content $core -Raw
  $txt = $txt -replace '(?m)^\s*accept-download\s*:\s*false\s*$', 'accept-download: true'
  Set-Content -Path $core -Value $txt -Encoding UTF8
} else {
  $txt = Get-Content $core -Raw
  if ($txt -notmatch '(?m)^\s*accept-download\s*:\s*true\s*$') {
    throw "BlueMap needs Mojang client resources. Re-run with -AcceptMojangDownloads only after explicit user agreement."
  }
}

$world = (Resolve-Path $WorldPath).Path.Replace('\','/')
$mapConf = @"
world: "$world"
dimension: "minecraft:overworld"
name: "Acq Inc - Lower Dock Ward QA"
storage: "file"
ignore-missing-light-data: true
enable-hires: true
"@
Set-Content -Path (Join-Path $MapDir "acq_lower_dock.conf") -Value $mapConf -Encoding UTF8

if ($ResourcePack) {
  $rp=(Resolve-Path $ResourcePack).Path
  Copy-Item $rp (Join-Path $PackDir (Split-Path $rp -Leaf)) -Force
}

Push-Location $WorkDir
try {
  & java -jar $Jar -c $Config -r -m acq_lower_dock
  if ($LASTEXITCODE -ne 0) { throw "BlueMap render failed with exit code $LASTEXITCODE" }
  if ($Serve) {
    Write-Host "Starting BlueMap web server. Open http://127.0.0.1:8100/"
    & java -jar $Jar -c $Config -w
  }
} finally { Pop-Location }
