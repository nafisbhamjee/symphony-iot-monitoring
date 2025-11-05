# Symphony IoT Monitoring and Analysis Stack

## 🚀 Overview
This repository demonstrates an end-to-end IoT monitoring pipeline deployed with **Eclipse Symphony** on Kubernetes.  
It includes:
- **Prometheus** for metrics collection and monitoring  
- **IoT-Sim** for generating random device telemetry  
- **Analysis Engine** for querying Prometheus data and exposing predictions  

The goal is to simulate IoT devices, collect their metrics, and prepare the data for analytics or visualization.

---

## 🧩 Architecture

```text
        ┌─────────────┐
        │  IoT-Sim    │  -->  emits metrics (8085)
        └─────┬───────┘
              │
              ▼
        ┌─────────────┐
        │ Prometheus  │  -->  scrapes IoT + Analysis metrics (9090)
        └─────┬───────┘
              │
              ▼
        ┌─────────────┐
        │ Analysis Eng│  -->  exposes predictions (8086)
        └─────────────┘

Components
Component	Purpose	Port	Folder
Prometheus	Scrapes metrics from IoT-Sim and Analysis Engine	9090	prometheus-deploy/
IoT-Sim	Generates random IoT data (temp, humidity, battery)	8085	iot-sim/
Analysis Engine	Processes data from Prometheus and emits predictions	8086	analysis-engine/
🧱 Folder Structure
symphony-iot-monitoring/
├── prometheus-deploy/
│   ├── target.yaml
│   ├── solution.yaml
│   ├── instance.yaml
│   ├── prometheus-config.yaml
├── iot-sim/
│   ├── Dockerfile
│   ├── app.py
│   ├── solution.yaml
│   ├── instance.yaml
├── analysis-engine/
│   ├── Dockerfile
│   ├── app.py
│   ├── requirements.txt
│   ├── solution.yaml
│   ├── instance.yaml
└── docs/
    ├── architecture-diagram.png
    ├── demo-script.md

🧰 Setup (Minikube / Symphony)
minikube start

# Prometheus
kubectl create -f prometheus-deploy/target.yaml
kubectl create -f prometheus-deploy/solution.yaml
kubectl create -f prometheus-deploy/instance.yaml

# IoT-Sim
kubectl create -f iot-sim/solution.yaml
kubectl create -f iot-sim/instance.yaml

# Analysis Engine
kubectl create -f analysis-engine/solution.yaml
kubectl create -f analysis-engine/instance.yaml


Access Prometheus → http://localhost:9090

Access Analysis Engine metrics → http://localhost:8086/metrics

✅ Current Status
Phase	Description	Result
Prometheus Deployment	Symphony solution + service up	✔️
IoT-Sim Integration	Metrics (iot_temperature_celsius) scraped	✔️
Analysis Engine Integration	Connectivity verified, metrics pending	⚙️
🧩 Next Steps

Finalize iot_predicted_temperature export in analysis-engine

Integrate Grafana for visualization

Automate deployment using Symphony pipelines

👥 Contributors

Nafis Bhamjee
Oluwadamifola Ademoye
Ankita Jayraj Patel
Canchi Sathya 
Devam Dharmendrabhai Shah

Guided by Professor Mohamed El-Darieby

📝 License

MIT License © 2025 Nafis Bhamjee and Contributors