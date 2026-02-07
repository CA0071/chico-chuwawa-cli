"""
Office 365 MCP Server Integration
Provides Office 365 Graph API access for email and collaboration
"""

import requests
from typing import Dict, Any, List, Optional
from .base import BaseMCPServer, MCPServerConfig


class Office365MCPServer(BaseMCPServer):
    """MCP Server for Office 365 integration"""
    
    def __init__(self, config: MCPServerConfig):
        super().__init__(config)
        self.access_token = None
        self.base_url = "https://graph.microsoft.com/v1.0"
        self.session = requests.Session()
    
    def authenticate(self) -> bool:
        """Authenticate with Office 365 Graph API"""
        self.access_token = self.config.get_credential("access_token")
        if not self.access_token:
            print("Error: Office 365 access token not found. Use 'mcp config office365 --access-token YOUR_TOKEN'")
            return False
        
        self.session.headers.update({
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        })
        return True
    
    def test_connection(self) -> bool:
        """Test connection to Office 365 Graph API"""
        try:
            response = self.session.get(f"{self.base_url}/me")
            return response.status_code == 200
        except Exception as e:
            print(f"Error testing Office 365 connection: {e}")
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """Get Office 365 service status"""
        try:
            response = self.session.get(f"{self.base_url}/me")
            if response.status_code == 200:
                user_data = response.json()
                return {
                    "status": "connected",
                    "user": user_data.get("displayName"),
                    "email": user_data.get("mail") or user_data.get("userPrincipalName"),
                    "mode": self.config.mode.value
                }
        except Exception as e:
            return {"status": "error", "message": str(e)}
        
        return {"status": "disconnected"}
    
    def list_emails(self, folder: str = "inbox", top: int = 10) -> List[Dict[str, Any]]:
        """List emails from a folder"""
        try:
            response = self.session.get(
                f"{self.base_url}/me/mailFolders/{folder}/messages",
                params={"$top": top, "$select": "subject,from,receivedDateTime,isRead"}
            )
            if response.status_code == 200:
                data = response.json()
                return data.get("value", [])
            else:
                print(f"Error listing emails: {response.status_code}")
                return []
        except Exception as e:
            print(f"Error listing emails: {e}")
            return []
    
    def send_email(self, to: str, subject: str, body: str, body_type: str = "Text") -> bool:
        """Send an email"""
        if self.config.is_sandbox():
            print("⚠️  Running in SANDBOX mode - email sending simulated")
            print(f"   To: {to}")
            print(f"   Subject: {subject}")
            return True
        
        try:
            message = {
                "message": {
                    "subject": subject,
                    "body": {
                        "contentType": body_type,
                        "content": body
                    },
                    "toRecipients": [
                        {
                            "emailAddress": {
                                "address": to
                            }
                        }
                    ]
                }
            }
            response = self.session.post(f"{self.base_url}/me/sendMail", json=message)
            return response.status_code == 202
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    def get_calendar_events(self, top: int = 10) -> List[Dict[str, Any]]:
        """Get calendar events"""
        try:
            response = self.session.get(
                f"{self.base_url}/me/calendar/events",
                params={"$top": top, "$select": "subject,start,end,location"}
            )
            if response.status_code == 200:
                data = response.json()
                return data.get("value", [])
            else:
                print(f"Error getting calendar events: {response.status_code}")
                return []
        except Exception as e:
            print(f"Error getting calendar events: {e}")
            return []
    
    def create_calendar_event(self, subject: str, start: str, end: str, location: str = "") -> Optional[Dict[str, Any]]:
        """Create a calendar event"""
        if self.config.is_sandbox():
            print("⚠️  Running in SANDBOX mode - event creation simulated")
            return {
                "subject": subject,
                "start": start,
                "end": end,
                "mode": "sandbox"
            }
        
        try:
            event = {
                "subject": subject,
                "start": {
                    "dateTime": start,
                    "timeZone": "UTC"
                },
                "end": {
                    "dateTime": end,
                    "timeZone": "UTC"
                },
                "location": {
                    "displayName": location
                }
            }
            response = self.session.post(f"{self.base_url}/me/calendar/events", json=event)
            if response.status_code == 201:
                return response.json()
            else:
                print(f"Error creating event: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error creating event: {e}")
            return None
