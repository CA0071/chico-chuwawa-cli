#!/usr/bin/env python3
"""
Chico Chuwawa AI CLI
A powerful command-line interface for interacting with OpenRouter and Ollama Cloud APIs

Built by: Max van Heerden
Version: 3.0.0 - Enhanced Edition
"""

import os
import sys
import json
import argparse
import time
import random
from pathlib import Path
from typing import Optional, List, Dict, Any

try:
    from openai import OpenAI
except ImportError:
    print("Error: openai package not found. Installing...")
    os.system(f"{sys.executable} -m pip install openai")
    from openai import OpenAI

# Import enhanced features
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.markdown import Markdown
    from rich.table import Table
    from rich import print as rprint
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    Console = None

try:
    import pyfiglet
    FIGLET_AVAILABLE = True
except ImportError:
    FIGLET_AVAILABLE = False

try:
    from duckduckgo_search import DDGS
    WEB_SEARCH_AVAILABLE = True
except ImportError:
    WEB_SEARCH_AVAILABLE = False

try:
    import git
    GIT_AVAILABLE = True
except ImportError:
    GIT_AVAILABLE = False


# Chihuahua ASCII Art and Animations
CHICO_ASCII_ART = [
    r"""
    /\_/\  
   ( o.o ) 
    > ^ <  Woof! I'm Chico!
   /|   |\
  (_|   |_)
    """,
    r"""
      /\_/\  
     ( ^.^ ) 
      > * <  Let's go!
     /|   |\
    (_|   |_)
    """,
    r"""
    /\_/\  
   ( -.-)zzz
    > ^ <  Thinking...
   /|   |\
  (_|   |_)
    """
]

CHICO_QUOTES = [
    "🐕 Woof! Ready to fetch some answers!",
    "🐾 Small dog, BIG intelligence!",
    "✨ Chico is on the case!",
    "🦴 Let me dig into that for you!",
    "🎾 Fetching the best response...",
    "🐶 Arf! I've got this!",
    "💪 Tiny but mighty!",
    "🌟 Chico to the rescue!"
]


