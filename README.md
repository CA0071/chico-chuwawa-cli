# Chico Chuwawa AI CLI

![Chico Chuwawa Logo](chico-logo.png)

**Built by Max van Heerden**  
**Version 2.1.0**

A powerful command-line interface (CLI) tool for Windows, macOS, and Linux that integrates with multiple AI providers. Access hundreds of AI models from OpenRouter, Ollama Cloud, DeepSeek, ChatGPT, Claude, and Manus AI through a single, easy-to-use interface.

## 🌟 Features

- **Multi-Provider Support**: OpenRouter, Ollama Cloud, DeepSeek, ChatGPT, Claude, and Manus AI integration
- **Hundreds of Models**: Access models from OpenAI, Anthropic, Google, Meta, Mistral, DeepSeek, and more
- **Easy Provider Switching**: Switch between providers with a single command
- **Interactive Chat Mode**: Multi-turn conversations with context
- **Streaming Responses**: Real-time response streaming with automatic fallback
- **Flexible Configuration**: Per-provider API keys and default models
- **No GPT Lock-in**: Choose your own models from any supported provider
- **Cross-Platform**: Works on Windows, macOS, and Linux

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

### DeepSeek
Direct access to DeepSeek AI models:
- `deepseek-chat` - Fast, general-purpose chat model
- `deepseek-reasoner` - Advanced reasoning with chain-of-thought
- `deepseek-coder` - Specialized coding model
- Supports up to 128K token context window

### ChatGPT (OpenAI)
Direct access to OpenAI's ChatGPT models:
- `gpt-4o` - Latest GPT-4 Omni model
- `gpt-4-turbo` - Fast and powerful
- `gpt-4` - Most capable GPT-4 model
- `gpt-3.5-turbo` - Fast and efficient
- `gpt-4o-mini` - Cost-effective option

### Claude (Anthropic)
Direct access to Anthropic's Claude models:
- `claude-opus-4-20250514` - Most powerful Claude model
- `claude-3-5-sonnet-20241022` - Balanced performance
- `claude-3-5-haiku-20241022` - Fast and efficient
- `claude-3-opus-20240229` - Previous generation flagship
- Excellent for coding, analysis, and long-form content

### Manus AI
Task-based autonomous AI agent:
- Create and manage complex tasks
- File attachments and context support
- Integration with productivity tools
- Ideal for automation and multi-step workflows

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
- `anthropic` - Claude/Anthropic API client
- `requests` - HTTP library

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

