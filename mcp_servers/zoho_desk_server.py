"""
Zoho Desk MCP Server Integration
Provides Zoho Desk API access for support ticket management
"""

import requests
from typing import Dict, Any, List, Optional
from .base import BaseMCPServer, MCPServerConfig


class ZohoDeskMCPServer(BaseMCPServer):
    """MCP Server for Zoho Desk integration"""
    
    def __init__(self, config: MCPServerConfig):
        super().__init__(config)
        self.access_token = None
        self.org_id = None
        # Base URL changes based on data center
        self.base_url = "https://desk.zoho.com/api/v1"
        self.session = requests.Session()
    
    def authenticate(self) -> bool:
        """Authenticate with Zoho Desk API"""
        self.access_token = self.config.get_credential("access_token")
        self.org_id = self.config.get_credential("org_id")
        
        if not self.access_token:
            print("Error: Zoho Desk access token not found. Use 'mcp config zoho-desk --access-token YOUR_TOKEN --org-id YOUR_ORG_ID'")
            return False
        
        if not self.org_id:
            print("Error: Zoho Desk org ID not found. Use 'mcp config zoho-desk --access-token YOUR_TOKEN --org-id YOUR_ORG_ID'")
            return False
        
        self.session.headers.update({
            "Authorization": f"Zoho-oauthtoken {self.access_token}",
            "orgId": self.org_id,
            "Content-Type": "application/json"
        })
        return True
    
    def test_connection(self) -> bool:
        """Test connection to Zoho Desk API"""
        try:
            response = self.session.get(f"{self.base_url}/departments")
            return response.status_code == 200
        except Exception as e:
            print(f"Error testing Zoho Desk connection: {e}")
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """Get Zoho Desk service status"""
        try:
            response = self.session.get(f"{self.base_url}/departments")
            if response.status_code == 200:
                return {
                    "status": "connected",
                    "org_id": self.org_id,
                    "mode": self.config.mode.value
                }
        except Exception as e:
            return {"status": "error", "message": str(e)}
        
        return {"status": "disconnected"}
    
    def list_tickets(self, status: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """List support tickets"""
        try:
            params = {"limit": limit}
            if status:
                params["status"] = status
            
            response = self.session.get(f"{self.base_url}/tickets", params=params)
            if response.status_code == 200:
                data = response.json()
                return data.get("data", [])
            else:
                print(f"Error listing tickets: {response.status_code}")
                return []
        except Exception as e:
            print(f"Error listing tickets: {e}")
            return []
    
    def get_ticket(self, ticket_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific ticket"""
        try:
            response = self.session.get(f"{self.base_url}/tickets/{ticket_id}")
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error getting ticket: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error getting ticket: {e}")
            return None
    
    def create_ticket(self, subject: str, description: str, contact_id: str, department_id: str) -> Optional[Dict[str, Any]]:
        """Create a new support ticket"""
        if self.config.is_sandbox():
            print("⚠️  Running in SANDBOX mode - ticket creation simulated")
            return {
                "subject": subject,
                "description": description,
                "mode": "sandbox",
                "simulated": True
            }
        
        try:
            ticket_data = {
                "subject": subject,
                "description": description,
                "contactId": contact_id,
                "departmentId": department_id,
                "status": "Open"
            }
            response = self.session.post(f"{self.base_url}/tickets", json=ticket_data)
            if response.status_code in [200, 201]:
                return response.json()
            else:
                print(f"Error creating ticket: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Error creating ticket: {e}")
            return None
    
    def update_ticket(self, ticket_id: str, updates: Dict[str, Any]) -> bool:
        """Update a ticket"""
        if self.config.is_sandbox():
            print("⚠️  Running in SANDBOX mode - ticket update simulated")
            return True
        
        try:
            response = self.session.patch(f"{self.base_url}/tickets/{ticket_id}", json=updates)
            return response.status_code == 200
        except Exception as e:
            print(f"Error updating ticket: {e}")
            return False
    
    def add_ticket_comment(self, ticket_id: str, comment: str, is_public: bool = False) -> Optional[Dict[str, Any]]:
        """Add a comment to a ticket"""
        if self.config.is_sandbox():
            print("⚠️  Running in SANDBOX mode - comment simulated")
            return {
                "comment": comment,
                "mode": "sandbox"
            }
        
        try:
            comment_data = {
                "content": comment,
                "isPublic": is_public
            }
            response = self.session.post(
                f"{self.base_url}/tickets/{ticket_id}/comments",
                json=comment_data
            )
            if response.status_code in [200, 201]:
                return response.json()
            else:
                print(f"Error adding comment: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error adding comment: {e}")
            return None
    
    def list_departments(self) -> List[Dict[str, Any]]:
        """List all departments"""
        try:
            response = self.session.get(f"{self.base_url}/departments")
            if response.status_code == 200:
                data = response.json()
                return data.get("data", [])
            else:
                print(f"Error listing departments: {response.status_code}")
                return []
        except Exception as e:
            print(f"Error listing departments: {e}")
            return []
