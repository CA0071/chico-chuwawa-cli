#!/usr/bin/env python3
"""
Chico Chuwawa AI CLI - Enhanced Version
A comprehensive command-line interface with multi-provider support and integrations

Built by: Max van Heerden
Version: 3.0.0
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Optional

# Add the chico package to path if running from repo
sys.path.insert(0, os.path.dirname(__file__))

try:
    from openai import OpenAI
except ImportError:
    print("Installing required packages...")
    os.system(f"{sys.executable} -m pip install openai --quiet")
    from openai import OpenAI

# Import enhanced modules
try:
    from chico.ui.animations import show_welcome_banner, show_animated_chihuahua
    from chico.ui.loading import LoadingSpinner, get_random_message
    from chico.ui.syntax import format_response
    from chico.utils.history import ChatHistory
    from chico.utils.search import CodeSearcher
    from chico.integrations.mcp_servers import (
        MCPServerManager, GitHubMCP, RailwayMCP, VercelMCP,
        Office365MCP, ZohoCRMMCP
    )
    from chico.integrations.desktop_apps import (
        DesktopAppManager, ManusAI, DeepSeekApp, ClaudeApp, ChatGPTApp
    )
    from chico.integrations.whatsapp import WhatsAppIntegration
    ENHANCED_FEATURES = True
except ImportError as e:
    ENHANCED_FEATURES = False
    print(f"Note: Some enhanced features unavailable. Run: pip install -r requirements.txt")


class APIConfig:
    """Manage API configuration and credentials"""
    
    def __init__(self):
        # Use cross-platform config storage
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
    
    def save_integration_config(self, integration_name: str, config: dict):
        """Save configuration for an integration"""
        full_config = self.load_config()
        if 'integrations' not in full_config:
            full_config['integrations'] = {}
        full_config['integrations'][integration_name] = config
        
        with open(self.config_file, 'w') as f:
            json.dump(full_config, f, indent=2)
    
    def get_integration_config(self, integration_name: str) -> dict:
        """Get configuration for an integration"""
        config = self.load_config()
        return config.get('integrations', {}).get(integration_name, {})


class AICLI:
    """Main CLI application class with enhanced features"""
    
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
    
    def __init__(self, show_banner: bool = False):
        self.config = APIConfig()
        self.client = None
        self.current_provider = None
        
        # Initialize enhanced features
        if ENHANCED_FEATURES:
            self.history = ChatHistory()
            self.searcher = CodeSearcher()
            self.mcp_manager = MCPServerManager()
            self.app_manager = DesktopAppManager()
            self.whatsapp = WhatsAppIntegration()
            
            if show_banner:
                show_welcome_banner()
    
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
            print(f"Please configure using: chico config {provider} --api-key YOUR_KEY")
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
                os.system(f"{sys.executable} -m pip install ollama --quiet")
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
            print(f"Configure it first: chico config {provider} --api-key YOUR_KEY")
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
    
    def chat(self, message: str, model: Optional[str] = None, stream: bool = True, 
             provider: Optional[str] = None, with_search: bool = False,
             save_history: bool = False):
        """Send a chat message to the API"""
        self.initialize_client(provider)
        
        provider_info = self.PROVIDERS[self.current_provider]
        
        # Use default model if not specified
        if not model:
            provider_config = self.config.get_provider_config(self.current_provider)
            model = provider_config.get('default_model', provider_info['default_model'])
        
        # Show loading animation
        if ENHANCED_FEATURES:
            spinner = LoadingSpinner(get_random_message())
            spinner.start()
            import time
            for _ in range(5):
                spinner.spin_once()
                time.sleep(0.1)
            spinner.stop()
        
        print(f"\n💬 Sending message to {model} via {provider_info['name']}...\n")
        
        # Optional: Search for coding solutions
        if with_search and ENHANCED_FEATURES:
            print("🔍 Searching for relevant coding solutions...")
            results = self.searcher.search_stackoverflow(message, max_results=3)
            search_context = self.searcher.format_results(results)
            print(search_context)
            message = f"{message}\n\nContext from search:\n{search_context}"
        
        # Create session if saving history
        session_id = None
        if save_history and ENHANCED_FEATURES:
            session_id = self.history.create_session(self.current_provider, model)
            self.history.add_message(session_id, 'user', message)
        
        try:
            response_text = ""
            if self.current_provider == 'ollama':
                # Use Ollama client
                if stream:
                    print("Response: ", end="", flush=True)
                    for part in self.client.chat(model, messages=[{'role': 'user', 'content': message}], stream=True):
                        content = part.get('message', {}).get('content', '')
                        if content:
                            print(content, end="", flush=True)
                            response_text += content
                    print("\n")
                else:
                    response = self.client.chat(model, messages=[{'role': 'user', 'content': message}], stream=False)
                    response_text = response.get('message', {}).get('content', '')
                    print("Response:", response_text)
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
                                content = chunk.choices[0].delta.content
                                print(content, end="", flush=True)
                                response_text += content
                        print("\n")
                    except Exception as stream_error:
                        if "streaming" in str(stream_error).lower():
                            # Fallback to non-streaming
                            response = self.client.chat.completions.create(
                                model=model,
                                messages=[{"role": "user", "content": message}],
                                stream=False
                            )
                            response_text = response.choices[0].message.content
                            print("Response:", response_text)
                            print()
                        else:
                            raise
                else:
                    response = self.client.chat.completions.create(
                        model=model,
                        messages=[{"role": "user", "content": message}],
                        stream=False
                    )
                    response_text = response.choices[0].message.content
                    
                    # Apply syntax highlighting if available
                    if ENHANCED_FEATURES:
                        response_text = format_response(response_text)
                    
                    print("Response:", response_text)
                    print()
            
            # Save to history
            if save_history and ENHANCED_FEATURES and session_id:
                self.history.add_message(session_id, 'assistant', response_text)
        
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    
    def chat_interactive(self, model: Optional[str] = None, provider: Optional[str] = None,
                        save_history: bool = True):
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
        print("Type 'exit' or 'quit' to end the session")
        if ENHANCED_FEATURES and save_history:
            print("💾 Chat history is being saved")
        print()
        
        messages = []
        use_streaming = True
        
        # Create history session
        session_id = None
        if ENHANCED_FEATURES and save_history:
            session_id = self.history.create_session(self.current_provider, model)
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['exit', 'quit']:
                    print("Goodbye! 👋")
                    break
                
                if not user_input:
                    continue
                
                messages.append({"role": "user", "content": user_input})
                
                # Save user message
                if ENHANCED_FEATURES and save_history and session_id:
                    self.history.add_message(session_id, 'user', user_input)
                
                print("AI: ", end="", flush=True)
                
                try:
                    assistant_message = ""
                    if self.current_provider == 'ollama':
                        # Ollama client
                        if use_streaming:
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
                    
                    # Save assistant message
                    if ENHANCED_FEATURES and save_history and session_id:
                        self.history.add_message(session_id, 'assistant', assistant_message)
                
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
                        
                        # Save assistant message
                        if ENHANCED_FEATURES and save_history and session_id:
                            self.history.add_message(session_id, 'assistant', assistant_message)
                    else:
                        raise
            
            except KeyboardInterrupt:
                print("\n\nGoodbye! 👋")
                break
            except Exception as e:
                print(f"\nError: {e}\n")
    
    def show_history(self, limit: int = 10):
        """Show recent chat history"""
        if not ENHANCED_FEATURES:
            print("History feature requires enhanced modules")
            return
        
        sessions = self.history.list_sessions(limit)
        
        print(f"\n📚 Recent Chat Sessions (last {limit}):")
        print("-" * 60)
        
        if not sessions:
            print("  No chat history yet")
            return
        
        for session in sessions:
            print(f"\n  Session #{session['id']}: {session['title']}")
            print(f"  Provider: {session['provider']} | Model: {session['model']}")
            print(f"  Created: {session['created_at']}")
        
        print()
    
    def search_code(self, query: str, source: str = 'general'):
        """Search for coding solutions"""
        if not ENHANCED_FEATURES:
            print("Search feature requires enhanced modules")
            return
        
        print(f"\n🔍 Searching for: {query}")
        print("-" * 60)
        
        if source == 'stackoverflow':
            results = self.searcher.search_stackoverflow(query)
        elif source == 'github':
            results = self.searcher.search_github(query)
        else:
            results = self.searcher.search(query)
        
        print(self.searcher.format_results(results))
    
    def setup_whatsapp(self):
        """Setup WhatsApp integration"""
        if not ENHANCED_FEATURES:
            print("WhatsApp feature requires enhanced modules")
            return
        
        print("\n📱 WhatsApp Integration Setup")
        print("-" * 60)
        
        self.whatsapp.connect()


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Chico Chuwawa AI CLI v3.0 - Built by Max van Heerden',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Configure OpenRouter
  chico config openrouter --api-key YOUR_KEY
  
  # Configure Ollama Cloud
  chico config ollama --api-key YOUR_KEY
  
  # List providers
  chico providers
  
  # Switch provider
  chico switch ollama
  
  # List available models
  chico models
  
  # Send a single message
  chico chat "What is the capital of France?"
  
  # Use a specific model with search
  chico chat "How to sort array in Python?" --search
  
  # Start interactive chat
  chico interactive
  
  # View chat history
  chico history
  
  # Search for code solutions
  chico search "python async await"
  
  # Setup WhatsApp integration
  chico whatsapp
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
    chat_parser.add_argument('--search', action='store_true', help='Search for coding solutions')
    chat_parser.add_argument('--save', action='store_true', help='Save to history')
    
    # Interactive command
    interactive_parser = subparsers.add_parser('interactive', help='Start interactive chat session')
    interactive_parser.add_argument('--model', help='Model to use')
    interactive_parser.add_argument('--provider', choices=['openrouter', 'ollama'], help='Provider to use')
    interactive_parser.add_argument('--no-save', action='store_true', help='Don\'t save history')
    interactive_parser.add_argument('--banner', action='store_true', help='Show welcome banner')
    
    # History command
    history_parser = subparsers.add_parser('history', help='View chat history')
    history_parser.add_argument('--limit', type=int, default=10, help='Number of sessions to show')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search for coding solutions')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('--source', choices=['general', 'stackoverflow', 'github'], 
                               default='general', help='Search source')
    
    # WhatsApp command
    subparsers.add_parser('whatsapp', help='Setup WhatsApp integration')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(0)
    
    # Create CLI instance
    show_banner = hasattr(args, 'banner') and args.banner
    cli = AICLI(show_banner=show_banner)
    
    # Execute command
    if args.command == 'config':
        cli.configure(args.provider, args.api_key, args.default_model)
    
    elif args.command == 'providers':
        cli.list_providers()
    
    elif args.command == 'switch':
        cli.switch_provider(args.provider)
    
    elif args.command == 'models':
        cli.list_models(args.provider)
    
    elif args.command == 'chat':
        cli.chat(args.message, args.model, stream=not args.no_stream, 
                provider=args.provider, with_search=args.search, save_history=args.save)
    
    elif args.command == 'interactive':
        cli.chat_interactive(args.model, args.provider, save_history=not args.no_save)
    
    elif args.command == 'history':
        cli.show_history(args.limit)
    
    elif args.command == 'search':
        cli.search_code(args.query, args.source)
    
    elif args.command == 'whatsapp':
        cli.setup_whatsapp()


if __name__ == '__main__':
    main()
