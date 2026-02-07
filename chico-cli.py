#!/usr/bin/env python3
"""
Chico Chuwawa AI CLI
A powerful command-line interface for interacting with OpenRouter and Ollama Cloud APIs

Built by: Max van Heerden
Version: 2.0.0
"""

import os
import sys
import json
import argparse
import time
import random
from pathlib import Path
from typing import Optional

try:
    from openai import OpenAI
except ImportError:
    print("Error: openai package not found. Installing...")
    os.system(f"{sys.executable} -m pip install openai")
    from openai import OpenAI

try:
    from rich.console import Console
    from rich.live import Live
    from rich.text import Text
    from rich.panel import Panel
except ImportError:
    print("Installing rich library for animations...")
    os.system(f"{sys.executable} -m pip install rich>=13.0.0")
    from rich.console import Console
    from rich.live import Live
    from rich.text import Text
    from rich.panel import Panel

console = Console()


# ASCII Art frames for walking Chihuahua (Applehead white Chihuahua)
CHIHUAHUA_FRAMES = [
    # Frame 1 - Left paw forward
    """
    /\\_/\\
   ( o.o )
    > ^ <
   /|   |\\
  (_|   |_)
    """,
    # Frame 2 - Mid-step
    """
    /\\_/\\
   ( o.o )
    > ^ <
   /|   |\\
  ( |   | )
    """,
    # Frame 3 - Right paw forward
    """
    /\\_/\\
   ( o.o )
    > ^ <
   /|   |\\
  (_|   |_)
    """,
    # Frame 4 - Mid-step (other side)
    """
    /\\_/\\
   ( ^.^ )
    > ^ <
   /|   |\\
  ( |   | )
    """
]

# Sitting Chihuahua logo
CHIHUAHUA_SITTING = """
      /\\_/\\
     ( o.o )
      > ^ <
     /|   |\\
    ( |   | )
   /  |   |  \\
  '---'   '---'
"""

# Coding-themed waiting messages (jokes/puns about coding, AI, and Chihuahuas)
WAITING_MESSAGES = [
    "🐕 Chihuahua compiling thoughts... (it's a small dog, big CPU!)",
    "🐾 Fetching data... No, not that kind of fetch!",
    "💭 Training neural networks... Just like potty training, but faster!",
    "🦴 Caching responses... (Chihuahuas love caching bones!)",
    "🎯 Optimizing bark-to-bite ratio in the algorithm...",
    "🐕 Running Chihuahua Neural Network (ChNN)...",
    "💻 Debugging with tiny paws... It's pawsible!",
    "🔍 Sniffing out the best tokens...",
    "🌟 Deploying Chihuahua Intelligence (CI/CD - Chihuahua Intelligence/Continuous Delivery)...",
    "🐾 Executing tail-recursive functions...",
    "🦴 Parsing bark data structures...",
    "💡 Chihuahua thinking: If(treats > 0) { wag(tail); }",
    "🎨 Rendering AI response in Chihuahua-style...",
    "⚡ Overclocking the tiny brain... Maximum cuteness achieved!",
    "🔧 Refactoring code with bite-sized commits...",
    "🐕 Stack overflow? More like snack overflow!",
    "💭 Consulting the Chihuahua documentation (it barks back)...",
    "🎯 Applying supervised learning... Chihuahua says: 'Sit! Stay! Code!'",
    "🌈 Transforming inputs with attention mechanisms... Squirrel!",
    "🦴 Garbage collecting... (Not literal garbage, we're sophisticated!)"
]


def display_walking_animation():
    """Display Chihuahua walking across the screen"""
    try:
        width = console.width
        # Number of positions to walk across
        positions = min(width - 15, 50)  # Limit animation width
        
        for pos in range(positions):
            # Cycle through frames
            frame = CHIHUAHUA_FRAMES[pos % len(CHIHUAHUA_FRAMES)]
            
            # Create padding to simulate movement
            padding = " " * pos
            animated_frame = "\n".join(padding + line for line in frame.split("\n"))
            
            # Clear and display
            console.clear()
            console.print(animated_frame, style="bold white")
            time.sleep(0.08)  # Animation speed
        
        # Clear after animation
        console.clear()
    except Exception:
        # Fallback if animation fails
        pass


def display_logo():
    """Display sitting Chihuahua as logo in the corner"""
    try:
        logo_panel = Panel(
            Text(CHIHUAHUA_SITTING, style="bold white", justify="center"),
            title="[bold cyan]🐕 Chico Chuwawa AI CLI[/bold cyan]",
            subtitle="[dim]Built by Max van Heerden[/dim]",
            border_style="cyan"
        )
        console.print(logo_panel)
    except Exception:
        # Fallback to simple text
        print("\n🐕 Chico Chuwawa AI CLI - Built by Max van Heerden\n")


def get_random_waiting_message():
    """Get a random waiting message"""
    return random.choice(WAITING_MESSAGES)


def show_waiting_message():
    """Show a random waiting message during API calls"""
    try:
        message = get_random_waiting_message()
        console.print(f"\n[dim cyan]{message}[/dim cyan]")
    except Exception:
        # Silent fallback
        pass


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
        
        print(f"\n💬 Sending message to {model} via {provider_info['name']}...")
        show_waiting_message()  # Show random waiting message
        print()
        
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
        
        # Display logo
        display_logo()
        
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
                
                # Show waiting message
                show_waiting_message()
                
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


def main():
    """Main entry point"""
    # Display walking animation on startup
    display_walking_animation()
    
    parser = argparse.ArgumentParser(
        description='Chico Chuwawa AI CLI - Built by Max van Heerden',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Configure OpenRouter
  chico-cli.py config openrouter --api-key YOUR_KEY
  
  # Configure Ollama Cloud
  chico-cli.py config ollama --api-key YOUR_KEY
  
  # List providers
  chico-cli.py providers
  
  # Switch provider
  chico-cli.py switch ollama
  
  # List available models
  chico-cli.py models
  
  # Send a single message
  chico-cli.py chat "What is the capital of France?"
  
  # Use a specific model
  chico-cli.py chat "Explain quantum computing" --model meta-llama/llama-3.3-70b-instruct
  
  # Start interactive chat
  chico-cli.py interactive
  
  # Interactive chat with specific model and provider
  chico-cli.py interactive --model gpt-oss:120b-cloud --provider ollama
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


if __name__ == '__main__':
    main()

