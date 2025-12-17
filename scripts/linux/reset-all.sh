#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "[Reset-All] Resetting IoT Sim..."
"${SCRIPT_DIR}/reset-iot.sh"

echo "[Reset-All] Resetting Analysis Engine..."
"${SCRIPT_DIR}/reset-analysis.sh"

echo "[Reset-All] Resetting Prometheus..."
"${SCRIPT_DIR}/reset-prometheus.sh"

echo "[Reset-All] Resetting Grafana..."
"${SCRIPT_DIR}/reset-grafana.sh"

echo "[Reset-All] All components reset."