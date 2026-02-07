#!/usr/bin/env python3
"""
Chico Chuwawa AI CLI - Enhanced Edition
A powerful command-line interface with rich TUI, integrations, and orchestration
"""

import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax
from rich.live import Live
from rich import box
import argparse
from typing import Optional, Dict, Any

# Import original CLI
from chico_cli import AICLI, APIConfig

# Import integrations
from chico_integrations.docker import DockerIntegration
from chico_integrations.kubernetes import KubernetesIntegration
from chico_integrations.npm import NpmIntegration
from chico_integrations.pypi import PyPIIntegration
from chico_integrations.cloud import AWSIntegration, GCPIntegration, AzureIntegration
from chico_integrations.mcp import MCPHub

# Initialize rich console
console = Console()


class EnhancedAICLI(AICLI):
    """Enhanced CLI with rich UI and integrations"""
    
    def __init__(self):
        super().__init__()
        self.hub = self._initialize_hub()
    
    def _initialize_hub(self) -> MCPHub:
        """Initialize MCP hub with integrations"""
        config_path = self.config.config_dir / 'integrations.json'
        hub = MCPHub(config_path)
        
        # Register available integrations
        hub.register_integration('docker', DockerIntegration())
        hub.register_integration('kubernetes', KubernetesIntegration())
        hub.register_integration('npm', NpmIntegration())
        hub.register_integration('pypi', PyPIIntegration())
        hub.register_integration('aws', AWSIntegration())
        hub.register_integration('gcp', GCPIntegration())
        hub.register_integration('azure', AzureIntegration())
        
        return hub
    
    def show_welcome(self):
        """Display welcome panel"""
        welcome_text = """
[bold cyan]🐕 Chico Chuwawa AI CLI - Enhanced Edition[/bold cyan]
[yellow]Built by: Max van Heerden[/yellow]
[green]Version: 2.1.0[/green]

[white]Features:[/white]
• Rich Terminal UI with colors and tables
• Multi-Provider AI (OpenRouter, Ollama)
• Docker & Kubernetes Integration
• npm & PyPI Package Management
• AWS, GCP, Azure Cloud Support
• MCP Orchestration Hub
        """
        console.print(Panel(welcome_text, box=box.DOUBLE, border_style="cyan"))
    
    def list_providers_rich(self):
        """List providers with rich formatting"""
        table = Table(title="Available AI Providers", box=box.ROUNDED)
        table.add_column("Provider", style="cyan", no_wrap=True)
        table.add_column("Status", style="green")
        table.add_column("Default Model", style="yellow")
        
        config = self.config.load_config()
        active = config.get('active_provider', 'openrouter')
        
        for key, info in self.PROVIDERS.items():
            status = "✓ Active" if key == active else ""
            configured = "✓ Configured" if key in config else "✗ Not configured"
            status_full = f"{configured} {status}"
            
            table.add_row(
                info['name'],
                status_full,
                info['default_model']
            )
        
        console.print(table)
    
    def list_models_rich(self, provider: Optional[str] = None):
        """List models with rich formatting"""
        self.initialize_client(provider)
        
        provider_info = self.PROVIDERS[self.current_provider]
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task(f"Fetching models from {provider_info['name']}...", total=None)
            
            try:
                models = []
                if self.current_provider == 'ollama':
                    import requests
                    response = requests.get(
                        f"{provider_info['base_url']}/api/tags",
                        timeout=10
                    )
                    if response.status_code == 200:
                        models_data = response.json().get('models', [])
                        models = [m.get('name', 'unknown') for m in models_data]
                else:
                    models_response = self.client.models.list()
                    models = [model.id for model in models_response.data[:20]]  # Limit to 20
                
                progress.update(task, completed=True)
            except Exception:
                models = [provider_info['default_model']]
        
        table = Table(title=f"Models for {provider_info['name']}", box=box.ROUNDED)
        table.add_column("Model ID", style="cyan")
        
        for model in models:
            table.add_row(model)
        
        console.print(table)
    
    def list_integrations_rich(self):
        """List all integrations with rich formatting"""
        health_results = self.hub.health_check_all()
        
        table = Table(title="Integration Status", box=box.ROUNDED)
        table.add_column("Integration", style="cyan", no_wrap=True)
        table.add_column("Status", style="yellow")
        table.add_column("Details", style="white")
        
        for name, health in health_results.items():
            status = health.get('status', 'unknown')
            status_emoji = {
                'healthy': '✓',
                'unhealthy': '✗',
                'degraded': '⚠',
                'unknown': '?'
            }.get(status, '?')
            
            details = health.get('message', '')
            if 'error' in health:
                details = f"Error: {health['error'][:50]}"
            
            table.add_row(
                name.upper(),
                f"{status_emoji} {status}",
                details
            )
        
        console.print(table)
    
    def show_hub_status(self):
        """Show MCP hub status"""
        summary = self.hub.get_status_summary()
        
        status_text = f"""
[bold]Total Integrations:[/bold] {summary['total']}
[green]Healthy:[/green] {summary['statuses']['healthy']}
[yellow]Degraded:[/yellow] {summary['statuses']['degraded']}
[red]Unhealthy:[/red] {summary['statuses']['unhealthy']}
[dim]Unknown:[/dim] {summary['statuses']['unknown']}

[bold]Overall Health:[/bold] {summary['overall_health'].upper()}
        """
        
        console.print(Panel(status_text, title="MCP Hub Status", border_style="cyan"))


