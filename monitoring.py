"""
Real-Time Monitoring Module
Provides live monitoring of integrations and services
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import time
from rich.live import Live
from rich.table import Table
from rich.console import Console
from rich import box
from threading import Thread


class IntegrationMonitor:
    """Real-time monitoring for integrations"""
    
    def __init__(self, hub):
        self.hub = hub
        self.console = Console()
        self.monitoring = False
        self.metrics = {}
    
    def start_monitoring(self, interval: int = 5):
        """Start monitoring integrations"""
        self.monitoring = True
        
        with Live(self._generate_status_table(), refresh_per_second=1, console=self.console) as live:
            while self.monitoring:
                live.update(self._generate_status_table())
                time.sleep(interval)
    
    def stop_monitoring(self):
        """Stop monitoring"""
        self.monitoring = False
    
    def _generate_status_table(self) -> Table:
        """Generate real-time status table"""
        table = Table(
            title=f"Integration Monitor - {datetime.now().strftime('%H:%M:%S')}",
            box=box.ROUNDED
        )
        
        table.add_column("Integration", style="cyan", no_wrap=True)
        table.add_column("Status", style="yellow")
        table.add_column("Health", style="green")
        table.add_column("Last Check", style="white")
        
        health_results = self.hub.health_check_all()
        
        for name, health in health_results.items():
            status = health.get('status', 'unknown')
            status_emoji = {
                'healthy': '🟢',
                'unhealthy': '🔴',
                'degraded': '🟡',
                'unknown': '⚪'
            }.get(status, '⚪')
            
            table.add_row(
                name.upper(),
                status_emoji,
                status.upper(),
                datetime.now().strftime('%H:%M:%S')
            )
        
        return table
    
    def collect_metrics(self) -> Dict[str, Any]:
        """Collect metrics from all integrations"""
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'integrations': {}
        }
        
        for name, integration in self.hub.integrations.items():
            try:
                health = integration.health_check()
                metrics['integrations'][name] = {
                    'status': integration.status.value,
                    'healthy': integration.is_healthy(),
                    'health_data': health
                }
            except Exception as e:
                metrics['integrations'][name] = {
                    'error': str(e)
                }
        
        self.metrics[datetime.now().isoformat()] = metrics
        return metrics
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get summary of collected metrics"""
        if not self.metrics:
            return {'message': 'No metrics collected yet'}
        
        total_checks = len(self.metrics)
        
        # Calculate uptime percentage for each integration
        uptime = {}
        for timestamp, metrics in self.metrics.items():
            for int_name, int_metrics in metrics['integrations'].items():
                if int_name not in uptime:
                    uptime[int_name] = {'healthy': 0, 'total': 0}
                
                uptime[int_name]['total'] += 1
                if int_metrics.get('healthy'):
                    uptime[int_name]['healthy'] += 1
        
        # Calculate percentages
        uptime_percentages = {}
        for int_name, counts in uptime.items():
            uptime_percentages[int_name] = (counts['healthy'] / counts['total']) * 100
        
        return {
            'total_checks': total_checks,
            'uptime_percentages': uptime_percentages,
            'first_check': list(self.metrics.keys())[0],
            'last_check': list(self.metrics.keys())[-1]
        }


class ServiceMonitor:
    """Monitor specific services (Docker containers, K8s pods, etc.)"""
    
    def __init__(self, integration, service_type: str):
        self.integration = integration
        self.service_type = service_type
        self.console = Console()
    
    def monitor_docker_containers(self, interval: int = 5):
        """Monitor Docker containers in real-time"""
        with Live(self._generate_docker_table(), refresh_per_second=1, console=self.console) as live:
            while True:
                try:
                    live.update(self._generate_docker_table())
                    time.sleep(interval)
                except KeyboardInterrupt:
                    break
    
    def _generate_docker_table(self) -> Table:
        """Generate Docker containers table"""
        table = Table(
            title=f"Docker Containers - {datetime.now().strftime('%H:%M:%S')}",
            box=box.ROUNDED
        )
        
        table.add_column("ID", style="cyan")
        table.add_column("Name", style="yellow")
        table.add_column("Status", style="green")
        table.add_column("Image", style="white")
        
        try:
            containers = self.integration.list_containers(all=True)
            for container in containers:
                if 'error' not in container:
                    status_emoji = '🟢' if container['status'] == 'running' else '🔴'
                    table.add_row(
                        container['id'],
                        container['name'],
                        f"{status_emoji} {container['status']}",
                        container['image']
                    )
        except Exception as e:
            table.add_row("Error", str(e), "", "")
        
        return table
    
    def monitor_k8s_pods(self, namespace: str = 'default', interval: int = 5):
        """Monitor Kubernetes pods in real-time"""
        with Live(self._generate_k8s_table(namespace), refresh_per_second=1, console=self.console) as live:
            while True:
                try:
                    live.update(self._generate_k8s_table(namespace))
                    time.sleep(interval)
                except KeyboardInterrupt:
                    break
    
    def _generate_k8s_table(self, namespace: str) -> Table:
        """Generate Kubernetes pods table"""
        table = Table(
            title=f"Kubernetes Pods ({namespace}) - {datetime.now().strftime('%H:%M:%S')}",
            box=box.ROUNDED
        )
        
        table.add_column("Name", style="cyan")
        table.add_column("Status", style="yellow")
        table.add_column("Node", style="green")
        
        try:
            pods = self.integration.list_pods(namespace)
            for pod in pods:
                if 'error' not in pod:
                    status_emoji = {
                        'Running': '🟢',
                        'Pending': '🟡',
                        'Failed': '🔴',
                        'Unknown': '⚪'
                    }.get(pod['status'], '⚪')
                    
                    table.add_row(
                        pod['name'],
                        f"{status_emoji} {pod['status']}",
                        pod.get('node', 'N/A')
                    )
        except Exception as e:
            table.add_row("Error", str(e), "")
        
        return table


def start_background_monitor(hub, interval: int = 10):
    """Start background monitoring thread"""
    monitor = IntegrationMonitor(hub)
    
    def monitor_loop():
        while True:
            monitor.collect_metrics()
            time.sleep(interval)
    
    thread = Thread(target=monitor_loop, daemon=True)
    thread.start()
    
    return monitor
