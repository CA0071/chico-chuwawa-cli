"""
Base Integration Framework
Provides abstract base class for all integrations
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from enum import Enum


class IntegrationStatus(Enum):
    """Status of an integration"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


class BaseIntegration(ABC):
    """Abstract base class for all integrations"""
    
    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        self.name = name
        self.config = config or {}
        self._status = IntegrationStatus.UNKNOWN
    
    @abstractmethod
    def connect(self) -> bool:
        """Establish connection to the integration"""
        pass
    
    @abstractmethod
    def health_check(self) -> Dict[str, Any]:
        """Check health of the integration"""
        pass
    
    @abstractmethod
    def get_info(self) -> Dict[str, Any]:
        """Get information about the integration"""
        pass
    
    @property
    def status(self) -> IntegrationStatus:
        """Get current status"""
        return self._status
    
    @status.setter
    def status(self, value: IntegrationStatus):
        """Set current status"""
        self._status = value
    
    def is_healthy(self) -> bool:
        """Check if integration is healthy"""
        return self._status == IntegrationStatus.HEALTHY
