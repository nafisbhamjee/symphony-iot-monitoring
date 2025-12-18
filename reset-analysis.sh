#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ANALYSIS_DIR="${SCRIPT_DIR}/analysis-engine"

echo "[Analysis] Deleting Symphony resources in 'default'..."

kubectl -n default delete instance analysis-engine-instance --ignore-not-found
kubectl -n default delete solution analysis-engine-v-1 --ignore-not-found
kubectl -n default delete solutioncontainer analysis-engine --ignore-not-found

echo "[Analysis] Deleting Kubernetes runtime objects in 'sample-k8s-scope'..."

kubectl -n sample-k8s-scope delete deploy analysis-engine-instance --ignore-not-found
kubectl -n sample-k8s-scope delete svc analysis-engine-instance --ignore-not-found

echo "[Analysis] Re-applying Symphony objects..."

kubectl -n default apply -f "${ANALYSIS_DIR}/solutioncontainer.yaml"
kubectl -n default apply -f "${ANALYSIS_DIR}/solution.yaml"
kubectl -n default apply -f "${ANALYSIS_DIR}/instance.yaml"

echo "[Analysis] Reset complete."