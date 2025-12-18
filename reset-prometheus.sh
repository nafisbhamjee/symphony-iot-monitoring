#!/usr/bin/env bash
set -euo pipefail

# Resolve this script's directory (repo root)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROM_DIR="${SCRIPT_DIR}/prometheus-deploy"

echo "[Prometheus] Deleting Symphony resources in 'default'..."

kubectl -n default delete instance sample-prometheus-instance --ignore-not-found
kubectl -n default delete solution sample-prometheus-v-1 --ignore-not-found
kubectl -n default delete solutioncontainer sample-prometheus --ignore-not-found

echo "[Prometheus] Deleting Kubernetes runtime objects in 'sample-k8s-scope'..."

kubectl -n sample-k8s-scope delete deploy sample-prometheus-instance --ignore-not-found
kubectl -n sample-k8s-scope delete svc sample-prometheus-instance --ignore-not-found
kubectl -n sample-k8s-scope delete configmap prometheus-config --ignore-not-found

echo "[Prometheus] Re-applying Target (idempotent)..."
kubectl apply -f "${PROM_DIR}/target.yaml"

echo "[Prometheus] Re-applying Symphony objects (SolutionContainer, Solution, Instance)..."

kubectl -n default apply -f "${PROM_DIR}/solutioncontainer.yaml"
kubectl -n default apply -f "${PROM_DIR}/solution.yaml"
kubectl -n default apply -f "${PROM_DIR}/instance.yaml"

echo "[Prometheus] Re-applying Prometheus ConfigMap (for reference / documentation)..."
kubectl -n sample-k8s-scope apply -f "${PROM_DIR}/prometheus-config.yaml"

echo "[Prometheus] Reset complete."