#### DeepSeek
1. Visit [platform.deepseek.com](https://platform.deepseek.com/)
2. Sign up or log in
3. Go to API Keys section
4. Create a new API key
5. Copy your key

#### ChatGPT (OpenAI)
1. Visit [platform.openai.com](https://platform.openai.com/)
2. Sign up or log in
3. Go to API Keys section
4. Create a new secret key
5. Copy your key (starts with `sk-...`)

#### Claude (Anthropic)
1. Visit [console.anthropic.com](https://console.anthropic.com/)
2. Sign up or log in
3. Go to Account Settings > API Keys
4. Create a new API key
5. Copy your key (starts with `sk-ant-...`)

#### Manus AI
1. Visit [open.manus.ai](https://open.manus.ai/)
2. Sign up or log in
3. Go to API section
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

#### Configure DeepSeek

```bash
python chico-cli.py config deepseek --api-key YOUR_DEEPSEEK_KEY
```

With a default model:
```bash
python chico-cli.py config deepseek --api-key YOUR_KEY --default-model "deepseek-chat"
```

#### Configure ChatGPT (OpenAI)

```bash
python chico-cli.py config chatgpt --api-key YOUR_OPENAI_KEY
```

With a default model:
```bash
python chico-cli.py config chatgpt --api-key YOUR_KEY --default-model "gpt-4o"
```

#### Configure Claude (Anthropic)

```bash
python chico-cli.py config claude --api-key YOUR_CLAUDE_KEY
```

With a default model:
```bash
python chico-cli.py config claude --api-key YOUR_KEY --default-model "claude-3-5-sonnet-20241022"
```

#### Configure Manus AI

```bash
python chico-cli.py config manus --api-key YOUR_MANUS_KEY
```

With a default model:
```bash
python chico-cli.py config manus --api-key YOUR_KEY --default-model "manus-1"
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
  
  • DeepSeek (deepseek)
    Status: ✓ Configured
    Default model: deepseek-chat
  
  • ChatGPT (OpenAI) (chatgpt)
    Status: ✓ Configured
    Default model: gpt-4o
  
  • Claude (Anthropic) (claude)
    Status: ✓ Configured
    Default model: claude-opus-4-20250514
  
  • Manus AI (manus)
    Status: ✓ Configured
    Default model: manus-1
```

### Switch Active Provider

```bash
python chico-cli.py switch deepseek
python chico-cli.py switch chatgpt
python chico-cli.py switch claude
python chico-cli.py switch manus
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
python chico-cli.py models --provider deepseek
python chico-cli.py models --provider chatgpt
python chico-cli.py models --provider claude
python chico-cli.py models --provider manus
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
python chico-cli.py chat "Explain recursion" --provider deepseek --model "deepseek-chat"
python chico-cli.py chat "Write Python code" --provider chatgpt --model "gpt-4o"
python chico-cli.py chat "Analyze this text" --provider claude --model "claude-3-5-sonnet-20241022"
python chico-cli.py chat "Create a report" --provider manus --model "manus-1"
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
| `config deepseek --api-key KEY` | Configure DeepSeek |
| `config chatgpt --api-key KEY` | Configure ChatGPT (OpenAI) |
| `config claude --api-key KEY` | Configure Claude (Anthropic) |
| `config manus --api-key KEY` | Configure Manus AI |
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

### DeepSeek Models

- `deepseek-chat` - General-purpose chat (default, recommended)
- `deepseek-reasoner` - Advanced reasoning with chain-of-thought
- `deepseek-coder` - Specialized for programming tasks

### ChatGPT (OpenAI) Models

- `gpt-4o` - Latest and most capable (default, recommended)
- `gpt-4-turbo` - Fast with strong performance
- `gpt-4` - Original GPT-4 model
- `gpt-3.5-turbo` - Fast and cost-effective
- `gpt-4o-mini` - Lightweight option

### Claude (Anthropic) Models

- `claude-opus-4-20250514` - Most powerful, best reasoning (default)
- `claude-3-5-sonnet-20241022` - Balanced, great for coding
- `claude-3-5-haiku-20241022` - Fast and efficient
- `claude-3-opus-20240229` - Previous flagship
- `claude-3-sonnet-20240229` - Previous balanced option

### Manus AI

- `manus-1` - Task-based autonomous agent
- Best for complex multi-step workflows
- Supports file attachments and tool integrations

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

### Example 4: Using DeepSeek for Reasoning

```bash
# Configure DeepSeek
python chico-cli.py config deepseek --api-key YOUR_DEEPSEEK_KEY

# Use for complex reasoning
python chico-cli.py chat "Solve this logic puzzle: If all roses are flowers..." \
  --provider deepseek --model "deepseek-reasoner"
```

### Example 5: Using ChatGPT (OpenAI) Directly

```bash
# Configure ChatGPT
python chico-cli.py config chatgpt --api-key YOUR_OPENAI_KEY

# Use GPT-4o
python chico-cli.py chat "Explain the difference between AI and ML" \
  --provider chatgpt --model "gpt-4o"
```

### Example 6: Using Claude for Code Review

```bash
# Configure Claude
python chico-cli.py config claude --api-key YOUR_CLAUDE_KEY

# Use for code analysis
python chico-cli.py chat "Review this Python code for improvements: def fib(n): ..." \
  --provider claude --model "claude-3-5-sonnet-20241022"
```

### Example 7: Using Manus AI for Tasks

```bash
# Configure Manus
python chico-cli.py config manus --api-key YOUR_MANUS_KEY

# Create a task
python chico-cli.py chat "Analyze this dataset and create a summary report" \
  --provider manus --model "manus-1"
```

### Example 8: Interactive Conversation

```bash
python chico-cli.py interactive --model "google/gemini-2.0-flash-exp"

You: I'm learning Python. Can you help me?
AI: Of course! I'd be happy to help you learn Python...

You: How do I read a CSV file?
AI: To read a CSV file in Python, you can use the csv module...

You: exit
Goodbye! 👋
```

### Example 9: Compare Models

```bash
# Try with Llama
python chico-cli.py chat "Write a haiku about AI" \
  --model "meta-llama/llama-3.3-70b-instruct"

# Try with Claude
python chico-cli.py chat "Write a haiku about AI" \
  --provider claude --model "claude-3-5-sonnet-20241022"

# Try with DeepSeek
python chico-cli.py chat "Write a haiku about AI" \
  --provider deepseek --model "deepseek-chat"

# Try with ChatGPT
python chico-cli.py chat "Write a haiku about AI" \
  --provider chatgpt --model "gpt-4o"
```

## 🔧 Advanced Configuration

### Environment Variables

You can also use environment variables (they override config file):

```bash
# Windows
set OPENROUTER_API_KEY=your_key
set OLLAMA_API_KEY=your_key
set DEEPSEEK_API_KEY=your_key
set CHATGPT_API_KEY=your_key
set CLAUDE_API_KEY=your_key
set MANUS_API_KEY=your_key

# Linux/Mac
export OPENROUTER_API_KEY=your_key
export OLLAMA_API_KEY=your_key
export DEEPSEEK_API_KEY=your_key
export CHATGPT_API_KEY=your_key
export CLAUDE_API_KEY=your_key
export MANUS_API_KEY=your_key
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
  "deepseek": {
    "api_key": "your_deepseek_key",
    "default_model": "deepseek-chat"
  },
  "chatgpt": {
    "api_key": "sk-xxxxx",
    "default_model": "gpt-4o"
  },
  "claude": {
    "api_key": "sk-ant-xxxxx",
    "default_model": "claude-3-5-sonnet-20241022"
  },
  "manus": {
    "api_key": "your_manus_key",
    "default_model": "manus-1"
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

## 💰 Pricing

### OpenRouter
- Pay-per-use pricing
- Varies by model
- Check [openrouter.ai/models](https://openrouter.ai/models) for current prices
- Free tier available for some models

### Ollama Cloud
- Currently in preview
- Check [ollama.com/cloud](https://ollama.com/cloud) for pricing details

### DeepSeek
- Highly competitive pricing
- Check [platform.deepseek.com](https://platform.deepseek.com/) for current rates
- Very cost-effective for high-volume usage

### ChatGPT (OpenAI)
- Pay-per-use pricing
- Varies by model (GPT-4o, GPT-4, GPT-3.5-turbo)
- Check [openai.com/pricing](https://openai.com/pricing) for current prices
- GPT-3.5-turbo is the most cost-effective option

### Claude (Anthropic)
- Pay-per-use pricing
- Varies by model (Opus, Sonnet, Haiku)
- Check [anthropic.com/pricing](https://www.anthropic.com/pricing) for current prices
- Haiku is the most cost-effective option

### Manus AI
- Task-based pricing
- Check [manus.im](https://manus.im/) for current pricing
- May include free tier for testing

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
- **DeepSeek**: [platform.deepseek.com](https://platform.deepseek.com/)
- **DeepSeek API Docs**: [api-docs.deepseek.com](https://api-docs.deepseek.com/)
- **ChatGPT (OpenAI)**: [platform.openai.com](https://platform.openai.com/)
- **OpenAI API Docs**: [platform.openai.com/docs](https://platform.openai.com/docs)
- **Claude (Anthropic)**: [console.anthropic.com](https://console.anthropic.com/)
- **Claude API Docs**: [docs.anthropic.com](https://docs.anthropic.com/)
- **Manus AI**: [manus.im](https://manus.im/)
- **Manus API Docs**: [open.manus.ai/docs](https://open.manus.ai/docs)

## 🎉 What's New in v2.1

- ✅ **DeepSeek Integration**: Direct access to DeepSeek models with reasoning capabilities
- ✅ **ChatGPT (OpenAI) Direct Access**: Use GPT-4o, GPT-4, and other OpenAI models directly
- ✅ **Claude (Anthropic) Integration**: Full support for Claude Opus, Sonnet, and Haiku models
- ✅ **Manus AI Support**: Task-based autonomous AI agent for complex workflows
- ✅ **6 Provider Ecosystem**: Access AI models from 6 different providers in one CLI
- ✅ **Enhanced Cross-Platform Support**: Improved compatibility across Windows, macOS, and Linux
- ✅ **Streaming Support**: Real-time responses for DeepSeek, ChatGPT, and Claude
- ✅ **Extended Model Selection**: Access to hundreds more models across all providers

### Previous v2.0 Features

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

**Chico Chuwawa AI CLI** - Your gateway to hundreds of AI models! 🐕✨

