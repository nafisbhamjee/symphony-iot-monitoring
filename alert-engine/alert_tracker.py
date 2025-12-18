"""
Alert Tracker
Tracks alert states and prevents duplicate notifications
"""

from datetime import datetime, timedelta
from typing import Dict, Optional
from enum import Enum


class AlertState(Enum):
    """Alert state enumeration"""
    NORMAL = "normal"
    PENDING = "pending"
    FIRING = "firing"
    RESOLVED = "resolved"


class AlertTracker:
    """Tracks alert states and history to prevent spam"""
    
    def __init__(self, cooldown_minutes: int = 15):
        self.cooldown_minutes = cooldown_minutes
        self.alerts = {}  # {rule_name: alert_info}
        
    def update_alert_state(self, rule_name: str, condition_met: bool, 
                          duration_seconds: int, current_value: float) -> tuple:
        """
        Update alert state based on current condition
        
        Args:
            rule_name: Name of the alert rule
            condition_met: Whether the alert condition is currently met
            duration_seconds: Required duration in seconds
            current_value: Current metric value
            
        Returns:
            Tuple of (should_fire: bool, should_resolve: bool, state: AlertState)
        """
        now = datetime.now()
        
        # Initialize alert if not tracked
        if rule_name not in self.alerts:
            self.alerts[rule_name] = {
                'state': AlertState.NORMAL,
                'first_triggered': None,
                'last_fired': None,
                'last_resolved': None,
                'fire_count': 0,
                'current_value': None
            }
        
        alert = self.alerts[rule_name]
        should_fire = False
        should_resolve = False
        
        if condition_met:
            # Condition is met
            if alert['state'] == AlertState.NORMAL:
                # Just started, enter pending state
                alert['state'] = AlertState.PENDING
                alert['first_triggered'] = now
                alert['current_value'] = current_value
                
            elif alert['state'] == AlertState.PENDING:
                # Check if duration threshold met
                time_in_pending = (now - alert['first_triggered']).total_seconds()
                if time_in_pending >= duration_seconds:
                    # Duration met, fire alert
                    alert['state'] = AlertState.FIRING
                    alert['last_fired'] = now
                    alert['fire_count'] += 1
                    alert['current_value'] = current_value
                    should_fire = True
                    
            elif alert['state'] == AlertState.FIRING:
                # Already firing, check cooldown
                if alert['last_fired']:
                    time_since_last = now - alert['last_fired']
                    if time_since_last > timedelta(minutes=self.cooldown_minutes):
                        # Cooldown expired, can fire again
                        alert['last_fired'] = now
                        alert['fire_count'] += 1
                        alert['current_value'] = current_value
                        should_fire = True
                        
            elif alert['state'] == AlertState.RESOLVED:
                # Was resolved, now triggering again
                alert['state'] = AlertState.PENDING
                alert['first_triggered'] = now
                alert['current_value'] = current_value
                
        else:
            # Condition not met
            if alert['state'] in [AlertState.FIRING, AlertState.PENDING]:
                # Alert is resolving
                alert['state'] = AlertState.RESOLVED
                alert['last_resolved'] = now
                alert['first_triggered'] = None
                should_resolve = True
                
            elif alert['state'] == AlertState.RESOLVED:
                # Stay resolved, eventually go back to normal
                if alert['last_resolved']:
                    time_since_resolved = now - alert['last_resolved']
                    if time_since_resolved > timedelta(minutes=5):
                        alert['state'] = AlertState.NORMAL
        
        return should_fire, should_resolve, alert['state']
    
    def get_alert_info(self, rule_name: str) -> Optional[Dict]:
        """Get current alert information"""
        return self.alerts.get(rule_name)
    
    def get_all_alerts(self) -> Dict:
        """Get all tracked alerts"""
        result = {}
        for name, info in self.alerts.items():
            result[name] = {
                'state': info['state'].value,
                'fire_count': info['fire_count'],
                'last_fired': info['last_fired'].isoformat() if info['last_fired'] else None,
                'last_resolved': info['last_resolved'].isoformat() if info['last_resolved'] else None,
                'current_value': info['current_value']
            }
        return result
    
    def reset(self):
        """Reset all alert states"""
        self.alerts.clear()
