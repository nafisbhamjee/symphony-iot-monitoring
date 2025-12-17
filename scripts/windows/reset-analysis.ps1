# scripts/windows/reset-analysis.ps1
# Resets Analysis Engine using Symphony CRDs

$ErrorActionPreference = "Stop"

# --- Namespaces (VERIFIED) ---
$ControlNS = "default"          # Symphony CRDs
$RuntimeNS = "sample-k8s-scope" # Runtime pods/services

function Info($msg) { Write-Host "[INFO] $msg" }
function Warn($msg) { Write-Host "[WARN] $msg" -ForegroundColor Yellow }

# --- Resolve repo root safely ---
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path      # scripts/windows
$RepoRoot  = Resolve-Path (Join-Path $ScriptDir "..\..")          # repo root
$AnalysisDir = Join-Path $RepoRoot "analysis-engine"

# --- YAML files (ACTUAL filenames) ---
$SC       = Join-Path $AnalysisDir "solutioncontainer.yaml"
$Solution = Join-Path $AnalysisDir "solution.yaml"
$Instance = Join-Path $AnalysisDir "instance.yaml"

Info "RepoRoot: $RepoRoot"
Info "Resetting Analysis Engine"
Info "Control Namespace : $ControlNS"
Info "Runtime Namespace : $RuntimeNS"

# --- Delete runtime resources ---
Info "Deleting Analysis Engine runtime service/deployment (ignore if missing)..."
kubectl delete svc analysis-engine-instance -n $RuntimeNS --ignore-not-found | Out-Null
kubectl delete deploy analysis-engine-instance -n $RuntimeNS --ignore-not-found | Out-Null

# --- Delete Symphony resources ---
Info "Deleting Symphony CRDs (ignore if missing)..."
kubectl delete instance analysis-engine-instance -n $ControlNS --ignore-not-found
kubectl delete solution analysis-engine-v-1 -n $ControlNS --ignore-not-found
kubectl delete solutioncontainer analysis-engine -n $ControlNS --ignore-not-found

# --- Reapply Symphony objects (ORDER MATTERS) ---
Info "Applying solutioncontainer..."
kubectl apply -f $SC -n $ControlNS

Info "Applying solution..."
kubectl apply -f $Solution -n $ControlNS

Info "Applying instance..."
kubectl apply -f $Instance -n $ControlNS

# --- Wait for deployment ---
Info "Waiting for Analysis Engine deployment to become available..."
kubectl wait --for=condition=available deploy/analysis-engine-instance `
  -n $RuntimeNS `
  --timeout=180s

# --- Status output ---
Info "Analysis Engine pods:"
kubectl get pods -n $RuntimeNS -l app=analysis-engine-instance -o wide

Info "Analysis Engine service:"
kubectl get svc -n $RuntimeNS | Select-String analysis-engine

Info "Analysis Engine reset complete."