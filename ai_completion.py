"""
AI-Powered Auto-Completion
Provides intelligent command suggestions and completions
"""

from typing import List, Dict, Any, Optional
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.document import Document


class AICommandCompleter(Completer):
    """AI-powered command completer"""
    
    def __init__(self, ai_client=None):
        self.ai_client = ai_client
        
        # Define command structure
        self.commands = {
            'welcome': [],
            'providers': [],
            'config': ['openrouter', 'ollama'],
            'switch': ['openrouter', 'ollama'],
            'models': ['--provider'],
            'chat': ['--model', '--provider', '--no-stream'],
            'interactive': ['--model', '--provider'],
            'integrations': [],
            'hub-status': [],
            'docker': ['containers', 'images', 'logs'],
            'k8s': ['pods', 'deployments', 'services', '--namespace'],
            'npm': ['search', 'info'],
            'pypi': ['info'],
        }
        
        self.providers = ['openrouter', 'ollama']
    
    def get_completions(self, document: Document, complete_event):
        """Get command completions"""
        text = document.text_before_cursor
        words = text.split()
        
        # Root level commands
        if len(words) == 0 or (len(words) == 1 and not text.endswith(' ')):
            for cmd in self.commands.keys():
                if cmd.startswith(text):
                    yield Completion(cmd, start_position=-len(text))
        
        # Subcommands
        elif len(words) >= 1:
            main_cmd = words[0]
            if main_cmd in self.commands:
                current_word = words[-1] if not text.endswith(' ') else ''
                
                for subcmd in self.commands[main_cmd]:
                    if subcmd.startswith(current_word):
                        yield Completion(subcmd, start_position=-len(current_word))


class AICommandSuggester:
    """Provides AI-driven command suggestions based on context"""
    
    def __init__(self, ai_client=None):
        self.ai_client = ai_client
        self.command_history = []
        self.context = {}
    
    def suggest_next_command(self, current_state: Dict[str, Any]) -> List[str]:
        """Suggest next commands based on current state"""
        suggestions = []
        
        # If no integrations are healthy, suggest checking status
        if current_state.get('unhealthy_integrations', 0) > 0:
            suggestions.append("hub-status  # Check integration health")
            suggestions.append("integrations  # View integration details")
        
        # If Docker is available, suggest Docker commands
        if current_state.get('docker_available'):
            suggestions.append("docker containers  # List Docker containers")
            suggestions.append("docker images  # List Docker images")
        
        # If Kubernetes is available
        if current_state.get('k8s_available'):
            suggestions.append("k8s pods  # List Kubernetes pods")
            suggestions.append("k8s deployments  # List deployments")
        
        # Always suggest chat
        suggestions.append("chat 'your question'  # Ask AI a question")
        suggestions.append("interactive  # Start interactive chat")
        
        return suggestions
    
    def analyze_command(self, command: str) -> Dict[str, Any]:
        """Analyze a command and provide insights"""
        parts = command.split()
        
        analysis = {
            'command': parts[0] if parts else '',
            'subcommand': parts[1] if len(parts) > 1 else '',
            'flags': [p for p in parts if p.startswith('--')],
            'args': [p for p in parts if not p.startswith('--')]
        }
        
        # Add context-specific suggestions
        if analysis['command'] == 'docker':
            analysis['tips'] = [
                "Use 'docker logs <container_id>' to view container logs",
                "Add '--all' flag to see stopped containers"
            ]
        elif analysis['command'] == 'k8s':
            analysis['tips'] = [
                "Use '--namespace <ns>' to specify a namespace",
                "Default namespace is 'default'"
            ]
        
        return analysis
    
    def get_smart_defaults(self, command: str) -> Dict[str, Any]:
        """Get intelligent defaults for a command"""
        defaults = {}
        
        if 'chat' in command or 'interactive' in command:
            defaults['model'] = 'meta-llama/llama-3.3-70b-instruct'
            defaults['provider'] = 'openrouter'
            defaults['streaming'] = True
        
        elif 'docker' in command:
            defaults['show_all'] = True
        
        elif 'k8s' in command:
            defaults['namespace'] = 'default'
        
        return defaults
    
    def add_to_history(self, command: str):
        """Add command to history for learning"""
        self.command_history.append(command)
        
        # Keep only last 100 commands
        if len(self.command_history) > 100:
            self.command_history = self.command_history[-100:]
    
    def get_frequent_commands(self, limit: int = 5) -> List[str]:
        """Get most frequently used commands"""
        from collections import Counter
        
        if not self.command_history:
            return []
        
        counter = Counter(self.command_history)
        return [cmd for cmd, _ in counter.most_common(limit)]


def create_interactive_session(completer: AICommandCompleter) -> PromptSession:
    """Create an interactive prompt session with auto-completion"""
    return PromptSession(
        completer=completer,
        complete_while_typing=True,
        enable_history_search=True
    )
