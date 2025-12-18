#!/bin/bash
# 🧪 Alert Engine Test Script
# This script monitors the alert engine and waits for email alerts

echo "============================================================"
echo "🧪 ALERT ENGINE TESTING - REAL GMAIL ALERTS"
echo "============================================================"
echo ""
echo "📧 Recipient: sathyacanchi@gmail.com"
echo "🌡️  High Temperature Alert: > 35°C for 2 minutes"
echo ""
echo "============================================================"
echo "📊 Current System Status"
echo "============================================================"
echo ""

# Check if all containers are running
docker-compose ps

echo ""
echo "============================================================"
echo "📈 Current IoT Metrics from Prometheus"
echo "============================================================"
echo ""

# Query Prometheus for current values
echo "🌡️  Temperature:"
curl -s 'http://localhost:9090/api/v1/query?query=iot_temperature_celsius' | jq -r '.data.result[0].value[1]' | awk '{printf "   Current: %.1f°C (Threshold: 35°C)\n", $1}'

echo ""
echo "🔋 Battery:"
curl -s 'http://localhost:9090/api/v1/query?query=iot_battery_percent' | jq -r '.data.result[0].value[1]' | awk '{printf "   Current: %.1f%% (Threshold: 20%%)\n", $1}'

echo ""
echo "💧 Humidity:"
curl -s 'http://localhost:9090/api/v1/query?query=iot_humidity_percent' | jq -r '.data.result[0].value[1]' | awk '{printf "   Current: %.1f%% (Threshold: 80%%)\n", $1}'

echo ""
echo "============================================================"
echo "🚨 Alert Engine Status"
echo "============================================================"
echo ""

# Check alert status
curl -s http://localhost:8087/alerts | jq '.'

echo ""
echo "============================================================"
echo "📝 Alert Rules Configuration"
echo "============================================================"
echo ""

curl -s http://localhost:8087/rules | jq -r '.rules[] | "• \(.name): \(.condition) \(.threshold) for \(.duration)s"'

echo ""
echo "============================================================"
echo "⏰ Waiting for Alert (This takes ~2 minutes)"
echo "============================================================"
echo ""
echo "The temperature is now forced to ~36.5°C"
echo "Alert will trigger after temperature stays > 35°C for 2 minutes"
echo ""
echo "Monitoring alert status every 15 seconds..."
echo "Press Ctrl+C to stop monitoring"
echo ""

# Monitor for alerts
for i in {1..20}; do
    sleep 15
    echo "[$i] Checking at $(date +%H:%M:%S)..."
    
    # Check for active alerts
    ALERT_COUNT=$(curl -s http://localhost:8087/alerts | jq '.alerts | length')
    
    if [ "$ALERT_COUNT" -gt 0 ]; then
        echo ""
        echo "🎉 =========================================="
        echo "🚨 ALERT TRIGGERED!"
        echo "============================================"
        curl -s http://localhost:8087/alerts | jq '.'
        echo ""
        echo "============================================"
        echo "📧 EMAIL SENT TO: sathyacanchi@gmail.com"
        echo "============================================"
        echo ""
        echo "✅ Check your email inbox!"
        echo "   Look for: '🔥 CRITICAL: High Temperature Alert'"
        echo ""
        break
    else
        TEMP=$(curl -s 'http://localhost:9090/api/v1/query?query=iot_temperature_celsius' | jq -r '.data.result[0].value[1]')
        echo "   Temperature: ${TEMP}°C - No alert yet (waiting...)"
    fi
done

echo ""
echo "============================================================"
echo "📊 Final Status"
echo "============================================================"
echo ""
docker logs symphony-alert-engine --tail 20
echo ""
echo "============================================================"
echo "🎯 Test Complete!"
echo "============================================================"
