"""
MCP (Model Context Protocol) Hub
Central orchestration hub for managing all integrations
"""

from typing import Dict, Any, List, Optional
from pathlib import Path
import json
from ..base import BaseIntegration, IntegrationStatus


class MCPHub:
    """Central hub for orchestrating all integrations"""
    
    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path
        self.integrations: Dict[str, BaseIntegration] = {}
        self.config = {}
        
        if config_path and config_path.exists():
            self.load_config()
    
    def load_config(self):
        """Load integration configurations from file"""
        if self.config_path and self.config_path.exists():
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)
    
    def save_config(self):
        """Save integration configurations to file"""
        if self.config_path:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
    
    def register_integration(self, name: str, integration: BaseIntegration):
        """Register a new integration"""
        self.integrations[name] = integration
    
    def unregister_integration(self, name: str):
        """Unregister an integration"""
        if name in self.integrations:
            del self.integrations[name]
    
    def get_integration(self, name: str) -> Optional[BaseIntegration]:
        """Get an integration by name"""
        return self.integrations.get(name)
    
    def list_integrations(self) -> List[Dict[str, Any]]:
        """List all registered integrations"""
        return [{
            'name': name,
            'status': integration.status.value,
            'healthy': integration.is_healthy()
        } for name, integration in self.integrations.items()]
    
    def connect_all(self) -> Dict[str, bool]:
        """Connect all integrations"""
        results = {}
        for name, integration in self.integrations.items():
            try:
                results[name] = integration.connect()
            except Exception as e:
                results[name] = False
        return results
    
    def health_check_all(self) -> Dict[str, Dict[str, Any]]:
        """Run health checks on all integrations"""
        results = {}
        for name, integration in self.integrations.items():
            try:
                results[name] = integration.health_check()
            except Exception as e:
                results[name] = {"status": "error", "error": str(e)}
        return results
    
    def get_all_info(self) -> Dict[str, Dict[str, Any]]:
        """Get information from all integrations"""
        results = {}
        for name, integration in self.integrations.items():
            try:
                results[name] = integration.get_info()
            except Exception as e:
                results[name] = {"error": str(e)}
        return results
    
    def get_status_summary(self) -> Dict[str, Any]:
        """Get a summary of all integration statuses"""
        statuses = {
            'healthy': 0,
            'degraded': 0,
            'unhealthy': 0,
            'unknown': 0
        }
        
        for integration in self.integrations.values():
            status = integration.status.value
            if status in statuses:
                statuses[status] += 1
        
        return {
            'total': len(self.integrations),
            'statuses': statuses,
            'overall_health': self._calculate_overall_health(statuses)
        }
    
    def _calculate_overall_health(self, statuses: Dict[str, int]) -> str:
        """Calculate overall health based on individual statuses"""
        total = sum(statuses.values())
        if total == 0:
            return 'unknown'
        
        healthy_ratio = statuses['healthy'] / total
        
        if healthy_ratio == 1.0:
            return 'healthy'
        elif healthy_ratio >= 0.7:
            return 'degraded'
        else:
            return 'unhealthy'
    
    def discover_services(self) -> List[Dict[str, Any]]:
        """Discover available services across all integrations"""
        services = []
        
        for name, integration in self.integrations.items():
            if integration.is_healthy():
                services.append({
                    'integration': name,
                    'type': integration.name,
                    'status': 'available',
                    'info': integration.get_info()
                })
        
        return services
    
    def configure_integration(self, name: str, config: Dict[str, Any]):
        """Configure an integration"""
        if name not in self.config:
            self.config[name] = {}
        
        self.config[name].update(config)
        self.save_config()
        
        # Update integration if already registered
        if name in self.integrations:
            self.integrations[name].config.update(config)
    
    def get_integration_config(self, name: str) -> Dict[str, Any]:
        """Get configuration for an integration"""
        return self.config.get(name, {})
