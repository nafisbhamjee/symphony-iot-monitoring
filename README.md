🌐 Eclipse Symphony IoT Monitoring & Predictive Analytics System

A complete cloud-native IoT monitoring and prediction pipeline orchestrated by Eclipse Symphony, integrating:

IoT Simulators → generate real-time sensor telemetry

Prometheus → scrapes raw & predicted metrics

Python Analysis Engine → computes moving-average predictions

Grafana → visualizes live and historical data

Symphony → orchestrates & manages components

🧩 Components

| Component           | Purpose                                | Port | Directory          |
| ------------------- | -------------------------------------- | ---- | ------------------ |
| **Prometheus**      | Scrapes IoT + Analysis Engine metrics  | 9090 | `prometheus/`      |
| **IoT Simulators**  | Generates IoT telemetry                | 8085 | `iot-sim/`         |
| **Analysis Engine** | Computes moving-average predictions    | 8086 | `analysis-engine/` |
| **Alert Engine**    | Monitors metrics & sends email alerts  | 8087 | `alert-engine/`    |
| **Grafana**         | Real-time monitoring dashboards        | 3000 | `grafana/`         |
| **Symphony**        | Orchestration and lifecycle management | N/A  | All solution dirs  |


---

## 📁 Folder Structure

```text
symphony-iot-monitoring/
├── iot-sim/
│   ├── Dockerfile
│   ├── app.py
│   ├── solution.yaml
│   ├── instance.yaml
│
├── analysis-engine/
│   ├── Dockerfile
│   ├── app.py
│   ├── requirements.txt
│   ├── solution.yaml
│   ├── instance.yaml
│
├── prometheus/
│   ├── prometheus-config.yaml
│   ├── solution.yaml
│   ├── instance.yaml
│   └── prometheus-custom/
│         ├── Dockerfile
│         ├── prometheus.yml
│
├── grafana/
│   ├── solution.yaml
│   ├── instance.yaml
│
└── scripts/
    ├── reset_prometheus.sh
    ├── reset_iot_sim.sh
    ├── reset_analysis_engine.sh
    ├── reset_grafana.sh
    └── reset_all.sh

```

⚙️ Deployment Instructions

1️⃣ Start Minikube  
minikube start  

2️⃣ Deploy Prometheus  
kubectl apply -f prometheus/solution.yaml  
kubectl apply -f prometheus/instance.yaml  

3️⃣ Deploy IoT-Sim  
kubectl apply -f iot-sim/solution.yaml  
kubectl apply -f iot-sim/instance.yaml  

4️⃣ Deploy Analysis Engine  
kubectl apply -f analysis-engine/solution.yaml  
kubectl apply -f analysis-engine/instance.yaml  

5️⃣ Deploy Alert Engine  
kubectl apply -f alert-engine/solution.yaml  
kubectl apply -f alert-engine/instance.yaml  

6️⃣ Deploy Grafana  
kubectl apply -f grafana/solution.yaml  
kubectl apply -f grafana/instance.yaml  

🔍 Accessing the System  

Prometheus  
kubectl port-forward svc/sample-prometheus 9090:9090 -n sample-k8s-scope  
→ http://localhost:9090  

Grafana  
kubectl port-forward svc/grafana 3000:3000 -n sample-k8s-scope  
→ http://localhost:3000  

IoT-Sim Metrics → http://localhost:8085/metrics  

Analysis Engine Predictions → http://localhost:8086/metrics  

Alert Engine  
kubectl port-forward svc/alert-engine-instance 8087:8087 -n sample-k8s-scope  
→ http://localhost:8087  
→ Test Email: curl -X POST http://localhost:8087/test-email  



📊 Features

| Feature                     | Description                                        |
| --------------------------- | -------------------------------------------------- |
| **Live IoT Telemetry**      | Sensor data scraped every 5 seconds                |
| **Predictive Analytics**    | Moving-average temperature forecasting             |
| **Unified Prometheus TSDB** | Raw + predicted metrics in one dataset             |
| **Grafana Dashboards**      | Real-time, low-latency visualization               |
| **Symphony Orchestration**  | Automated deployment, reconciliation, self-healing |


🔄 Reset Scripts

| Script Name              | Purpose                                                |
| ------------------------ | ------------------------------------------------------ |
| `reset-iot.sh`           | Resets IoT Simulator solution, container, and instance |
| `reset-prometheus.sh`    | Resets Prometheus and its custom config                |
| `reset-analysis.sh`      | Resets the Python Analysis Engine                      |
| `reset-alert-engine.sh`  | Resets the Alert Engine                                |
| `reset-grafana.sh`       | Resets Grafana deployment and configs                  |
| `reset-all.sh`           | Full system reset                                      |

👥 Contributors

| Name                          | Contribution                                                 |
| ----------------------------- | ------------------------------------------------------------ |
| **Nafis Bhamjee**             | Lead Developer, Architecture, Prometheus/Grafana Integration |
| **Canchi Sathya**             | Testing, Validation                                          |
| **Ankita Jayraj Patel**       | Documentation, Research, Configuration                       |
| **Oluwadamifola Ademoye**     | IoT Simulator Development, Pipeline Debugging                |
| **Devam Dharmendrabhai Shah** | Validation                                                   |


Guided by:
Professor Mohamed El-Darielby

📜 License

MIT License © 2025 — IoT Monitoring & Analytics Team
