#!/bin/bash
# Chico Chuwawa AI CLI - Linux/Unix Installation Script
# Built by Max van Heerden
# Version 3.0.0

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}============================================================${NC}"
echo -e "${CYAN}  🐕 Chico Chuwawa AI CLI Installer${NC}"
echo -e "${CYAN}  Built by Max van Heerden${NC}"
echo -e "${CYAN}============================================================${NC}"
echo ""

# Check if Python is installed
echo -e "${YELLOW}Checking Python installation...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓ Python found: $PYTHON_VERSION${NC}"
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version)
    echo -e "${GREEN}✓ Python found: $PYTHON_VERSION${NC}"
    PYTHON_CMD="python"
else
    echo -e "${RED}✗ Python not found!${NC}"
    echo -e "${RED}Please install Python 3.7 or higher${NC}"
    echo -e "${YELLOW}  Ubuntu/Debian: sudo apt-get install python3 python3-pip${NC}"
    echo -e "${YELLOW}  Fedora/RHEL: sudo dnf install python3 python3-pip${NC}"
    echo -e "${YELLOW}  Arch: sudo pacman -S python python-pip${NC}"
    exit 1
fi

# Check if pip is installed
echo -e "${YELLOW}Checking pip installation...${NC}"
if command -v pip3 &> /dev/null; then
    echo -e "${GREEN}✓ pip found${NC}"
    PIP_CMD="pip3"
elif command -v pip &> /dev/null; then
    echo -e "${GREEN}✓ pip found${NC}"
    PIP_CMD="pip"
else
    echo -e "${RED}✗ pip not found!${NC}"
    echo -e "${YELLOW}Installing pip...${NC}"
    $PYTHON_CMD -m ensurepip --default-pip
    PIP_CMD="$PYTHON_CMD -m pip"
fi

# Set installation directory
INSTALL_DIR="$HOME/.local/share/chico-cli"
BIN_DIR="$HOME/.local/bin"

echo ""
echo -e "${CYAN}Installation directory: $INSTALL_DIR${NC}"
echo -e "${CYAN}Binary directory: $BIN_DIR${NC}"

# Create directories if they don't exist
echo ""
echo -e "${YELLOW}Creating installation directories...${NC}"
mkdir -p "$INSTALL_DIR"
mkdir -p "$BIN_DIR"
echo -e "${GREEN}✓ Directories created${NC}"

# Copy or download files
echo ""
echo -e "${YELLOW}Installing Chico Chuwawa CLI files...${NC}"

# If running from repo, copy files
if [ -f "chico-cli.py" ]; then
    echo -e "${YELLOW}Copying files from current directory...${NC}"
    cp -r chico-cli.py requirements.txt chico/ "$INSTALL_DIR/" 2>/dev/null || true
    if [ -f "chico-logo.png" ]; then
        cp chico-logo.png "$INSTALL_DIR/"
    fi
    echo -e "${GREEN}✓ Files copied${NC}"
else
    echo -e "${RED}Error: chico-cli.py not found${NC}"
    echo -e "${YELLOW}Please run this script from the repository directory${NC}"
    exit 1
fi

# Install Python dependencies
echo ""
echo -e "${YELLOW}Installing Python dependencies...${NC}"
cd "$INSTALL_DIR"
$PIP_CMD install -r requirements.txt --user --quiet
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Create executable wrapper script
echo ""
echo -e "${YELLOW}Creating 'chico' command...${NC}"

cat > "$BIN_DIR/chico" << 'EOF'
#!/bin/bash
# Chico CLI wrapper script
INSTALL_DIR="$HOME/.local/share/chico-cli"
PYTHON_CMD="python3"

# Check if python3 exists, fallback to python
if ! command -v python3 &> /dev/null; then
    PYTHON_CMD="python"
fi

exec $PYTHON_CMD "$INSTALL_DIR/chico-cli.py" "$@"
EOF

# Make it executable
chmod +x "$BIN_DIR/chico"
echo -e "${GREEN}✓ 'chico' command created${NC}"

# Check if $HOME/.local/bin is in PATH
echo ""
if [[ ":$PATH:" == *":$BIN_DIR:"* ]]; then
    echo -e "${GREEN}✓ $BIN_DIR is already in PATH${NC}"
else
    echo -e "${YELLOW}⚠️  $BIN_DIR is not in your PATH${NC}"
    echo -e "${YELLOW}Adding to PATH configuration...${NC}"
    
    # Determine shell config file
    if [ -n "$BASH_VERSION" ]; then
        SHELL_CONFIG="$HOME/.bashrc"
    elif [ -n "$ZSH_VERSION" ]; then
        SHELL_CONFIG="$HOME/.zshrc"
    else
        SHELL_CONFIG="$HOME/.profile"
    fi
    
    # Add to PATH if not already there
    if ! grep -q "$BIN_DIR" "$SHELL_CONFIG" 2>/dev/null; then
        echo "" >> "$SHELL_CONFIG"
        echo "# Chico CLI" >> "$SHELL_CONFIG"
        echo "export PATH=\"\$HOME/.local/bin:\$PATH\"" >> "$SHELL_CONFIG"
        echo -e "${GREEN}✓ Added to $SHELL_CONFIG${NC}"
        echo -e "${YELLOW}Run: source $SHELL_CONFIG${NC}"
        echo -e "${YELLOW}Or restart your terminal to use 'chico' command${NC}"
    fi
fi

# Create symlink in /usr/local/bin (if we have permission)
if [ -w "/usr/local/bin" ]; then
    echo ""
    echo -e "${YELLOW}Creating global symlink...${NC}"
    ln -sf "$BIN_DIR/chico" "/usr/local/bin/chico" 2>/dev/null || true
    echo -e "${GREEN}✓ Global 'chico' command available${NC}"
fi

# Installation complete
echo ""
echo -e "${CYAN}============================================================${NC}"
echo -e "${GREEN}  Installation Complete!${NC}"
echo -e "${CYAN}============================================================${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo -e "${NC}1. Get your API key from:${NC}"
echo -e "${CYAN}   - OpenRouter: https://openrouter.ai/${NC}"
echo -e "${CYAN}   - Ollama Cloud: https://ollama.com/${NC}"
echo ""
echo -e "${NC}2. Configure your provider:${NC}"
echo -e "   ${NC}chico config openrouter --api-key YOUR_KEY${NC}"
echo ""
echo -e "${NC}3. Start chatting:${NC}"
echo -e "   ${NC}chico chat \"Hello Chico!\"${NC}"
echo -e "   ${NC}chico interactive${NC}"
echo ""
echo -e "${YELLOW}For help: chico --help${NC}"
echo ""
echo -e "${GREEN}🐕 Chico Chuwawa AI CLI is ready!${NC}"
echo ""

# Show test command
echo -e "${YELLOW}Testing installation...${NC}"
if command -v chico &> /dev/null; then
    echo -e "${GREEN}✓ 'chico' command is available!${NC}"
    echo -e "${CYAN}Try: chico --help${NC}"
else
    echo -e "${YELLOW}⚠️  'chico' command not yet available in current session${NC}"
    echo -e "${YELLOW}Please restart your terminal or run:${NC}"
    echo -e "${CYAN}  source ~/.bashrc${NC}"
    echo -e "${CYAN}Or use: $BIN_DIR/chico${NC}"
fi
