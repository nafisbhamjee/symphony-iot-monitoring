"""
Rule Engine
Evaluates alert rules against current metrics
"""

from typing import Dict, List, Any, Optional
from prometheus_query import PrometheusQuery
from alert_tracker import AlertTracker
from email_notifier import EmailNotifier


class RuleEngine:
    """Evaluates alert rules and triggers notifications"""
    
    def __init__(self, prometheus_query: PrometheusQuery, 
                 alert_tracker: AlertTracker,
                 email_notifier: Optional[EmailNotifier] = None):
        self.prometheus_query = prometheus_query
        self.alert_tracker = alert_tracker
        self.email_notifier = email_notifier
        self.rules_evaluated = 0
        self.alerts_fired = 0
        
    def evaluate_rule(self, rule: Dict[str, Any]) -> bool:
        """
        Evaluate a single alert rule
        
        Args:
            rule: Alert rule configuration
            
        Returns:
            True if alert was fired, False otherwise
        """
        rule_name = rule['name']
        metric_name = rule['metric']
        condition = rule['condition']
        threshold = rule['threshold']
        duration = rule['duration']
        
        # Query current metric value
        current_value = self.prometheus_query.query_metric(metric_name)
        
        if current_value is None:
            print(f"⚠ Cannot evaluate rule '{rule_name}': metric data unavailable")
            return False
        
        # Check condition
        condition_met = self._check_condition(current_value, condition, threshold)
        
        # Update alert state
        should_fire, should_resolve, state = self.alert_tracker.update_alert_state(
            rule_name, condition_met, duration, current_value
        )
        
        # Print status
        status_emoji = "✓" if not condition_met else "⚠"
        print(f"{status_emoji} {metric_name} = {current_value} (state: {state.value})")
        
        # Fire alert if needed
        if should_fire and self.email_notifier:
            self._send_alert(rule, current_value)
            self.alerts_fired += 1
            return True
        
        # Send resolution if needed
        if should_resolve and self.email_notifier:
            resolution_enabled = rule.get('resolution_notification', True)
            if resolution_enabled:
                self._send_resolution(rule, current_value)
        
        return False
    
    def evaluate_all_rules(self, rules: List[Dict[str, Any]]):
        """
        Evaluate all alert rules
        
        Args:
            rules: List of alert rule configurations
        """
        print(f"\n{'='*50}")
        print(f"Evaluating {len(rules)} alert rules...")
        print(f"{'='*50}")
        
        for rule in rules:
            self.rules_evaluated += 1
            self.evaluate_rule(rule)
        
        print(f"{'='*50}\n")
    
    def _check_condition(self, value: float, condition: str, threshold: float) -> bool:
        """Check if condition is met"""
        if condition == '>':
            return value > threshold
        elif condition == '<':
            return value < threshold
        elif condition == '>=':
            return value >= threshold
        elif condition == '<=':
            return value <= threshold
        elif condition == '==':
            return value == threshold
        elif condition == '!=':
            return value != threshold
        else:
            print(f"✗ Unknown condition: {condition}")
            return False
    
    def _send_alert(self, rule: Dict[str, Any], current_value: float):
        """Send alert notification"""
        if not self.email_notifier:
            return
        
        success = self.email_notifier.send_alert_email(
            rule_name=rule['name'],
            subject=rule['email_subject'],
            body=rule['email_body'],
            metric_name=rule['metric'],
            current_value=current_value,
            threshold=rule['threshold'],
            condition=rule['condition'],
            severity=rule['severity']
        )
        
        if success:
            print(f"🚨 ALERT FIRED: {rule['name']}")
    
    def _send_resolution(self, rule: Dict[str, Any], current_value: float):
        """Send resolution notification"""
        if not self.email_notifier:
            return
        
        success = self.email_notifier.send_resolution_email(
            rule_name=rule['name'],
            subject=rule['email_subject'],
            metric_name=rule['metric'],
            current_value=current_value
        )
        
        if success:
            print(f"✅ ALERT RESOLVED: {rule['name']}")
    
    def get_stats(self) -> Dict:
        """Get rule evaluation statistics"""
        return {
            'rules_evaluated': self.rules_evaluated,
            'alerts_fired': self.alerts_fired
        }