class GamificationSystem:
    """Gamification system for tracking user achievements and progress"""
    
    def __init__(self, config_dir: Path):
        self.progress_file = config_dir / 'chico_progress.json'
        self.load_progress()
    
    def load_progress(self):
        """Load user progress and achievements"""
        if self.progress_file.exists():
            with open(self.progress_file, 'r') as f:
                data = json.load(f)
        else:
            data = {
                'level': 1,
                'xp': 0,
                'commands_used': 0,
                'chats_completed': 0,
                'workflows_completed': 0,
                'achievements': [],
                'bones_collected': 0
            }
        
        self.level = data.get('level', 1)
        self.xp = data.get('xp', 0)
        self.commands_used = data.get('commands_used', 0)
        self.chats_completed = data.get('chats_completed', 0)
        self.workflows_completed = data.get('workflows_completed', 0)
        self.achievements = data.get('achievements', [])
        self.bones_collected = data.get('bones_collected', 0)
    
    def save_progress(self):
        """Save user progress"""
        data = {
            'level': self.level,
            'xp': self.xp,
            'commands_used': self.commands_used,
            'chats_completed': self.chats_completed,
            'workflows_completed': self.workflows_completed,
            'achievements': self.achievements,
            'bones_collected': self.bones_collected
        }
        with open(self.progress_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def add_xp(self, amount: int, reason: str = ""):
        """Add XP and check for level ups"""
        self.xp += amount
        self.commands_used += 1
        
        # Level up logic: each level requires level * 100 XP
        while self.xp >= self.level * 100:
            self.xp -= self.level * 100
            self.level += 1
            self.show_level_up()
        
        self.save_progress()
    
    def show_level_up(self):
        """Display level up message"""
        if RICH_AVAILABLE:
            console = Console()
            console.print(f"\n[bold yellow]🎉 LEVEL UP! 🎉[/bold yellow]")
            console.print(f"[green]Chico is now level {self.level}![/green]")
            console.print(f"[cyan]🦴 Bone reward: +{self.level} bones![/cyan]\n")
        else:
            print(f"\n🎉 LEVEL UP! Chico is now level {self.level}! 🦴 +{self.level} bones!\n")
        
        self.bones_collected += self.level
    
    def add_achievement(self, achievement: str):
        """Add a new achievement"""
        if achievement not in self.achievements:
            self.achievements.append(achievement)
            if RICH_AVAILABLE:
                console = Console()
                console.print(f"\n[bold green]🏆 Achievement Unlocked: {achievement}![/bold green]\n")
            else:
                print(f"\n🏆 Achievement: {achievement}!\n")
            self.save_progress()
    
    def show_stats(self):
        """Display user stats"""
        if RICH_AVAILABLE:
            console = Console()
            table = Table(title="🐕 Chico's Stats", show_header=True, header_style="bold magenta")
            table.add_column("Stat", style="cyan")
            table.add_column("Value", style="green")
            
            table.add_row("Level", str(self.level))
            table.add_row("XP", f"{self.xp}/{self.level * 100}")
            table.add_row("Commands Used", str(self.commands_used))
            table.add_row("Chats Completed", str(self.chats_completed))
            table.add_row("Workflows Done", str(self.workflows_completed))
            table.add_row("🦴 Bones", str(self.bones_collected))
            table.add_row("🏆 Achievements", str(len(self.achievements)))
            
            console.print(table)
            
            if self.achievements:
                console.print("\n[bold]Achievements:[/bold]")
                for achievement in self.achievements:
                    console.print(f"  🏆 {achievement}")
        else:
            print(f"\n🐕 Chico's Stats:")
            print(f"  Level: {self.level}")
            print(f"  XP: {self.xp}/{self.level * 100}")
            print(f"  Commands: {self.commands_used}")
            print(f"  Chats: {self.chats_completed}")
            print(f"  Workflows: {self.workflows_completed}")
            print(f"  🦴 Bones: {self.bones_collected}")
            print(f"  🏆 Achievements: {len(self.achievements)}")
            if self.achievements:
                print("\nAchievements:")
                for a in self.achievements:
                    print(f"  🏆 {a}")


class WebSearcher:
    """Web search integration for enhanced responses"""
    
    def __init__(self):
        self.search_available = WEB_SEARCH_AVAILABLE
    
    def search(self, query: str, max_results: int = 5) -> List[Dict[str, str]]:
        """Search the web and return results"""
        if not self.search_available:
            return []
        
        try:
            with DDGS() as ddgs:
                results = []
                for r in ddgs.text(query, max_results=max_results):
                    results.append({
                        'title': r.get('title', ''),
                        'url': r.get('href', ''),
                        'snippet': r.get('body', '')
                    })
                return results
        except Exception as e:
            print(f"Search error: {e}")
            return []


class RepoAnalyzer:
    """Analyze repository structure and content"""
    
    def __init__(self):
        self.git_available = GIT_AVAILABLE
    
    def analyze_repo(self, path: str = ".") -> Dict[str, Any]:
        """Analyze a repository and return structured information"""
        repo_info = {
            'path': path,
            'is_git_repo': False,
            'files': [],
            'structure': {},
            'languages': {},
            'total_files': 0
        }
        
        # Check if it's a git repo
        if self.git_available:
            try:
                repo = git.Repo(path, search_parent_directories=True)
                repo_info['is_git_repo'] = True
                repo_info['branch'] = repo.active_branch.name
                repo_info['remote'] = repo.remotes.origin.url if repo.remotes else None
            except:
                pass
        
        # Analyze file structure
        path_obj = Path(path)
        if path_obj.exists():
            # Count files by extension
            for file_path in path_obj.rglob('*'):
                if file_path.is_file():
                    repo_info['total_files'] += 1
                    ext = file_path.suffix.lower()
                    if ext:
                        repo_info['languages'][ext] = repo_info['languages'].get(ext, 0) + 1
                    
                    # Add to file list (limit to prevent overwhelming output)
                    if len(repo_info['files']) < 50:
                        repo_info['files'].append(str(file_path.relative_to(path_obj)))
        
        return repo_info
    
    def get_repo_context(self, path: str = ".") -> str:
        """Get a text summary of the repository"""
        info = self.analyze_repo(path)
        
        context = f"Repository at: {info['path']}\n"
        if info['is_git_repo']:
            context += f"Git branch: {info.get('branch', 'unknown')}\n"
        context += f"Total files: {info['total_files']}\n"
        
        if info['languages']:
            context += "File types:\n"
            for ext, count in sorted(info['languages'].items(), key=lambda x: x[1], reverse=True)[:10]:
                context += f"  {ext}: {count} files\n"
        
        return context


class WorkflowEngine:
    """Multi-step workflow automation engine"""
    
    def __init__(self, cli_instance):
        self.cli = cli_instance
        self.workflows = {
            'code-review': {
                'name': 'Code Review Assistant',
                'steps': [
                    'Analyze repository structure',
                    'Identify main code files',
                    'Review code quality',
                    'Provide improvement suggestions'
                ]
            },
            'debug': {
                'name': 'Debug Assistant',
                'steps': [
                    'Understand the error',
                    'Search for similar issues',
                    'Analyze potential causes',
                    'Suggest fixes'
                ]
            },
            'research': {
                'name': 'Research Assistant',
                'steps': [
                    'Search web for information',
                    'Analyze results',
                    'Synthesize findings',
                    'Provide summary'
                ]
            }
        }
    
    def run_workflow(self, workflow_name: str, context: str, model: Optional[str] = None):
        """Execute a multi-step workflow"""
        if workflow_name not in self.workflows:
            print(f"Unknown workflow: {workflow_name}")
            print(f"Available: {', '.join(self.workflows.keys())}")
            return
        
        workflow = self.workflows[workflow_name]
        
        if RICH_AVAILABLE:
            console = Console()
            console.print(f"\n[bold cyan]🔄 Starting Workflow: {workflow['name']}[/bold cyan]\n")
        else:
            print(f"\n🔄 Starting Workflow: {workflow['name']}\n")
        
        results = []
        
        # Execute each step
        for i, step in enumerate(workflow['steps'], 1):
            if RICH_AVAILABLE:
                console.print(f"[yellow]Step {i}/{len(workflow['steps'])}: {step}[/yellow]")
            else:
                print(f"Step {i}/{len(workflow['steps'])}: {step}")
            
            # Build step-specific prompt
            step_prompt = f"{context}\n\nTask: {step}\nPrevious context: {' '.join(results[-2:]) if results else 'None'}"
            
            # Execute step
            try:
                self.cli.initialize_client()
                provider_info = self.cli.PROVIDERS[self.cli.current_provider]
                
                if not model:
                    provider_config = self.cli.config.get_provider_config(self.cli.current_provider)
                    model = provider_config.get('default_model', provider_info['default_model'])
                
                if self.cli.current_provider == 'ollama':
                    response = self.cli.client.chat(model, messages=[{'role': 'user', 'content': step_prompt}], stream=False)
                    result = response.get('message', {}).get('content', '')
                else:
                    response = self.cli.client.chat.completions.create(
                        model=model,
                        messages=[{"role": "user", "content": step_prompt}],
                        stream=False
                    )
                    result = response.choices[0].message.content
                
                results.append(result)
                
                if RICH_AVAILABLE:
                    console.print(Panel(result[:500] + ("..." if len(result) > 500 else ""), 
                                      title=f"Step {i} Result", border_style="green"))
                else:
                    print(f"Result: {result[:300]}...")
                
                time.sleep(1)  # Brief pause between steps
                
            except Exception as e:
                print(f"Error in step {i}: {e}")
                break
        
        if RICH_AVAILABLE:
            console.print(f"\n[bold green]✅ Workflow Complete![/bold green]\n")
        else:
            print("\n✅ Workflow Complete!\n")
        
        # Award XP for workflow completion
        if hasattr(self.cli, 'gamification'):
            self.cli.gamification.workflows_completed += 1
            self.cli.gamification.add_xp(50, "workflow completion")
            
            # Check for first workflow achievement
            if self.cli.gamification.workflows_completed == 1:
                self.cli.gamification.add_achievement("First Workflow Master")


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
        
        # Initialize gamification system
        self.gamification = GamificationSystem(config_dir)
    
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
        self.gamification = self.config.gamification
        self.web_searcher = WebSearcher()
        self.repo_analyzer = RepoAnalyzer()
        self.workflow_engine = WorkflowEngine(self)
        self.console = Console() if RICH_AVAILABLE else None
    
    def show_welcome(self):
        """Display welcome message with Chico theme"""
        if FIGLET_AVAILABLE:
            try:
                figlet = pyfiglet.figlet_format("CHICO CLI", font="slant")
                if RICH_AVAILABLE:
                    self.console.print(f"[bold cyan]{figlet}[/bold cyan]")
                else:
                    print(figlet)
            except:
                pass
        
        # Show ASCII art
        art = random.choice(CHICO_ASCII_ART)
        quote = random.choice(CHICO_QUOTES)
        
        if RICH_AVAILABLE:
            self.console.print(Panel(f"[yellow]{art}[/yellow]\n[green]{quote}[/green]",
                                    title="🐕 Chico Chuwawa AI CLI v3.0", 
                                    border_style="cyan"))
        else:
            print("\n" + "="*60)
            print(art)
            print(quote)
            print("="*60 + "\n")
    
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
    
    def chat(self, message: str, model: Optional[str] = None, stream: bool = True, provider: Optional[str] = None, 
             web_search: bool = False, repo_context: bool = False):
        """Send a chat message to the API"""
        self.initialize_client(provider)
        
        provider_info = self.PROVIDERS[self.current_provider]
        
        # Use default model if not specified
        if not model:
            provider_config = self.config.get_provider_config(self.current_provider)
            model = provider_config.get('default_model', provider_info['default_model'])
        
        # Enhance message with web search if requested
        enhanced_message = message
        if web_search and self.web_searcher.search_available:
            if RICH_AVAILABLE:
                self.console.print("[yellow]🔍 Searching the web...[/yellow]")
            else:
                print("🔍 Searching the web...")
            
            results = self.web_searcher.search(message, max_results=3)
            if results:
                search_context = "\n\nWeb search results:\n"
                for i, r in enumerate(results, 1):
                    search_context += f"{i}. {r['title']}\n   {r['snippet']}\n   URL: {r['url']}\n\n"
                enhanced_message = f"{message}\n{search_context}\nPlease use the above web search results to provide an informed answer."
        
        # Add repository context if requested
        if repo_context:
            if RICH_AVAILABLE:
                self.console.print("[yellow]📁 Analyzing repository...[/yellow]")
            else:
                print("📁 Analyzing repository...")
            
            repo_info = self.repo_analyzer.get_repo_context()
            enhanced_message = f"Repository Context:\n{repo_info}\n\nUser Question: {enhanced_message}"
        
        if RICH_AVAILABLE:
            self.console.print(f"\n[cyan]💬 Sending message to {model} via {provider_info['name']}...[/cyan]\n")
        else:
            print(f"\n💬 Sending message to {model} via {provider_info['name']}...\n")
        
        try:
            if self.current_provider == 'ollama':
                # Use Ollama client
                if stream:
                    print("Response: ", end="", flush=True)
                    for part in self.client.chat(model, messages=[{'role': 'user', 'content': enhanced_message}], stream=True):
                        content = part.get('message', {}).get('content', '')
                        if content:
                            print(content, end="", flush=True)
                    print("\n")
                else:
                    response = self.client.chat(model, messages=[{'role': 'user', 'content': enhanced_message}], stream=False)
                    print("Response:", response.get('message', {}).get('content', ''))
                    print()
            else:
                # OpenRouter and other OpenAI-compatible
                if stream:
                    try:
                        response = self.client.chat.completions.create(
                            model=model,
                            messages=[{"role": "user", "content": enhanced_message}],
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
                                messages=[{"role": "user", "content": enhanced_message}],
                                stream=False
                            )
                            print("Response:", response.choices[0].message.content)
                            print()
                        else:
                            raise
                else:
                    response = self.client.chat.completions.create(
                        model=model,
                        messages=[{"role": "user", "content": enhanced_message}],
                        stream=False
                    )
                    print("Response:", response.choices[0].message.content)
                    print()
            
            # Award XP for chat completion
            self.gamification.chats_completed += 1
            xp_earned = 10 + (5 if web_search else 0) + (5 if repo_context else 0)
            self.gamification.add_xp(xp_earned, "chat completion")
            
            # Check for achievements
            if self.gamification.chats_completed == 1:
                self.gamification.add_achievement("First Chat")
            if web_search and "Web Explorer" not in self.gamification.achievements:
                self.gamification.add_achievement("Web Explorer")
            if repo_context and "Code Navigator" not in self.gamification.achievements:
                self.gamification.add_achievement("Code Navigator")
        
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
        
        # Show welcome
        self.show_welcome()
        
        if RICH_AVAILABLE:
            self.console.print("[bold cyan]🤖 Interactive Chat Mode[/bold cyan]")
            self.console.print(f"[green]Provider:[/green] {provider_info['name']}")
            self.console.print(f"[green]Model:[/green] {model}")
            self.console.print(f"[green]Level:[/green] {self.gamification.level} | [yellow]XP:[/yellow] {self.gamification.xp}/{self.gamification.level * 100} | [cyan]🦴:[/cyan] {self.gamification.bones_collected}")
            self.console.print("[dim]Type 'exit' or 'quit' to end, 'stats' for your progress, 'help' for commands[/dim]\n")
        else:
            print("\n" + "="*60)
            print("  🐕 Chico Chuwawa AI CLI - Built by Max van Heerden")
            print("="*60)
            print(f"\n🤖 Interactive Chat Mode")
            print(f"Provider: {provider_info['name']}")
            print(f"Model: {model}")
            print(f"Level: {self.gamification.level} | XP: {self.gamification.xp}/{self.gamification.level * 100}")
            print("Type 'exit' or 'quit' to end, 'stats' for progress\n")
        
        messages = []
        use_streaming = True
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['exit', 'quit']:
                    if RICH_AVAILABLE:
                        self.console.print("\n[yellow]🐾 Goodbye! Chico will miss you![/yellow]")
                    else:
                        print("\n🐾 Goodbye! Chico will miss you!")
                    break
                
                if user_input.lower() == 'stats':
                    self.gamification.show_stats()
                    continue
                
                if user_input.lower() == 'help':
                    self.show_interactive_help()
                    continue
                
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
                    
                    # Award XP
                    self.gamification.chats_completed += 1
                    self.gamification.add_xp(10, "interactive chat")
                    
                    # Show random Chico encouragement occasionally
                    if random.random() < 0.1:  # 10% chance
                        if RICH_AVAILABLE:
                            self.console.print(f"[dim italic]{random.choice(CHICO_QUOTES)}[/dim italic]")
                        else:
                            print(f"{random.choice(CHICO_QUOTES)}")
                
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
                if RICH_AVAILABLE:
                    self.console.print("\n\n[yellow]🐾 Goodbye! Chico will miss you![/yellow]")
                else:
                    print("\n\n🐾 Goodbye! Chico will miss you!")
                break
            except Exception as e:
                print(f"\nError: {e}\n")
    
    def show_interactive_help(self):
        """Show help for interactive mode"""
        if RICH_AVAILABLE:
            help_text = """
[bold cyan]Interactive Mode Commands:[/bold cyan]

[green]exit/quit[/green] - Exit interactive mode
[green]stats[/green] - Show your level, XP, and achievements
[green]help[/green] - Show this help message

[bold yellow]Tips:[/bold yellow]
• Chat naturally with the AI
• Build on previous messages in the conversation
• Earn XP and level up as you chat!
• Collect bones 🦴 when you level up
            """
            self.console.print(Panel(help_text, border_style="cyan"))
        else:
            print("""
Interactive Mode Commands:
  exit/quit - Exit interactive mode
  stats - Show your level, XP, and achievements  
  help - Show this help message

Tips:
• Chat naturally with the AI
• Build on previous messages
• Earn XP and level up!
            """)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Chico Chuwawa AI CLI v3.0 - Built by Max van Heerden',
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
  
  # Chat with web search
  chico-cli.py chat "Latest AI news" --web-search
  
  # Chat with repository context
  chico-cli.py chat "Review this code" --repo-context
  
  # Use a specific model
  chico-cli.py chat "Explain quantum computing" --model meta-llama/llama-3.3-70b-instruct
  
  # Start interactive chat
  chico-cli.py interactive
  
  # Run a workflow
  chico-cli.py workflow research "Learn about quantum computing"
  
  # Check your stats and achievements
  chico-cli.py stats
  
  # Analyze repository
  chico-cli.py analyze-repo
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
    chat_parser.add_argument('--web-search', action='store_true', help='Enable web search')
    chat_parser.add_argument('--repo-context', action='store_true', help='Include repository context')
    
    # Interactive command
    interactive_parser = subparsers.add_parser('interactive', help='Start interactive chat session')
    interactive_parser.add_argument('--model', help='Model to use')
    interactive_parser.add_argument('--provider', choices=['openrouter', 'ollama'], help='Provider to use')
    
    # Workflow command
    workflow_parser = subparsers.add_parser('workflow', help='Run a multi-step workflow')
    workflow_parser.add_argument('workflow_type', choices=['code-review', 'debug', 'research'], 
                                  help='Type of workflow to run')
    workflow_parser.add_argument('context', help='Context or question for the workflow')
    workflow_parser.add_argument('--model', help='Model to use')
    
    # Stats command
    subparsers.add_parser('stats', help='Show your stats and achievements')
    
    # Analyze repo command
    analyze_parser = subparsers.add_parser('analyze-repo', help='Analyze repository structure')
    analyze_parser.add_argument('--path', default='.', help='Path to repository (default: current directory)')
    
    # Web search command
    search_parser = subparsers.add_parser('search', help='Search the web')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('--max-results', type=int, default=5, help='Maximum results to show')
    
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
        cli.chat(args.message, args.model, stream=not args.no_stream, provider=args.provider,
                web_search=args.web_search, repo_context=args.repo_context)
    
    elif args.command == 'interactive':
        cli.chat_interactive(args.model, args.provider)
    
    elif args.command == 'workflow':
        cli.workflow_engine.run_workflow(args.workflow_type, args.context, args.model)
    
    elif args.command == 'stats':
        cli.gamification.show_stats()
    
    elif args.command == 'analyze-repo':
        repo_info = cli.repo_analyzer.analyze_repo(args.path)
        if RICH_AVAILABLE:
            console = Console()
            table = Table(title=f"📁 Repository Analysis: {args.path}")
            table.add_column("Property", style="cyan")
            table.add_column("Value", style="green")
            
            table.add_row("Path", repo_info['path'])
            table.add_row("Git Repository", "Yes" if repo_info['is_git_repo'] else "No")
            if repo_info['is_git_repo']:
                table.add_row("Branch", repo_info.get('branch', 'N/A'))
            table.add_row("Total Files", str(repo_info['total_files']))
            
            console.print(table)
            
            if repo_info['languages']:
                console.print("\n[bold]File Types:[/bold]")
                for ext, count in sorted(repo_info['languages'].items(), key=lambda x: x[1], reverse=True)[:10]:
                    console.print(f"  {ext}: {count} files")
        else:
            print(f"\n📁 Repository Analysis: {args.path}")
            print(f"  Path: {repo_info['path']}")
            print(f"  Git Repository: {'Yes' if repo_info['is_git_repo'] else 'No'}")
            if repo_info['is_git_repo']:
                print(f"  Branch: {repo_info.get('branch', 'N/A')}")
            print(f"  Total Files: {repo_info['total_files']}")
            if repo_info['languages']:
                print("\nFile Types:")
                for ext, count in sorted(repo_info['languages'].items(), key=lambda x: x[1], reverse=True)[:10]:
                    print(f"  {ext}: {count} files")
    
    elif args.command == 'search':
        if not WEB_SEARCH_AVAILABLE:
            print("Error: Web search requires duckduckgo-search package")
            print("Install with: pip install duckduckgo-search")
            sys.exit(1)
        
        if RICH_AVAILABLE:
            console = Console()
            console.print(f"[yellow]🔍 Searching: {args.query}[/yellow]\n")
        else:
            print(f"🔍 Searching: {args.query}\n")
        
        results = cli.web_searcher.search(args.query, args.max_results)
        
        if results:
            for i, r in enumerate(results, 1):
                if RICH_AVAILABLE:
                    console.print(f"[bold cyan]{i}. {r['title']}[/bold cyan]")
                    console.print(f"[dim]{r['url']}[/dim]")
                    console.print(f"{r['snippet']}\n")
                else:
                    print(f"{i}. {r['title']}")
                    print(f"   {r['url']}")
                    print(f"   {r['snippet']}\n")
        else:
            print("No results found.")
        
        # Award XP for using search
        cli.gamification.add_xp(5, "web search")


if __name__ == '__main__':
    main()

