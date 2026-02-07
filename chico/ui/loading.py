"""
Coding-themed waiting messages and loading indicators
"""

import random
import itertools
import time
import sys
from typing import Optional

CODING_MESSAGES = [
    "🔨 Compiling your thoughts...",
    "⚙️  Running AI inference...",
    "🧠 Neural networks processing...",
    "💡 Generating brilliant code...",
    "🔍 Searching the knowledge base...",
    "🚀 Deploying logic circuits...",
    "📚 Consulting the docs...",
    "🎯 Optimizing the response...",
    "🔧 Debugging the universe...",
    "💻 sudo thinking...",
    "🎨 Painting with pixels...",
    "🌐 Traversing the internet...",
    "🔬 Running experiments...",
    "🎭 Training the model...",
    "🏗️  Building your solution...",
    "🎪 Juggling tokens...",
    "🔮 Consulting the AI oracle...",
    "⚡ Charging neural pathways...",
    "🎵 Harmonizing algorithms...",
    "🌟 Channeling digital wisdom...",
]

class LoadingSpinner:
    """Animated loading spinner with coding messages"""
    
    def __init__(self, message: Optional[str] = None):
        self.message = message or random.choice(CODING_MESSAGES)
        self.spinner = itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
        self.running = False
    
    def start(self):
        """Start the loading spinner"""
        self.running = True
    
    def stop(self):
        """Stop the loading spinner"""
        self.running = False
        sys.stdout.write('\r' + ' ' * (len(self.message) + 5) + '\r')
        sys.stdout.flush()
    
    def spin_once(self):
        """Display one frame of the spinner"""
        if self.running:
            sys.stdout.write(f'\r{next(self.spinner)} {self.message}')
            sys.stdout.flush()

def get_random_message() -> str:
    """Get a random coding-themed message"""
    return random.choice(CODING_MESSAGES)

def show_thinking_animation(duration: float = 1.0):
    """
    Show a thinking animation for a specified duration
    
    Args:
        duration: How long to show the animation in seconds
    """
    spinner = LoadingSpinner()
    spinner.start()
    
    end_time = time.time() + duration
    while time.time() < end_time:
        spinner.spin_once()
        time.sleep(0.1)
    
    spinner.stop()
