# Chico Chuwawa AI CLI - Enhanced Edition

![Chico Chuwawa Logo](chico-logo.png)

**Built by Max van Heerden**  
**Version 2.1.0**

A powerful command-line interface (CLI) tool with **rich terminal UI**, **multi-cloud integrations**, and **AI-driven orchestration**. Access hundreds of AI models while managing Docker, Kubernetes, npm, PyPI, and cloud services - all from a unified interface.

## 🌟 Enhanced Features

### AI & LLM Capabilities
- **Multi-Provider Support**: OpenRouter and Ollama Cloud integration
- **Hundreds of Models**: Access models from OpenAI, Anthropic, Google, Meta, Mistral, DeepSeek, and more
- **Easy Provider Switching**: Switch between providers with a single command
- **Interactive Chat Mode**: Multi-turn conversations with context
- **Streaming Responses**: Real-time response streaming with automatic fallback
- **AI-Powered Auto-Completion**: Intelligent command suggestions and completions
- **No GPT Lock-in**: Choose your own models from any supported provider

### Rich Terminal UI (via rich library)
- **Beautiful Tables**: Styled tables with colors and borders
- **Syntax Highlighting**: Code and log syntax highlighting
- **Progress Indicators**: Spinners and progress bars for operations
- **Panels**: Organized information display
- **Live Updates**: Real-time monitoring dashboards

### Integration Hub (MCP-like Orchestration)
- **Docker Integration**: Manage containers, images, and view logs
- **Kubernetes Integration**: Monitor pods, deployments, services across clusters
- **npm Registry**: Search and get info on npm packages
- **PyPI Integration**: Search and get info on Python packages
- **AWS Integration**: Basic S3 and EC2 management
- **GCP Integration**: Google Cloud Storage management
- **Azure Integration**: Blob storage management
- **Unified Health Monitoring**: Track status of all integrations
- **Service Discovery**: Automatic detection of available services

### Advanced Command Features
- **Auto-Completion**: Tab completion for commands and arguments
- **Smart Defaults**: AI-driven default values based on context
- **Command History**: Track and reuse frequent commands
- **Real-Time Monitoring**: Live dashboards for containers, pods, and services

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
- `rich` - Beautiful terminal formatting
- `click` - Advanced command-line parsing
- `docker` - Docker API client
- `kubernetes` - Kubernetes API client
- `boto3` - AWS SDK
- `google-cloud-storage` - Google Cloud SDK
- `azure-storage-blob` - Azure SDK
- `prompt-toolkit` - Interactive prompts and auto-completion

## 🎯 Quick Start

### Basic Usage (Original CLI)

```bash
# Configure OpenRouter
python chico_cli.py config openrouter --api-key YOUR_KEY

# Chat with AI
python chico_cli.py chat "What is Python?"

# Interactive mode
python chico_cli.py interactive
```

### Enhanced CLI with Rich UI

```bash
# Show welcome screen with all features
python chico-cli-enhanced.py welcome

# View AI providers with rich table
python chico-cli-enhanced.py providers

# View integration status
python chico-cli-enhanced.py integrations

# View MCP hub status
python chico-cli-enhanced.py hub-status
```

### Docker Integration

```bash
# List all containers
python chico-cli-enhanced.py docker containers

# List images
python chico-cli-enhanced.py docker images

# View container logs
python chico-cli-enhanced.py docker logs <container_id>
```

### Kubernetes Integration

```bash
# List pods in default namespace
python chico-cli-enhanced.py k8s pods

# List pods in specific namespace
python chico-cli-enhanced.py k8s pods --namespace production

# List deployments
python chico-cli-enhanced.py k8s deployments

# List services
python chico-cli-enhanced.py k8s services
```

### Package Management

```bash
# Search npm packages
python chico-cli-enhanced.py npm search react

# Get npm package info
python chico-cli-enhanced.py npm info react

# Get PyPI package info
python chico-cli-enhanced.py pypi info requests
```

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

## 🔧 Integration Configuration

### Docker Integration

Docker integration works automatically if Docker is running on your system. No additional configuration needed.

```bash
# Test Docker connection
python chico-cli-enhanced.py docker containers
```

**For remote Docker:**
Create/edit `integrations.json` in your config directory:
```json
{
  "docker": {
    "base_url": "tcp://remote-host:2375"
  }
}
```

### Kubernetes Integration

Kubernetes integration uses your existing `kubectl` configuration.

```bash
# Test K8s connection
python chico-cli-enhanced.py k8s pods
```

**For custom kubeconfig:**
```json
{
  "kubernetes": {
    "kubeconfig_path": "/path/to/custom/kubeconfig"
  }
}
```

### npm and PyPI

These integrations work out of the box - no configuration needed.

```bash
# Test npm
python chico-cli-enhanced.py npm search typescript

# Test PyPI
python chico-cli-enhanced.py pypi info django
```

### AWS Integration

Configure AWS credentials:

```json
{
  "aws": {
    "aws_access_key_id": "YOUR_ACCESS_KEY",
    "aws_secret_access_key": "YOUR_SECRET_KEY",
    "region": "us-east-1"
  }
}
```

Or use AWS CLI default credentials from `~/.aws/credentials`.

### GCP Integration

Set up Google Cloud credentials:

```json
{
  "gcp": {
    "credentials_path": "/path/to/service-account-key.json"
  }
}
```

Or set `GOOGLE_APPLICATION_CREDENTIALS` environment variable.

### Azure Integration

Configure Azure connection:

```json
{
  "azure": {
    "connection_string": "DefaultEndpointsProtocol=https;AccountName=...;AccountKey=...;EndpointSuffix=core.windows.net"
  }
}
```

**Configuration File Location:**
- **Windows**: `%APPDATA%\ChicoChuwawa-CLI\integrations.json`
- **Linux/Mac**: `~/.config/chico-cli/integrations.json`

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

## 🤝 About

**Chico Chuwawa AI CLI** is designed to give you freedom of choice in AI models. No lock-in to specific providers or models - use what works best for your needs.

**Built by**: Max van Heerden  
**Version**: 2.0.0  
**License**: Free for personal and commercial use

---

**Chico Chuwawa AI CLI** - Your gateway to hundreds of AI models! 🐕✨

