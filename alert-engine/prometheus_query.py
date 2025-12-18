"""
Prometheus Query Client
Fetches current metric values from Prometheus
"""

import requests
from typing import Optional, Dict
from datetime import datetime


class PrometheusQuery:
    """Query Prometheus for current metric values"""
    
    def __init__(self, prometheus_url: str):
        self.prometheus_url = prometheus_url.rstrip('/')
        self.api_url = f"{self.prometheus_url}/api/v1/query"
        
    def query_metric(self, metric_name: str) -> Optional[float]:
        """
        Query Prometheus for the current value of a metric
        
        Args:
            metric_name: Name of the metric (e.g., 'iot_temperature_celsius')
            
        Returns:
            Current value as float, or None if query fails
        """
        try:
            params = {'query': metric_name}
            response = requests.get(self.api_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data['status'] != 'success':
                print(f"✗ Prometheus query failed: {data}")
                return None
            
            results = data['data']['result']
            
            if not results:
                print(f"⚠ No data found for metric: {metric_name}")
                return None
            
            # Get the first result's value
            value = float(results[0]['value'][1])
            return value
            
        except requests.exceptions.RequestException as e:
            print(f"✗ Error querying Prometheus: {e}")
            return None
        except (KeyError, ValueError, IndexError) as e:
            print(f"✗ Error parsing Prometheus response: {e}")
            return None
    
    def query_all_metrics(self, metric_names: list) -> Dict[str, Optional[float]]:
        """
        Query multiple metrics at once
        
        Args:
            metric_names: List of metric names to query
            
        Returns:
            Dictionary mapping metric names to their current values
        """
        results = {}
        for metric in metric_names:
            results[metric] = self.query_metric(metric)
        return results
    
    def health_check(self) -> bool:
        """Check if Prometheus is reachable"""
        try:
            response = requests.get(f"{self.prometheus_url}/-/healthy", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
