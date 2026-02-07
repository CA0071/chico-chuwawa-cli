#!/usr/bin/env python3
"""
Chico Chihuahua Animations Module
A collection of ASCII animations featuring our tiny but mighty Chihuahua hero
Theme: "Small dog, big power" - A pocket-sized white apple head Chihuahua achieving big feats
"""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.spinner import Spinner
from rich.live import Live
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
import time
import random

console = Console()

# ASCII Art - Chico the Chihuahua (white apple head breed, small and cute)
CHICO_SITTING = r"""
    /\_/\  
   ( o.o ) 
    > ^ <
   /|   |\
  (_|   |_)
"""

CHICO_CODING = r"""
    /\_/\  ⌨️
   ( ^.^ ) 💻
    > ^ <  
   /|█▓▒|\  
  (_|░▒▓|_)
  ═══════
"""

CHICO_LAUNCHING = r"""
    /\_/\  🚀
   ( ⊙.⊙) ✨
    > ^ <  
   /| ↑ |\  
  (_| ↑ |_)
   ═══════
"""

CHICO_SEARCHING = r"""
    /\_/\  🔍
   ( ◉.◉ ) 
    > ^ <  
   /|   |\🌐
  (_|   |_)
  ═══════
"""

CHICO_SUCCESS = r"""
    /\_/\  ⭐
   ( ^‿^ ) ✨
    > ^ <  
   /| ✓ |\  
  (_| ✓ |_)
  ═══════
"""

CHICO_POWER = r"""
    /\_/\  ⚡
   ( ◉‿◉ ) 💪
    > ^ <  
   /|⚡⚡|\  
  (_|⚡⚡|_)
  ═══════
"""

# Animated sequences
CHICO_RUNNING_FRAMES = [
    r"""
    /\_/\  
   ( o.o ) 
    > ^ <
   /|   |\
  ⌇|   |⌇
""",
    r"""
    /\_/\  
   ( o.o ) 
    > ^ <
  /|   |\
 (_|   |_)
""",
    r"""
    /\_/\  
   ( o.o ) 
    > ^ <
  ⌇|   |⌇
   |     |
"""
]

CHICO_WORKING_FRAMES = [
    (CHICO_CODING, "Typing code..."),
    (CHICO_SEARCHING, "Searching APIs..."),
    (CHICO_LAUNCHING, "Launching requests..."),
    (CHICO_POWER, "Processing power!"),
]


def show_banner():
    """Display the Chico Chihuahua banner"""
    banner_text = Text()
    banner_text.append("🐕 ", style="bold yellow")
    banner_text.append("CHICO CHIHUAHUA", style="bold cyan")
    banner_text.append(" 🐕\n", style="bold yellow")
    banner_text.append("Tiny Dog, Big Power!", style="italic magenta")
    
    panel = Panel(
        banner_text,
        border_style="bright_cyan",
        padding=(1, 2),
    )
    console.print(panel)


def show_chico_art(art_type="sitting", message=None):
    """Display Chico ASCII art with optional message"""
    art_map = {
        "sitting": CHICO_SITTING,
        "coding": CHICO_CODING,
        "launching": CHICO_LAUNCHING,
        "searching": CHICO_SEARCHING,
        "success": CHICO_SUCCESS,
        "power": CHICO_POWER,
    }
    
    art = art_map.get(art_type, CHICO_SITTING)
    
    if message:
        console.print(f"[cyan]{art}[/cyan]")
        console.print(f"[bold yellow]{message}[/bold yellow]")
    else:
        console.print(f"[cyan]{art}[/cyan]")


def loading_animation(task_description, duration=2):
    """Show a loading animation with Chico working hard"""
    messages = [
        "🐾 Tiny paws, big actions...",
        "⚡ Small but mighty...",
        "💪 Chihuahua power activating...",
        "🚀 Launching with pocket-sized energy...",
    ]
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task(f"[cyan]{task_description}[/cyan]", total=None)
        
        for _ in range(int(duration * 2)):  # Roughly the duration
            time.sleep(0.5)
            progress.update(task, description=f"[cyan]{random.choice(messages)}[/cyan]")


def animated_working(message="Working...", duration=1.5):
    """Show Chico animating through different work poses"""
    frames = CHICO_WORKING_FRAMES
    iterations = int(duration / (len(frames) * 0.3))
    
    # Note: Animation disabled to avoid clearing terminal. Use static art instead.
    # If needed, this could be re-enabled with in-place updates using rich.live
    art, status = frames[0]
    console.print(f"[cyan]{art}[/cyan]")
    console.print(f"[bold yellow]{message} - {status}[/bold yellow]")


def success_animation(message="Success!"):
    """Show a success animation with Chico celebrating"""
    console.print("\n")
    console.print(f"[green]{CHICO_SUCCESS}[/green]")
    console.print(f"[bold green]✨ {message} ✨[/bold green]")
    console.print("[italic yellow]Tiny dog achieves big feat! 🏆[/italic yellow]\n")


