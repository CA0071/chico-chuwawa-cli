# Chico Chuwawa AI CLI - Quick Start Guide

![Chico Logo](chico-logo.png)

**Built by Max van Heerden** | **Version 2.1.0**

Get started with Chico Chuwawa AI CLI in 5 minutes! Access hundreds of AI models from OpenRouter, Ollama Cloud, Hugging Face, and Qwen.

## Prerequisites

- Windows, macOS, or Linux PC with Python 3.7+ installed
- API key from one or more providers:
  - **OpenRouter** (recommended for variety)
  - **Ollama Cloud** (cloud-hosted models)
  - **Hugging Face** (open-source models)
  - **Qwen** (Alibaba's powerful models)

## Getting Your API Keys

### OpenRouter (Recommended for Beginners)
1. Visit [openrouter.ai](https://openrouter.ai/)
2. Sign up (free)
3. Go to Keys → Create new key
4. Copy your key (starts with `sk-or-v1-...`)

### Ollama Cloud
1. Visit [ollama.com](https://ollama.com/)
2. Sign up
3. Go to Settings → API Keys
4. Create and copy your key

### Hugging Face
1. Visit [huggingface.co](https://huggingface.co/)
2. Sign up (free)
3. Go to Settings → Access Tokens
4. Create new token (read access is enough)
5. Copy your token

### Qwen (DashScope)
1. Visit [dashscope.aliyun.com](https://dashscope.aliyun.com/)
2. Sign up (Alibaba Cloud account)
3. Go to API Keys section
4. Create and copy your key

## Installation

### 1. Extract the Files

Extract to your desired location:
```
C:\Tools\chico-cli
```

### 2. Open Command Prompt/Terminal

**Windows**: Press `Win + R`, type `cmd`, press Enter

**Mac/Linux**: Open Terminal

### 3. Navigate to Folder

```bash
cd C:\Tools\chico-cli
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs all required packages including the interactive menu system.

### 5. Run Interactive Setup (Easiest!)

```bash
python chico-cli.py setup
```

The wizard will guide you through:
1. Choosing your provider
2. Entering your API key
3. Selecting a default model
4. Testing your first message

**That's it!** You're ready to use the CLI.

### Alternative: Manual Configuration

If you prefer manual setup:

**For OpenRouter:**
```bash
python chico-cli.py config openrouter --api-key YOUR_OPENROUTER_KEY
```

**For Ollama Cloud:**
```bash
python chico-cli.py config ollama --api-key YOUR_OLLAMA_KEY
```

**For Hugging Face:**
```bash
python chico-cli.py config huggingface --api-key YOUR_HF_TOKEN
```

**For Qwen:**
```bash
python chico-cli.py config qwen --api-key YOUR_QWEN_KEY
```

## Basic Usage

### Interactive Menu (Easiest)

Just run without arguments:
```bash
python chico-cli.py
```

Or:
```bash
python chico-cli.py menu
```

This shows a menu with options:
- Start interactive chat
- Send a quick message
- List available models
- Switch provider
- Configure new provider

### Quick Chat

```bash
python chico-cli.py chat "What is artificial intelligence?"
```

### List Available Models

```bash
python chico-cli.py models
```

### Use Specific Model

```bash
python chico-cli.py chat "Explain Python" --model "anthropic/claude-3.5-sonnet"
```

### Interactive Chat

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

## Popular Models to Try

### OpenRouter Models

**Best Overall:**
```bash
python chico-cli.py chat "Your question" --model "anthropic/claude-3.5-sonnet"
python chico-cli.py chat "Your question" --model "google/gemini-2.0-flash-exp"
python chico-cli.py chat "Your question" --model "meta-llama/llama-3.3-70b-instruct"
```

**For Coding:**
```bash
python chico-cli.py chat "Write a Python function" --model "qwen/qwen-2.5-coder-32b-instruct"
```

### Ollama Cloud Models

```bash
python chico-cli.py chat "Your question" --provider ollama --model "gpt-oss:120b-cloud"
python chico-cli.py chat "Your question" --provider ollama --model "deepseek-v3.1:671b-cloud"
```

### Hugging Face Models

```bash
python chico-cli.py chat "Your question" --provider huggingface --model "meta-llama/Meta-Llama-3-8B-Instruct"
python chico-cli.py chat "Your question" --provider huggingface --model "mistralai/Mistral-7B-Instruct-v0.2"
```

### Qwen Models

```bash
python chico-cli.py chat "Your question" --provider qwen --model "qwen-turbo"
python chico-cli.py chat "Your question" --provider qwen --model "qwen-plus"
```

## Common Commands

| Command | Description |
|---------|-------------|
| `python chico-cli.py` or `python chico-cli.py menu` | Interactive quick menu |
| `python chico-cli.py setup` | Interactive setup wizard |
| `python chico-cli.py providers` | List all providers |
| `python chico-cli.py models` | List available models |
| `python chico-cli.py chat "message"` | Send a message |
| `python chico-cli.py interactive` | Start interactive chat |
| `python chico-cli.py switch PROVIDER` | Switch provider |
| `python chico-cli.py --help` | Show all commands |

## Tips

### 1. Use Batch File (Windows)

Instead of typing `python chico-cli.py`:
```bash
chico-cli.bat chat "Hello!"
```

### 2. Set Default Model

```bash
python chico-cli.py config openrouter --api-key YOUR_KEY --default-model "anthropic/claude-3.5-sonnet"
```

### 3. Configure Multiple Providers

```bash
# Configure all providers
python chico-cli.py config openrouter --api-key KEY1
python chico-cli.py config ollama --api-key KEY2
python chico-cli.py config huggingface --api-key KEY3
python chico-cli.py config qwen --api-key KEY4

# Switch between them
python chico-cli.py switch huggingface
python chico-cli.py switch qwen
python chico-cli.py switch openrouter
```

### 4. Build Executable

```bash
python build_windows.py
```

Creates `dist/chico-cli.exe` - no Python needed!

## Troubleshooting

**"python is not recognized"**
- Install Python from [python.org](https://python.org)
- Check "Add Python to PATH" during installation

**"No API key found"**
- Run: `python chico-cli.py config openrouter --api-key YOUR_KEY`

**"Provider not configured"**
- Configure before switching: `python chico-cli.py config PROVIDER --api-key KEY`

**"Model not found"**
- List models: `python chico-cli.py models`
- Use exact model ID from the list

## Next Steps

- Read the full [README.md](README.md) for all features
- Try different models to find your favorite
- Use interactive mode for conversations
- Build the executable for easy distribution

## Quick Examples

### Example 1: First Time Setup
```bash
# Run the setup wizard
python chico-cli.py setup

# Follow the interactive prompts
# It will guide you through everything!
```

### Example 2: Ask a Question
```bash
python chico-cli.py chat "What are the benefits of renewable energy?"
```

### Example 3: Try Different Providers
```bash
# With OpenRouter
python chico-cli.py chat "Explain AI" --provider openrouter

# With Hugging Face
python chico-cli.py chat "Explain AI" --provider huggingface

# With Qwen
python chico-cli.py chat "Explain AI" --provider qwen
```

### Example 4: Code Generation
```bash
python chico-cli.py chat "Write a Python function to sort a list" --model "anthropic/claude-3.5-sonnet"
```

### Example 5: Creative Writing
```bash
python chico-cli.py chat "Write a short story about a robot" --model "meta-llama/llama-3.3-70b-instruct"
```

### Example 6: Interactive Conversation
```bash
python chico-cli.py interactive --model "google/gemini-2.0-flash-exp"
```

---

**You're all set!** Start chatting with Chico Chuwawa AI! 🐕✨

For detailed documentation, see [README.md](README.md)

**Version 2.1.0** - Now with 4 AI providers and interactive menus!

