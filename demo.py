#!/usr/bin/env python3
"""
Demo script showing Chico Chihuahua CLI animations in action
"""

import subprocess
import sys
import time

def run_command(description, command):
    """Run a command and show its output"""
    print("\n" + "="*80)
    print(f"DEMO: {description}")
    print("="*80)
    print(f"Command: {command}")
    print("-"*80)
    
    result = subprocess.run(command, shell=True, capture_output=False, text=True)
    time.sleep(1)
    return result.returncode

def main():
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║          CHICO CHIHUAHUA CLI - ANIMATION DEMO                 ║
    ║          Tiny Dog, Big Power!                                 ║
    ║                                                               ║
    ╔═══════════════════════════════════════════════════════════════╗
    """)
    
    time.sleep(1)
    
    # Demo 1: Show providers
    run_command(
        "List available providers",
        "python3 chico-cli.py providers"
    )
    
    # Demo 2: Show help
    run_command(
        "Display help message",
        "python3 chico-cli.py --help"
    )
    
    print("\n\n" + "="*80)
    print("✨ DEMO COMPLETE! ✨")
    print("The Chico Chihuahua CLI now has amazing animations!")
    print("Small dog with BIG presentation power! 🐕⚡")
    print("="*80)

if __name__ == "__main__":
    main()
