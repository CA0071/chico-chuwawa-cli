#!/usr/bin/env python3
"""
Chico Chuwawa AI CLI
A powerful command-line interface for interacting with multiple AI providers

Built by: Max van Heerden
Version: 2.1.0
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Optional

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
        },
        'deepseek': {
            'name': 'DeepSeek',
            'base_url': 'https://api.deepseek.com',
            'default_model': 'deepseek-chat',
            'supports_streaming': True,
            'models_endpoint': True
        },
        'chatgpt': {
            'name': 'ChatGPT (OpenAI)',
            'base_url': 'https://api.openai.com/v1',
            'default_model': 'gpt-4o',
            'supports_streaming': True,
            'models_endpoint': True
        },
        'claude': {
            'name': 'Claude (Anthropic)',
            'base_url': 'https://api.anthropic.com',
            'default_model': 'claude-opus-4-20250514',
            'supports_streaming': True,
            'models_endpoint': False,
            'api_version': '2023-06-01'
        },
        'manus': {
            'name': 'Manus AI',
            'base_url': 'https://open.manus.ai',
            'default_model': 'manus-1',
            'supports_streaming': False,
            'models_endpoint': False
        }
    }
    
    def __init__(self):
        self.config = APIConfig()
        self.client = None
        self.current_provider = None
    
    def initialize_client(self, provider: Optional[str] = None):
        """Initialize API client with configuration"""
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
        
        # For Claude, use Anthropic SDK
        if provider == 'claude':
            try:
                from anthropic import Anthropic
                self.client = Anthropic(api_key=api_key)
                self.current_provider = provider
                return
            except ImportError:
                print("Installing anthropic package...")
                os.system(f"{sys.executable} -m pip install anthropic")
                from anthropic import Anthropic
                self.client = Anthropic(api_key=api_key)
                self.current_provider = provider
                return
        
        # For Manus, use requests library
        if provider == 'manus':
            import requests
            self.client = requests.Session()
            self.client.headers.update({
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            })
            self.current_provider = provider
            return
        
        # For OpenRouter, DeepSeek, ChatGPT and other OpenAI-compatible APIs
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
            
            elif self.current_provider == 'claude':
                # Claude doesn't have a models list endpoint, show common models
                print(f"  • {provider_info['default_model']} (default)")
                print("  • claude-3-5-sonnet-20241022")
                print("  • claude-3-5-haiku-20241022")
                print("  • claude-3-opus-20240229")
                print("  • claude-3-sonnet-20240229")
                print("  • claude-3-haiku-20240307")
                print("\nNote: Visit https://docs.anthropic.com/en/docs/about-claude/models for full model list.")
            
            elif self.current_provider == 'manus':
                # Manus doesn't expose models list, show default
                print(f"  • {provider_info['default_model']} (default)")
                print("\nNote: Visit https://manus.im for available models and capabilities.")
            
            elif self.current_provider in ['deepseek', 'chatgpt']:
                # Show common models for these providers
                if self.current_provider == 'deepseek':
                    print(f"  • {provider_info['default_model']} (default)")
                    print("  • deepseek-reasoner")
                    print("  • deepseek-coder")
                    print("\nNote: Visit https://platform.deepseek.com for full model list.")
                else:  # chatgpt
                    print(f"  • {provider_info['default_model']} (default)")
                    print("  • gpt-4")
                    print("  • gpt-4-turbo")
                    print("  • gpt-3.5-turbo")
                    print("  • gpt-4o-mini")
                    print("\nNote: Visit https://platform.openai.com/docs/models for full model list.")
            
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
            
            elif self.current_provider == 'claude':
                # Use Claude/Anthropic client
                if stream:
                    print("Response: ", end="", flush=True)
                    with self.client.messages.stream(
                        model=model,
                        max_tokens=4096,
                        messages=[{"role": "user", "content": message}]
                    ) as stream:
                        for text in stream.text_stream:
                            print(text, end="", flush=True)
                    print("\n")
                else:
                    response = self.client.messages.create(
                        model=model,
                        max_tokens=4096,
                        messages=[{"role": "user", "content": message}]
                    )
                    print("Response:", response.content[0].text)
                    print()
            
            elif self.current_provider == 'manus':
                # Use Manus API - creates a task and retrieves result
                import requests
                task_data = {
                    "description": message,
                    "model": model
                }
                response = self.client.post(
                    f"{provider_info['base_url']}/v1/tasks",
                    json=task_data
                )
                
                if response.status_code == 200 or response.status_code == 201:
                    task = response.json()
                    task_id = task.get('id') or task.get('task_id')
                    print(f"Task created: {task_id}")
                    print("Response:", task.get('result', task.get('response', 'Task created successfully')))
                    print()
                else:
                    print(f"Error: API returned status {response.status_code}")
                    print(response.text)
            
            else:
                # OpenRouter, DeepSeek, ChatGPT and other OpenAI-compatible
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
        
        # Warn about Manus not supporting interactive mode well
        if self.current_provider == 'manus':
            print("\nNote: Manus AI is task-based and may not be ideal for interactive chat.")
            print("Each message creates a new task. Consider using 'chat' command instead.\n")
        
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
                    
                    elif self.current_provider == 'claude':
                        # Claude client - convert messages to Claude format
                        claude_messages = []
                        for msg in messages:
                            claude_messages.append({"role": msg["role"], "content": msg["content"]})
                        
                        if use_streaming:
                            assistant_message = ""
                            with self.client.messages.stream(
                                model=model,
                                max_tokens=4096,
                                messages=claude_messages
                            ) as stream:
                                for text in stream.text_stream:
                                    print(text, end="", flush=True)
                                    assistant_message += text
                        else:
                            response = self.client.messages.create(
                                model=model,
                                max_tokens=4096,
                                messages=claude_messages
                            )
                            assistant_message = response.content[0].text
                            print(assistant_message, end="", flush=True)
                    
                    elif self.current_provider == 'manus':
                        # Manus - create task for each message (not ideal for conversation)
                        import requests
                        task_data = {
                            "description": user_input,
                            "model": model
                        }
                        response = self.client.post(
                            f"{provider_info['base_url']}/v1/tasks",
                            json=task_data
                        )
                        
                        if response.status_code == 200 or response.status_code == 201:
                            task = response.json()
                            assistant_message = task.get('result', task.get('response', 'Task created'))
                            print(assistant_message, end="", flush=True)
                        else:
                            assistant_message = f"Error: API returned status {response.status_code}"
                            print(assistant_message, end="", flush=True)
                    
                    else:
                        # OpenRouter, DeepSeek, ChatGPT and others
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
                        elif self.current_provider == 'claude':
                            response = self.client.messages.create(
                                model=model,
                                max_tokens=4096,
                                messages=messages
                            )
                            assistant_message = response.content[0].text
                        elif self.current_provider == 'manus':
                            # Already non-streaming
                            raise
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
    config_parser.add_argument('provider', choices=['openrouter', 'ollama', 'deepseek', 'chatgpt', 'claude', 'manus'], help='Provider to configure')
    config_parser.add_argument('--api-key', required=True, help='API key')
    config_parser.add_argument('--default-model', help='Default model to use (optional)')
    
    # Providers command
    subparsers.add_parser('providers', help='List available providers')
    
    # Switch command
    switch_parser = subparsers.add_parser('switch', help='Switch active provider')
    switch_parser.add_argument('provider', choices=['openrouter', 'ollama', 'deepseek', 'chatgpt', 'claude', 'manus'], help='Provider to switch to')
    
    # Models command
    models_parser = subparsers.add_parser('models', help='List available models')
    models_parser.add_argument('--provider', choices=['openrouter', 'ollama', 'deepseek', 'chatgpt', 'claude', 'manus'], help='Provider to list models from')
    
    # Chat command
    chat_parser = subparsers.add_parser('chat', help='Send a chat message')
    chat_parser.add_argument('message', help='Message to send')
    chat_parser.add_argument('--model', help='Model to use')
    chat_parser.add_argument('--provider', choices=['openrouter', 'ollama', 'deepseek', 'chatgpt', 'claude', 'manus'], help='Provider to use')
    chat_parser.add_argument('--no-stream', action='store_true', help='Disable streaming response')
    
    # Interactive command
    interactive_parser = subparsers.add_parser('interactive', help='Start interactive chat session')
    interactive_parser.add_argument('--model', help='Model to use')
    interactive_parser.add_argument('--provider', choices=['openrouter', 'ollama', 'deepseek', 'chatgpt', 'claude', 'manus'], help='Provider to use')
    
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

