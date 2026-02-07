"""
PyPI Integration
Provides Python Package Index search and information capabilities
"""

from typing import Dict, Any, List, Optional
import requests
from ..base import BaseIntegration, IntegrationStatus


class PyPIIntegration(BaseIntegration):
    """PyPI integration"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__("PyPI", config)
        self.api_url = 'https://pypi.org/pypi'
        self.search_url = 'https://pypi.org/search'
    
    def connect(self) -> bool:
        """Test connection to PyPI"""
        try:
            response = requests.get(f"{self.api_url}/pip/json", timeout=5)
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
        """Check PyPI health"""
        try:
            response = requests.get(f"{self.api_url}/pip/json", timeout=5)
            if response.status_code == 200:
                self.status = IntegrationStatus.HEALTHY
                return {"status": "healthy", "api_url": self.api_url}
            else:
                self.status = IntegrationStatus.UNHEALTHY
                return {"status": "unhealthy", "api_url": self.api_url}
        except Exception as e:
            self.status = IntegrationStatus.UNHEALTHY
            return {"status": "unhealthy", "error": str(e)}
    
    def get_info(self) -> Dict[str, Any]:
        """Get PyPI information"""
        return {
            "api_url": self.api_url,
            "search_url": self.search_url
        }
    
    def get_package_info(self, package_name: str) -> Dict[str, Any]:
        """Get detailed information about a package"""
        try:
            response = requests.get(
                f"{self.api_url}/{package_name}/json",
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                info = data.get('info', {})
                
                return {
                    'name': info.get('name'),
                    'version': info.get('version'),
                    'summary': info.get('summary', 'No summary'),
                    'description': info.get('description', 'No description')[:500],  # Truncate
                    'author': info.get('author', 'Unknown'),
                    'license': info.get('license', 'Unknown'),
                    'homepage': info.get('home_page', 'N/A'),
                    'project_url': info.get('project_url', 'N/A'),
                    'requires_python': info.get('requires_python', 'Any'),
                    'releases': list(data.get('releases', {}).keys())[-10:]  # Last 10 versions
                }
            else:
                return {"error": f"Package not found: {package_name}"}
        except Exception as e:
            return {"error": str(e)}
    
    def get_package_releases(self, package_name: str) -> List[str]:
        """Get list of available releases for a package"""
        try:
            response = requests.get(
                f"{self.api_url}/{package_name}/json",
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return list(data.get('releases', {}).keys())
            else:
                return []
        except Exception as e:
            return []
    
    def search_packages(self, query: str) -> List[Dict[str, Any]]:
        """Search for packages (note: PyPI doesn't have a public search API, 
        so we'll use a simple package info lookup for common packages)"""
        # PyPI removed their search API, so this is a limited implementation
        # In a real implementation, you might use a third-party service or scraping
        return [{
            "note": "PyPI search API is not available. Use 'get_package_info' for specific packages.",
            "query": query
        }]
    
    def get_latest_version(self, package_name: str) -> Optional[str]:
        """Get the latest version of a package"""
        try:
            response = requests.get(
                f"{self.api_url}/{package_name}/json",
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('info', {}).get('version')
            else:
                return None
        except Exception:
            return None
