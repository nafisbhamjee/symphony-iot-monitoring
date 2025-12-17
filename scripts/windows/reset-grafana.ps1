# scripts/windows/reset-grafana.ps1
# Resets Grafana using Symphony CRDs

$ErrorActionPreference = "Stop"

# --- Namespaces (VERIFIED FROM YOUR CLUSTER) ---
$ControlNS = "default"          # Symphony CRDs
$RuntimeNS = "sample-k8s-scope" # Runtime pods/services

function Info($msg) { Write-Host "[INFO] $msg" }
function Warn($msg) { Write-Host "[WARN] $msg" -ForegroundColor Yellow }

# --- Resolve repo root safely ---
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path      # scripts/windows
$RepoRoot  = Resolve-Path (Join-Path $ScriptDir "..\..")          # repo root
$GrafanaDir = Join-Path $RepoRoot "grafana"

# --- YAML files (ACTUAL filenames pattern used in repo) ---
$SC       = Join-Path $GrafanaDir "grafana-solutioncontainer.yaml"
$Solution = Join-Path $GrafanaDir "grafana-solution.yaml"
$Instance = Join-Path $GrafanaDir "grafana-instance.yaml"

Info "RepoRoot: $RepoRoot"
Info "Resetting Grafana"
Info "Control Namespace : $ControlNS"
Info "Runtime Namespace : $RuntimeNS"

# --- Delete runtime resources ---
Info "Deleting Grafana runtime service/deployment (ignore if missing)..."
kubectl delete svc grafana-instance -n $RuntimeNS --ignore-not-found | Out-Null
kubectl delete deploy grafana-instance -n $RuntimeNS --ignore-not-found | Out-Null

# --- Delete Symphony resources ---
Info "Deleting Symphony CRDs (ignore if missing)..."
kubectl delete instance grafana-instance -n $ControlNS --ignore-not-found
kubectl delete solution grafana-v-1 -n $ControlNS --ignore-not-found
kubectl delete solutioncontainer grafana -n $ControlNS --ignore-not-found

# --- Reapply Symphony objects (ORDER MATTERS) ---
Info "Applying solutioncontainer..."
kubectl apply -f $SC -n $ControlNS

Info "Applying solution..."
kubectl apply -f $Solution -n $ControlNS

Info "Applying instance..."
kubectl apply -f $Instance -n $ControlNS

# --- Wait for deployment ---
Info "Waiting for Grafana deployment to become available..."
kubectl wait --for=condition=available deploy/grafana-instance `
  -n $RuntimeNS `
  --timeout=180s

# --- Status output ---
Info "Grafana pods:"
kubectl get pods -n $RuntimeNS -l app=grafana-instance -o wide

Info "Grafana service:"
kubectl get svc -n $RuntimeNS | Select-String grafana

Info "Grafana reset complete."