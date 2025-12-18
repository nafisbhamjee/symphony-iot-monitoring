# 🚨 Symphony IoT Alert Engine

Intelligent alert system that monitors IoT metrics from Prometheus and sends email notifications when thresholds are exceeded.

## Features

- ✅ **Smart Alerting** - Evaluates rules every 30 seconds
- ✅ **Email Notifications** - Gmail SMTP integration
- ✅ **Anti-Spam Logic** - Prevents duplicate alerts
- ✅ **Resolution Notifications** - "All clear" emails when issues resolve
- ✅ **Configurable Rules** - Easy YAML-based configuration
- ✅ **Prometheus Integration** - Exposes its own metrics
- ✅ **REST API** - Query alert status and history

## Quick Start

### 1. Configure Email Settings

Edit `alert_rules.yaml`:

```yaml
email:
  from_email: "your-email@gmail.com"
  to_emails:
    - "recipient@example.com"
  username: "your-email@gmail.com"
  password: "your-16-char-app-password"
```

### 2. Build Docker Image

```bash
cd alert-engine
docker build -t alert-engine:latest .
```

### 3. Deploy to Kubernetes

```bash
kubectl apply -f solution.yaml
kubectl apply -f instance.yaml
```

### 4. Verify Deployment

```bash
# Check pod status
kubectl get pods -n sample-k8s-scope | grep alert-engine

# View logs
kubectl logs -f $(kubectl get pods -n sample-k8s-scope -l app=alert-engine -o name) -n sample-k8s-scope

# Test email
kubectl port-forward svc/alert-engine-instance 8087:8087 -n sample-k8s-scope
curl -X POST http://localhost:8087/test-email
```

## Configuration

### Alert Rules

Define alert rules in `alert_rules.yaml`:

```yaml
alert_rules:
  - name: "critical_temperature"
    metric: "iot_temperature_celsius"
    condition: ">"
    threshold: 35
    duration: 120  # seconds
    severity: "critical"
    email_subject: "🔥 High Temperature Alert"
    email_body: "Temperature exceeded 35°C!"
```

### Gmail Setup

1. Enable 2-Factor Authentication on Gmail
2. Go to: Google Account → Security → App passwords
3. Create app password for "Mail"
4. Use the 16-character password in config

## API Endpoints

- `GET /` - Service info
- `GET /health` - Health check
- `GET /metrics` - Prometheus metrics
- `GET /alerts` - Current alert status
- `GET /history` - Alert history
- `GET /rules` - Configured rules
- `POST /test-email` - Send test email

## Alert Lifecycle

```
NORMAL → PENDING → FIRING → RESOLVED → NORMAL
```

- **NORMAL**: Condition is false
- **PENDING**: Condition true, waiting for duration
- **FIRING**: Alert sent, in cooldown period
- **RESOLVED**: Condition resolved, "all clear" sent

## Troubleshooting

### Test Email Fails

```bash
# Check email config
kubectl port-forward svc/alert-engine-instance 8087:8087 -n sample-k8s-scope
curl http://localhost:8087/rules

# Send test email
curl -X POST http://localhost:8087/test-email
```

### No Alerts Firing

```bash
# Check alert status
curl http://localhost:8087/alerts

# Check Prometheus connectivity
curl http://localhost:8087/health
```

### View Logs

```bash
kubectl logs -f alert-engine-instance-xxx -n sample-k8s-scope
```

## Metrics Exposed

The alert engine exposes its own metrics:

- `alert_engine_alerts_fired_total{rule_name, severity}`
- `alert_engine_emails_sent_total{status}`
- `alert_engine_rules_evaluated_total`
- `alert_engine_last_evaluation_timestamp`

## Reset/Restart

```bash
# Quick reset
../reset-alert-engine.sh

# Or manually
kubectl delete -f instance.yaml
kubectl delete -f solution.yaml
kubectl apply -f solution.yaml
kubectl apply -f instance.yaml
```
