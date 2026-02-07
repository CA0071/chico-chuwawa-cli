# Chico Chuwawa AI CLI

![Chico Chuwawa Logo](chico-logo.png)

**Built by Max van Heerden**  
**Version 3.0.0 - Enhanced Edition** 🐕✨

A powerful, feature-rich command-line interface (CLI) tool that combines the best of Qwen, Claude AI, and Gemini CLIs with unique Chihuahua-themed gamification! Access hundreds of AI models, run multi-step workflows, search the web, analyze repositories, and level up as you go!

## 🌟 Features

### 🎯 Core AI Capabilities
- **Multi-Provider Support**: OpenRouter and Ollama Cloud integration
- **Hundreds of Models**: Access models from OpenAI, Anthropic, Google, Meta, Mistral, DeepSeek, Qwen, and more
- **Easy Provider Switching**: Switch between providers with a single command
- **Interactive Chat Mode**: Multi-turn conversations with context
- **Streaming Responses**: Real-time response streaming with automatic fallback
- **Flexible Configuration**: Per-provider API keys and default models
- **No GPT Lock-in**: Choose your own models from any supported provider

### 🔄 Advanced Agentic Workflows (Qwen-style)
- **Multi-Step Automation**: Run complex workflows that break down tasks into steps
- **Code Review Workflow**: Automatically analyze repo structure, review code quality, and provide suggestions
- **Debug Assistant**: Understand errors, search for solutions, analyze causes, and suggest fixes
- **Research Assistant**: Search the web, analyze results, synthesize findings, and provide summaries
- **Workflow Persistence**: Track completed workflows and earn rewards

### 📚 Deep Repository Understanding (Claude-style)
- **Repository Analysis**: Automatically understand your project structure
- **Git Integration**: Detect branches, commits, and repository metadata
- **File Type Recognition**: Identify programming languages and file distributions
- **Context-Aware Responses**: Include repo context in your AI conversations
- **Project Summarization**: Get quick overviews of any codebase

### 🌐 Multimodality & Web Search (Gemini-style)
- **Web Search Integration**: Search the web directly from the CLI using DuckDuckGo
- **Enhanced Responses**: Augment AI responses with real-time web data
- **Citation Support**: Get sources and URLs with your answers
- **Research Mode**: Combine AI reasoning with current information
- **Multimodal Ready**: Architecture supports future image and document analysis

### 🎮 Unique Chico Features
- **🐕 Chihuahua Theme**: Adorable ASCII art and themed interactions
- **✨ Beautiful UI**: Rich terminal interface with colors, panels, and tables
- **🎯 Gamification System**: 
  - Earn XP for every command
  - Level up and collect bones 🦴
  - Unlock achievements (First Chat, Web Explorer, Code Navigator, etc.)
  - Track your progress with detailed stats
- **🎨 Animations**: Dynamic ASCII art and encouraging messages from Chico
- **🎪 Easter Eggs**: Random fun interactions and Chico quotes
- **📊 Progress Tracking**: Persistent stats across sessions

### 🔧 Integration & Tools
- **Command History**: Track all your commands and interactions
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Open Source**: Fully open and extensible
- **Plugin Ready**: Modular architecture for future extensions
- **Configuration Management**: Secure API key storage and settings

## 🚀 Supported Providers

### OpenRouter
Access 500+ models from multiple providers:
- **Anthropic**: Claude 3.5 Sonnet, Claude 3 Opus
- **Google**: Gemini 2.0 Flash, Gemini Pro
- **Meta**: Llama 3.3 70B, Llama 3.1 405B
- **Mistral**: Mistral Large, Mixtral
- **DeepSeek**: DeepSeek V3
- **Qwen**: Qwen 2.5 72B
- And many more!

### Ollama Cloud
Cloud-hosted models without local GPU:
- `gpt-oss:120b-cloud`
- `deepseek-v3.1:671b-cloud`
- `gpt-oss:20b-cloud`
- `kimi-k2:1t-cloud`
- `qwen3-coder:480b-cloud`
- `glm-4.6:cloud`

## 📦 Installation

### Prerequisites
- Python 3.7 or higher
- Windows, macOS, or Linux

### Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `openai` - OpenAI-compatible API client
- `ollama` - Ollama Cloud client
- `requests` - HTTP library
- `rich` - Beautiful terminal UI (colors, tables, panels)
- `beautifulsoup4` - Web scraping for enhanced features
- `duckduckgo-search` - Web search integration
- `gitpython` - Git repository analysis
- `pillow` - Image processing (for future multimodal features)
- `pyfiglet` - ASCII art generation

## 🔑 Configuration

### Get Your API Keys

#### OpenRouter
1. Visit [openrouter.ai](https://openrouter.ai/)
2. Sign up or log in
3. Go to Keys section
4. Create a new API key
5. Copy your key (starts with `sk-or-v1-...`)

#### Ollama Cloud
1. Visit [ollama.com](https://ollama.com/)
2. Sign up or log in
3. Go to [API keys](https://ollama.com/settings/keys)
4. Create a new API key
5. Copy your key

### Configure Providers

#### Configure OpenRouter

```bash
python chico-cli.py config openrouter --api-key YOUR_OPENROUTER_KEY
```

With a default model:
```bash
python chico-cli.py config openrouter --api-key YOUR_KEY --default-model "meta-llama/llama-3.3-70b-instruct"
```

#### Configure Ollama Cloud

```bash
python chico-cli.py config ollama --api-key YOUR_OLLAMA_KEY
```

With a default model:
```bash
python chico-cli.py config ollama --api-key YOUR_KEY --default-model "gpt-oss:120b-cloud"
```

### View Configured Providers

```bash
python chico-cli.py providers
```

Output:
```
📋 Available Providers:
------------------------------------------------------------
  • OpenRouter (openrouter)
    Status: ✓ Configured ✓ Active
    Default model: meta-llama/llama-3.3-70b-instruct

  • Ollama Cloud (ollama)
    Status: ✓ Configured 
    Default model: gpt-oss:120b-cloud
```

### Switch Active Provider

```bash
python chico-cli.py switch ollama
```

## 💬 Usage

### List Available Models

List models from active provider:
```bash
python chico-cli.py models
```

List models from specific provider:
```bash
python chico-cli.py models --provider openrouter
python chico-cli.py models --provider ollama
```

### Send a Single Message

Using active provider and default model:
```bash
python chico-cli.py chat "What is artificial intelligence?"
```

Using specific model:
```bash
python chico-cli.py chat "Explain quantum computing" --model "anthropic/claude-3.5-sonnet"
```

Using specific provider:
```bash
python chico-cli.py chat "Write a poem" --provider ollama --model "gpt-oss:120b-cloud"
```

Disable streaming:
```bash
python chico-cli.py chat "Tell me a joke" --no-stream
```

### 🔍 Enhanced Chat with Web Search

Search the web and get AI-powered answers with citations:
```bash
python chico-cli.py chat "What are the latest developments in AI?" --web-search
```

The AI will search DuckDuckGo, retrieve relevant results, and provide an informed answer with sources!

### 📁 Chat with Repository Context

Analyze your code repository and ask questions:
```bash
python chico-cli.py chat "Review the code structure" --repo-context
```

Chico will analyze your repository, understand the file structure, and provide context-aware responses!

### 🔄 Multi-Step Workflows

Run intelligent workflows that break down complex tasks:

**Research Assistant** - Search, analyze, and synthesize:
```bash
python chico-cli.py workflow research "Learn about quantum computing applications"
```

**Code Review** - Analyze repo, review code, suggest improvements:
```bash
python chico-cli.py workflow code-review "Review this project for best practices"
```

**Debug Assistant** - Understand, search, analyze, and fix:
```bash
python chico-cli.py workflow debug "My API endpoint is returning 500 errors"
```

### 🌐 Web Search

Search the web directly from CLI:
```bash
python chico-cli.py search "Python best practices 2024"
```

Get top results with titles, URLs, and snippets!

### 📊 Track Your Progress

View your stats, level, XP, and achievements:
```bash
python chico-cli.py stats
```

Example output:
```
🐕 Chico's Stats
┏━━━━━━━━━━━━━━━━━┳━━━━━━━┓
┃ Stat            ┃ Value ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━┩
│ Level           │ 5     │
│ XP              │ 250/500│
│ Commands Used   │ 47    │
│ Chats Completed │ 23    │
│ Workflows Done  │ 3     │
│ 🦴 Bones        │ 15    │
│ 🏆 Achievements │ 5     │
└─────────────────┴───────┘

Achievements:
  🏆 First Chat
  🏆 Web Explorer
  🏆 Code Navigator
  🏆 First Workflow Master
  🏆 Level 5 Hero
```

### 🔍 Analyze Repository

Get detailed analysis of any codebase:
```bash
python chico-cli.py analyze-repo
```

Or analyze a specific path:
```bash
python chico-cli.py analyze-repo --path /path/to/project
```

### Interactive Chat Mode

Start interactive chat with default settings:
```bash
python chico-cli.py interactive
```

You'll see:
```
============================================================
  🐕 Chico Chuwawa AI CLI - Built by Max van Heerden
============================================================

🤖 Interactive Chat Mode
Provider: OpenRouter
Model: meta-llama/llama-3.3-70b-instruct
Type 'exit' or 'quit' to end the session

You: 
```

With specific model:
```bash
python chico-cli.py interactive --model "google/gemini-2.0-flash-exp"
```

With specific provider:
```bash
python chico-cli.py interactive --provider ollama --model "deepseek-v3.1:671b-cloud"
```

## 📋 Command Reference

### Configuration Commands

| Command | Description |
|---------|-------------|
| `config openrouter --api-key KEY` | Configure OpenRouter |
| `config ollama --api-key KEY` | Configure Ollama Cloud |
| `config PROVIDER --api-key KEY --default-model MODEL` | Set default model |
| `providers` | List all providers and their status |
| `switch PROVIDER` | Switch active provider |

### Model Commands

| Command | Description |
|---------|-------------|
| `models` | List models from active provider |
| `models --provider PROVIDER` | List models from specific provider |

### Chat Commands

| Command | Description |
|---------|-------------|
| `chat "message"` | Send message with default settings |
| `chat "message" --model MODEL` | Use specific model |
| `chat "message" --provider PROVIDER` | Use specific provider |
| `chat "message" --no-stream` | Disable streaming |
| `chat "message" --web-search` | Enable web search |
| `chat "message" --repo-context` | Include repository context |
| `interactive` | Start interactive chat |
| `interactive --model MODEL` | Interactive with specific model |
| `interactive --provider PROVIDER` | Interactive with specific provider |

### Workflow Commands

| Command | Description |
|---------|-------------|
| `workflow code-review "context"` | Run code review workflow |
| `workflow debug "issue"` | Run debug assistant workflow |
| `workflow research "topic"` | Run research assistant workflow |

### Utility Commands

| Command | Description |
|---------|-------------|
| `stats` | Show your level, XP, and achievements |
| `analyze-repo` | Analyze current repository |
| `analyze-repo --path PATH` | Analyze specific repository |
| `search "query"` | Search the web |
| `search "query" --max-results N` | Limit search results |

| Command | Description |
|---------|-------------|
| `chat "message"` | Send message with default settings |
| `chat "message" --model MODEL` | Use specific model |
| `chat "message" --provider PROVIDER` | Use specific provider |
| `chat "message" --no-stream` | Disable streaming |
| `interactive` | Start interactive chat |
| `interactive --model MODEL` | Interactive with specific model |
| `interactive --provider PROVIDER` | Interactive with specific provider |

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

**Creative Writing:**
- `anthropic/claude-3.5-sonnet` - Creative and nuanced
- `google/gemini-pro` - Good for creative tasks
- `meta-llama/llama-3.3-70b-instruct` - Strong creative abilities

### Ollama Cloud Models

- `gpt-oss:120b-cloud` - Large, capable model
- `deepseek-v3.1:671b-cloud` - Massive model with reasoning
- `qwen3-coder:480b-cloud` - Specialized for coding
- `gpt-oss:20b-cloud` - Smaller, faster option

## 📖 Examples

### Example 1: Quick Question with OpenRouter

```bash
# Configure OpenRouter
python chico-cli.py config openrouter --api-key sk-or-v1-xxxxx

# Ask a question
python chico-cli.py chat "What are the benefits of renewable energy?"
```

### Example 2: Web-Enhanced Research

```bash
# Search the web and get AI-powered answer
python chico-cli.py chat "What are the latest AI breakthroughs in 2024?" --web-search

# The AI will:
# 1. Search DuckDuckGo for relevant results
# 2. Analyze the findings
# 3. Provide a comprehensive answer with sources
```

### Example 3: Repository Code Review Workflow

```bash
# Navigate to your project directory
cd /path/to/your/project

# Run the code review workflow
python chico-cli.py workflow code-review "Please review this codebase for best practices"

# Chico will:
# 1. Analyze the repository structure
# 2. Identify main code files
# 3. Review code quality
# 4. Provide improvement suggestions
# You earn 50 XP and unlock achievements!
```

### Example 4: Debug with Context

```bash
# Get help debugging with repository awareness
python chico-cli.py chat "Why is my API returning 500 errors?" --repo-context

# Or use the debug workflow
python chico-cli.py workflow debug "API endpoint failing with 500 status code"
```

### Example 5: Interactive Chat with Gamification

```bash
python chico-cli.py interactive --model "google/gemini-2.0-flash-exp"

# You'll see:
    /\_/\  
   ( ^.^ ) 
    > * <  Let's go!
   /|   |\
  (_|   |_)

🐕 Woof! Ready to fetch some answers!

🤖 Interactive Chat Mode
Provider: OpenRouter
Model: google/gemini-2.0-flash-exp
Level: 1 | XP: 0/100 | 🦴: 0
Type 'stats' to see your progress!

You: What is quantum computing?
AI: [AI provides detailed explanation]
+10 XP! 💪 Tiny but mighty!

You: stats
🐕 Chico's Stats
Level: 1 | XP: 10/100
Chats: 1 | Achievements: 1

You: exit
🐾 Goodbye! Chico will miss you!
```

### Example 6: Track Your Progress

```bash
# Check your stats anytime
python chico-cli.py stats

# Output shows:
# - Current level
# - XP progress
# - Commands used
# - Chats completed
# - Workflows completed
# - Bones collected 🦴
# - Achievements unlocked 🏆
```

### Example 7: Search the Web Directly

```bash
# Quick web search
python chico-cli.py search "Python best practices 2024" --max-results 5

# Returns titles, URLs, and snippets from top results
# Earn 5 XP for exploring!
```

### Example 8: Analyze Any Repository

```bash
# Analyze your current project
python chico-cli.py analyze-repo

# Or analyze another project
python chico-cli.py analyze-repo --path /path/to/other/project

# See:
# - Git information
# - File count
# - Language breakdown
# - Project structure
```

### Example 9: Research Workflow

```bash
# Deep research on a topic
python chico-cli.py workflow research "Machine learning applications in healthcare"

# Chico will:
# 1. Search for information
# 2. Analyze results
# 3. Synthesize findings
# 4. Provide a comprehensive summary
```

### Example 10: Compare Models

```bash
# Try with Llama
python chico-cli.py chat "Write a haiku about AI" \
  --model "meta-llama/llama-3.3-70b-instruct"

# Try with Claude
python chico-cli.py chat "Write a haiku about AI" \
  --model "anthropic/claude-3.5-sonnet"

# Try with Gemini
python chico-cli.py chat "Write a haiku about AI" \
  --model "google/gemini-2.0-flash-exp"
```

## 🔧 Advanced Configuration

### Environment Variables

You can also use environment variables (they override config file):

```bash
# Windows
set OPENROUTER_API_KEY=your_key
set OLLAMA_API_KEY=your_key

# Linux/Mac
export OPENROUTER_API_KEY=your_key
export OLLAMA_API_KEY=your_key
```

### Configuration File Location

- **Windows**: `%APPDATA%\ChicoChuwawa-CLI\config.json`
- **Linux/Mac**: `~/.config/chico-cli/config.json`

### Configuration File Format

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
  "active_provider": "openrouter"
}
```

## 🏗️ Building Windows Executable

### Build the Executable

```bash
python build_windows.py
```

This creates `dist/chico-cli.exe` - a standalone executable that includes:
- All Python dependencies
- The Chico Chuwawa logo
- Configuration management

### Using the Executable

```bash
# Configure
chico-cli.exe config openrouter --api-key YOUR_KEY

# Chat
chico-cli.exe chat "Hello!"

# Interactive
chico-cli.exe interactive
```

### Add to PATH

1. Copy `chico-cli.exe` to `C:\Tools\` (or your preferred location)
2. Add `C:\Tools\` to your Windows PATH
3. Open new Command Prompt and type: `chico-cli --help`

## 🐛 Troubleshooting

### "No API key found"

**Solution**: Configure the provider first:
```bash
python chico-cli.py config openrouter --api-key YOUR_KEY
```

### "Unknown provider"

**Solution**: Use `openrouter` or `ollama`:
```bash
python chico-cli.py providers  # List available providers
```

### "Provider not configured"

**Solution**: Configure before switching:
```bash
python chico-cli.py config ollama --api-key YOUR_KEY
python chico-cli.py switch ollama
```

### Import Errors

**Solution**: Install dependencies:
```bash
pip install -r requirements.txt
```

### Model Not Found

**Solution**: List available models:
```bash
python chico-cli.py models
```

Use the exact model ID from the list.

### Rate Limits

OpenRouter and Ollama have rate limits. If you hit them:
- Wait a few seconds and try again
- Use a different model
- Check your account limits on the provider's website

## 💰 Pricing

### OpenRouter
- Pay-per-use pricing
- Varies by model
- Check [openrouter.ai/models](https://openrouter.ai/models) for current prices
- Free tier available for some models

### Ollama Cloud
- Currently in preview
- Check [ollama.com/cloud](https://ollama.com/cloud) for pricing details

## 🔐 Security

- API keys are stored in plain text in config file
- Ensure proper file permissions on your system
- Don't commit config files to version control
- Use environment variables for CI/CD pipelines
- Rotate API keys regularly

## 📚 Resources

- **OpenRouter**: [openrouter.ai](https://openrouter.ai/)
- **OpenRouter Docs**: [openrouter.ai/docs](https://openrouter.ai/docs)
- **OpenRouter Models**: [openrouter.ai/models](https://openrouter.ai/models)
- **Ollama Cloud**: [ollama.com/cloud](https://ollama.com/cloud)
- **Ollama Docs**: [docs.ollama.com](https://docs.ollama.com/)

## 🎉 What's New in v3.0 - Enhanced Edition

### 🔄 Agentic Workflows (Qwen-style)
- ✅ **Multi-Step Automation**: Code review, debug, and research workflows
- ✅ **Intelligent Task Breakdown**: Complex tasks split into manageable steps
- ✅ **Progress Tracking**: See each step execute in real-time
- ✅ **Workflow Templates**: Pre-built workflows for common tasks

### 📚 Repository Understanding (Claude-style)
- ✅ **Repository Analysis**: Automatic project structure detection
- ✅ **Git Integration**: Branch, commit, and metadata awareness
- ✅ **Context-Aware Chat**: Include repo context in conversations
- ✅ **File Type Recognition**: Understand your codebase composition

### 🌐 Web Search & Multimodality (Gemini-style)
- ✅ **Web Search Integration**: DuckDuckGo search built-in
- ✅ **Enhanced Responses**: Augment AI with real-time data
- ✅ **Citation Support**: Get sources with your answers
- ✅ **Research Mode**: Combine AI reasoning with current info

### 🎮 Unique Chico Features
- ✅ **Gamification System**: Earn XP, level up, collect bones 🦴
- ✅ **Achievement System**: Unlock achievements for milestones
- ✅ **Beautiful UI**: Rich terminal with colors, tables, and panels
- ✅ **Chihuahua Theme**: Adorable ASCII art and fun interactions
- ✅ **Progress Persistence**: Your stats save between sessions
- ✅ **Encouraging Messages**: Chico cheers you on!

### Previous Features (v2.0)
- ✅ **OpenRouter Integration**: Access 500+ models
- ✅ **Ollama Cloud Support**: Cloud-hosted models
- ✅ **Multi-Provider System**: Switch between providers easily
- ✅ **No GPT Lock-in**: Use any model you want
- ✅ **Improved Configuration**: Per-provider settings
- ✅ **Better Error Handling**: Clear error messages
- ✅ **Model Discovery**: List available models per provider

## 🤝 About

**Chico Chuwawa AI CLI v3.0** combines the strengths of the best AI CLIs:
- **Qwen's** multi-step agentic workflows
- **Claude's** deep repository understanding
- **Gemini's** multimodality and web search
- **Chico's** unique gamification and Chihuahua charm!

No lock-in to specific providers or models - use what works best for your needs, while having fun and leveling up!

**Built by**: Max van Heerden  
**Version**: 3.0.0 - Enhanced Edition  
**License**: Free for personal and commercial use  
**Open Source**: Fully extensible and customizable

---

**Chico Chuwawa AI CLI** - Your gateway to hundreds of AI models with style! 🐕✨🎮

