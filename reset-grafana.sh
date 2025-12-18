#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
GRAFANA_DIR="${SCRIPT_DIR}/grafana"

echo "[Grafana] Deleting Symphony resources in 'default'..."

kubectl -n default delete instance grafana-instance --ignore-not-found
kubectl -n default delete solution grafana-v-1 --ignore-not-found
kubectl -n default delete solutioncontainer grafana --ignore-not-found

echo "[Grafana] Deleting Kubernetes runtime objects in 'sample-k8s-scope'..."

kubectl -n sample-k8s-scope delete deploy grafana-instance --ignore-not-found
kubectl -n sample-k8s-scope delete svc grafana-instance --ignore-not-found

echo "[Grafana] Re-applying Symphony objects..."

kubectl -n default apply -f "${GRAFANA_DIR}/solutioncontainer.yaml"
kubectl -n default apply -f "${GRAFANA_DIR}/solution.yaml"
kubectl -n default apply -f "${GRAFANA_DIR}/instance.yaml"

echo "[Grafana] Reset complete."