# Chico Chuwawa AI CLI

![Chico Chuwawa Logo](chico-logo.png)

**Built by Max van Heerden**  
**Version 2.0.0**

A powerful command-line interface (CLI) tool for Windows that integrates with **OpenRouter** and **Ollama Cloud** APIs. Access hundreds of AI models from multiple providers through a single, easy-to-use interface.

## 🌟 Features

- **Multi-Provider Support**: OpenRouter and Ollama Cloud integration
- **Hundreds of Models**: Access models from OpenAI, Anthropic, Google, Meta, Mistral, DeepSeek, and more
- **Easy Provider Switching**: Switch between providers with a single command
- **Interactive Chat Mode**: Multi-turn conversations with context
- **Streaming Responses**: Real-time response streaming with automatic fallback
- **Flexible Configuration**: Per-provider API keys and default models
- **No GPT Lock-in**: Choose your own models from any supported provider
- **🐕 Chico Chihuahua Animations**: Engaging ASCII animations with "Small Dog, Big Power" theme
  - Cute Chihuahua ASCII art in multiple poses (sitting, coding, launching, searching, celebrating)
  - Success animations showing the mighty Chihuahua achieving big feats
  - Loading spinners with motivational messages
  - Thematic transitions between operations
  - Interactive mode welcome animations
  - Celebration animations for completed tasks

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
- `rich` - Beautiful terminal formatting and animations

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

### Example 2: Code Generation with Specific Model

```bash
# Use Claude for coding
python chico-cli.py chat "Write a Python function to calculate fibonacci numbers" \
  --model "anthropic/claude-3.5-sonnet"
```

### Example 3: Switch to Ollama Cloud

```bash
# Configure Ollama
python chico-cli.py config ollama --api-key ollama_xxxxx

# Switch to Ollama
python chico-cli.py switch ollama

# Use Ollama model
python chico-cli.py chat "Explain machine learning" \
  --model "gpt-oss:120b-cloud"
```

### Example 4: Interactive Conversation

```bash
python chico-cli.py interactive --model "google/gemini-2.0-flash-exp"

You: I'm learning Python. Can you help me?
AI: Of course! I'd be happy to help you learn Python...

You: How do I read a CSV file?
AI: To read a CSV file in Python, you can use the csv module...

You: exit
Goodbye! 👋
```

### Example 5: Compare Models

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

## 🎉 What's New in v2.0

- ✅ **OpenRouter Integration**: Access 500+ models
- ✅ **Ollama Cloud Support**: Cloud-hosted models
- ✅ **Multi-Provider System**: Switch between providers easily
- ✅ **No GPT Lock-in**: Use any model you want
- ✅ **Improved Configuration**: Per-provider settings
- ✅ **Better Error Handling**: Clear error messages
- ✅ **Model Discovery**: List available models per provider
- ✅ **🐕 Chico Chihuahua Animations**: Engaging ASCII animations with "Small Dog, Big Power" theme

## 🐕 Chico Chihuahua Animations

The CLI now features delightful ASCII animations starring Chico, a tiny but mighty white apple-head Chihuahua! Each animation embodies the "small dog, big power" theme.

### Animation Features

**ASCII Art Gallery:**
- 🐕 **Sitting Chico**: Ready and waiting
- 💻 **Coding Chico**: Programming incredible worlds
- 🚀 **Launching Chico**: Deploying powerful integrations
- 🔍 **Searching Chico**: Navigating vast databases
- ⚡ **Power Chico**: Showing off Chihuahua power
- ⭐ **Success Chico**: Celebrating achievements

**Interactive Animations:**
- Welcome banner when starting the CLI
- Configuration success celebrations
- Provider switching transitions
- Model listing with search animations
- Chat thinking spinners with motivational messages
- Big feat celebrations (coding worlds, launching integrations, powering searches)
- Session end animations

**Motivational Messages:**
Random quotes from Chico:
- 🐕 "Size doesn't define power!" - Chico
- ⚡ "Small but fierce!" - Chico the Mighty
- 💪 "Pocket-sized but powerful!" - Chico
- 🚀 "Big dreams in a tiny package!" - Chico
- ✨ "Never underestimate a Chihuahua!" - Chico
- 🏆 "Tiny paws, giant achievements!" - Chico

### Testing Animations

To see all animations in action:

```bash
python test_animations.py
```

This runs a comprehensive showcase of all animation types, perfect for demonstrations!

### Animation Dependencies

Animations are powered by the `rich` library for beautiful terminal output. If `rich` is not installed, the CLI gracefully falls back to simple text output without breaking functionality.

## 🤝 About

**Chico Chuwawa AI CLI** is designed to give you freedom of choice in AI models. No lock-in to specific providers or models - use what works best for your needs.

**Built by**: Max van Heerden  
**Version**: 2.0.0  
**License**: Free for personal and commercial use

---

**Chico Chuwawa AI CLI** - Your gateway to hundreds of AI models! 🐕✨

