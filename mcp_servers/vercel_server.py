"""
Vercel MCP Server Integration
Provides Vercel API access for deployment management
"""

import requests
from typing import Dict, Any, List, Optional
from .base import BaseMCPServer, MCPServerConfig


class VercelMCPServer(BaseMCPServer):
    """MCP Server for Vercel integration"""
    
    def __init__(self, config: MCPServerConfig):
        super().__init__(config)
        self.api_token = None
        self.base_url = "https://api.vercel.com"
        self.session = requests.Session()
    
    def authenticate(self) -> bool:
        """Authenticate with Vercel API"""
        self.api_token = self.config.get_credential("token")
        if not self.api_token:
            print("Error: Vercel token not found. Use 'mcp config vercel --token YOUR_TOKEN'")
            return False
        
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        })
        return True
    
    def test_connection(self) -> bool:
        """Test connection to Vercel API"""
        try:
            response = self.session.get(f"{self.base_url}/v2/user")
            return response.status_code == 200
        except Exception as e:
            print(f"Error testing Vercel connection: {e}")
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """Get Vercel service status"""
        try:
            response = self.session.get(f"{self.base_url}/v2/user")
            if response.status_code == 200:
                user_data = response.json()
                return {
                    "status": "connected",
                    "user": user_data.get("username"),
                    "email": user_data.get("email"),
                    "mode": self.config.mode.value
                }
        except Exception as e:
            return {"status": "error", "message": str(e)}
        
        return {"status": "disconnected"}
    
    def list_projects(self) -> List[Dict[str, Any]]:
        """List all projects"""
        try:
            response = self.session.get(f"{self.base_url}/v9/projects")
            if response.status_code == 200:
                data = response.json()
                return data.get("projects", [])
            else:
                print(f"Error listing projects: {response.status_code}")
                return []
        except Exception as e:
            print(f"Error listing projects: {e}")
            return []
    
    def get_project(self, project_id: str) -> Optional[Dict[str, Any]]:
        """Get project details"""
        try:
            response = self.session.get(f"{self.base_url}/v9/projects/{project_id}")
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error getting project: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error getting project: {e}")
            return None
    
    def list_deployments(self, project_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """List deployments"""
        try:
            url = f"{self.base_url}/v6/deployments"
            params = {}
            if project_id:
                params["projectId"] = project_id
            
            response = self.session.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                return data.get("deployments", [])
            else:
                print(f"Error listing deployments: {response.status_code}")
                return []
        except Exception as e:
            print(f"Error listing deployments: {e}")
            return []
    
    def create_deployment(self, project_name: str, files: Dict[str, str]) -> Optional[Dict[str, Any]]:
        """Create a new deployment"""
        if self.config.is_sandbox():
            print("⚠️  Running in SANDBOX mode - deployment simulated")
            return {
                "project_name": project_name,
                "status": "simulated",
                "mode": "sandbox"
            }
        
        try:
            response = self.session.post(
                f"{self.base_url}/v13/deployments",
                json={
                    "name": project_name,
                    "files": [{"file": k, "data": v} for k, v in files.items()],
                    "projectSettings": {"framework": None}
                }
            )
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error creating deployment: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error creating deployment: {e}")
            return None
    
    def get_deployment_status(self, deployment_id: str) -> Optional[Dict[str, Any]]:
        """Get deployment status"""
        try:
            response = self.session.get(f"{self.base_url}/v13/deployments/{deployment_id}")
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error getting deployment status: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error getting deployment status: {e}")
            return None
