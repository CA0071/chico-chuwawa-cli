"""
Kubernetes Integration
Provides Kubernetes cluster management capabilities
"""

from typing import Dict, Any, List, Optional
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from ..base import BaseIntegration, IntegrationStatus


class KubernetesIntegration(BaseIntegration):
    """Kubernetes integration for cluster management"""
    
    def __init__(self, integration_config: Optional[Dict[str, Any]] = None):
        super().__init__("Kubernetes", integration_config)
        self.core_api = None
        self.apps_api = None
    
    def connect(self) -> bool:
        """Connect to Kubernetes cluster"""
        try:
            # Try to load config from default location or in-cluster config
            if self.config.get('kubeconfig_path'):
                config.load_kube_config(config_file=self.config['kubeconfig_path'])
            else:
                try:
                    config.load_kube_config()
                except Exception:
                    # If not in kubeconfig, try in-cluster config
                    config.load_incluster_config()
            
            self.core_api = client.CoreV1Api()
            self.apps_api = client.AppsV1Api()
            
            # Test connection
            self.core_api.get_api_resources()
            self.status = IntegrationStatus.HEALTHY
            return True
        except Exception as e:
            self.status = IntegrationStatus.UNHEALTHY
            return False
    
    def health_check(self) -> Dict[str, Any]:
        """Check Kubernetes cluster health"""
        if not self.core_api:
            return {"status": "unhealthy", "message": "Not connected"}
        
        try:
            # Check if we can list nodes
            nodes = self.core_api.list_node()
            ready_nodes = sum(1 for node in nodes.items 
                            if any(cond.type == "Ready" and cond.status == "True" 
                                   for cond in node.status.conditions))
            
            self.status = IntegrationStatus.HEALTHY
            return {
                "status": "healthy",
                "total_nodes": len(nodes.items),
                "ready_nodes": ready_nodes
            }
        except Exception as e:
            self.status = IntegrationStatus.UNHEALTHY
            return {"status": "unhealthy", "error": str(e)}
    
    def get_info(self) -> Dict[str, Any]:
        """Get Kubernetes cluster information"""
        if not self.core_api:
            return {"error": "Not connected"}
        
        try:
            version_api = client.VersionApi()
            version = version_api.get_code()
            
            nodes = self.core_api.list_node()
            namespaces = self.core_api.list_namespace()
            
            return {
                "version": f"{version.major}.{version.minor}",
                "nodes": len(nodes.items),
                "namespaces": len(namespaces.items)
            }
        except Exception as e:
            return {"error": str(e)}
    
    def list_pods(self, namespace: str = "default") -> List[Dict[str, Any]]:
        """List pods in a namespace"""
        if not self.core_api:
            return []
        
        try:
            pods = self.core_api.list_namespaced_pod(namespace)
            return [{
                'name': pod.metadata.name,
                'namespace': pod.metadata.namespace,
                'status': pod.status.phase,
                'node': pod.spec.node_name,
                'created': str(pod.metadata.creation_timestamp)
            } for pod in pods.items]
        except Exception as e:
            return [{"error": str(e)}]
    
    def list_deployments(self, namespace: str = "default") -> List[Dict[str, Any]]:
        """List deployments in a namespace"""
        if not self.apps_api:
            return []
        
        try:
            deployments = self.apps_api.list_namespaced_deployment(namespace)
            return [{
                'name': dep.metadata.name,
                'namespace': dep.metadata.namespace,
                'replicas': dep.status.replicas,
                'ready_replicas': dep.status.ready_replicas or 0,
                'created': str(dep.metadata.creation_timestamp)
            } for dep in deployments.items]
        except Exception as e:
            return [{"error": str(e)}]
    
    def list_services(self, namespace: str = "default") -> List[Dict[str, Any]]:
        """List services in a namespace"""
        if not self.core_api:
            return []
        
        try:
            services = self.core_api.list_namespaced_service(namespace)
            return [{
                'name': svc.metadata.name,
                'namespace': svc.metadata.namespace,
                'type': svc.spec.type,
                'cluster_ip': svc.spec.cluster_ip,
                'ports': [f"{p.port}/{p.protocol}" for p in svc.spec.ports] if svc.spec.ports else []
            } for svc in services.items]
        except Exception as e:
            return [{"error": str(e)}]
    
    def get_pod_logs(self, pod_name: str, namespace: str = "default", tail_lines: int = 100) -> str:
        """Get logs from a pod"""
        if not self.core_api:
            return "Not connected to Kubernetes"
        
        try:
            logs = self.core_api.read_namespaced_pod_log(
                name=pod_name,
                namespace=namespace,
                tail_lines=tail_lines
            )
            return logs
        except Exception as e:
            return f"Error: {str(e)}"
