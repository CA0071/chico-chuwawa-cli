# Chico Chuwawa AI CLI

![Chico Chuwawa Logo](chico-logo.png)

**Built by Max van Heerden**  
**Version 2.1.0**

A powerful command-line interface (CLI) tool for Windows, macOS, and Linux that integrates with **OpenRouter**, **Ollama Cloud**, **Hugging Face Inference**, and **Qwen (DashScope)** APIs. Access hundreds of AI models from multiple providers through a single, easy-to-use interface with interactive menus for beginners!

## 🌟 Features

- **Multi-Provider Support**: OpenRouter, Ollama Cloud, Hugging Face, and Qwen integration
- **Interactive Setup Wizard**: Beginner-friendly guided configuration with intuitive menus
- **Quick Action Menu**: Fast access to common tasks through interactive prompts
- **Hundreds of Models**: Access models from OpenAI, Anthropic, Google, Meta, Mistral, DeepSeek, and more
- **Easy Provider Switching**: Switch between providers with a single command
- **Interactive Chat Mode**: Multi-turn conversations with context
- **Streaming Responses**: Real-time response streaming with automatic fallback
- **Flexible Configuration**: Per-provider API keys and default models
- **Auto-Install Dependencies**: Automatically installs missing packages on first use
- **No GPT Lock-in**: Choose your own models from any supported provider

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

### Hugging Face Inference
Open-source models via Hugging Face:
- `meta-llama/Meta-Llama-3-8B-Instruct`
- `meta-llama/Meta-Llama-3-70B-Instruct`
- `mistralai/Mistral-7B-Instruct-v0.2`
- `microsoft/Phi-3-mini-4k-instruct`
- `google/gemma-7b-it`
- And thousands more from the Hugging Face Hub!

### Qwen (DashScope)
Alibaba Cloud's powerful Qwen models:
- `qwen-turbo` - Fast and efficient
- `qwen-plus` - Enhanced capabilities
- `qwen-max` - Maximum performance
- `qwen-max-longcontext` - Extended context
- `qwen-vl-plus` - Vision + Language
- `qwen-vl-max` - Advanced multimodal

## 📦 Installation

### Prerequisites
- Python 3.7 or higher
- Windows, macOS, or Linux

### Quick Start for Beginners

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Run Interactive Setup**
```bash
python chico-cli.py setup
```

The interactive wizard will guide you through:
- Selecting your preferred AI provider
- Getting and configuring your API key
- Choosing a default model
- Testing your first message

That's it! The CLI will auto-install any missing dependencies.

### Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `openai` - OpenAI-compatible API client
- `ollama` - Ollama Cloud client
- `requests` - HTTP library
- `inquirer` - Interactive menu system
- `huggingface_hub` - Hugging Face API client
- `dashscope` - Qwen/DashScope API client

## 🔑 Configuration

### Interactive Setup (Recommended for Beginners)

The easiest way to get started:

```bash
python chico-cli.py setup
```

This launches an interactive wizard that guides you through:
1. Choosing a provider
2. Entering your API key
3. Selecting a default model
4. Running your first test

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

