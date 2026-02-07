"""
Zoho CRM MCP Server Integration
Provides Zoho CRM API access for customer relationship management
"""

import requests
from typing import Dict, Any, List, Optional
from .base import BaseMCPServer, MCPServerConfig


class ZohoCRMMCPServer(BaseMCPServer):
    """MCP Server for Zoho CRM integration"""
    
    def __init__(self, config: MCPServerConfig):
        super().__init__(config)
        self.access_token = None
        # Base URL changes based on sandbox/production
        if config.is_sandbox():
            self.base_url = "https://sandbox.zohoapis.com/crm/v3"
        else:
            self.base_url = "https://www.zohoapis.com/crm/v3"
        self.session = requests.Session()
    
    def authenticate(self) -> bool:
        """Authenticate with Zoho CRM API"""
        self.access_token = self.config.get_credential("access_token")
        if not self.access_token:
            print("Error: Zoho CRM access token not found. Use 'mcp config zoho-crm --access-token YOUR_TOKEN'")
            return False
        
        self.session.headers.update({
            "Authorization": f"Zoho-oauthtoken {self.access_token}",
            "Content-Type": "application/json"
        })
        return True
    
    def test_connection(self) -> bool:
        """Test connection to Zoho CRM API"""
        try:
            response = self.session.get(f"{self.base_url}/users?type=CurrentUser")
            return response.status_code == 200
        except Exception as e:
            print(f"Error testing Zoho CRM connection: {e}")
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """Get Zoho CRM service status"""
        try:
            response = self.session.get(f"{self.base_url}/users?type=CurrentUser")
            if response.status_code == 200:
                data = response.json()
                users = data.get("users", [])
                if users:
                    user = users[0]
                    return {
                        "status": "connected",
                        "user": user.get("full_name"),
                        "email": user.get("email"),
                        "mode": self.config.mode.value
                    }
        except Exception as e:
            return {"status": "error", "message": str(e)}
        
        return {"status": "disconnected"}
    
    def list_leads(self, page: int = 1, per_page: int = 200) -> List[Dict[str, Any]]:
        """List leads from CRM"""
        try:
            response = self.session.get(
                f"{self.base_url}/Leads",
                params={"page": page, "per_page": per_page}
            )
            if response.status_code == 200:
                data = response.json()
                return data.get("data", [])
            else:
                print(f"Error listing leads: {response.status_code}")
                return []
        except Exception as e:
            print(f"Error listing leads: {e}")
            return []
    
    def create_lead(self, first_name: str, last_name: str, email: str, company: str) -> Optional[Dict[str, Any]]:
        """Create a new lead"""
        if self.config.is_sandbox():
            print("⚠️  Running in SANDBOX mode - using Zoho CRM Sandbox")
        
        try:
            lead_data = {
                "data": [
                    {
                        "First_Name": first_name,
                        "Last_Name": last_name,
                        "Email": email,
                        "Company": company
                    }
                ]
            }
            response = self.session.post(f"{self.base_url}/Leads", json=lead_data)
            if response.status_code in [200, 201]:
                return response.json()
            else:
                print(f"Error creating lead: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Error creating lead: {e}")
            return None
    
    def get_lead(self, lead_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific lead"""
        try:
            response = self.session.get(f"{self.base_url}/Leads/{lead_id}")
            if response.status_code == 200:
                data = response.json()
                leads = data.get("data", [])
                return leads[0] if leads else None
            else:
                print(f"Error getting lead: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error getting lead: {e}")
            return None
    
    def update_lead(self, lead_id: str, updates: Dict[str, Any]) -> bool:
        """Update a lead"""
        if self.config.is_sandbox():
            print("⚠️  Running in SANDBOX mode - using Zoho CRM Sandbox")
        
        try:
            lead_data = {"data": [updates]}
            response = self.session.put(f"{self.base_url}/Leads/{lead_id}", json=lead_data)
            return response.status_code == 200
        except Exception as e:
            print(f"Error updating lead: {e}")
            return False
    
    def list_contacts(self, page: int = 1, per_page: int = 200) -> List[Dict[str, Any]]:
        """List contacts from CRM"""
        try:
            response = self.session.get(
                f"{self.base_url}/Contacts",
                params={"page": page, "per_page": per_page}
            )
            if response.status_code == 200:
                data = response.json()
                return data.get("data", [])
            else:
                print(f"Error listing contacts: {response.status_code}")
                return []
        except Exception as e:
            print(f"Error listing contacts: {e}")
            return []
    
    def create_task(self, subject: str, due_date: str, related_to: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Create a task"""
        if self.config.is_sandbox():
            print("⚠️  Running in SANDBOX mode - using Zoho CRM Sandbox")
        
        try:
            task_data = {
                "data": [
                    {
                        "Subject": subject,
                        "Due_Date": due_date,
                        "Status": "Not Started"
                    }
                ]
            }
            if related_to:
                task_data["data"][0]["$se_module"] = "Leads"
                task_data["data"][0]["What_Id"] = related_to
            
            response = self.session.post(f"{self.base_url}/Tasks", json=task_data)
            if response.status_code in [200, 201]:
                return response.json()
            else:
                print(f"Error creating task: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error creating task: {e}")
            return None
