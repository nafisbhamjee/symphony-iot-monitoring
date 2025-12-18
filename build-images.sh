#!/bin/bash

set -e

echo "Building Docker image: iot-sim"
docker build -t iot-sim:latest ./iot-sim

echo "Building Docker image: analysis-engine"
docker build -t analysis-engine:latest ./analysis-engine

echo "Building Docker image: alert-engine"
docker build -t alert-engine:latest ./alert-engine

echo "Images built successfully"
