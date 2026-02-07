"""
ASCII Art and Animation Module
Provides visual enhancements including Chihuahua animations and logos
"""

import time
import sys
from typing import List

# ASCII Chihuahua frames for animation
CHIHUAHUA_FRAMES = [
    r"""
       /\_/\  
      ( o.o ) 
       > ^ <  
      /|   |\
     (_|   |_)
    """,
    r"""
       /\_/\  
      ( ^.^ ) 
       > - <  
      /|   |\
     (_|   |_)
    """,
    r"""
       /\_/\  
      ( o.o ) 
       > v <  
      /|   |\
     (_|   |_)
    """
]

CHIHUAHUA_LOGO = r"""
   _____ _     _                _____ _     _ 
  / ____| |   (_)              / ____| |   (_)
 | |    | |__  _  ___ ___     | |    | |__  _ 
 | |    | '_ \| |/ __/ _ \    | |    | '_ \| |
 | |____| | | | | (_| (_) |   | |____| | | | |
  \_____|_| |_|_|\___\___/     \_____|_| |_|_|
                                              
        🐕 Your AI Companion 🐕
"""

def show_animated_chihuahua(duration: float = 2.0, clear: bool = False):
    """
    Display an animated Chihuahua
    
    Args:
        duration: How long to show the animation in seconds
        clear: Whether to clear the screen before animation
    """
    try:
        from rich.console import Console
        console = Console()
        
        if clear:
            console.clear()
        
        frames_to_show = int(duration / 0.3)
        for i in range(frames_to_show):
            frame = CHIHUAHUA_FRAMES[i % len(CHIHUAHUA_FRAMES)]
            console.print(frame, style="cyan")
            time.sleep(0.3)
            if i < frames_to_show - 1:
                # Move cursor up to overwrite
                console.print(f"\033[{len(frame.split('\n'))}A", end="")
    except ImportError:
        # Fallback without rich
        print(CHIHUAHUA_FRAMES[0])

def show_logo():
    """Display the Chico Chuwawa logo"""
    try:
        from rich.console import Console
        console = Console()
        console.print(CHIHUAHUA_LOGO, style="bold cyan")
    except ImportError:
        print(CHIHUAHUA_LOGO)

def show_welcome_banner():
    """Display welcome banner with animation"""
    show_animated_chihuahua(duration=1.5)
    print()
    show_logo()
    print()
