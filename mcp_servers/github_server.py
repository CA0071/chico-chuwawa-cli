"""
GitHub MCP Server Integration
Provides GitHub API access for repository management
"""

import requests
from typing import Dict, Any, List, Optional
from .base import BaseMCPServer, MCPServerConfig


class GitHubMCPServer(BaseMCPServer):
    """MCP Server for GitHub integration"""
    
    def __init__(self, config: MCPServerConfig):
        super().__init__(config)
        self.api_token = None
        self.base_url = "https://api.github.com"
        self.session = requests.Session()
    
    def authenticate(self) -> bool:
        """Authenticate with GitHub API"""
        self.api_token = self.config.get_credential("token")
        if not self.api_token:
            print("Error: GitHub token not found. Use 'mcp config github --token YOUR_TOKEN'")
            return False
        
        self.session.headers.update({
            "Authorization": f"token {self.api_token}",
            "Accept": "application/vnd.github.v3+json"
        })
        return True
    
    def test_connection(self) -> bool:
        """Test connection to GitHub API"""
        try:
            response = self.session.get(f"{self.base_url}/user")
            return response.status_code == 200
        except Exception as e:
            print(f"Error testing GitHub connection: {e}")
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """Get GitHub service status"""
        try:
            response = self.session.get(f"{self.base_url}/user")
            if response.status_code == 200:
                user_data = response.json()
                return {
                    "status": "connected",
                    "user": user_data.get("login"),
                    "mode": self.config.mode.value
                }
        except Exception as e:
            return {"status": "error", "message": str(e)}
        
        return {"status": "disconnected"}
    
    def list_repositories(self, visibility: str = "all") -> List[Dict[str, Any]]:
        """List user repositories"""
        try:
            response = self.session.get(
                f"{self.base_url}/user/repos",
                params={"visibility": visibility, "per_page": 100}
            )
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error listing repositories: {response.status_code}")
                return []
        except Exception as e:
            print(f"Error listing repositories: {e}")
            return []
    
    def get_repository(self, owner: str, repo: str) -> Optional[Dict[str, Any]]:
        """Get repository details"""
        try:
            response = self.session.get(f"{self.base_url}/repos/{owner}/{repo}")
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error getting repository: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error getting repository: {e}")
            return None
    
    def create_repository(self, name: str, description: str = "", private: bool = False) -> Optional[Dict[str, Any]]:
        """Create a new repository"""
        if self.config.is_sandbox():
            print("⚠️  Running in SANDBOX mode - repository creation simulated")
            return {
                "name": name,
                "description": description,
                "private": private,
                "mode": "sandbox",
                "simulated": True
            }
        
        try:
            response = self.session.post(
                f"{self.base_url}/user/repos",
                json={
                    "name": name,
                    "description": description,
                    "private": private
                }
            )
            if response.status_code == 201:
                return response.json()
            else:
                print(f"Error creating repository: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Error creating repository: {e}")
            return None
    
    def list_branches(self, owner: str, repo: str) -> List[str]:
        """List repository branches"""
        try:
            response = self.session.get(f"{self.base_url}/repos/{owner}/{repo}/branches")
            if response.status_code == 200:
                return [branch["name"] for branch in response.json()]
            else:
                print(f"Error listing branches: {response.status_code}")
                return []
        except Exception as e:
            print(f"Error listing branches: {e}")
            return []
    
    def create_issue(self, owner: str, repo: str, title: str, body: str = "") -> Optional[Dict[str, Any]]:
        """Create a new issue"""
        if self.config.is_sandbox():
            print("⚠️  Running in SANDBOX mode - issue creation simulated")
            return {
                "title": title,
                "body": body,
                "mode": "sandbox",
                "simulated": True
            }
        
        try:
            response = self.session.post(
                f"{self.base_url}/repos/{owner}/{repo}/issues",
                json={"title": title, "body": body}
            )
            if response.status_code == 201:
                return response.json()
            else:
                print(f"Error creating issue: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error creating issue: {e}")
            return None
