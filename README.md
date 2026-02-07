# Chico Chuwawa AI CLI v3.0

![Chico Chuwawa Logo](chico-logo.png)

**Built by Max van Heerden**  
**Version 3.0.0**

A comprehensive command-line interface (CLI) tool with multi-provider AI support, beautiful animations, persistent chat history, internet search, MCP server integrations, desktop app connections, WhatsApp integration, and more!

## 🌟 What's New in v3.0

### 🎨 Visual Enhancements
- **ASCII Chihuahua Animation** - Animated welcome screen with Chihuahua mascot
- **Coding-Themed Loading Messages** - Fun, developer-focused waiting indicators
- **Syntax Highlighting** - Automatic code block highlighting with Pygments
- **Rich Console Output** - Beautiful, colorful terminal interface

### 💾 Persistent Features
- **Chat History** - All conversations saved to SQLite database
- **Session Management** - Resume previous chats anytime
- **Builder Markers** - Mark important points in conversations
- **Search History** - Find previous conversations by content

### 🔗 Integrations & Connections
- **MCP Servers** - GitHub, Railway, Vercel, Office 365, Zoho (CRM/Desk/Invoice)
- **Desktop Apps** - Connect to Manus AI, DeepSeek, Claude, ChatGPT
- **Internet Search** - DuckDuckGo integration for coding solutions
- **WhatsApp** - QR code connection for monitoring and prompting

### 🌍 Cross-Platform Installation
- **Linux/Unix** - One-line installer with global `chico` command
- **Windows** - PowerShell installer with PATH configuration
- **pip** - Install via `pip install chico-cli`
- **All Platforms** - Works on Windows, macOS, Linux, Ubuntu, Debian

## 📦 Installation

### Quick Install (Linux/Unix/macOS)

```bash
curl -fsSL https://raw.githubusercontent.com/CA0071/chico-chuwawa-cli/main/install.sh | bash
```

Or download and run:
```bash
git clone https://github.com/CA0071/chico-chuwawa-cli.git
cd chico-chuwawa-cli
chmod +x install.sh
./install.sh
```

### Quick Install (Windows PowerShell)

```powershell
iwr -useb https://raw.githubusercontent.com/CA0071/chico-chuwawa-cli/main/install.ps1 | iex
```

Or download and run:
```powershell
git clone https://github.com/CA0071/chico-chuwawa-cli.git
cd chico-chuwawa-cli
powershell -ExecutionPolicy Bypass -File install.ps1
```

### Install via pip (All Platforms)

```bash
pip install git+https://github.com/CA0071/chico-chuwawa-cli.git
```

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

## 🚀 Quick Start

### 1. Configure Your AI Provider

```bash
# OpenRouter (recommended - 500+ models)
chico config openrouter --api-key YOUR_OPENROUTER_KEY

# Ollama Cloud
chico config ollama --api-key YOUR_OLLAMA_KEY
```

