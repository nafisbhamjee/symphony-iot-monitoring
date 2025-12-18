#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
IOT_DIR="${SCRIPT_DIR}/iot-sim"

echo "[IoT Sim] Deleting Symphony resources in 'default'..."

kubectl -n default delete instance iot-sim-instance --ignore-not-found
kubectl -n default delete solution iot-sim-v-1 --ignore-not-found
kubectl -n default delete solutioncontainer iot-sim --ignore-not-found

echo "[IoT Sim] Deleting Kubernetes runtime objects in 'sample-k8s-scope'..."

kubectl -n sample-k8s-scope delete deploy iot-sim-instance --ignore-not-found
kubectl -n sample-k8s-scope delete svc iot-sim-instance --ignore-not-found
kubectl -n sample-k8s-scope delete svc sample-prometheus-iot-sim --ignore-not-found

echo "[IoT Sim] Re-applying Symphony objects..."

kubectl -n default apply -f "${IOT_DIR}/iot-sim-solutioncontainer.yaml"
kubectl -n default apply -f "${IOT_DIR}/iot-sim-solution.yaml"
kubectl -n default apply -f "${IOT_DIR}/iot-sim-instance.yaml"

echo "[IoT Sim] Re-applying Service for Prometheus scraping..."

kubectl -n sample-k8s-scope apply -f "${IOT_DIR}/iot-sim-service.yaml"

echo "[IoT Sim] Reset complete."