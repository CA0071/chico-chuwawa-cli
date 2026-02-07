"""
Base MCP Server class and configuration
Provides common functionality for all MCP server integrations
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from enum import Enum


class EnvironmentMode(Enum):
    """Environment modes for MCP servers"""
    SANDBOX = "sandbox"
    PRODUCTION = "production"


class MCPServerConfig:
    """Configuration for MCP servers"""
    
    def __init__(self, name: str, mode: EnvironmentMode = EnvironmentMode.SANDBOX):
        self.name = name
        self.mode = mode
        self.credentials: Dict[str, str] = {}
        self.settings: Dict[str, Any] = {}
    
    def set_credential(self, key: str, value: str):
        """Set a credential value"""
        self.credentials[key] = value
    
    def get_credential(self, key: str) -> Optional[str]:
        """Get a credential value"""
        return self.credentials.get(key)
    
    def set_setting(self, key: str, value: Any):
        """Set a setting value"""
        self.settings[key] = value
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a setting value"""
        return self.settings.get(key, default)
    
    def is_sandbox(self) -> bool:
        """Check if running in sandbox mode"""
        return self.mode == EnvironmentMode.SANDBOX
    
    def is_production(self) -> bool:
        """Check if running in production mode"""
        return self.mode == EnvironmentMode.PRODUCTION


class BaseMCPServer(ABC):
    """Base class for all MCP server integrations"""
    
    def __init__(self, config: MCPServerConfig):
        self.config = config
        self._initialized = False
    
    @abstractmethod
    def authenticate(self) -> bool:
        """
        Authenticate with the service
        Returns True if authentication is successful
        """
        pass
    
    @abstractmethod
    def test_connection(self) -> bool:
        """
        Test the connection to the service
        Returns True if connection is successful
        """
        pass
    
    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """
        Get the current status of the service
        Returns a dictionary with status information
        """
        pass
    
    def initialize(self) -> bool:
        """
        Initialize the MCP server
        Returns True if initialization is successful
        """
        if self._initialized:
            return True
        
        if not self.authenticate():
            return False
        
        if not self.test_connection():
            return False
        
        self._initialized = True
        return True
    
    def is_initialized(self) -> bool:
        """Check if the server is initialized"""
        return self._initialized
    
    def get_environment_info(self) -> Dict[str, str]:
        """Get information about the current environment"""
        return {
            "name": self.config.name,
            "mode": self.config.mode.value,
            "initialized": str(self._initialized)
        }