Get your API keys:
- **OpenRouter**: [openrouter.ai](https://openrouter.ai/)
- **Ollama Cloud**: [ollama.com](https://ollama.com/)

### 2. Start Chatting!

```bash
# Simple chat
chico chat "What is AI?"

# Interactive mode with animation
chico interactive --banner

# Chat with code search
chico chat "How to sort array in Python?" --search

# Save conversation to history
chico chat "Explain async/await" --save
```

## 💬 Usage Examples

### Basic Chat

```bash
# Quick question
chico chat "What is the capital of France?"

# Use specific model
chico chat "Explain quantum computing" --model "anthropic/claude-3.5-sonnet"

# Use specific provider
chico chat "Write a poem" --provider ollama --model "gpt-oss:120b-cloud"
```

### Interactive Chat Mode

```bash
# Start interactive session
chico interactive

# With specific model
chico interactive --model "google/gemini-2.0-flash-exp"

# With welcome animation
chico interactive --banner

# Without saving history
chico interactive --no-save
```

### Chat History

```bash
# View recent sessions
chico history

# View last 20 sessions
chico history --limit 20
```

### Code Search

```bash
# General search
chico search "python async programming"

# Stack Overflow search
chico search "javascript promises" --source stackoverflow

# GitHub search
chico search "rust async" --source github
```

### Provider Management

```bash
# List all providers
chico providers

# Switch active provider
chico switch ollama

# List available models
chico models

# List models for specific provider
chico models --provider openrouter
```

### WhatsApp Integration

```bash
# Setup WhatsApp connection
chico whatsapp
# Scan QR code with your phone
```

## 🎨 Visual Features

### ASCII Chihuahua Animation

When you run `chico interactive --banner`, you'll see:
- Animated Chihuahua mascot
- ASCII art logo
- Beautiful colored output

### Syntax Highlighting

Code blocks in AI responses are automatically highlighted:
```python
def hello_world():
    print("Hello from Chico!")
```

### Loading Messages

While waiting for AI responses, you'll see fun messages like:
- 🔨 Compiling your thoughts...
- 🧠 Neural networks processing...
- 💡 Generating brilliant code...

## 🔧 Advanced Features

### MCP Server Integrations

Connect to various services for enhanced functionality:

```python
# Example: GitHub integration
from chico.integrations.mcp_servers import GitHubMCP

github = GitHubMCP({'api_token': 'YOUR_TOKEN', 'sandbox_mode': True})
github.connect()
github.execute('list_repos', {})
```

Supported services:
- **GitHub** - Repository management, issue creation
- **Railway** - Deployment automation
- **Vercel** - Deployment and hosting
- **Office 365** - Email and calendar
- **Zoho CRM/Desk/Invoice** - Business operations

### Desktop App Connections

Connect to AI desktop applications:

```python
# Example: Claude desktop app
from chico.integrations.desktop_apps import ClaudeApp

claude = ClaudeApp({'api_url': 'http://localhost:5003'})
if claude.connect():
    response = claude.send_message("Hello!")
```

Supported apps:
- Manus AI
- DeepSeek
- Claude AI
- ChatGPT

### Internet Search for Coding

Automatically search for coding solutions:

```bash
# Chat with automatic search
chico chat "How to implement binary search in Python?" --search
```

This will:
1. Search Stack Overflow and other sources
2. Include relevant results in the AI context
3. Provide more accurate, up-to-date answers

## 📋 Command Reference

### Configuration Commands

| Command | Description |
|---------|-------------|
| `chico config openrouter --api-key KEY` | Configure OpenRouter |
| `chico config ollama --api-key KEY` | Configure Ollama Cloud |
| `chico config PROVIDER --api-key KEY --default-model MODEL` | Set default model |
| `chico providers` | List all providers |
| `chico switch PROVIDER` | Switch active provider |

### Chat Commands

| Command | Description |
|---------|-------------|
| `chico chat "message"` | Send message with default settings |
| `chico chat "message" --model MODEL` | Use specific model |
| `chico chat "message" --search` | Include web search |
| `chico chat "message" --save` | Save to history |
| `chico interactive` | Start interactive chat |
| `chico interactive --banner` | Show welcome animation |
| `chico interactive --no-save` | Don't save history |

### History Commands

| Command | Description |
|---------|-------------|
| `chico history` | View recent chat sessions |
| `chico history --limit N` | Show last N sessions |

### Search Commands

| Command | Description |
|---------|-------------|
| `chico search "query"` | Search for coding solutions |
| `chico search "query" --source stackoverflow` | Search Stack Overflow |
| `chico search "query" --source github` | Search GitHub |

### Integration Commands

| Command | Description |
|---------|-------------|
| `chico whatsapp` | Setup WhatsApp integration |
| `chico models` | List available AI models |

## 🔑 Configuration

### Configuration File Location

- **Windows**: `%APPDATA%\ChicoChuwawa-CLI\config.json`
- **Linux/Mac**: `~/.config/chico-cli/config.json`

### Configuration Format

```json
{
  "openrouter": {
    "api_key": "sk-or-v1-xxxxx",
    "default_model": "meta-llama/llama-3.3-70b-instruct"
  },
  "ollama": {
    "api_key": "ollama_xxxxx",
    "default_model": "gpt-oss:120b-cloud"
  },
  "active_provider": "openrouter",
  "integrations": {
    "github": {
      "api_token": "ghp_xxxxx",
      "sandbox_mode": true
    }
  }
}
```

### Environment Variables

You can also use environment variables:

```bash
# Linux/Mac
export OPENROUTER_API_KEY=your_key
export OLLAMA_API_KEY=your_key

# Windows
set OPENROUTER_API_KEY=your_key
set OLLAMA_API_KEY=your_key
```

## 🎯 Popular Models

### OpenRouter Models

**Best Overall:**
- `anthropic/claude-3.5-sonnet` - Excellent reasoning and coding
- `google/gemini-2.0-flash-exp` - Fast and capable
- `meta-llama/llama-3.3-70b-instruct` - Open source powerhouse

**Coding:**
- `anthropic/claude-3.5-sonnet` - Best for complex code
- `qwen/qwen-2.5-coder-32b-instruct` - Specialized coding model
- `deepseek/deepseek-coder` - Strong coding capabilities

**Fast & Efficient:**
- `google/gemini-2.0-flash-exp` - Very fast responses
- `meta-llama/llama-3.1-8b-instruct` - Lightweight
- `mistralai/mistral-7b-instruct` - Efficient and capable

### Ollama Cloud Models

- `gpt-oss:120b-cloud` - Large, capable model
- `deepseek-v3.1:671b-cloud` - Massive model with reasoning
- `qwen3-coder:480b-cloud` - Specialized for coding
- `gpt-oss:20b-cloud` - Smaller, faster option

## 🏗️ Project Structure

```
chico-chuwawa-cli/
├── chico/                    # Main package
│   ├── core/                # Core functionality
│   ├── integrations/        # MCP servers & desktop apps
│   │   ├── mcp_servers.py  # GitHub, Railway, Vercel, etc.
│   │   ├── desktop_apps.py # Manus, DeepSeek, Claude, ChatGPT
│   │   └── whatsapp.py     # WhatsApp integration
│   ├── ui/                  # User interface components
│   │   ├── animations.py   # ASCII art and animations
│   │   ├── loading.py      # Loading spinners
│   │   └── syntax.py       # Code highlighting
│   └── utils/              # Utilities
│       ├── history.py      # Chat history management
│       └── search.py       # Internet search
├── chico-cli.py            # Main CLI application
├── requirements.txt        # Python dependencies
├── setup.py               # pip installation
├── install.sh             # Linux/Unix installer
└── install.ps1            # Windows installer
```

## 🔐 Security

- API keys stored in config directory (plain text)
- Use file permissions to protect config files
- Environment variables recommended for CI/CD
- Sandbox mode available for MCP servers
- Never commit config files to version control

## 🐛 Troubleshooting

### "No API key found"
**Solution**: Configure the provider first
```bash
chico config openrouter --api-key YOUR_KEY
```

### "chico command not found"
**Solution**: Add to PATH or restart terminal
```bash
# Linux/Mac
source ~/.bashrc
# Or
export PATH="$HOME/.local/bin:$PATH"
```

### Import Errors
**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### Enhanced features not available
**Solution**: Install optional dependencies
```bash
pip install pygments rich colorama duckduckgo-search qrcode
```

## 📚 Resources

- **GitHub**: [github.com/CA0071/chico-chuwawa-cli](https://github.com/CA0071/chico-chuwawa-cli)
- **OpenRouter**: [openrouter.ai](https://openrouter.ai/)
- **OpenRouter Docs**: [openrouter.ai/docs](https://openrouter.ai/docs)
- **Ollama Cloud**: [ollama.com/cloud](https://ollama.com/cloud)

## 🎉 What's New in v3.0

- ✅ **Modular Architecture** - Clean, maintainable code structure
- ✅ **ASCII Animations** - Beautiful Chihuahua mascot and logo
- ✅ **Syntax Highlighting** - Automatic code block highlighting
- ✅ **Persistent History** - SQLite-based chat history
- ✅ **Internet Search** - DuckDuckGo integration for coding help
- ✅ **MCP Server Framework** - GitHub, Railway, Vercel, Office 365, Zoho
- ✅ **Desktop App Connections** - Manus, DeepSeek, Claude, ChatGPT
- ✅ **WhatsApp Integration** - QR code connection for mobile access
- ✅ **Cross-Platform Installers** - Linux, Windows, macOS support
- ✅ **Enhanced Error Handling** - Better error messages and recovery
- ✅ **Loading Animations** - Fun coding-themed messages
- ✅ **Global Command** - Use `chico` anywhere on your system

## 🤝 Contributing

Contributions welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

## 📄 License

Free for personal and commercial use.

## 🙏 Credits

**Built by**: Max van Heerden  
**Version**: 3.0.0  
**Year**: 2026

---

**Chico Chuwawa AI CLI** - Your comprehensive AI companion! 🐕✨
