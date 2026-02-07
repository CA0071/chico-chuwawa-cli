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
        'huggingface': {
            'name': 'Hugging Face Inference',
            'base_url': 'https://api-inference.huggingface.co',
            'default_model': 'meta-llama/Meta-Llama-3-8B-Instruct',
            'supports_streaming': True,
            'models_endpoint': False
        },
        'qwen': {
            'name': 'Qwen (DashScope)',
            'base_url': 'https://dashscope.aliyuncs.com/api/v1',
            'default_model': 'qwen-turbo',
            'supports_streaming': True,
            'models_endpoint': False
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
        
        # For Hugging Face, use the huggingface_hub library
        if provider == 'huggingface':
            try:
                from huggingface_hub import InferenceClient
                self.client = InferenceClient(token=api_key)
                self.current_provider = provider
                return
            except ImportError:
                print("Installing huggingface_hub package...")
                os.system(f"{sys.executable} -m pip install huggingface_hub")
                from huggingface_hub import InferenceClient
                self.client = InferenceClient(token=api_key)
                self.current_provider = provider
                return
        
        # For Qwen (DashScope), use the dashscope library
        if provider == 'qwen':
            try:
                import dashscope
                dashscope.api_key = api_key
                self.client = dashscope
                self.current_provider = provider
                return
            except ImportError:
                print("Installing dashscope package...")
                os.system(f"{sys.executable} -m pip install dashscope")
                import dashscope
                dashscope.api_key = api_key
                self.client = dashscope
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
            elif self.current_provider == 'huggingface':
                # Show common Hugging Face models
                print(f"  • {provider_info['default_model']} (default)")
                print("  • meta-llama/Meta-Llama-3-70B-Instruct")
                print("  • mistralai/Mistral-7B-Instruct-v0.2")
                print("  • microsoft/Phi-3-mini-4k-instruct")
                print("  • google/gemma-7b-it")
                print("  • HuggingFaceH4/zephyr-7b-beta")
                print("\nNote: Visit https://huggingface.co/models for full model list.")
            elif self.current_provider == 'qwen':
                # Show Qwen models
                print(f"  • {provider_info['default_model']} (default)")
                print("  • qwen-plus")
                print("  • qwen-max")
                print("  • qwen-max-longcontext")
                print("  • qwen-vl-plus")
                print("  • qwen-vl-max")
                print("\nNote: Visit https://dashscope.aliyun.com for full model list.")
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
            elif self.current_provider == 'huggingface':
                print("  • meta-llama/Meta-Llama-3-70B-Instruct")
                print("  • mistralai/Mistral-7B-Instruct-v0.2")
                print("  • microsoft/Phi-3-mini-4k-instruct")
                print("  • google/gemma-7b-it")
            elif self.current_provider == 'qwen':
                print("  • qwen-plus")
                print("  • qwen-max")
                print("  • qwen-max-longcontext")
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
            elif self.current_provider == 'huggingface':
                # Use Hugging Face Inference Client
                if stream:
                    print("Response: ", end="", flush=True)
                    response_text = ""
                    for token in self.client.chat_completion(
                        model=model,
                        messages=[{"role": "user", "content": message}],
                        stream=True,
                        max_tokens=1024
                    ):
                        content = token.choices[0].delta.content
                        if content:
                            print(content, end="", flush=True)
                            response_text += content
                    print("\n")
                else:
                    response = self.client.chat_completion(
                        model=model,
                        messages=[{"role": "user", "content": message}],
                        stream=False,
                        max_tokens=1024
                    )
                    print("Response:", response.choices[0].message.content)
                    print()
            elif self.current_provider == 'qwen':
                # Use Qwen DashScope API
                from dashscope import Generation
                response = Generation.call(
                    model=model,
                    messages=[{'role': 'user', 'content': message}],
                    result_format='message',
                    stream=stream,
                    incremental_output=stream
                )
                
                if stream:
                    print("Response: ", end="", flush=True)
                    for chunk in response:
                        if chunk.status_code == 200:
                            content = chunk.output.choices[0].message.content
                            if content:
                                print(content, end="", flush=True)
                    print("\n")
                else:
                    if response.status_code == 200:
                        print("Response:", response.output.choices[0].message.content)
                        print()
                    else:
                        print(f"Error: {response.message}")
                        sys.exit(1)
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
                    elif self.current_provider == 'huggingface':
                        # Hugging Face client
                        if use_streaming:
                            assistant_message = ""
                            for token in self.client.chat_completion(
                                model=model,
                                messages=messages,
                                stream=True,
                                max_tokens=1024
                            ):
                                content = token.choices[0].delta.content
                                if content:
                                    print(content, end="", flush=True)
                                    assistant_message += content
                        else:
                            response = self.client.chat_completion(
                                model=model,
                                messages=messages,
                                stream=False,
                                max_tokens=1024
                            )
                            assistant_message = response.choices[0].message.content
                            print(assistant_message, end="", flush=True)
                    elif self.current_provider == 'qwen':
                        # Qwen DashScope client
                        from dashscope import Generation
                        response = Generation.call(
                            model=model,
                            messages=messages,
                            result_format='message',
                            stream=use_streaming,
                            incremental_output=use_streaming
                        )
                        
                        if use_streaming:
                            assistant_message = ""
                            for chunk in response:
                                if chunk.status_code == 200:
                                    content = chunk.output.choices[0].message.content
                                    if content:
                                        print(content, end="", flush=True)
                                        assistant_message += content
                        else:
                            if response.status_code == 200:
                                assistant_message = response.output.choices[0].message.content
                                print(assistant_message, end="", flush=True)
                            else:
                                assistant_message = ""
                                print(f"Error: {response.message}", end="", flush=True)
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
                        elif self.current_provider == 'huggingface':
                            response = self.client.chat_completion(
                                model=model,
                                messages=messages,
                                stream=False,
                                max_tokens=1024
                            )
                            assistant_message = response.choices[0].message.content
                        elif self.current_provider == 'qwen':
                            from dashscope import Generation
                            response = Generation.call(
                                model=model,
                                messages=messages,
                                result_format='message',
                                stream=False
                            )
                            assistant_message = response.output.choices[0].message.content
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
    
    def interactive_setup(self):
        """Interactive setup wizard using inquirer menus"""
        try:
            import inquirer
        except ImportError:
            print("Installing inquirer package for interactive menus...")
            os.system(f"{sys.executable} -m pip install inquirer")
            import inquirer
        
        print("\n" + "="*60)
        print("  🐕 Chico Chuwawa AI CLI - Interactive Setup")
        print("  Built by Max van Heerden")
        print("="*60)
        print("\n👋 Welcome! Let's set up your AI CLI.\n")
        
        # Step 1: Select provider
        questions = [
            inquirer.List('provider',
                message="Which AI provider would you like to configure?",
                choices=[
                    ('OpenRouter (500+ models)', 'openrouter'),
                    ('Ollama Cloud (Cloud-hosted models)', 'ollama'),
                    ('Hugging Face Inference (Open models)', 'huggingface'),
                    ('Qwen/DashScope (Alibaba Cloud)', 'qwen')
                ],
            ),
        ]
        answers = inquirer.prompt(questions)
        
        if not answers:
            print("Setup cancelled.")
            return
        
        provider = answers['provider']
        provider_info = self.PROVIDERS[provider]
        
        # Step 2: Get API key
        print(f"\n📝 Configuring {provider_info['name']}...")
        print(f"\nTo get your API key:")
        
        if provider == 'openrouter':
            print("  1. Visit https://openrouter.ai/")
            print("  2. Sign up or log in")
            print("  3. Go to Keys section")
            print("  4. Create a new API key")
        elif provider == 'ollama':
            print("  1. Visit https://ollama.com/")
            print("  2. Sign up or log in")
            print("  3. Go to Settings → API Keys")
            print("  4. Create a new API key")
        elif provider == 'huggingface':
            print("  1. Visit https://huggingface.co/")
            print("  2. Sign up or log in")
            print("  3. Go to Settings → Access Tokens")
            print("  4. Create a new token")
        elif provider == 'qwen':
            print("  1. Visit https://dashscope.aliyun.com/")
            print("  2. Sign up or log in")
            print("  3. Go to API Keys section")
            print("  4. Create a new API key")
        
        questions = [
            inquirer.Text('api_key',
                message=f"Enter your {provider_info['name']} API key",
            ),
        ]
        answers = inquirer.prompt(questions)
        
        if not answers or not answers['api_key']:
            print("Setup cancelled - no API key provided.")
            return
        
        api_key = answers['api_key']
        
        # Step 3: Select default model
        if provider == 'openrouter':
            model_choices = [
                ('meta-llama/llama-3.3-70b-instruct (Recommended)', 'meta-llama/llama-3.3-70b-instruct'),
                ('anthropic/claude-3.5-sonnet', 'anthropic/claude-3.5-sonnet'),
                ('google/gemini-2.0-flash-exp', 'google/gemini-2.0-flash-exp'),
                ('Use provider default', None)
            ]
        elif provider == 'ollama':
            model_choices = [
                ('gpt-oss:120b-cloud (Recommended)', 'gpt-oss:120b-cloud'),
                ('deepseek-v3.1:671b-cloud', 'deepseek-v3.1:671b-cloud'),
                ('qwen3-coder:480b-cloud', 'qwen3-coder:480b-cloud'),
                ('Use provider default', None)
            ]
        elif provider == 'huggingface':
            model_choices = [
                ('meta-llama/Meta-Llama-3-8B-Instruct (Recommended)', 'meta-llama/Meta-Llama-3-8B-Instruct'),
                ('mistralai/Mistral-7B-Instruct-v0.2', 'mistralai/Mistral-7B-Instruct-v0.2'),
                ('microsoft/Phi-3-mini-4k-instruct', 'microsoft/Phi-3-mini-4k-instruct'),
                ('Use provider default', None)
            ]
        elif provider == 'qwen':
            model_choices = [
                ('qwen-turbo (Recommended)', 'qwen-turbo'),
                ('qwen-plus', 'qwen-plus'),
                ('qwen-max', 'qwen-max'),
                ('Use provider default', None)
            ]
        
        questions = [
            inquirer.List('model',
                message="Select a default model",
                choices=model_choices,
            ),
        ]
        answers = inquirer.prompt(questions)
        
        default_model = answers.get('model') if answers else None
        
        # Save configuration
        self.config.save_config(provider, api_key, default_model)
        
        # Step 4: What to do next?
        print(f"\n✓ {provider_info['name']} configured successfully!\n")
        
        questions = [
            inquirer.List('action',
                message="What would you like to do next?",
                choices=[
                    ('Start interactive chat', 'chat'),
                    ('Send a test message', 'test'),
                    ('List available models', 'models'),
                    ('Exit', 'exit')
                ],
            ),
        ]
        answers = inquirer.prompt(questions)
        
        if not answers:
            return
        
        action = answers['action']
        
        if action == 'chat':
            self.chat_interactive(default_model, provider)
        elif action == 'test':
            self.chat("Hello! Please respond with a brief greeting.", default_model, provider=provider)
        elif action == 'models':
            self.list_models(provider)
        
        print("\n✨ Setup complete! You can now use all CLI commands.\n")
    
    def interactive_menu(self):
        """Interactive main menu for quick actions"""
        try:
            import inquirer
        except ImportError:
            print("Installing inquirer package for interactive menus...")
            os.system(f"{sys.executable} -m pip install inquirer")
            import inquirer
        
        config = self.config.load_config()
        
        # Check if any provider is configured
        if not any(p in config for p in self.PROVIDERS.keys()):
            print("\n❗ No providers configured yet.")
            questions = [
                inquirer.Confirm('setup',
                    message="Would you like to run the setup wizard?",
                    default=True
                ),
            ]
            answers = inquirer.prompt(questions)
            
            if answers and answers['setup']:
                self.interactive_setup()
            return
        
        print("\n" + "="*60)
        print("  🐕 Chico Chuwawa AI CLI - Quick Menu")
        print("  Built by Max van Heerden")
        print("="*60 + "\n")
        
        # Main menu
        questions = [
            inquirer.List('action',
                message="What would you like to do?",
                choices=[
                    ('Start interactive chat', 'chat'),
                    ('Send a quick message', 'message'),
                    ('List available models', 'models'),
                    ('Switch provider', 'switch'),
                    ('Configure new provider', 'config'),
                    ('View configured providers', 'providers'),
                    ('Exit', 'exit')
                ],
            ),
        ]
        answers = inquirer.prompt(questions)
        
        if not answers or answers['action'] == 'exit':
            return
        
        action = answers['action']
        
        if action == 'chat':
            # Select provider
            configured_providers = [(self.PROVIDERS[p]['name'], p) for p in self.PROVIDERS.keys() if p in config]
            
            if len(configured_providers) == 1:
                provider = configured_providers[0][1]
            else:
                questions = [
                    inquirer.List('provider',
                        message="Select provider",
                        choices=configured_providers,
                    ),
                ]
                answers = inquirer.prompt(questions)
                provider = answers['provider'] if answers else None
            
            if provider:
                self.chat_interactive(provider=provider)
        
        elif action == 'message':
            # Get message
            questions = [
                inquirer.Text('message',
                    message="Enter your message",
                ),
            ]
            answers = inquirer.prompt(questions)
            
            if answers and answers['message']:
                self.chat(answers['message'])
        
        elif action == 'models':
            # Select provider
            configured_providers = [(self.PROVIDERS[p]['name'], p) for p in self.PROVIDERS.keys() if p in config]
            
            if len(configured_providers) == 1:
                provider = configured_providers[0][1]
            else:
                questions = [
                    inquirer.List('provider',
                        message="Select provider",
                        choices=configured_providers,
                    ),
                ]
                answers = inquirer.prompt(questions)
                provider = answers['provider'] if answers else None
            
            if provider:
                self.list_models(provider)
        
        elif action == 'switch':
            configured_providers = [(self.PROVIDERS[p]['name'], p) for p in self.PROVIDERS.keys() if p in config]
            
            questions = [
                inquirer.List('provider',
                    message="Select provider to switch to",
                    choices=configured_providers,
                ),
            ]
            answers = inquirer.prompt(questions)
            
            if answers:
                self.switch_provider(answers['provider'])
        
        elif action == 'config':
            self.interactive_setup()
        
        elif action == 'providers':
            self.list_providers()


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Chico Chuwawa AI CLI - Built by Max van Heerden',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive setup wizard
  chico-cli.py setup
  
  # Interactive quick menu
  chico-cli.py menu
  
  # Configure OpenRouter
  chico-cli.py config openrouter --api-key YOUR_KEY
  
  # Configure Hugging Face
  chico-cli.py config huggingface --api-key YOUR_KEY
  
  # Configure Qwen
  chico-cli.py config qwen --api-key YOUR_KEY
  
  # List providers
  chico-cli.py providers
  
  # Switch provider
  chico-cli.py switch huggingface
  
  # List available models
  chico-cli.py models
  
  # Send a single message
  chico-cli.py chat "What is the capital of France?"
  
  # Use a specific model
  chico-cli.py chat "Explain quantum computing" --model meta-llama/llama-3.3-70b-instruct
  
  # Start interactive chat
  chico-cli.py interactive
  
  # Interactive chat with specific model and provider
  chico-cli.py interactive --model qwen-turbo --provider qwen
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Setup command (interactive wizard)
    subparsers.add_parser('setup', help='Interactive setup wizard for beginners')
    
    # Menu command (interactive quick menu)
    subparsers.add_parser('menu', help='Interactive quick menu for common tasks')
    
    # Config command
    config_parser = subparsers.add_parser('config', help='Configure API credentials')
    config_parser.add_argument('provider', choices=['openrouter', 'ollama', 'huggingface', 'qwen'], 
                               help='Provider to configure')
    config_parser.add_argument('--api-key', required=True, help='API key')
    config_parser.add_argument('--default-model', help='Default model to use (optional)')
    
    # Providers command
    subparsers.add_parser('providers', help='List available providers')
    
    # Switch command
    switch_parser = subparsers.add_parser('switch', help='Switch active provider')
    switch_parser.add_argument('provider', choices=['openrouter', 'ollama', 'huggingface', 'qwen'], 
                               help='Provider to switch to')
    
    # Models command
    models_parser = subparsers.add_parser('models', help='List available models')
    models_parser.add_argument('--provider', choices=['openrouter', 'ollama', 'huggingface', 'qwen'], 
                               help='Provider to list models from')
    
    # Chat command
    chat_parser = subparsers.add_parser('chat', help='Send a chat message')
    chat_parser.add_argument('message', help='Message to send')
    chat_parser.add_argument('--model', help='Model to use')
    chat_parser.add_argument('--provider', choices=['openrouter', 'ollama', 'huggingface', 'qwen'], 
                            help='Provider to use')
    chat_parser.add_argument('--no-stream', action='store_true', help='Disable streaming response')
    
    # Interactive command
    interactive_parser = subparsers.add_parser('interactive', help='Start interactive chat session')
    interactive_parser.add_argument('--model', help='Model to use')
    interactive_parser.add_argument('--provider', choices=['openrouter', 'ollama', 'huggingface', 'qwen'], 
                                   help='Provider to use')
    
    args = parser.parse_args()
    
    cli = AICLI()
    
    if not args.command:
        # If no command given, show interactive menu for beginners
        cli.interactive_menu()
        return
    
    if args.command == 'setup':
        cli.interactive_setup()
    
    elif args.command == 'menu':
        cli.interactive_menu()
    
    elif args.command == 'config':
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

