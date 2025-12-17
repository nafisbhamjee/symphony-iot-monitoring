# scripts/windows/reset-iot.ps1
# Resets IoT Simulators using Symphony CRDs

$ErrorActionPreference = "Stop"

# --- Namespaces (VERIFIED FROM YOUR CLUSTER) ---
$ControlNS = "default"          # Symphony CRDs
$RuntimeNS = "sample-k8s-scope" # Runtime pods/services

function Info($msg) { Write-Host "[INFO] $msg" }
function Warn($msg) { Write-Host "[WARN] $msg" -ForegroundColor Yellow }

# --- Resolve repo root safely ---
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path      # scripts/windows
$RepoRoot  = Resolve-Path (Join-Path $ScriptDir "..\..")          # repo root
$IotDir    = Join-Path $RepoRoot "iot-sim"

# --- YAML files (ACTUAL filenames used in repo) ---
$SC       = Join-Path $IotDir "iot-sim-solutioncontainer.yaml"
$Solution = Join-Path $IotDir "iot-sim-solution.yaml"
$Instance = Join-Path $IotDir "iot-sim-instance.yaml"
$Service  = Join-Path $IotDir "iot-sim-service.yaml"

Info "RepoRoot: $RepoRoot"
Info "Resetting IoT Simulators"
Info "Control Namespace : $ControlNS"
Info "Runtime Namespace : $RuntimeNS"

# --- Delete runtime resources ---
Info "Deleting IoT runtime services/deployments (ignore if missing)..."
kubectl delete svc iot-sim-instance -n $RuntimeNS --ignore-not-found | Out-Null
kubectl delete deploy iot-sim-instance -n $RuntimeNS --ignore-not-found | Out-Null

# --- Delete Symphony resources ---
Info "Deleting Symphony CRDs (ignore if missing)..."
kubectl delete instance iot-sim-instance -n $ControlNS --ignore-not-found
kubectl delete solution iot-sim-v-1 -n $ControlNS --ignore-not-found
kubectl delete solutioncontainer iot-sim -n $ControlNS --ignore-not-found

# --- Reapply Symphony objects (ORDER MATTERS) ---
Info "Applying solutioncontainer..."
kubectl apply -f $SC -n $ControlNS

Info "Applying solution..."
kubectl apply -f $Solution -n $ControlNS

Info "Applying instance..."
kubectl apply -f $Instance -n $ControlNS

# --- Apply service ---
Info "Applying IoT service..."
kubectl apply -f $Service -n $RuntimeNS

# --- Wait for deployment ---
Info "Waiting for IoT deployment to become available..."
kubectl wait --for=condition=available deploy/iot-sim-instance `
  -n $RuntimeNS `
  --timeout=180s

# --- Status output ---
Info "IoT simulator pods:"
kubectl get pods -n $RuntimeNS -l app=iot-sim-instance -o wide

Info "IoT simulator service:"
kubectl get svc -n $RuntimeNS | Select-String iot

Info "IoT reset complete."