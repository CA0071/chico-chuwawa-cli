"""
Zoho Invoice MCP Server Integration
Provides Zoho Invoice API access for invoice management
"""

import requests
from typing import Dict, Any, List, Optional
from .base import BaseMCPServer, MCPServerConfig


class ZohoInvoiceMCPServer(BaseMCPServer):
    """MCP Server for Zoho Invoice integration"""
    
    def __init__(self, config: MCPServerConfig):
        super().__init__(config)
        self.access_token = None
        self.organization_id = None
        self.base_url = "https://invoice.zoho.com/api/v3"
        self.session = requests.Session()
    
    def authenticate(self) -> bool:
        """Authenticate with Zoho Invoice API"""
        self.access_token = self.config.get_credential("access_token")
        self.organization_id = self.config.get_credential("organization_id")
        
        if not self.access_token:
            print("Error: Zoho Invoice access token not found. Use 'mcp config zoho-invoice --access-token YOUR_TOKEN --org-id YOUR_ORG_ID'")
            return False
        
        if not self.organization_id:
            print("Error: Zoho Invoice organization ID not found. Use 'mcp config zoho-invoice --access-token YOUR_TOKEN --org-id YOUR_ORG_ID'")
            return False
        
        self.session.headers.update({
            "Authorization": f"Zoho-oauthtoken {self.access_token}",
            "Content-Type": "application/json"
        })
        return True
    
    def test_connection(self) -> bool:
        """Test connection to Zoho Invoice API"""
        try:
            response = self.session.get(
                f"{self.base_url}/organizations",
                params={"organization_id": self.organization_id}
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Error testing Zoho Invoice connection: {e}")
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """Get Zoho Invoice service status"""
        try:
            response = self.session.get(
                f"{self.base_url}/organizations",
                params={"organization_id": self.organization_id}
            )
            if response.status_code == 200:
                return {
                    "status": "connected",
                    "organization_id": self.organization_id,
                    "mode": self.config.mode.value
                }
        except Exception as e:
            return {"status": "error", "message": str(e)}
        
        return {"status": "disconnected"}
    
    def list_invoices(self, status: Optional[str] = None, page: int = 1, per_page: int = 200) -> List[Dict[str, Any]]:
        """List invoices"""
        try:
            params = {
                "organization_id": self.organization_id,
                "page": page,
                "per_page": per_page
            }
            if status:
                params["status"] = status
            
            response = self.session.get(f"{self.base_url}/invoices", params=params)
            if response.status_code == 200:
                data = response.json()
                return data.get("invoices", [])
            else:
                print(f"Error listing invoices: {response.status_code}")
                return []
        except Exception as e:
            print(f"Error listing invoices: {e}")
            return []
    
    def get_invoice(self, invoice_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific invoice"""
        try:
            response = self.session.get(
                f"{self.base_url}/invoices/{invoice_id}",
                params={"organization_id": self.organization_id}
            )
            if response.status_code == 200:
                data = response.json()
                return data.get("invoice")
            else:
                print(f"Error getting invoice: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error getting invoice: {e}")
            return None
    
    def create_invoice(self, customer_id: str, line_items: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Create a new invoice"""
        if self.config.is_sandbox():
            print("⚠️  Running in SANDBOX mode - invoice creation simulated")
            return {
                "customer_id": customer_id,
                "line_items": line_items,
                "mode": "sandbox",
                "simulated": True
            }
        
        try:
            invoice_data = {
                "customer_id": customer_id,
                "line_items": line_items
            }
            response = self.session.post(
                f"{self.base_url}/invoices",
                params={"organization_id": self.organization_id},
                json=invoice_data
            )
            if response.status_code in [200, 201]:
                data = response.json()
                return data.get("invoice")
            else:
                print(f"Error creating invoice: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Error creating invoice: {e}")
            return None
    
    def update_invoice(self, invoice_id: str, updates: Dict[str, Any]) -> bool:
        """Update an invoice"""
        if self.config.is_sandbox():
            print("⚠️  Running in SANDBOX mode - invoice update simulated")
            return True
        
        try:
            response = self.session.put(
                f"{self.base_url}/invoices/{invoice_id}",
                params={"organization_id": self.organization_id},
                json=updates
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Error updating invoice: {e}")
            return False
    
    def list_customers(self, page: int = 1, per_page: int = 200) -> List[Dict[str, Any]]:
        """List customers"""
        try:
            params = {
                "organization_id": self.organization_id,
                "page": page,
                "per_page": per_page
            }
            response = self.session.get(f"{self.base_url}/contacts", params=params)
            if response.status_code == 200:
                data = response.json()
                return data.get("contacts", [])
            else:
                print(f"Error listing customers: {response.status_code}")
                return []
        except Exception as e:
            print(f"Error listing customers: {e}")
            return []
    
    def create_customer(self, contact_name: str, email: str, company_name: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Create a new customer"""
        if self.config.is_sandbox():
            print("⚠️  Running in SANDBOX mode - customer creation simulated")
            return {
                "contact_name": contact_name,
                "email": email,
                "mode": "sandbox"
            }
        
        try:
            customer_data = {
                "contact_name": contact_name,
                "email": email
            }
            if company_name:
                customer_data["company_name"] = company_name
            
            response = self.session.post(
                f"{self.base_url}/contacts",
                params={"organization_id": self.organization_id},
                json=customer_data
            )
            if response.status_code in [200, 201]:
                data = response.json()
                return data.get("contact")
            else:
                print(f"Error creating customer: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error creating customer: {e}")
            return None
