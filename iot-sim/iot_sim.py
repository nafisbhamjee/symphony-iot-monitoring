#!/usr/bin/env python3
"""
Force High Temperature Alert Test
This script modifies the IoT simulator to generate temperature > 35°C
to trigger the critical temperature alert.
"""

from flask import Flask
from prometheus_client import Gauge, generate_latest, REGISTRY
import random
import time
import threading

app = Flask(__name__)

# Create Prometheus metrics
temp_gauge = Gauge('iot_temperature_celsius', 'Current temperature in Celsius')
battery_gauge = Gauge('iot_battery_percent', 'Current battery percentage')
humidity_gauge = Gauge('iot_humidity_percent', 'Current humidity percentage')

# Force high temperature to trigger alert
FORCE_HIGH_TEMP = True
TARGET_TEMP = 36.5  # Above 35°C threshold

def update_metrics():
    """Update metrics every second"""
    while True:
        if FORCE_HIGH_TEMP:
            # Force high temperature (will trigger alert after 2 minutes)
            temp = TARGET_TEMP + random.uniform(-0.5, 0.5)
        else:
            # Normal temperature range
            temp = random.uniform(18, 28)
        
        battery = random.uniform(40, 100)  # Normal battery
        humidity = random.uniform(30, 70)  # Normal humidity
        
        temp_gauge.set(temp)
        battery_gauge.set(battery)
        humidity_gauge.set(humidity)
        
        print(f"🌡️  Temp: {temp:.1f}°C | 🔋 Battery: {battery:.1f}% | 💧 Humidity: {humidity:.1f}%")
        time.sleep(1)

@app.route('/metrics')
def metrics():
    from flask import Response
    return Response(generate_latest(REGISTRY), mimetype='text/plain; version=0.0.4')

@app.route('/')
def home():
    return "IoT Simulator (HIGH TEMP MODE) - Metrics available at /metrics"

if __name__ == '__main__':
    # Start metrics update thread
    metrics_thread = threading.Thread(target=update_metrics, daemon=True)
    metrics_thread.start()
    
    print("=" * 60)
    print("🔥 IoT Simulator - HIGH TEMPERATURE MODE")
    print("=" * 60)
    print(f"Target Temperature: {TARGET_TEMP}°C (Threshold: 35°C)")
    print("Alert should trigger in ~2 minutes")
    print("=" * 60)
    
    # Start Flask server
    app.run(host='0.0.0.0', port=8080)
