"""
Alert Engine - Main Application
Monitors IoT metrics and sends email alerts
"""

from flask import Flask, Response, jsonify, request
from prometheus_client import Gauge, Counter, generate_latest, REGISTRY
import time
import threading
from datetime import datetime

from config_loader import ConfigLoader
from prometheus_query import PrometheusQuery
from alert_tracker import AlertTracker
from email_notifier import EmailNotifier
from rule_engine import RuleEngine

app = Flask(__name__)

# Prometheus metrics for the alert engine itself
alerts_fired_total = Counter('alert_engine_alerts_fired_total', 
                             'Total number of alerts fired',
                             ['rule_name', 'severity'])
emails_sent_total = Counter('alert_engine_emails_sent_total',
                           'Total number of emails sent',
                           ['status'])
rules_evaluated_total = Counter('alert_engine_rules_evaluated_total',
                               'Total number of rule evaluations')
last_evaluation_time = Gauge('alert_engine_last_evaluation_timestamp',
                            'Timestamp of last rule evaluation')

# Global components
config_loader = None
prometheus_query = None
alert_tracker = None
email_notifier = None
rule_engine = None
is_running = False


def initialize_components():
    """Initialize all alert engine components"""
    global config_loader, prometheus_query, alert_tracker, email_notifier, rule_engine
    
    print("\n" + "="*60)
    print("🚀 Alert Engine Starting...")
    print("="*60)
    
    # Load configuration
    config_loader = ConfigLoader()
    config = config_loader.load()
    
    if not config_loader.validate():
        raise Exception("Configuration validation failed")
    
    # Initialize Prometheus query client
    prom_config = config_loader.get_prometheus_config()
    prometheus_query = PrometheusQuery(prom_config['url'])
    
    # Check Prometheus connectivity
    if prometheus_query.health_check():
        print("✓ Connected to Prometheus")
    else:
        print("⚠ Warning: Cannot connect to Prometheus (will retry)")
    
    # Initialize alert tracker
    alert_settings = config_loader.get_alert_settings()
    cooldown = alert_settings.get('cooldown_minutes', 15)
    alert_tracker = AlertTracker(cooldown_minutes=cooldown)
    print(f"✓ Alert tracker initialized (cooldown: {cooldown} minutes)")
    
    # Initialize email notifier
    email_config = config_loader.get_email_config()
    if email_config.get('enabled', True):
        email_notifier = EmailNotifier(
            smtp_server=email_config['smtp_server'],
            smtp_port=email_config['smtp_port'],
            from_email=email_config['from_email'],
            username=email_config['username'],
            password=email_config['password'],
            to_emails=email_config.get('to_emails', [])
        )
        print(f"✓ Email notifier configured: {email_config['from_email']}")
    else:
        print("⚠ Email notifications disabled")
    
    # Initialize rule engine
    rule_engine = RuleEngine(prometheus_query, alert_tracker, email_notifier)
    
    alert_rules = config_loader.get_alert_rules()
    print(f"✓ Loaded {len(alert_rules)} alert rules")
    
    print("="*60)
    print("✅ Alert Engine Ready")
    print("="*60 + "\n")


def evaluation_loop():
    """Main evaluation loop - runs in background thread"""
    global is_running
    
    if not config_loader:
        return
    
    prom_config = config_loader.get_prometheus_config()
    interval = prom_config.get('scrape_interval', 30)
    alert_rules = config_loader.get_alert_rules()
    
    print(f"🔄 Evaluation loop started (interval: {interval}s)")
    
    while is_running:
        try:
            # Evaluate all rules
            rule_engine.evaluate_all_rules(alert_rules)
            
            # Update metrics
            rules_evaluated_total.inc(len(alert_rules))
            last_evaluation_time.set(time.time())
            
            # Update alert metrics
            for rule_name, alert_info in alert_tracker.get_all_alerts().items():
                if alert_info['fire_count'] > 0:
                    # Find severity from rules
                    severity = next((r['severity'] for r in alert_rules 
                                   if r['name'] == rule_name), 'unknown')
                    alerts_fired_total.labels(rule_name=rule_name, 
                                            severity=severity).inc(0)
            
            # Update email metrics
            if email_notifier:
                stats = email_notifier.get_stats()
                emails_sent_total.labels(status='success').inc(0)
                emails_sent_total.labels(status='failed').inc(0)
            
        except Exception as e:
            print(f"✗ Error in evaluation loop: {e}")
        
        # Sleep until next evaluation
        time.sleep(interval)


@app.route('/')
def home():
    """Home endpoint"""
    return jsonify({
        'service': 'Symphony IoT Alert Engine',
        'status': 'running',
        'timestamp': datetime.now().isoformat()
    })


@app.route('/health')
def health():
    """Health check endpoint"""
    health_status = {
        'status': 'healthy',
        'components': {
            'prometheus': prometheus_query.health_check() if prometheus_query else False,
            'email': email_notifier is not None,
            'evaluation_loop': is_running
        },
        'timestamp': datetime.now().isoformat()
    }
    
    status_code = 200 if all(health_status['components'].values()) else 503
    return jsonify(health_status), status_code


@app.route('/metrics')
def metrics():
    """Prometheus metrics endpoint"""
    return Response(generate_latest(REGISTRY), mimetype='text/plain')


@app.route('/alerts')
def alerts():
    """Get current alert status"""
    if not alert_tracker:
        return jsonify({'error': 'Alert tracker not initialized'}), 500
    
    return jsonify({
        'alerts': alert_tracker.get_all_alerts(),
        'timestamp': datetime.now().isoformat()
    })


@app.route('/history')
def history():
    """Get alert history"""
    if not alert_tracker:
        return jsonify({'error': 'Alert tracker not initialized'}), 500
    
    return jsonify({
        'history': alert_tracker.get_all_alerts(),
        'stats': rule_engine.get_stats() if rule_engine else {},
        'email_stats': email_notifier.get_stats() if email_notifier else {},
        'timestamp': datetime.now().isoformat()
    })


@app.route('/test-email', methods=['POST'])
def test_email():
    """Send test email"""
    if not email_notifier:
        return jsonify({'error': 'Email notifier not configured'}), 500
    
    success = email_notifier.send_test_email()
    
    if success:
        return jsonify({
            'status': 'success',
            'message': 'Test email sent successfully'
        })
    else:
        return jsonify({
            'status': 'failed',
            'message': 'Failed to send test email'
        }), 500


@app.route('/rules')
def rules():
    """Get configured alert rules"""
    if not config_loader:
        return jsonify({'error': 'Configuration not loaded'}), 500
    
    return jsonify({
        'rules': config_loader.get_alert_rules(),
        'count': len(config_loader.get_alert_rules())
    })


if __name__ == '__main__':
    # Initialize components
    try:
        initialize_components()
    except Exception as e:
        print(f"✗ Failed to initialize: {e}")
        exit(1)
    
    # Start evaluation loop in background thread
    is_running = True
    eval_thread = threading.Thread(target=evaluation_loop, daemon=True)
    eval_thread.start()
    
    # Start Flask app
    print("🌐 Starting Flask server on port 8087...")
    app.run(host='0.0.0.0', port=8087, debug=False)
