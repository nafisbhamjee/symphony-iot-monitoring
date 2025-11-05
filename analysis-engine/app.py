from flask import Flask, Response
from prometheus_client import Gauge, generate_latest, REGISTRY
import random

app = Flask(__name__)

# Create a global metric ONCE
iot_pred_temp = Gauge("iot_predicted_temperature", "Predicted temperature in Celsius")

@app.route("/metrics")
def metrics():
    # Update value dynamically each scrape
    iot_pred_temp.set(30 + random.random() * 5)
    return Response(generate_latest(REGISTRY), mimetype="text/plain")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8086)
