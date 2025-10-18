"""
Chico Chuwawa AI CLI - Build Script
Built by: Max van Heerden

Build script for creating Windows executable using PyInstaller
"""

import os
import sys
import subprocess

def install_pyinstaller():
    """Install PyInstaller if not already installed"""
    try:
        import PyInstaller
        print("✓ PyInstaller is already installed")
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✓ PyInstaller installed successfully")

def build_executable():
    """Build the Windows executable"""
    print("\n🔨 Building Windows executable...")
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",  # Create a single executable file
        "--name=chico-cli",  # Name of the executable
        "--console",  # Console application
        "--clean",  # Clean PyInstaller cache
        "--add-data=chico-logo.png;.",  # Include logo
        "chico-cli.py"
    ]
    
    try:
        subprocess.check_call(cmd)
        print("\n✓ Build completed successfully!")
        print("\n📦 Executable location: dist/chico-cli.exe")
        print("\n🐕 Chico Chuwawa AI CLI - Built by Max van Heerden")
        print("\nTo use the CLI:")
        print("  1. Copy dist/chico-cli.exe to a directory in your PATH")
        print("  2. Or run it directly: .\\dist\\chico-cli.exe")
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Build failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("=" * 60)
    print("🐕 Chico Chuwawa AI CLI - Executable Builder")
    print("Built by: Max van Heerden")
    print("=" * 60)
    
    install_pyinstaller()
    build_executable()

