#!/bin/bash

echo "🔄 Resetting Alert Engine..."

# Delete existing resources
echo "Deleting instance..."
kubectl delete -f alert-engine/instance.yaml --ignore-not-found=true

echo "Deleting solution..."
kubectl delete -f alert-engine/solution.yaml --ignore-not-found=true

echo "Waiting for cleanup..."
sleep 5

# Reapply resources
echo "Applying solution..."
kubectl apply -f alert-engine/solution.yaml

echo "Applying instance..."
kubectl apply -f alert-engine/instance.yaml

echo "✅ Alert Engine reset complete!"
echo ""
echo "Check status with:"
echo "  kubectl get pods -n sample-k8s-scope | grep alert-engine"
echo ""
echo "View logs with:"
echo "  kubectl logs -f \$(kubectl get pods -n sample-k8s-scope -l app=alert-engine -o name) -n sample-k8s-scope"
