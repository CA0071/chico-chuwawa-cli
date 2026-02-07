"""
Docker Integration
Provides Docker container and image management capabilities
"""

from typing import Dict, Any, List, Optional
import docker
from docker.errors import DockerException
from ..base import BaseIntegration, IntegrationStatus


class DockerIntegration(BaseIntegration):
    """Docker integration for container management"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__("Docker", config)
        self.client = None
    
    def connect(self) -> bool:
        """Connect to Docker daemon"""
        try:
            base_url = self.config.get('base_url', None)
            if base_url:
                self.client = docker.DockerClient(base_url=base_url)
            else:
                self.client = docker.from_env()
            
            # Test connection
            self.client.ping()
            self.status = IntegrationStatus.HEALTHY
            return True
        except DockerException as e:
            self.status = IntegrationStatus.UNHEALTHY
            return False
    
    def health_check(self) -> Dict[str, Any]:
        """Check Docker daemon health"""
        if not self.client:
            return {"status": "unhealthy", "message": "Not connected"}
        
        try:
            info = self.client.info()
            self.status = IntegrationStatus.HEALTHY
            return {
                "status": "healthy",
                "version": self.client.version(),
                "containers": info.get('Containers', 0),
                "images": info.get('Images', 0)
            }
        except Exception as e:
            self.status = IntegrationStatus.UNHEALTHY
            return {"status": "unhealthy", "error": str(e)}
    
    def get_info(self) -> Dict[str, Any]:
        """Get Docker system information"""
        if not self.client:
            return {"error": "Not connected"}
        
        try:
            return self.client.info()
        except Exception as e:
            return {"error": str(e)}
    
    def list_containers(self, all: bool = False) -> List[Dict[str, Any]]:
        """List Docker containers"""
        if not self.client:
            return []
        
        try:
            containers = self.client.containers.list(all=all)
            return [{
                'id': c.id[:12],
                'name': c.name,
                'image': c.image.tags[0] if c.image.tags else c.image.id[:12],
                'status': c.status,
                'created': c.attrs.get('Created', 'Unknown')
            } for c in containers]
        except Exception as e:
            return [{"error": str(e)}]
    
    def list_images(self) -> List[Dict[str, Any]]:
        """List Docker images"""
        if not self.client:
            return []
        
        try:
            images = self.client.images.list()
            return [{
                'id': img.id[:12],
                'tags': img.tags,
                'size': img.attrs.get('Size', 0) / (1024 * 1024),  # Convert to MB
                'created': img.attrs.get('Created', 'Unknown')
            } for img in images]
        except Exception as e:
            return [{"error": str(e)}]
    
    def get_container_logs(self, container_id: str, tail: int = 100) -> str:
        """Get logs from a container"""
        if not self.client:
            return "Not connected to Docker"
        
        try:
            container = self.client.containers.get(container_id)
            logs = container.logs(tail=tail).decode('utf-8')
            return logs
        except Exception as e:
            return f"Error: {str(e)}"
    
    def get_container_stats(self, container_id: str) -> Dict[str, Any]:
        """Get stats from a container"""
        if not self.client:
            return {"error": "Not connected"}
        
        try:
            container = self.client.containers.get(container_id)
            stats = container.stats(stream=False)
            return stats
        except Exception as e:
            return {"error": str(e)}
