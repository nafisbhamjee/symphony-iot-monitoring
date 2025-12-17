# scripts/windows/reset-prometheus.ps1
# Resets Prometheus (custom image + config) using Symphony CRDs

$ErrorActionPreference = "Stop"

# --- Namespaces (VERIFIED FROM YOUR CLUSTER) ---
$ControlNS = "default"          # Symphony objects
$RuntimeNS = "sample-k8s-scope" # Runtime pods/services

function Info($msg) { Write-Host "[INFO] $msg" }
function Warn($msg) { Write-Host "[WARN] $msg" -ForegroundColor Yellow }

# --- Resolve repo root safely ---
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path      # scripts/windows
$RepoRoot  = Resolve-Path (Join-Path $ScriptDir "..\..")          # repo root
$PromDir   = Join-Path $RepoRoot "prometheus-deploy"

# --- YAML files (ACTUAL filenames) ---
$ConfigMap = Join-Path $PromDir "prometheus-config.yaml"
$SC        = Join-Path $PromDir "solutioncontainer.yaml"
$Solution  = Join-Path $PromDir "solution.yaml"
$Instance  = Join-Path $PromDir "instance.yaml"

Info "RepoRoot: $RepoRoot"
Info "Resetting Prometheus"
Info "Control Namespace : $ControlNS"
Info "Runtime Namespace : $RuntimeNS"

# --- Delete runtime resources (safe) ---
Info "Deleting Prometheus runtime service/deployment (ignore if missing)..."
kubectl delete svc sample-prometheus-instance -n $RuntimeNS --ignore-not-found | Out-Null
kubectl delete deploy sample-prometheus-instance -n $RuntimeNS --ignore-not-found | Out-Null

# --- Delete Symphony resources ---
Info "Deleting Symphony CRDs (ignore if missing)..."
kubectl delete instance sample-prometheus-instance -n $ControlNS --ignore-not-found
kubectl delete solution sample-prometheus-v-1 -n $ControlNS --ignore-not-found
kubectl delete solutioncontainer sample-prometheus -n $ControlNS --ignore-not-found

# --- Reapply Prometheus ConfigMap ---
Info "Applying Prometheus ConfigMap..."
kubectl apply -f $ConfigMap -n $RuntimeNS

# --- Reapply Symphony objects (ORDER MATTERS) ---
Info "Applying solutioncontainer..."
kubectl apply -f $SC -n $ControlNS

Info "Applying solution..."
kubectl apply -f $Solution -n $ControlNS

Info "Applying instance..."
kubectl apply -f $Instance -n $ControlNS

# --- Wait for deployment ---
Info "Waiting for Prometheus deployment to become available..."
kubectl wait --for=condition=available deploy/sample-prometheus-instance `
  -n $RuntimeNS `
  --timeout=180s

# --- Status output ---
Info "Prometheus pods:"
kubectl get pods -n $RuntimeNS -l app=sample-prometheus-instance -o wide

Info "Prometheus service:"
kubectl get svc -n $RuntimeNS | Select-String sample-prometheus

Info "Prometheus endpoints:"
kubectl get endpoints -n $RuntimeNS | Select-String sample-prometheus 2>$null

Info "Prometheus reset complete."