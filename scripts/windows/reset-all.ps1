# scripts/windows/reset-all.ps1
# Full system reset (IoT → Prometheus → Analysis → Grafana)

$ErrorActionPreference = "Stop"

function Info($msg) { Write-Host "[INFO] $msg" }

# --- Resolve repo root safely ---
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path      # scripts/windows
$RepoRoot  = Resolve-Path (Join-Path $ScriptDir "..\..")

$ScriptsDir = Join-Path $RepoRoot "scripts\windows"

Info "RepoRoot: $RepoRoot"
Info "Running full system reset in correct dependency order"

# --- Order matters ---
& (Join-Path $ScriptsDir "reset-iot.ps1")
& (Join-Path $ScriptsDir "reset-prometheus.ps1")
& (Join-Path $ScriptsDir "reset-analysis.ps1")
& (Join-Path $ScriptsDir "reset-grafana.ps1")

Info "Full system reset completed successfully."