#### Hugging Face
1. Visit [huggingface.co](https://huggingface.co/)
2. Sign up or log in
3. Go to Settings → Access Tokens
4. Create a new token (read access is sufficient)
5. Copy your token

#### Qwen (DashScope)
1. Visit [dashscope.aliyun.com](https://dashscope.aliyun.com/)
2. Sign up or log in (Alibaba Cloud account required)
3. Go to API Keys section
4. Create a new API key
5. Copy your key

### Manual Configuration

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

#### Configure Hugging Face

```bash
python chico-cli.py config huggingface --api-key YOUR_HF_TOKEN
```

With a default model:
```bash
python chico-cli.py config huggingface --api-key YOUR_TOKEN --default-model "meta-llama/Meta-Llama-3-8B-Instruct"
```

#### Configure Qwen (DashScope)

```bash
python chico-cli.py config qwen --api-key YOUR_QWEN_KEY
```

With a default model:
```bash
python chico-cli.py config qwen --api-key YOUR_KEY --default-model "qwen-turbo"
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
  
  • Hugging Face Inference (huggingface)
    Status: ✓ Configured
    Default model: meta-llama/Meta-Llama-3-8B-Instruct
  
  • Qwen (DashScope) (qwen)
    Status: ✓ Configured
    Default model: qwen-turbo
```

### Switch Active Provider

```bash
python chico-cli.py switch ollama
python chico-cli.py switch huggingface
python chico-cli.py switch qwen
```

## 💬 Usage

### Interactive Quick Menu

For quick access to common tasks:

```bash
python chico-cli.py menu
```

Or simply run without arguments:

```bash
python chico-cli.py
```

This shows an interactive menu with options:
- Start interactive chat
- Send a quick message
- List available models
- Switch provider
- Configure new provider
- View configured providers

### List Available Models

List models from active provider:
```bash
python chico-cli.py models
```

List models from specific provider:
```bash
python chico-cli.py models --provider openrouter
python chico-cli.py models --provider ollama
python chico-cli.py models --provider huggingface
python chico-cli.py models --provider qwen
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
python chico-cli.py chat "Explain Python" --provider huggingface --model "meta-llama/Meta-Llama-3-8B-Instruct"
python chico-cli.py chat "Tell me about AI" --provider qwen --model "qwen-turbo"
```

Disable streaming:
```bash
python chico-cli.py chat "Tell me a joke" --no-stream
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
python chico-cli.py interactive --provider huggingface --model "mistralai/Mistral-7B-Instruct-v0.2"
python chico-cli.py interactive --provider qwen --model "qwen-plus"
```

## 📋 Command Reference

### Interactive Commands

| Command | Description |
|---------|-------------|
| `setup` | Interactive setup wizard for beginners |
| `menu` or no command | Quick interactive menu for common tasks |

### Configuration Commands

| Command | Description |
|---------|-------------|
| `config openrouter --api-key KEY` | Configure OpenRouter |
| `config ollama --api-key KEY` | Configure Ollama Cloud |
| `config huggingface --api-key KEY` | Configure Hugging Face |
| `config qwen --api-key KEY` | Configure Qwen/DashScope |
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

### Hugging Face Models

**Popular Open Models:**
- `meta-llama/Meta-Llama-3-8B-Instruct` - Efficient and capable
- `meta-llama/Meta-Llama-3-70B-Instruct` - Larger, more powerful
- `mistralai/Mistral-7B-Instruct-v0.2` - Fast and efficient
- `microsoft/Phi-3-mini-4k-instruct` - Compact but powerful
- `google/gemma-7b-it` - Google's open model

### Qwen (DashScope) Models

- `qwen-turbo` - Fast, cost-effective for everyday tasks
- `qwen-plus` - Enhanced capabilities for complex tasks
- `qwen-max` - Maximum performance and reasoning
- `qwen-max-longcontext` - Extended context window support
- `qwen-vl-plus` - Vision + Language capabilities
- `qwen-vl-max` - Advanced multimodal understanding

## 📖 Examples

### Example 1: Interactive Setup (Easiest)

```bash
# Run the setup wizard
python chico-cli.py setup

# Follow the prompts to:
# 1. Choose a provider
# 2. Enter your API key
# 3. Select a default model
# 4. Test with your first message
```

### Example 2: Quick Question with OpenRouter

```bash
# Configure OpenRouter
python chico-cli.py config openrouter --api-key sk-or-v1-xxxxx

# Ask a question
python chico-cli.py chat "What are the benefits of renewable energy?"
```

### Example 3: Use Hugging Face Open Models

```bash
# Configure Hugging Face
python chico-cli.py config huggingface --api-key hf_xxxxx

# Use Llama 3
python chico-cli.py chat "Explain neural networks" \
  --provider huggingface --model "meta-llama/Meta-Llama-3-8B-Instruct"
```

### Example 4: Try Qwen for Chinese Language

```bash
# Configure Qwen
python chico-cli.py config qwen --api-key sk-xxxxx

# Ask in Chinese or English
python chico-cli.py chat "解释人工智能的基本概念" \
  --provider qwen --model "qwen-turbo"
```

### Example 5: Code Generation with Specific Model

```bash
# Use Claude for coding
python chico-cli.py chat "Write a Python function to calculate fibonacci numbers" \
  --model "anthropic/claude-3.5-sonnet"
```

### Example 6: Switch Between Providers

```bash
# Configure multiple providers
python chico-cli.py config openrouter --api-key KEY1
python chico-cli.py config huggingface --api-key KEY2
python chico-cli.py config qwen --api-key KEY3

# Switch between them
python chico-cli.py switch huggingface
python chico-cli.py switch qwen
python chico-cli.py switch openrouter
```

### Example 7: Interactive Conversation

```bash
python chico-cli.py interactive --model "google/gemini-2.0-flash-exp"

You: I'm learning Python. Can you help me?
AI: Of course! I'd be happy to help you learn Python...

You: How do I read a CSV file?
AI: To read a CSV file in Python, you can use the csv module...

You: exit
Goodbye! 👋
```

### Example 8: Compare Models Across Providers

```bash
# Try with Llama on OpenRouter
python chico-cli.py chat "Write a haiku about AI" \
  --model "meta-llama/llama-3.3-70b-instruct"

# Try with Llama on Hugging Face
python chico-cli.py chat "Write a haiku about AI" \
  --provider huggingface --model "meta-llama/Meta-Llama-3-8B-Instruct"

# Try with Qwen
python chico-cli.py chat "Write a haiku about AI" \
  --provider qwen --model "qwen-turbo"
```

## 🔧 Advanced Configuration

### Environment Variables

You can also use environment variables (they override config file):

```bash
# Windows
set OPENROUTER_API_KEY=your_key
set OLLAMA_API_KEY=your_key
set HUGGINGFACE_API_KEY=your_key
set QWEN_API_KEY=your_key

# Linux/Mac
export OPENROUTER_API_KEY=your_key
export OLLAMA_API_KEY=your_key
export HUGGINGFACE_API_KEY=your_key
export QWEN_API_KEY=your_key
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
  "huggingface": {
    "api_key": "hf_xxxxx",
    "default_model": "meta-llama/Meta-Llama-3-8B-Instruct"
  },
  "qwen": {
    "api_key": "sk-xxxxx",
    "default_model": "qwen-turbo"
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

All providers have rate limits. If you hit them:
- Wait a few seconds and try again
- Use a different model
- Check your account limits on the provider's website
- Consider upgrading your account tier

## 💰 Pricing

### OpenRouter
- Pay-per-use pricing
- Varies by model
- Check [openrouter.ai/models](https://openrouter.ai/models) for current prices
- Free tier available for some models

### Ollama Cloud
- Currently in preview
- Check [ollama.com/cloud](https://ollama.com/cloud) for pricing details

### Hugging Face Inference
- Free tier available with rate limits
- Pro subscription for higher limits
- Check [huggingface.co/pricing](https://huggingface.co/pricing) for details

### Qwen (DashScope)
- Pay-per-use pricing
- Free tier for testing
- Check [dashscope.aliyun.com](https://dashscope.aliyun.com/) for pricing details

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
- **Hugging Face**: [huggingface.co](https://huggingface.co/)
- **Hugging Face Docs**: [huggingface.co/docs](https://huggingface.co/docs)
- **Qwen DashScope**: [dashscope.aliyun.com](https://dashscope.aliyun.com/)
- **Qwen Docs**: [help.aliyun.com/zh/dashscope](https://help.aliyun.com/zh/dashscope)

## 🎉 What's New in v2.1

- ✅ **Hugging Face Integration**: Access thousands of open-source models
- ✅ **Qwen (DashScope) Support**: Alibaba's powerful Qwen models
- ✅ **Interactive Setup Wizard**: Beginner-friendly guided configuration
- ✅ **Quick Action Menu**: Fast access to common tasks
- ✅ **Auto-Install Dependencies**: Automatically installs missing packages
- ✅ **4 Provider Support**: OpenRouter, Ollama, Hugging Face, and Qwen
- ✅ **Improved Error Handling**: Better error messages for all providers
- ✅ **Enhanced Documentation**: Updated guides and examples

### Previous Updates (v2.0)

- ✅ **OpenRouter Integration**: Access 500+ models
- ✅ **Ollama Cloud Support**: Cloud-hosted models
- ✅ **Multi-Provider System**: Switch between providers easily
- ✅ **No GPT Lock-in**: Use any model you want
- ✅ **Improved Configuration**: Per-provider settings
- ✅ **Better Error Handling**: Clear error messages
- ✅ **Model Discovery**: List available models per provider

## 🤝 About

**Chico Chuwawa AI CLI** is designed to give you freedom of choice in AI models. No lock-in to specific providers or models - use what works best for your needs.

**Built by**: Max van Heerden  
**Version**: 2.1.0  
**License**: Free for personal and commercial use

---

**Chico Chuwawa AI CLI** - Your gateway to hundreds of AI models from 4 major providers! 🐕✨

