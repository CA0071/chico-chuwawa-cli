"""
Railway MCP Server Integration
Provides Railway API access for deployment management
"""

import requests
from typing import Dict, Any, List, Optional
from .base import BaseMCPServer, MCPServerConfig


class RailwayMCPServer(BaseMCPServer):
    """MCP Server for Railway integration"""
    
    def __init__(self, config: MCPServerConfig):
        super().__init__(config)
        self.api_token = None
        self.base_url = "https://backboard.railway.app/graphql/v2"
        self.session = requests.Session()
    
    def authenticate(self) -> bool:
        """Authenticate with Railway API"""
        self.api_token = self.config.get_credential("token")
        if not self.api_token:
            print("Error: Railway token not found. Use 'mcp config railway --token YOUR_TOKEN'")
            return False
        
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        })
        return True
    
    def test_connection(self) -> bool:
        """Test connection to Railway API"""
        try:
            query = """
            query {
                me {
                    id
                    name
                }
            }
            """
            response = self.session.post(self.base_url, json={"query": query})
            return response.status_code == 200 and "data" in response.json()
        except Exception as e:
            print(f"Error testing Railway connection: {e}")
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """Get Railway service status"""
        try:
            query = """
            query {
                me {
                    id
                    name
                    email
                }
            }
            """
            response = self.session.post(self.base_url, json={"query": query})
            if response.status_code == 200:
                data = response.json().get("data", {})
                user = data.get("me", {})
                return {
                    "status": "connected",
                    "user": user.get("name"),
                    "email": user.get("email"),
                    "mode": self.config.mode.value
                }
        except Exception as e:
            return {"status": "error", "message": str(e)}
        
        return {"status": "disconnected"}
    
    def list_projects(self) -> List[Dict[str, Any]]:
        """List all projects"""
        try:
            query = """
            query {
                projects {
                    edges {
                        node {
                            id
                            name
                            description
                        }
                    }
                }
            }
            """
            response = self.session.post(self.base_url, json={"query": query})
            if response.status_code == 200:
                data = response.json().get("data", {})
                edges = data.get("projects", {}).get("edges", [])
                return [edge["node"] for edge in edges]
            else:
                print(f"Error listing projects: {response.status_code}")
                return []
        except Exception as e:
            print(f"Error listing projects: {e}")
            return []
    
    def get_project_deployments(self, project_id: str) -> List[Dict[str, Any]]:
        """Get deployments for a project"""
        try:
            query = """
            query($projectId: String!) {
                project(id: $projectId) {
                    deployments {
                        edges {
                            node {
                                id
                                status
                                createdAt
                            }
                        }
                    }
                }
            }
            """
            response = self.session.post(
                self.base_url,
                json={"query": query, "variables": {"projectId": project_id}}
            )
            if response.status_code == 200:
                data = response.json().get("data", {})
                edges = data.get("project", {}).get("deployments", {}).get("edges", [])
                return [edge["node"] for edge in edges]
            else:
                print(f"Error getting deployments: {response.status_code}")
                return []
        except Exception as e:
            print(f"Error getting deployments: {e}")
            return []
    
    def trigger_deployment(self, project_id: str, service_id: str) -> Optional[Dict[str, Any]]:
        """Trigger a new deployment"""
        if self.config.is_sandbox():
            print("⚠️  Running in SANDBOX mode - deployment simulated")
            return {
                "project_id": project_id,
                "service_id": service_id,
                "status": "simulated",
                "mode": "sandbox"
            }
        
        try:
            mutation = """
            mutation($serviceId: String!) {
                serviceDeploy(serviceId: $serviceId) {
                    id
                    status
                }
            }
            """
            response = self.session.post(
                self.base_url,
                json={"query": mutation, "variables": {"serviceId": service_id}}
            )
            if response.status_code == 200:
                return response.json().get("data", {}).get("serviceDeploy")
            else:
                print(f"Error triggering deployment: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error triggering deployment: {e}")
            return None
