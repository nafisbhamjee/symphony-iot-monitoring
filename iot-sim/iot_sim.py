from flask import Flask, Response
from prometheus_client import Gauge, CollectorRegistry, generate_latest
import random, time

app = Flask(__name__)
registry = CollectorRegistry()

# Define metrics
temp_gauge = Gauge('iot_temperature_celsius', 'Temperature in Celsius', registry=registry)
humid_gauge = Gauge('iot_humidity_percent', 'Humidity in percent', registry=registry)
battery_gauge = Gauge('iot_battery_percent', 'Battery level in percent', registry=registry)

@app.route('/metrics')
def metrics():
    # Randomly generate data
    temp_gauge.set(round(20 + random.random() * 15, 2))
    humid_gauge.set(round(40 + random.random() * 30, 2))
    battery_gauge.set(round(50 + random.random() * 50, 2))
    return Response(generate_latest(registry), mimetype='text/plain')

@app.route('/')
def home():
    return "IoT Simulator Running"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8085)