def main():
    """Enhanced main entry point"""
    parser = argparse.ArgumentParser(
        description='Chico Chuwawa AI CLI - Enhanced Edition',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Show welcome screen
  python chico-cli-enhanced.py welcome
  
  # List providers (rich UI)
  python chico-cli-enhanced.py providers
  
  # List integrations
  python chico-cli-enhanced.py integrations
  
  # Show MCP hub status
  python chico-cli-enhanced.py hub-status
  
  # Docker integration
  python chico-cli-enhanced.py docker containers
  python chico-cli-enhanced.py docker images
  
  # Kubernetes integration
  python chico-cli-enhanced.py k8s pods
  python chico-cli-enhanced.py k8s deployments
  
  # npm integration
  python chico-cli-enhanced.py npm search react
  python chico-cli-enhanced.py npm info react
  
  # PyPI integration
  python chico-cli-enhanced.py pypi info requests
  
  # Regular chat commands still work
  python chico-cli-enhanced.py chat "Hello!"
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Welcome command
    subparsers.add_parser('welcome', help='Show welcome screen')
    
    # Enhanced provider commands
    subparsers.add_parser('providers', help='List AI providers (rich UI)')
    
    # Config command (from original)
    config_parser = subparsers.add_parser('config', help='Configure API credentials')
    config_parser.add_argument('provider', choices=['openrouter', 'ollama'], help='Provider to configure')
    config_parser.add_argument('--api-key', required=True, help='API key')
    config_parser.add_argument('--default-model', help='Default model to use')
    
    # Switch command
    switch_parser = subparsers.add_parser('switch', help='Switch active provider')
    switch_parser.add_argument('provider', choices=['openrouter', 'ollama'], help='Provider to switch to')
    
    # Models command
    models_parser = subparsers.add_parser('models', help='List available models (rich UI)')
    models_parser.add_argument('--provider', choices=['openrouter', 'ollama'], help='Provider to list models from')
    
    # Chat command
    chat_parser = subparsers.add_parser('chat', help='Send a chat message')
    chat_parser.add_argument('message', help='Message to send')
    chat_parser.add_argument('--model', help='Model to use')
    chat_parser.add_argument('--provider', choices=['openrouter', 'ollama'], help='Provider to use')
    chat_parser.add_argument('--no-stream', action='store_true', help='Disable streaming')
    
    # Interactive command
    interactive_parser = subparsers.add_parser('interactive', help='Start interactive chat')
    interactive_parser.add_argument('--model', help='Model to use')
    interactive_parser.add_argument('--provider', choices=['openrouter', 'ollama'], help='Provider to use')
    
    # Integration commands
    subparsers.add_parser('integrations', help='List all integrations')
    subparsers.add_parser('hub-status', help='Show MCP hub status')
    
    # Docker commands
    docker_parser = subparsers.add_parser('docker', help='Docker integration')
    docker_subparsers = docker_parser.add_subparsers(dest='docker_command')
    docker_subparsers.add_parser('containers', help='List containers')
    docker_subparsers.add_parser('images', help='List images')
    docker_logs = docker_subparsers.add_parser('logs', help='Get container logs')
    docker_logs.add_argument('container_id', help='Container ID')
    
    # Kubernetes commands
    k8s_parser = subparsers.add_parser('k8s', help='Kubernetes integration')
    k8s_subparsers = k8s_parser.add_subparsers(dest='k8s_command')
    k8s_pods = k8s_subparsers.add_parser('pods', help='List pods')
    k8s_pods.add_argument('--namespace', default='default', help='Namespace')
    k8s_deployments = k8s_subparsers.add_parser('deployments', help='List deployments')
    k8s_deployments.add_argument('--namespace', default='default', help='Namespace')
    k8s_services = k8s_subparsers.add_parser('services', help='List services')
    k8s_services.add_argument('--namespace', default='default', help='Namespace')
    
    # npm commands
    npm_parser = subparsers.add_parser('npm', help='npm registry integration')
    npm_subparsers = npm_parser.add_subparsers(dest='npm_command')
    npm_search = npm_subparsers.add_parser('search', help='Search packages')
    npm_search.add_argument('query', help='Search query')
    npm_info = npm_subparsers.add_parser('info', help='Get package info')
    npm_info.add_argument('package', help='Package name')
    
    # PyPI commands
    pypi_parser = subparsers.add_parser('pypi', help='PyPI integration')
    pypi_subparsers = pypi_parser.add_subparsers(dest='pypi_command')
    pypi_info = pypi_subparsers.add_parser('info', help='Get package info')
    pypi_info.add_argument('package', help='Package name')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(0)
    
    cli = EnhancedAICLI()
    
    # Enhanced commands
    if args.command == 'welcome':
        cli.show_welcome()
    
    elif args.command == 'providers':
        cli.list_providers_rich()
    
    elif args.command == 'models':
        cli.list_models_rich(args.provider)
    
    elif args.command == 'integrations':
        cli.list_integrations_rich()
    
    elif args.command == 'hub-status':
        cli.show_hub_status()
    
    # Docker commands
    elif args.command == 'docker':
        docker_int = cli.hub.get_integration('docker')
        if not docker_int.connect():
            console.print("[red]Failed to connect to Docker[/red]")
            sys.exit(1)
        
        if args.docker_command == 'containers':
            containers = docker_int.list_containers(all=True)
            table = Table(title="Docker Containers", box=box.ROUNDED)
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="yellow")
            table.add_column("Image", style="green")
            table.add_column("Status", style="magenta")
            
            for container in containers:
                if 'error' not in container:
                    table.add_row(
                        container['id'],
                        container['name'],
                        container['image'],
                        container['status']
                    )
            console.print(table)
        
        elif args.docker_command == 'images':
            images = docker_int.list_images()
            table = Table(title="Docker Images", box=box.ROUNDED)
            table.add_column("ID", style="cyan")
            table.add_column("Tags", style="yellow")
            table.add_column("Size (MB)", style="green")
            
            for image in images:
                if 'error' not in image:
                    table.add_row(
                        image['id'],
                        ', '.join(image['tags']) if image['tags'] else 'none',
                        f"{image['size']:.2f}"
                    )
            console.print(table)
        
        elif args.docker_command == 'logs':
            logs = docker_int.get_container_logs(args.container_id)
            syntax = Syntax(logs, "log", theme="monokai", line_numbers=True)
            console.print(Panel(syntax, title=f"Logs: {args.container_id}", border_style="cyan"))
    
    # Kubernetes commands
    elif args.command == 'k8s':
        k8s_int = cli.hub.get_integration('kubernetes')
        if not k8s_int.connect():
            console.print("[red]Failed to connect to Kubernetes[/red]")
            sys.exit(1)
        
        if args.k8s_command == 'pods':
            pods = k8s_int.list_pods(args.namespace)
            table = Table(title=f"Kubernetes Pods ({args.namespace})", box=box.ROUNDED)
            table.add_column("Name", style="cyan")
            table.add_column("Status", style="yellow")
            table.add_column("Node", style="green")
            
            for pod in pods:
                if 'error' not in pod:
                    table.add_row(pod['name'], pod['status'], pod.get('node', 'N/A'))
            console.print(table)
        
        elif args.k8s_command == 'deployments':
            deployments = k8s_int.list_deployments(args.namespace)
            table = Table(title=f"Kubernetes Deployments ({args.namespace})", box=box.ROUNDED)
            table.add_column("Name", style="cyan")
            table.add_column("Replicas", style="yellow")
            table.add_column("Ready", style="green")
            
            for dep in deployments:
                if 'error' not in dep:
                    table.add_row(
                        dep['name'],
                        str(dep.get('replicas', 0)),
                        str(dep.get('ready_replicas', 0))
                    )
            console.print(table)
        
        elif args.k8s_command == 'services':
            services = k8s_int.list_services(args.namespace)
            table = Table(title=f"Kubernetes Services ({args.namespace})", box=box.ROUNDED)
            table.add_column("Name", style="cyan")
            table.add_column("Type", style="yellow")
            table.add_column("Cluster IP", style="green")
            table.add_column("Ports", style="magenta")
            
            for svc in services:
                if 'error' not in svc:
                    table.add_row(
                        svc['name'],
                        svc['type'],
                        svc['cluster_ip'],
                        ', '.join(svc['ports'])
                    )
            console.print(table)
    
    # npm commands
    elif args.command == 'npm':
        npm_int = cli.hub.get_integration('npm')
        if not npm_int.connect():
            console.print("[red]Failed to connect to npm registry[/red]")
            sys.exit(1)
        
        if args.npm_command == 'search':
            packages = npm_int.search_packages(args.query)
            table = Table(title=f"npm Packages: {args.query}", box=box.ROUNDED)
            table.add_column("Name", style="cyan")
            table.add_column("Version", style="yellow")
            table.add_column("Description", style="white")
            
            for pkg in packages[:10]:
                if 'error' not in pkg:
                    table.add_row(
                        pkg['name'],
                        pkg['version'],
                        pkg['description'][:60]
                    )
            console.print(table)
        
        elif args.npm_command == 'info':
            info = npm_int.get_package_info(args.package)
            if 'error' not in info:
                info_text = f"""
[bold]Name:[/bold] {info['name']}
[bold]Version:[/bold] {info['version']}
[bold]Description:[/bold] {info['description']}
[bold]Author:[/bold] {info['author']}
[bold]License:[/bold] {info['license']}
[bold]Homepage:[/bold] {info['homepage']}
                """
                console.print(Panel(info_text, title="Package Info", border_style="cyan"))
            else:
                console.print(f"[red]{info['error']}[/red]")
    
    # PyPI commands
    elif args.command == 'pypi':
        pypi_int = cli.hub.get_integration('pypi')
        if not pypi_int.connect():
            console.print("[red]Failed to connect to PyPI[/red]")
            sys.exit(1)
        
        if args.pypi_command == 'info':
            info = pypi_int.get_package_info(args.package)
            if 'error' not in info:
                info_text = f"""
[bold]Name:[/bold] {info['name']}
[bold]Version:[/bold] {info['version']}
[bold]Summary:[/bold] {info['summary']}
[bold]Author:[/bold] {info['author']}
[bold]License:[/bold] {info['license']}
[bold]Requires Python:[/bold] {info['requires_python']}
                """
                console.print(Panel(info_text, title="Package Info", border_style="cyan"))
            else:
                console.print(f"[red]{info['error']}[/red]")
    
    # Original CLI commands
    elif args.command == 'config':
        cli.configure(args.provider, args.api_key, args.default_model)
    
    elif args.command == 'switch':
        cli.switch_provider(args.provider)
    
    elif args.command == 'chat':
        cli.chat(args.message, args.model, stream=not args.no_stream, provider=args.provider)
    
    elif args.command == 'interactive':
        cli.chat_interactive(args.model, args.provider)


if __name__ == '__main__':
    main()
