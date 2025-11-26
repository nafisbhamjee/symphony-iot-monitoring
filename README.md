# Symphony IoT Monitoring and Analysis Stack

## 🚀 Overview
This repository demonstrates an end-to-end IoT monitoring pipeline deployed with **Eclipse Symphony** on Kubernetes.  
It includes:
- **Prometheus** for metrics collection and monitoring  
- **IoT-Sim** for generating random device telemetry  
- **Analysis Engine** for querying Prometheus data and exposing predictions  

The goal is to simulate IoT devices, collect their metrics, and prepare the data for analytics or visualization.

---

## Architecture

            ┌───────────────────┐
            │   IoT Simulators  │
            │  /metrics @ 8085  │
            └─────────┬─────────┘
                      │
                      ▼
            ┌───────────────────┐
            │   Prometheus      │
            │  (Custom Image)   │
            │ Scrapes: IoT, AE  │
            │        9090       │
            └─────────┬─────────┘
                      │
                      ▼
            ┌───────────────────┐
            │  Analysis Engine  │
            │ Queries PromQL    │
            │ Exposes /metrics  │
            │     @ 8086        │
            └─────────┬─────────┘
                      │
                      ▼
            ┌───────────────────┐
            │      Grafana      │
            │ Dashboards from   │
            │   Prometheus      │
            │     @ 3000        │
            └───────────────────┘

        Orchestration Layer → Eclipse Symphony
Components
Component	Purpose	Port	Folder
Prometheus	Scrapes metrics from IoT-Sim and Analysis Engine	9090	prometheus-deploy/
IoT-Sim	Generates random IoT data (temp, humidity, battery)	8085	iot-sim/
Analysis Engine	Processes data from Prometheus and emits predictions	8086	analysis-engine/

🧱 Folder Structure
symphony-iot-monitoring/
│
├── iot-sim/
│   ├── Dockerfile
│   ├── app.py
│   ├── solution.yaml
│   ├── solutioncontainer.yaml
│   ├── instance.yaml
│
├── analysis-engine/
│   ├── Dockerfile
│   ├── app.py
│   ├── requirements.txt
│   ├── solution.yaml
│   ├── solutioncontainer.yaml
│   ├── instance.yaml
│
├── prometheus-deploy/
│   ├── prometheus-config.yaml        # ConfigMap
│   ├── prometheus-custom/
│   │    ├── Dockerfile               # Custom Prometheus image
│   │    └── prometheus.yml
│   ├── solution.yaml
│   ├── solutioncontainer.yaml
│   ├── instance.yaml
│
├── grafana/
│   ├── solution.yaml
│   ├── solutioncontainer.yaml
│   ├── instance.yaml
└── docs/
    ├── architecture-diagram.png
    ├── demo-script.md

🧰 Setup (Minikube / Symphony)
minikube start

2️⃣ Deploy IoT Simulators
kubectl apply -f iot-sim/solution.yaml
kubectl apply -f iot-sim/instance.yaml

3️⃣ Deploy Custom Prometheus
kubectl apply -f prometheus-deploy/prometheus-config.yaml
kubectl apply -f prometheus-deploy/solution.yaml
kubectl apply -f prometheus-deploy/instance.yaml

4️⃣ Deploy Analysis Engine
kubectl apply -f analysis-engine/solution.yaml
kubectl apply -f analysis-engine/instance.yaml

5️⃣ Deploy Grafana
kubectl apply -f grafana/solution.yaml
kubectl apply -f grafana/instance.yaml

🌐 Port Forwarding

Prometheus
kubectl -n sample-k8s-scope port-forward svc/sample-prometheus-instance 9090:9090

Grafana
kubectl -n sample-k8s-scope port-forward svc/grafana-instance 3000:3000

Analysis Engine Metrics
kubectl -n sample-k8s-scope port-forward deployment/analysis-engine-instance 8086:8086

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
