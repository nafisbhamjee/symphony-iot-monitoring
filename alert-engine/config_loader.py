"""
Configuration Loader
Loads alert rules and email settings from YAML file
"""

import yaml
import os
from typing import Dict, List, Any


class ConfigLoader:
    """Loads and validates configuration from alert_rules.yaml"""
    
    def __init__(self, config_path: str = "alert_rules.yaml"):
        self.config_path = config_path
        self.config = None
        
    def load(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        try:
            with open(self.config_path, 'r') as f:
                self.config = yaml.safe_load(f)
            print(f"✓ Configuration loaded from {self.config_path}")
            return self.config
        except FileNotFoundError:
            print(f"✗ Configuration file not found: {self.config_path}")
            raise
        except yaml.YAMLError as e:
            print(f"✗ Error parsing YAML configuration: {e}")
            raise
    
    def get_prometheus_config(self) -> Dict[str, Any]:
        """Get Prometheus configuration"""
        return self.config.get('prometheus', {})
    
    def get_email_config(self) -> Dict[str, Any]:
        """Get email configuration"""
        return self.config.get('email', {})
    
    def get_alert_settings(self) -> Dict[str, Any]:
        """Get general alert settings"""
        return self.config.get('alert_settings', {})
    
    def get_alert_rules(self) -> List[Dict[str, Any]]:
        """Get list of alert rules"""
        return self.config.get('alert_rules', [])
    
    def validate(self) -> bool:
        """Validate configuration has required fields"""
        if not self.config:
            return False
        
        # Check required sections
        required_sections = ['prometheus', 'email', 'alert_rules']
        for section in required_sections:
            if section not in self.config:
                print(f"✗ Missing required section: {section}")
                return False
        
        # Check email config
        email_config = self.get_email_config()
        required_email_fields = ['smtp_server', 'from_email', 'username', 'password']
        for field in required_email_fields:
            if field not in email_config:
                print(f"✗ Missing required email field: {field}")
                return False
        
        # Check alert rules
        alert_rules = self.get_alert_rules()
        if not alert_rules:
            print("✗ No alert rules defined")
            return False
        
        print(f"✓ Configuration validated successfully ({len(alert_rules)} rules)")
        return True
