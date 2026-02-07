"""
npm Registry Integration
Provides npm package registry search and information capabilities
"""

from typing import Dict, Any, List, Optional
import requests
from ..base import BaseIntegration, IntegrationStatus


class NpmIntegration(BaseIntegration):
    """npm registry integration"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__("npm", config)
        self.registry_url = self.config.get('registry_url', 'https://registry.npmjs.org')
        self.api_url = 'https://api.npms.io/v2'
    
    def connect(self) -> bool:
        """Test connection to npm registry"""
        try:
            response = requests.get(f"{self.registry_url}/-/ping", timeout=5)
            if response.status_code == 200:
                self.status = IntegrationStatus.HEALTHY
                return True
            else:
                self.status = IntegrationStatus.UNHEALTHY
                return False
        except Exception:
            self.status = IntegrationStatus.UNHEALTHY
            return False
    
    def health_check(self) -> Dict[str, Any]:
        """Check npm registry health"""
        try:
            response = requests.get(f"{self.registry_url}/-/ping", timeout=5)
            if response.status_code == 200:
                self.status = IntegrationStatus.HEALTHY
                return {"status": "healthy", "registry": self.registry_url}
            else:
                self.status = IntegrationStatus.UNHEALTHY
                return {"status": "unhealthy", "registry": self.registry_url}
        except Exception as e:
            self.status = IntegrationStatus.UNHEALTHY
            return {"status": "unhealthy", "error": str(e)}
    
    def get_info(self) -> Dict[str, Any]:
        """Get npm registry information"""
        return {
            "registry_url": self.registry_url,
            "api_url": self.api_url
        }
    
    def search_packages(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Search for npm packages"""
        try:
            response = requests.get(
                f"{self.api_url}/search",
                params={"q": query, "size": limit},
                timeout=10
            )
            
            if response.status_code == 200:
                results = response.json().get('results', [])
                return [{
                    'name': pkg['package']['name'],
                    'version': pkg['package']['version'],
                    'description': pkg['package'].get('description', 'No description'),
                    'author': pkg['package'].get('author', {}).get('name', 'Unknown'),
                    'downloads': pkg['score']['detail'].get('popularity', 0)
                } for pkg in results]
            else:
                return []
        except Exception as e:
            return [{"error": str(e)}]
    
    def get_package_info(self, package_name: str) -> Dict[str, Any]:
        """Get detailed information about a package"""
        try:
            response = requests.get(
                f"{self.registry_url}/{package_name}",
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                latest_version = data.get('dist-tags', {}).get('latest', 'unknown')
                
                return {
                    'name': data.get('name'),
                    'version': latest_version,
                    'description': data.get('description', 'No description'),
                    'homepage': data.get('homepage', 'N/A'),
                    'repository': data.get('repository', {}).get('url', 'N/A'),
                    'license': data.get('license', 'Unknown'),
                    'author': data.get('author', {}).get('name', 'Unknown') if isinstance(data.get('author'), dict) else data.get('author', 'Unknown'),
                    'versions': list(data.get('versions', {}).keys())
                }
            else:
                return {"error": f"Package not found: {package_name}"}
        except Exception as e:
            return {"error": str(e)}
    
    def get_package_downloads(self, package_name: str) -> Dict[str, Any]:
        """Get download statistics for a package"""
        try:
            # Get last week downloads
            response = requests.get(
                f"https://api.npmjs.org/downloads/point/last-week/{package_name}",
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": "Could not fetch download stats"}
        except Exception as e:
            return {"error": str(e)}
