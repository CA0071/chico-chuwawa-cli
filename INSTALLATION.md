# Chico Chuwawa AI CLI - Installation Guide

## Quick Installation

### Linux / Unix / macOS

**One-Line Install:**
```bash
curl -fsSL https://raw.githubusercontent.com/CA0071/chico-chuwawa-cli/main/install.sh | bash
```

**Or Manual Install:**
```bash
git clone https://github.com/CA0071/chico-chuwawa-cli.git
cd chico-chuwawa-cli
chmod +x install.sh
./install.sh
```

After installation, restart your terminal or run:
```bash
source ~/.bashrc
```

Then test with:
```bash
chico --help
```

### Windows PowerShell

**One-Line Install:**
```powershell
iwr -useb https://raw.githubusercontent.com/CA0071/chico-chuwawa-cli/main/install.ps1 | iex
```

**Or Manual Install:**
```powershell
git clone https://github.com/CA0071/chico-chuwawa-cli.git
cd chico-chuwawa-cli
powershell -ExecutionPolicy Bypass -File install.ps1
```

Then test with:
```powershell
chico --help
```

### Via pip (All Platforms)

```bash
pip install git+https://github.com/CA0071/chico-chuwawa-cli.git
```

## Detailed Installation

### Prerequisites

1. **Python 3.7+**
   - Linux/Mac: Usually pre-installed
   - Windows: Download from [python.org](https://www.python.org/downloads/)
   - **Important**: Check "Add Python to PATH" during installation

2. **pip** (Python package manager)
   - Usually comes with Python
   - If missing: `python -m ensurepip --default-pip`

3. **Git** (optional, for cloning repository)
   - Linux: `sudo apt-get install git`
   - Mac: `brew install git`
   - Windows: Download from [git-scm.com](https://git-scm.com/)

### Platform-Specific Instructions

#### Ubuntu / Debian

```bash
# 1. Install prerequisites
sudo apt-get update
sudo apt-get install -y python3 python3-pip git

# 2. Clone repository
git clone https://github.com/CA0071/chico-chuwawa-cli.git
cd chico-chuwawa-cli

# 3. Run installer
chmod +x install.sh
./install.sh

# 4. Reload shell configuration
source ~/.bashrc

# 5. Test installation
chico --help
```

#### Fedora / RHEL / CentOS

```bash
# 1. Install prerequisites
sudo dnf install -y python3 python3-pip git

# 2. Clone repository
git clone https://github.com/CA0071/chico-chuwawa-cli.git
cd chico-chuwawa-cli

# 3. Run installer
chmod +x install.sh
./install.sh

# 4. Reload shell configuration
source ~/.bashrc

# 5. Test installation
chico --help
```

#### Arch Linux

```bash
# 1. Install prerequisites
sudo pacman -S python python-pip git

# 2. Clone repository
git clone https://github.com/CA0071/chico-chuwawa-cli.git
cd chico-chuwawa-cli

# 3. Run installer
chmod +x install.sh
./install.sh

# 4. Reload shell configuration
source ~/.bashrc

# 5. Test installation
chico --help
```

#### macOS

```bash
# 1. Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Install prerequisites
brew install python git

# 3. Clone repository
git clone https://github.com/CA0071/chico-chuwawa-cli.git
cd chico-chuwawa-cli

# 4. Run installer
chmod +x install.sh
./install.sh

# 5. Reload shell configuration
source ~/.zshrc  # or ~/.bashrc

# 6. Test installation
chico --help
```

#### Windows

**Option 1: PowerShell (Recommended)**

```powershell
# 1. Open PowerShell as Administrator

# 2. Install Python (if not installed)
# Download from https://www.python.org/downloads/
# Check "Add Python to PATH" during installation

# 3. Install Git (if not installed)
# Download from https://git-scm.com/

# 4. Clone repository
git clone https://github.com/CA0071/chico-chuwawa-cli.git
cd chico-chuwawa-cli

# 5. Run installer
powershell -ExecutionPolicy Bypass -File install.ps1

# 6. Restart PowerShell

# 7. Test installation
chico --help
```

**Option 2: Python Script**

```powershell
# 1. Clone repository
git clone https://github.com/CA0071/chico-chuwawa-cli.git
cd chico-chuwawa-cli

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run directly
python chico-cli.py --help

# 4. Create alias (optional)
# Add to PowerShell profile:
New-Item -ItemType File -Path $PROFILE -Force
Add-Content $PROFILE 'function chico { python C:\path\to\chico-cli.py $args }'
```

## Post-Installation Setup

### 1. Configure AI Provider

Get your API key from:
- **OpenRouter**: [openrouter.ai](https://openrouter.ai/) (500+ models)
- **Ollama Cloud**: [ollama.com](https://ollama.com/) (cloud models)

Then configure:
```bash
chico config openrouter --api-key YOUR_API_KEY
```

### 2. Test Basic Chat

```bash
chico chat "Hello, Chico!"
```

### 3. Try Interactive Mode

```bash
chico interactive --banner
```

### 4. View Available Models

```bash
chico models
```

## Installing Enhanced Features

The basic installation includes core AI chat functionality. For enhanced features, install additional dependencies:

```bash
# Full feature set
pip install pygments colorama rich qrcode pillow duckduckgo-search

# Or using requirements.txt
cd /path/to/chico-chuwawa-cli
pip install -r requirements.txt
```

### Enhanced Features:
- 🎨 **Syntax Highlighting** (pygments)
- 🌈 **Colored Output** (colorama, rich)
- 📱 **QR Codes** (qrcode, pillow)
- 🔍 **Internet Search** (duckduckgo-search)
- 📊 **Chat History** (built-in SQLite)

## Making 'chico' a Global Command

### Linux / Unix / macOS

The installer automatically adds `chico` to your PATH. If it's not working:

**Option 1: Add to PATH manually**
```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

**Option 2: Create system-wide symlink (requires sudo)**
```bash
sudo ln -s $HOME/.local/bin/chico /usr/local/bin/chico
```

### Windows

**Option 1: Add to System PATH**
1. Open "Environment Variables" (Win + S, search "environment")
2. Edit "Path" under "User variables"
3. Add: `%USERPROFILE%\ChicoChuwawa-CLI`
4. Click OK and restart terminal

**Option 2: PowerShell Function**
```powershell
# Add to PowerShell profile
notepad $PROFILE
# Add this line:
function chico { python $HOME\ChicoChuwawa-CLI\chico-cli.py $args }
```

## Verification

After installation, verify all features work:

```bash
# Check version
chico --help

# Test configuration
chico providers

# Test basic chat (requires API key)
chico config openrouter --api-key YOUR_KEY
chico chat "Hello!"

# Test enhanced features
chico history
chico search "python async"
```

## Troubleshooting

### Command not found

**Linux/Mac:**
```bash
# Check if installed
ls -la ~/.local/bin/chico

# Check PATH
echo $PATH

# Add to PATH if missing
export PATH="$HOME/.local/bin:$PATH"
```

**Windows:**
```powershell
# Check if installed
dir $HOME\ChicoChuwawa-CLI\chico-cli.py

# Use full path temporarily
python $HOME\ChicoChuwawa-CLI\chico-cli.py --help
```

### Permission denied

**Linux/Mac:**
```bash
chmod +x ~/.local/bin/chico
chmod +x /path/to/chico-cli.py
```

### Python not found

**Linux:**
```bash
# Try python3
python3 chico-cli.py --help

# Install Python
sudo apt-get install python3 python3-pip
```

**Windows:**
```powershell
# Download from https://www.python.org/
# Make sure to check "Add Python to PATH"
```

### Import errors

```bash
# Install dependencies
pip install -r requirements.txt

# Or minimal install
pip install openai requests
```

### Enhanced features unavailable

```bash
# Install optional dependencies
pip install pygments colorama rich qrcode pillow duckduckgo-search
```

## Upgrading

To upgrade to the latest version:

```bash
# Pull latest changes
cd /path/to/chico-chuwawa-cli
git pull

# Reinstall
./install.sh  # Linux/Mac
# or
powershell -ExecutionPolicy Bypass -File install.ps1  # Windows

# Update dependencies
pip install -r requirements.txt --upgrade
```

## Uninstallation

### Linux / Mac

```bash
# Remove binary
rm ~/.local/bin/chico

# Remove installation directory
rm -rf ~/.local/share/chico-cli

# Remove configuration
rm -rf ~/.config/chico-cli

# Remove from PATH (edit ~/.bashrc and remove the export line)
```

### Windows

```powershell
# Remove installation directory
Remove-Item -Recurse -Force $HOME\ChicoChuwawa-CLI

# Remove configuration
Remove-Item -Recurse -Force $env:APPDATA\ChicoChuwawa-CLI

# Remove from PATH (through Environment Variables GUI)
```

## Support

If you encounter issues:
1. Check this guide thoroughly
2. Review the main [README.md](README.md)
3. Open an issue on [GitHub](https://github.com/CA0071/chico-chuwawa-cli/issues)

---

**Chico Chuwawa AI CLI** - Your comprehensive AI companion! 🐕✨