def error_animation(message="Oops!"):
    """Show an error animation with Chico looking concerned"""
    sad_chico = r"""
    /\_/\  
   ( •́_•̀ ) 
    > ^ <
   /|   |\
  (_|   |_)
"""
    console.print("\n")
    console.print(f"[red]{sad_chico}[/red]")
    console.print(f"[bold red]❌ {message}[/bold red]")
    console.print("[italic]Even mighty Chihuahuas need to try again![/italic]\n")


def transition_animation(from_task, to_task):
    """Show a transition animation between tasks"""
    console.print(f"\n[dim]← {from_task}[/dim]")
    
    # Running animation
    for frame in CHICO_RUNNING_FRAMES * 2:
        console.print(f"[yellow]{frame}[/yellow]", end="\r")
        time.sleep(0.15)
    
    console.print(f"[dim]→ {to_task}[/dim]\n")


def config_success_animation():
    """Special animation for successful configuration"""
    console.print("\n")
    
    config_art = r"""
    /\_/\  ⚙️
   ( ^ᴗ^ ) ✓
    > ^ <  
   /|✓✓✓|\  
  (_|✓✓✓|_)
  ═══════
"""
    
    console.print(f"[green]{config_art}[/green]")
    console.print("[bold green]🎉 Configuration Complete! 🎉[/bold green]")
    console.print("[italic cyan]Tiny Chihuahua configured BIG systems![/italic cyan]\n")


def model_listing_animation():
    """Animation for listing models"""
    console.print("\n")
    console.print(f"[cyan]{CHICO_SEARCHING}[/cyan]")
    console.print("[bold yellow]🔍 Searching through vast model libraries...[/bold yellow]")
    console.print("[italic]Small paws accessing big databases![/italic]\n")


def chat_thinking_spinner(message="Chico is thinking..."):
    """Show a spinner while waiting for chat response"""
    spinners = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    thoughts = [
        "🐾 Processing with pocket-sized neurons...",
        "⚡ Tiny brain, HUGE intelligence...",
        "💭 Chihuahua computing in progress...",
        "🧠 Small head, big thoughts...",
    ]
    
    return thoughts[random.randint(0, len(thoughts) - 1)]


def interactive_start_animation():
    """Animation when starting interactive mode"""
    console.print("\n")
    
    interactive_art = r"""
    /\_/\  💬
   ( ^ω^ ) 
    > ^ <  
   /|   |\  
  (_|▓▒░|_)
  ═══════
"""
    
    console.print(f"[cyan]{interactive_art}[/cyan]")
    console.print("[bold cyan]🐕 Interactive Mode Activated! 🐕[/bold cyan]")
    console.print("[italic yellow]Ready to chat with pocket-sized power![/italic yellow]\n")


def provider_switch_animation(from_provider, to_provider):
    """Animation when switching providers"""
    console.print("\n")
    
    switch_art = r"""
    /\_/\  🔄
   ( ↔.↔ ) 
    > ^ <  
   /|⇄⇄⇄|\  
  (_|⇄⇄⇄|_)
  ═══════
"""
    
    console.print(f"[yellow]{switch_art}[/yellow]")
    console.print(f"[bold yellow]Switching from {from_provider} to {to_provider}...[/bold yellow]")
    console.print("[italic]Little legs running between big platforms![/italic]\n")
    time.sleep(0.8)


def show_motivational_message():
    """Show a random motivational message from Chico"""
    messages = [
        "🐕 'Size doesn't define power!' - Chico",
        "⚡ 'Small but fierce!' - Chico the Mighty",
        "💪 'Pocket-sized but powerful!' - Chico",
        "🚀 'Big dreams in a tiny package!' - Chico",
        "✨ 'Never underestimate a Chihuahua!' - Chico",
        "🏆 'Tiny paws, giant achievements!' - Chico",
    ]
    
    console.print(f"\n[italic magenta]{random.choice(messages)}[/italic magenta]\n")


def big_feat_celebration(feat_name):
    """Celebrate a big feat achieved by tiny Chico"""
    console.print("\n")
    
    celebration = r"""
    /\_/\  🏆✨
   ( ☆ᴗ☆) 🎉
    > ^ <  
   /|⭐⭐|\  
  (_|⭐⭐|_)
  ═══════
"""
    
    console.print(f"[bold yellow]{celebration}[/bold yellow]")
    console.print(f"[bold green]🎊 {feat_name} - ACHIEVED! 🎊[/bold green]")
    console.print("[italic cyan]Tiny Chihuahua conquers another big challenge![/italic cyan]")
    console.print("[bold magenta]Small Dog. BIG POWER! 💪[/bold magenta]\n")
    time.sleep(1)


# Quick display functions for minimal code changes
def quick_loading(message="Loading..."):
    """Quick loading message with Chico"""
    console.print(f"[yellow]🐾 {message}[/yellow]")


def quick_success(message="Done!"):
    """Quick success message with Chico"""
    console.print(f"[green]✓ {message} 🐕[/green]")


def quick_error(message="Error"):
    """Quick error message with Chico"""
    console.print(f"[red]✗ {message} 😿[/red]")
