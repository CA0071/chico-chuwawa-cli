"""
Desktop App Connection Framework
Connect to various AI desktop applications
"""

from typing import Dict, Optional, Any
from abc import ABC, abstractmethod
import requests
import json


class DesktopApp(ABC):
    """Base class for desktop app connections"""
    
    def __init__(self, name: str, config: Optional[Dict] = None):
        self.name = name
        self.config = config or {}
        self.connected = False
    
    @abstractmethod
    def connect(self) -> bool:
        """Connect to the desktop app"""
        pass
    
    @abstractmethod
    def send_message(self, message: str) -> str:
        """Send a message to the app"""
        pass
    
    @abstractmethod
    def read_response(self) -> str:
        """Read response from the app"""
        pass


class ManusAI(DesktopApp):
    """Manus AI desktop app integration"""
    
    def __init__(self, config: Optional[Dict] = None):
        super().__init__("Manus AI", config)
        self.api_url = self.config.get('api_url', 'http://localhost:5001')
    
    def connect(self) -> bool:
        """Connect to Manus AI"""
        try:
            response = requests.get(f"{self.api_url}/health", timeout=2)
            self.connected = response.status_code == 200
            return self.connected
        except requests.RequestException:
            return False
    
    def send_message(self, message: str) -> str:
        """Send message to Manus AI"""
        if not self.connected:
            return "Not connected to Manus AI"
        
        try:
            response = requests.post(
                f"{self.api_url}/chat",
                json={'message': message},
                timeout=30
            )
            return response.json().get('response', '')
        except Exception as e:
            return f"Error: {str(e)}"
    
    def read_response(self) -> str:
        """Read latest response"""
        # Implementation depends on Manus AI API
        return ""


class DeepSeekApp(DesktopApp):
    """DeepSeek desktop app integration"""
    
    def __init__(self, config: Optional[Dict] = None):
        super().__init__("DeepSeek", config)
        self.api_url = self.config.get('api_url', 'http://localhost:5002')
    
    def connect(self) -> bool:
        """Connect to DeepSeek"""
        try:
            response = requests.get(f"{self.api_url}/health", timeout=2)
            self.connected = response.status_code == 200
            return self.connected
        except requests.RequestException:
            return False
    
    def send_message(self, message: str) -> str:
        """Send message to DeepSeek"""
        if not self.connected:
            return "Not connected to DeepSeek"
        
        try:
            response = requests.post(
                f"{self.api_url}/chat",
                json={'message': message},
                timeout=30
            )
            return response.json().get('response', '')
        except Exception as e:
            return f"Error: {str(e)}"
    
    def read_response(self) -> str:
        """Read latest response"""
        return ""


class ClaudeApp(DesktopApp):
    """Claude AI desktop app integration"""
    
    def __init__(self, config: Optional[Dict] = None):
        super().__init__("Claude AI", config)
        self.api_url = self.config.get('api_url', 'http://localhost:5003')
    
    def connect(self) -> bool:
        """Connect to Claude"""
        try:
            response = requests.get(f"{self.api_url}/health", timeout=2)
            self.connected = response.status_code == 200
            return self.connected
        except requests.RequestException:
            return False
    
    def send_message(self, message: str) -> str:
        """Send message to Claude"""
        if not self.connected:
            return "Not connected to Claude AI"
        
        try:
            response = requests.post(
                f"{self.api_url}/chat",
                json={'message': message},
                timeout=30
            )
            return response.json().get('response', '')
        except Exception as e:
            return f"Error: {str(e)}"
    
    def read_response(self) -> str:
        """Read latest response"""
        return ""


class ChatGPTApp(DesktopApp):
    """ChatGPT desktop app integration"""
    
    def __init__(self, config: Optional[Dict] = None):
        super().__init__("ChatGPT", config)
        self.api_url = self.config.get('api_url', 'http://localhost:5004')
    
    def connect(self) -> bool:
        """Connect to ChatGPT"""
        try:
            response = requests.get(f"{self.api_url}/health", timeout=2)
            self.connected = response.status_code == 200
            return self.connected
        except requests.RequestException:
            return False
    
    def send_message(self, message: str) -> str:
        """Send message to ChatGPT"""
        if not self.connected:
            return "Not connected to ChatGPT"
        
        try:
            response = requests.post(
                f"{self.api_url}/chat",
                json={'message': message},
                timeout=30
            )
            return response.json().get('response', '')
        except Exception as e:
            return f"Error: {str(e)}"
    
    def read_response(self) -> str:
        """Read latest response"""
        return ""


class DesktopAppManager:
    """Manage multiple desktop app connections"""
    
    def __init__(self):
        self.apps: Dict[str, DesktopApp] = {}
    
    def register_app(self, app: DesktopApp):
        """Register a desktop app"""
        self.apps[app.name] = app
    
    def get_app(self, name: str) -> Optional[DesktopApp]:
        """Get a registered app"""
        return self.apps.get(name)
    
    def list_apps(self) -> list:
        """List all registered apps"""
        return list(self.apps.keys())
    
    def connect_all(self) -> Dict[str, bool]:
        """Attempt to connect to all registered apps"""
        results = {}
        for name, app in self.apps.items():
            results[name] = app.connect()
        return results
    
    def send_to_all(self, message: str) -> Dict[str, str]:
        """Send message to all connected apps"""
        results = {}
        for name, app in self.apps.items():
            if app.connected:
                results[name] = app.send_message(message)
        return results
