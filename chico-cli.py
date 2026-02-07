#!/usr/bin/env python3
"""
Chico Chuwawa AI CLI
A powerful command-line interface for interacting with OpenRouter and Ollama Cloud APIs
Includes MCP Server integrations for GitHub, Railway, Vercel, Office 365, Browser, and Zoho services

Built by: Max van Heerden
Version: 2.1.0
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Optional, Dict, Any

try:
    from openai import OpenAI
except ImportError:
    print("Error: openai package not found. Installing...")
    os.system(f"{sys.executable} -m pip install openai")
    from openai import OpenAI


class APIConfig:
    """Manage API configuration and credentials"""
    
    def __init__(self):
        # Use Windows AppData for config storage
        if os.name == 'nt':
            config_dir = Path(os.environ.get('APPDATA', '')) / 'ChicoChuwawa-CLI'
        else:
            config_dir = Path.home() / '.config' / 'chico-cli'
        
        self.config_dir = config_dir
        self.config_file = config_dir / 'config.json'
        self.config_dir.mkdir(parents=True, exist_ok=True)
    
    def save_config(self, provider: str, api_key: str, default_model: Optional[str] = None):
        """Save API configuration for a provider"""
        config = self.load_config()
        
        if provider not in config:
            config[provider] = {}
        
        config[provider]['api_key'] = api_key
        if default_model:
            config[provider]['default_model'] = default_model
        
        # Set active provider
        config['active_provider'] = provider
        
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"✓ Configuration saved for {provider}")
    
    def load_config(self) -> dict:
        """Load API configuration"""
        if not self.config_file.exists():
            return {}
        
        with open(self.config_file, 'r') as f:
            return json.load(f)
    
    def get_active_provider(self) -> str:
        """Get the active provider"""
        config = self.load_config()
        return config.get('active_provider', 'openrouter')
    
    def get_provider_config(self, provider: str) -> dict:
        """Get configuration for a specific provider"""
        config = self.load_config()
        return config.get(provider, {})
    
    def save_mcp_config(self, service: str, credentials: Dict[str, str], mode: str = "sandbox"):
        """Save MCP server configuration"""
        config = self.load_config()
        
        if 'mcp_servers' not in config:
            config['mcp_servers'] = {}
        
        if service not in config['mcp_servers']:
            config['mcp_servers'][service] = {}
        
        config['mcp_servers'][service]['credentials'] = credentials
        config['mcp_servers'][service]['mode'] = mode
        
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"✓ MCP configuration saved for {service} ({mode} mode)")
    
    def get_mcp_config(self, service: str) -> dict:
        """Get MCP server configuration"""
        config = self.load_config()
        mcp_servers = config.get('mcp_servers', {})
        return mcp_servers.get(service, {})


class AICLI:
    """Main CLI application class"""
    
    # Provider configurations
    PROVIDERS = {
        'openrouter': {
            'name': 'OpenRouter',
            'base_url': 'https://openrouter.ai/api/v1',
            'default_model': 'meta-llama/llama-3.3-70b-instruct',
            'supports_streaming': True,
            'models_endpoint': True
        },
        'ollama': {
            'name': 'Ollama Cloud',
            'base_url': 'https://ollama.com',
            'default_model': 'gpt-oss:120b-cloud',
            'supports_streaming': True,
            'models_endpoint': True
        }
    }
    
    def __init__(self):
        self.config = APIConfig()
        self.client = None
        self.current_provider = None
    
    def initialize_client(self, provider: Optional[str] = None):
        """Initialize OpenAI-compatible client with configuration"""
        if not provider:
            provider = self.config.get_active_provider()
        
        if provider not in self.PROVIDERS:
            print(f"Error: Unknown provider '{provider}'")
            print(f"Available providers: {', '.join(self.PROVIDERS.keys())}")
            sys.exit(1)
        
        provider_config = self.config.get_provider_config(provider)
        api_key = provider_config.get('api_key')
        
        # Check environment variable as fallback
        if not api_key:
            env_var = f"{provider.upper()}_API_KEY"
            api_key = os.environ.get(env_var)
        
        if not api_key:
            print(f"Error: No API key found for {provider}.")
            print(f"Please configure using: chico-cli.py config {provider} --api-key YOUR_KEY")
            sys.exit(1)
        
        provider_info = self.PROVIDERS[provider]
        
        # For Ollama, we need to use the ollama library approach
        if provider == 'ollama':
            try:
                import ollama
                self.client = ollama.Client(
                    host=provider_info['base_url'],
                    headers={'Authorization': f'Bearer {api_key}'}
                )
                self.current_provider = provider
                return
            except ImportError:
                print("Installing ollama package...")
                os.system(f"{sys.executable} -m pip install ollama")
                import ollama
                self.client = ollama.Client(
                    host=provider_info['base_url'],
                    headers={'Authorization': f'Bearer {api_key}'}
                )
                self.current_provider = provider
                return
        
        # For OpenRouter and other OpenAI-compatible APIs
        self.client = OpenAI(
            base_url=provider_info['base_url'],
            api_key=api_key
        )
        self.current_provider = provider
    
    def configure(self, provider: str, api_key: str, default_model: Optional[str] = None):
        """Configure API credentials for a provider"""
        if provider not in self.PROVIDERS:
            print(f"Error: Unknown provider '{provider}'")
            print(f"Available providers: {', '.join(self.PROVIDERS.keys())}")
            sys.exit(1)
        
        self.config.save_config(provider, api_key, default_model)
    
    def list_providers(self):
        """List available providers"""
        print("\n📋 Available Providers:")
        print("-" * 60)
        
        config = self.config.load_config()
        active = config.get('active_provider', 'openrouter')
        
        for key, info in self.PROVIDERS.items():
            status = "✓ Active" if key == active else ""
            configured = "✓ Configured" if key in config else "✗ Not configured"
            print(f"  • {info['name']} ({key})")
            print(f"    Status: {configured} {status}")
            print(f"    Default model: {info['default_model']}")
            print()
    
    def switch_provider(self, provider: str):
        """Switch active provider"""
        if provider not in self.PROVIDERS:
            print(f"Error: Unknown provider '{provider}'")
            sys.exit(1)
        
        config = self.config.load_config()
        if provider not in config:
            print(f"Error: Provider '{provider}' is not configured yet.")
            print(f"Configure it first: chico-cli.py config {provider} --api-key YOUR_KEY")
            sys.exit(1)
        
        config['active_provider'] = provider
        with open(self.config.config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"✓ Switched to {self.PROVIDERS[provider]['name']}")
    
    def list_models(self, provider: Optional[str] = None):
        """List available models"""
        self.initialize_client(provider)
        
        provider_info = self.PROVIDERS[self.current_provider]
        
        print(f"\n📋 Available Models for {provider_info['name']}:")
        print("-" * 60)
        
        try:
            if self.current_provider == 'ollama':
                # Use Ollama's tags endpoint
                import requests
                response = requests.get(
                    f"{provider_info['base_url']}/api/tags",
                    headers=self.client.headers if hasattr(self.client, 'headers') else {}
                )
                if response.status_code == 200:
                    models = response.json().get('models', [])
                    for model in models:
                        print(f"  • {model.get('name', 'unknown')}")
                else:
                    print(f"  • {provider_info['default_model']} (default)")
                    print("\nNote: Could not fetch full model list.")
            else:
                # OpenRouter and other OpenAI-compatible
                models = self.client.models.list()
                for model in models.data:
                    print(f"  • {model.id}")
            print()
        except Exception as e:
            # Fallback to showing common models
            print(f"  • {provider_info['default_model']} (default)")
            if self.current_provider == 'openrouter':
                print("  • anthropic/claude-3.5-sonnet")
                print("  • google/gemini-2.0-flash-exp")
                print("  • meta-llama/llama-3.3-70b-instruct")
                print("  • mistralai/mistral-large")
                print("  • qwen/qwen-2.5-72b-instruct")
            elif self.current_provider == 'ollama':
                print("  • deepseek-v3.1:671b-cloud")
                print("  • gpt-oss:20b-cloud")
                print("  • kimi-k2:1t-cloud")
                print("  • qwen3-coder:480b-cloud")
                print("  • glm-4.6:cloud")
            print(f"\nNote: Visit {provider_info['name']} website for full model list.")
            print()
    
    def chat(self, message: str, model: Optional[str] = None, stream: bool = True, provider: Optional[str] = None):
        """Send a chat message to the API"""
        self.initialize_client(provider)
        
        provider_info = self.PROVIDERS[self.current_provider]
        
        # Use default model if not specified
        if not model:
            provider_config = self.config.get_provider_config(self.current_provider)
            model = provider_config.get('default_model', provider_info['default_model'])
        
        print(f"\n💬 Sending message to {model} via {provider_info['name']}...\n")
        
        try:
            if self.current_provider == 'ollama':
                # Use Ollama client
                if stream:
                    print("Response: ", end="", flush=True)
                    for part in self.client.chat(model, messages=[{'role': 'user', 'content': message}], stream=True):
                        content = part.get('message', {}).get('content', '')
                        if content:
                            print(content, end="", flush=True)
                    print("\n")
                else:
                    response = self.client.chat(model, messages=[{'role': 'user', 'content': message}], stream=False)
                    print("Response:", response.get('message', {}).get('content', ''))
                    print()
            else:
                # OpenRouter and other OpenAI-compatible
                if stream:
                    try:
                        response = self.client.chat.completions.create(
                            model=model,
                            messages=[{"role": "user", "content": message}],
                            stream=True
                        )
                        
                        print("Response: ", end="", flush=True)
                        for chunk in response:
                            if chunk.choices[0].delta.content:
                                print(chunk.choices[0].delta.content, end="", flush=True)
                        print("\n")
                    except Exception as stream_error:
                        if "streaming" in str(stream_error).lower():
                            # Fallback to non-streaming
                            response = self.client.chat.completions.create(
                                model=model,
                                messages=[{"role": "user", "content": message}],
                                stream=False
                            )
                            print("Response:", response.choices[0].message.content)
                            print()
                        else:
                            raise
                else:
                    response = self.client.chat.completions.create(
                        model=model,
                        messages=[{"role": "user", "content": message}],
                        stream=False
                    )
                    print("Response:", response.choices[0].message.content)
                    print()
        
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    
    def chat_interactive(self, model: Optional[str] = None, provider: Optional[str] = None):
        """Start an interactive chat session"""
        self.initialize_client(provider)
        
        provider_info = self.PROVIDERS[self.current_provider]
        
        # Use default model if not specified
        if not model:
            provider_config = self.config.get_provider_config(self.current_provider)
            model = provider_config.get('default_model', provider_info['default_model'])
        
        print("\n" + "="*60)
        print("  🐕 Chico Chuwawa AI CLI - Built by Max van Heerden")
        print("="*60)
        print(f"\n🤖 Interactive Chat Mode")
        print(f"Provider: {provider_info['name']}")
        print(f"Model: {model}")
        print("Type 'exit' or 'quit' to end the session\n")
        
        messages = []
        use_streaming = True
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['exit', 'quit']:
                    print("Goodbye! 👋")
                    break
                
                if not user_input:
                    continue
                
                messages.append({"role": "user", "content": user_input})
                
                print("AI: ", end="", flush=True)
                
                try:
                    if self.current_provider == 'ollama':
                        # Ollama client
                        if use_streaming:
                            assistant_message = ""
                            for part in self.client.chat(model, messages=messages, stream=True):
                                content = part.get('message', {}).get('content', '')
                                if content:
                                    print(content, end="", flush=True)
                                    assistant_message += content
                        else:
                            response = self.client.chat(model, messages=messages, stream=False)
                            assistant_message = response.get('message', {}).get('content', '')
                            print(assistant_message, end="", flush=True)
                    else:
                        # OpenRouter and others
                        if use_streaming:
                            response = self.client.chat.completions.create(
                                model=model,
                                messages=messages,
                                stream=True
                            )
                            
                            assistant_message = ""
                            for chunk in response:
                                if chunk.choices[0].delta.content:
                                    content = chunk.choices[0].delta.content
                                    print(content, end="", flush=True)
                                    assistant_message += content
                        else:
                            response = self.client.chat.completions.create(
                                model=model,
                                messages=messages,
                                stream=False
                            )
                            assistant_message = response.choices[0].message.content
                            print(assistant_message, end="", flush=True)
                    
                    print("\n")
                    messages.append({"role": "assistant", "content": assistant_message})
                
                except Exception as api_error:
                    if "streaming" in str(api_error).lower() and use_streaming:
                        # Disable streaming for this model
                        use_streaming = False
                        print("\n(Streaming not supported, switching to non-streaming mode)\n")
                        # Retry without streaming
                        if self.current_provider == 'ollama':
                            response = self.client.chat(model, messages=messages, stream=False)
                            assistant_message = response.get('message', {}).get('content', '')
                        else:
                            response = self.client.chat.completions.create(
                                model=model,
                                messages=messages,
                                stream=False
                            )
                            assistant_message = response.choices[0].message.content
                        print(f"AI: {assistant_message}\n")
                        messages.append({"role": "assistant", "content": assistant_message})
                    else:
                        raise
            
            except KeyboardInterrupt:
                print("\n\nGoodbye! 👋")
                break
            except Exception as e:
                print(f"\nError: {e}\n")


class MCPManager:
    """Manager for MCP Server integrations"""
    
    def __init__(self):
        self.config = APIConfig()
        self.servers = {}
    
    def configure_service(self, service: str, credentials: Dict[str, str], mode: str = "sandbox"):
        """Configure an MCP service"""
        self.config.save_mcp_config(service, credentials, mode)
    
    def get_server(self, service: str):
        """Get or create an MCP server instance"""
        if service in self.servers:
            return self.servers[service]
        
        # Import MCP servers
        try:
            from mcp_servers import (
                MCPServerConfig, EnvironmentMode,
                GitHubMCPServer, RailwayMCPServer, VercelMCPServer,
                Office365MCPServer, BrowserMCPServer, ZohoCRMMCPServer,
                ZohoDeskMCPServer, ZohoInvoiceMCPServer
            )
        except ImportError as e:
            print(f"Error importing MCP servers: {e}")
            print("Please ensure all required packages are installed: pip install -r requirements.txt")
            return None
        
        # Get configuration
        config_data = self.config.get_mcp_config(service)
        if not config_data:
            print(f"Error: {service} not configured. Use 'mcp config {service}' first.")
            return None
        
        mode = EnvironmentMode.SANDBOX if config_data.get('mode', 'sandbox') == 'sandbox' else EnvironmentMode.PRODUCTION
        server_config = MCPServerConfig(service, mode)
        
        # Set credentials
        for key, value in config_data.get('credentials', {}).items():
            server_config.set_credential(key, value)
        
        # Create server instance
        server_map = {
            'github': GitHubMCPServer,
            'railway': RailwayMCPServer,
            'vercel': VercelMCPServer,
            'office365': Office365MCPServer,
            'browser': BrowserMCPServer,
            'zoho-crm': ZohoCRMMCPServer,
            'zoho-desk': ZohoDeskMCPServer,
            'zoho-invoice': ZohoInvoiceMCPServer
        }
        
        if service not in server_map:
            print(f"Error: Unknown service '{service}'")
            return None
        
        server = server_map[service](server_config)
        if not server.initialize():
            print(f"Error: Failed to initialize {service}")
            return None
        
        self.servers[service] = server
        return server
    
    def list_services(self):
        """List all configured MCP services"""
        config = self.config.load_config()
        mcp_servers = config.get('mcp_servers', {})
        
        print("\n📋 MCP Services:")
        print("-" * 60)
        
        if not mcp_servers:
            print("  No MCP services configured yet.")
            print("  Use 'mcp config <service>' to configure a service.")
        else:
            for service, data in mcp_servers.items():
                mode = data.get('mode', 'sandbox')
                mode_icon = "🧪" if mode == "sandbox" else "🚀"
                print(f"  {mode_icon} {service.upper()}")
                print(f"     Mode: {mode}")
                print(f"     Credentials: {'✓ Configured' if data.get('credentials') else '✗ Not configured'}")
                print()


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Chico Chuwawa AI CLI - Built by Max van Heerden',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # AI Provider Commands:
  chico-cli.py config openrouter --api-key YOUR_KEY
  chico-cli.py chat "What is the capital of France?"
  chico-cli.py interactive
  
  # MCP Server Commands:
  chico-cli.py mcp config github --token YOUR_TOKEN --mode sandbox
  chico-cli.py mcp list
  chico-cli.py mcp github list-repos
  chico-cli.py mcp railway list-projects
  chico-cli.py mcp vercel list-deployments
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Config command
    config_parser = subparsers.add_parser('config', help='Configure API credentials')
    config_parser.add_argument('provider', choices=['openrouter', 'ollama'], help='Provider to configure')
    config_parser.add_argument('--api-key', required=True, help='API key')
    config_parser.add_argument('--default-model', help='Default model to use (optional)')
    
    # Providers command
    subparsers.add_parser('providers', help='List available providers')
    
    # Switch command
    switch_parser = subparsers.add_parser('switch', help='Switch active provider')
    switch_parser.add_argument('provider', choices=['openrouter', 'ollama'], help='Provider to switch to')
    
    # Models command
    models_parser = subparsers.add_parser('models', help='List available models')
    models_parser.add_argument('--provider', choices=['openrouter', 'ollama'], help='Provider to list models from')
    
    # Chat command
    chat_parser = subparsers.add_parser('chat', help='Send a chat message')
    chat_parser.add_argument('message', help='Message to send')
    chat_parser.add_argument('--model', help='Model to use')
    chat_parser.add_argument('--provider', choices=['openrouter', 'ollama'], help='Provider to use')
    chat_parser.add_argument('--no-stream', action='store_true', help='Disable streaming response')
    
    # Interactive command
    interactive_parser = subparsers.add_parser('interactive', help='Start interactive chat session')
    interactive_parser.add_argument('--model', help='Model to use')
    interactive_parser.add_argument('--provider', choices=['openrouter', 'ollama'], help='Provider to use')
    
    # MCP command
    mcp_parser = subparsers.add_parser('mcp', help='MCP server commands')
    mcp_subparsers = mcp_parser.add_subparsers(dest='mcp_command', help='MCP commands')
    
    # MCP config
    mcp_config_parser = mcp_subparsers.add_parser('config', help='Configure MCP service')
    mcp_config_parser.add_argument('service', choices=['github', 'railway', 'vercel', 'office365', 'browser', 'zoho-crm', 'zoho-desk', 'zoho-invoice'], help='Service to configure')
    mcp_config_parser.add_argument('--token', help='API token/access token')
    mcp_config_parser.add_argument('--access-token', help='Access token (alternative)')
    mcp_config_parser.add_argument('--org-id', help='Organization ID (for services that require it)')
    mcp_config_parser.add_argument('--mode', choices=['sandbox', 'production'], default='sandbox', help='Environment mode (default: sandbox)')
    
    # MCP list
    mcp_subparsers.add_parser('list', help='List configured MCP services')
    
    # MCP service-specific commands
    mcp_github = mcp_subparsers.add_parser('github', help='GitHub operations')
    github_subs = mcp_github.add_subparsers(dest='github_command')
    github_subs.add_parser('status', help='Get GitHub status')
    github_subs.add_parser('list-repos', help='List repositories')
    github_create_repo = github_subs.add_parser('create-repo', help='Create repository')
    github_create_repo.add_argument('name', help='Repository name')
    github_create_repo.add_argument('--description', default='', help='Repository description')
    github_create_repo.add_argument('--private', action='store_true', help='Make repository private')
    
    mcp_railway = mcp_subparsers.add_parser('railway', help='Railway operations')
    railway_subs = mcp_railway.add_subparsers(dest='railway_command')
    railway_subs.add_parser('status', help='Get Railway status')
    railway_subs.add_parser('list-projects', help='List projects')
    
    mcp_vercel = mcp_subparsers.add_parser('vercel', help='Vercel operations')
    vercel_subs = mcp_vercel.add_subparsers(dest='vercel_command')
    vercel_subs.add_parser('status', help='Get Vercel status')
    vercel_subs.add_parser('list-projects', help='List projects')
    vercel_subs.add_parser('list-deployments', help='List deployments')
    
    mcp_office365 = mcp_subparsers.add_parser('office365', help='Office 365 operations')
    office365_subs = mcp_office365.add_subparsers(dest='office365_command')
    office365_subs.add_parser('status', help='Get Office 365 status')
    office365_subs.add_parser('list-emails', help='List emails')
    office365_send = office365_subs.add_parser('send-email', help='Send email')
    office365_send.add_argument('to', help='Recipient email')
    office365_send.add_argument('subject', help='Email subject')
    office365_send.add_argument('body', help='Email body')
    
    mcp_browser = mcp_subparsers.add_parser('browser', help='Browser automation operations')
    browser_subs = mcp_browser.add_subparsers(dest='browser_command')
    browser_subs.add_parser('status', help='Get browser status')
    browser_launch = browser_subs.add_parser('launch', help='Launch browser')
    browser_launch.add_argument('--headless', action='store_true', default=True, help='Launch in headless mode')
    browser_navigate = browser_subs.add_parser('navigate', help='Navigate to URL')
    browser_navigate.add_argument('url', help='URL to navigate to')
    browser_screenshot = browser_subs.add_parser('screenshot', help='Take screenshot')
    browser_screenshot.add_argument('path', help='Output file path')
    
    mcp_zoho_crm = mcp_subparsers.add_parser('zoho-crm', help='Zoho CRM operations')
    zoho_crm_subs = mcp_zoho_crm.add_subparsers(dest='zoho_crm_command')
    zoho_crm_subs.add_parser('status', help='Get Zoho CRM status')
    zoho_crm_subs.add_parser('list-leads', help='List leads')
    zoho_crm_create_lead = zoho_crm_subs.add_parser('create-lead', help='Create lead')
    zoho_crm_create_lead.add_argument('first_name', help='First name')
    zoho_crm_create_lead.add_argument('last_name', help='Last name')
    zoho_crm_create_lead.add_argument('email', help='Email')
    zoho_crm_create_lead.add_argument('company', help='Company name')
    
    mcp_zoho_desk = mcp_subparsers.add_parser('zoho-desk', help='Zoho Desk operations')
    zoho_desk_subs = mcp_zoho_desk.add_subparsers(dest='zoho_desk_command')
    zoho_desk_subs.add_parser('status', help='Get Zoho Desk status')
    zoho_desk_subs.add_parser('list-tickets', help='List tickets')
    
    mcp_zoho_invoice = mcp_subparsers.add_parser('zoho-invoice', help='Zoho Invoice operations')
    zoho_invoice_subs = mcp_zoho_invoice.add_subparsers(dest='zoho_invoice_command')
    zoho_invoice_subs.add_parser('status', help='Get Zoho Invoice status')
    zoho_invoice_subs.add_parser('list-invoices', help='List invoices')
    zoho_invoice_subs.add_parser('list-customers', help='List customers')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(0)
    
    cli = AICLI()
    
    if args.command == 'config':
        cli.configure(args.provider, args.api_key, args.default_model)
    
    elif args.command == 'providers':
        cli.list_providers()
    
    elif args.command == 'switch':
        cli.switch_provider(args.provider)
    
    elif args.command == 'models':
        cli.list_models(args.provider)
    
    elif args.command == 'chat':
        cli.chat(args.message, args.model, stream=not args.no_stream, provider=args.provider)
    
    elif args.command == 'interactive':
        cli.chat_interactive(args.model, args.provider)
    
    elif args.command == 'mcp':
        mcp_manager = MCPManager()
        
        if args.mcp_command == 'config':
            # Configure MCP service
            credentials = {}
            
            # Gather credentials based on service
            if args.service in ['github', 'railway', 'vercel']:
                token = args.token or args.access_token
                if not token:
                    print(f"Error: --token is required for {args.service}")
                    sys.exit(1)
                credentials['token'] = token
            
            elif args.service == 'office365':
                access_token = args.token or args.access_token
                if not access_token:
                    print("Error: --access-token is required for Office 365")
                    sys.exit(1)
                credentials['access_token'] = access_token
            
            elif args.service == 'browser':
                # No credentials needed for browser
                pass
            
            elif args.service == 'zoho-crm':
                access_token = args.token or args.access_token
                if not access_token:
                    print("Error: --access-token is required for Zoho CRM")
                    sys.exit(1)
                credentials['access_token'] = access_token
            
            elif args.service == 'zoho-desk':
                access_token = args.token or args.access_token
                org_id = args.org_id
                if not access_token or not org_id:
                    print("Error: --access-token and --org-id are required for Zoho Desk")
                    sys.exit(1)
                credentials['access_token'] = access_token
                credentials['org_id'] = org_id
            
            elif args.service == 'zoho-invoice':
                access_token = args.token or args.access_token
                org_id = args.org_id
                if not access_token or not org_id:
                    print("Error: --access-token and --org-id are required for Zoho Invoice")
                    sys.exit(1)
                credentials['access_token'] = access_token
                credentials['organization_id'] = org_id
            
            mcp_manager.configure_service(args.service, credentials, args.mode)
        
        elif args.mcp_command == 'list':
            mcp_manager.list_services()
        
        elif args.mcp_command == 'github':
            server = mcp_manager.get_server('github')
            if not server:
                sys.exit(1)
            
            if args.github_command == 'status':
                status = server.get_status()
                print(f"\nGitHub Status: {status}")
            elif args.github_command == 'list-repos':
                repos = server.list_repositories()
                print(f"\n📦 Repositories ({len(repos)}):")
                for repo in repos[:20]:  # Limit to 20
                    print(f"  • {repo['full_name']} - {repo.get('description', 'No description')}")
            elif args.github_command == 'create-repo':
                result = server.create_repository(args.name, args.description, args.private)
                if result:
                    print(f"\n✓ Repository created: {result.get('full_name', args.name)}")
        
        elif args.mcp_command == 'railway':
            server = mcp_manager.get_server('railway')
            if not server:
                sys.exit(1)
            
            if args.railway_command == 'status':
                status = server.get_status()
                print(f"\nRailway Status: {status}")
            elif args.railway_command == 'list-projects':
                projects = server.list_projects()
                print(f"\n🚂 Projects ({len(projects)}):")
                for project in projects:
                    print(f"  • {project['name']} - {project.get('description', 'No description')}")
        
        elif args.mcp_command == 'vercel':
            server = mcp_manager.get_server('vercel')
            if not server:
                sys.exit(1)
            
            if args.vercel_command == 'status':
                status = server.get_status()
                print(f"\nVercel Status: {status}")
            elif args.vercel_command == 'list-projects':
                projects = server.list_projects()
                print(f"\n▲ Projects ({len(projects)}):")
                for project in projects:
                    print(f"  • {project['name']}")
            elif args.vercel_command == 'list-deployments':
                deployments = server.list_deployments()
                print(f"\n🚀 Deployments ({len(deployments)}):")
                for deployment in deployments[:20]:  # Limit to 20
                    print(f"  • {deployment.get('name', 'N/A')} - {deployment.get('state', 'N/A')}")
        
        elif args.mcp_command == 'office365':
            server = mcp_manager.get_server('office365')
            if not server:
                sys.exit(1)
            
            if args.office365_command == 'status':
                status = server.get_status()
                print(f"\nOffice 365 Status: {status}")
            elif args.office365_command == 'list-emails':
                emails = server.list_emails()
                print(f"\n📧 Emails ({len(emails)}):")
                for email in emails:
                    print(f"  • {email.get('subject', 'No subject')} - From: {email.get('from', {}).get('emailAddress', {}).get('address', 'Unknown')}")
            elif args.office365_command == 'send-email':
                success = server.send_email(args.to, args.subject, args.body)
                if success:
                    print("\n✓ Email sent successfully")
                else:
                    print("\n✗ Failed to send email")
        
        elif args.mcp_command == 'browser':
            server = mcp_manager.get_server('browser')
            if not server:
                sys.exit(1)
            
            if args.browser_command == 'status':
                status = server.get_status()
                print(f"\nBrowser Status: {status}")
            elif args.browser_command == 'launch':
                success = server.launch_browser(headless=args.headless)
                if success:
                    print("\n✓ Browser launched successfully")
                else:
                    print("\n✗ Failed to launch browser")
            elif args.browser_command == 'navigate':
                success = server.navigate_to(args.url)
                if success:
                    print(f"\n✓ Navigated to {args.url}")
                    print(f"   Page title: {server.get_page_title()}")
                else:
                    print(f"\n✗ Failed to navigate to {args.url}")
            elif args.browser_command == 'screenshot':
                success = server.screenshot(args.path)
                if success:
                    print(f"\n✓ Screenshot saved to {args.path}")
                else:
                    print(f"\n✗ Failed to save screenshot")
        
        elif args.mcp_command == 'zoho-crm':
            server = mcp_manager.get_server('zoho-crm')
            if not server:
                sys.exit(1)
            
            if args.zoho_crm_command == 'status':
                status = server.get_status()
                print(f"\nZoho CRM Status: {status}")
            elif args.zoho_crm_command == 'list-leads':
                leads = server.list_leads()
                print(f"\n👤 Leads ({len(leads)}):")
                for lead in leads[:20]:  # Limit to 20
                    print(f"  • {lead.get('Full_Name', 'N/A')} - {lead.get('Email', 'N/A')}")
            elif args.zoho_crm_command == 'create-lead':
                result = server.create_lead(args.first_name, args.last_name, args.email, args.company)
                if result:
                    print(f"\n✓ Lead created successfully")
                else:
                    print("\n✗ Failed to create lead")
        
        elif args.mcp_command == 'zoho-desk':
            server = mcp_manager.get_server('zoho-desk')
            if not server:
                sys.exit(1)
            
            if args.zoho_desk_command == 'status':
                status = server.get_status()
                print(f"\nZoho Desk Status: {status}")
            elif args.zoho_desk_command == 'list-tickets':
                tickets = server.list_tickets()
                print(f"\n🎫 Tickets ({len(tickets)}):")
                for ticket in tickets[:20]:  # Limit to 20
                    print(f"  • #{ticket.get('ticketNumber', 'N/A')} - {ticket.get('subject', 'No subject')}")
        
        elif args.mcp_command == 'zoho-invoice':
            server = mcp_manager.get_server('zoho-invoice')
            if not server:
                sys.exit(1)
            
            if args.zoho_invoice_command == 'status':
                status = server.get_status()
                print(f"\nZoho Invoice Status: {status}")
            elif args.zoho_invoice_command == 'list-invoices':
                invoices = server.list_invoices()
                print(f"\n🧾 Invoices ({len(invoices)}):")
                for invoice in invoices[:20]:  # Limit to 20
                    print(f"  • #{invoice.get('invoice_number', 'N/A')} - {invoice.get('customer_name', 'N/A')}")
            elif args.zoho_invoice_command == 'list-customers':
                customers = server.list_customers()
                print(f"\n👥 Customers ({len(customers)}):")
                for customer in customers[:20]:  # Limit to 20
                    print(f"  • {customer.get('contact_name', 'N/A')} - {customer.get('email', 'N/A')}")


if __name__ == '__main__':
    main()


