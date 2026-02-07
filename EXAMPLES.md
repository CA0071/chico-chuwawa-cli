# Chico CLI - Usage Examples

Complete guide with real-world examples for every feature of Chico Chuwawa AI CLI v3.0.

## Table of Contents
- [Quick Start](#quick-start)
- [Basic Chat](#basic-chat)
- [Interactive Mode](#interactive-mode)
- [History Management](#history-management)
- [Code Search](#code-search)
- [Provider Management](#provider-management)
- [Advanced Features](#advanced-features)
- [Integration Examples](#integration-examples)
- [Tips & Tricks](#tips--tricks)

## Quick Start

### First Time Setup

```bash
# 1. Configure your AI provider
chico config openrouter --api-key sk-or-v1-YOUR_KEY_HERE

# 2. Set a default model (optional)
chico config openrouter --api-key YOUR_KEY --default-model "anthropic/claude-3.5-sonnet"

# 3. Test it out!
chico chat "Hello, world!"
```

## Basic Chat

### Simple Questions

```bash
# General knowledge
chico chat "What is the capital of France?"

# Math
chico chat "What is 1234 * 5678?"

# Explanations
chico chat "Explain quantum computing in simple terms"
```

### Using Specific Models

```bash
# Use Claude for reasoning
chico chat "Solve this logic puzzle: ..." --model "anthropic/claude-3.5-sonnet"

# Use Gemini for speed
chico chat "Quick summary of Python" --model "google/gemini-2.0-flash-exp"

# Use Llama for open source
chico chat "Write a haiku" --model "meta-llama/llama-3.3-70b-instruct"
```

### Code Generation

```bash
# Python code
chico chat "Write a Python function to calculate fibonacci numbers"

# JavaScript code
chico chat "Create a React component for a login form" --model "anthropic/claude-3.5-sonnet"

# With specific requirements
chico chat "Write a Python script that reads a CSV file, sorts by column 2, and writes to a new file"
```

### With Internet Search

```bash
# Search for latest information
chico chat "What are the new features in Python 3.12?" --search

# Find coding solutions
chico chat "How to implement JWT authentication in Node.js?" --search

# Get current information
chico chat "Best practices for React hooks in 2026" --search
```

### Saving to History

```bash
# Save important conversations
chico chat "Explain async/await in JavaScript" --save

# Save complex queries
chico chat "Design a microservices architecture for e-commerce" --save --search
```

## Interactive Mode

### Basic Interactive Session

```bash
# Start interactive mode
chico interactive

# Example conversation:
# You: What is React?
# AI: React is a JavaScript library...
# You: Show me an example
# AI: Here's a simple React component...
# You: exit
```

### With Welcome Animation

```bash
# Show the ASCII Chihuahua and logo
chico interactive --banner

# You'll see:
# - Animated Chihuahua mascot
# - ASCII art logo
# - Colorful welcome message
```

### Using Specific Model

```bash
# Interactive with Claude
chico interactive --model "anthropic/claude-3.5-sonnet"

# Interactive with Gemini
chico interactive --model "google/gemini-2.0-flash-exp"

# Interactive with Ollama
chico interactive --provider ollama --model "gpt-oss:120b-cloud"
```

### Without Saving History

```bash
# Private conversation (not saved)
chico interactive --no-save

# Useful for:
# - Sensitive information
# - Quick tests
# - Temporary queries
```

### Full-Featured Session

```bash
# Everything enabled
chico interactive --banner --model "anthropic/claude-3.5-sonnet"

# This gives you:
# - Welcome animation
# - Best AI model
# - Saved history
# - Streaming responses
```

## History Management

### View Recent Conversations

```bash
# Last 10 sessions (default)
chico history

# Output:
# 📚 Recent Chat Sessions (last 10):
# ------------------------------------------------------------
#   Session #1: Chat 2026-02-07 22:30
#   Provider: openrouter | Model: anthropic/claude-3.5-sonnet
#   Created: 2026-02-07 22:30:15
#
#   Session #2: Chat 2026-02-07 21:45
#   ...
```

### View More History

```bash
# Last 20 sessions
chico history --limit 20

# Last 50 sessions
chico history --limit 50
```

### Resume Previous Conversations

```bash
# Note the session ID from history
chico history

# Use the session information to remember context
# (Future feature: chico resume --session 123)
```

## Code Search

### General Search

```bash
# Search the web for coding help
chico search "python async await tutorial"

# Output shows:
# 🔍 Search Results:
# ============================================================
# 1. Async IO in Python: A Complete Walkthrough
#    https://realpython.com/async-io-python/
#    Learn how to use Python's async and await...
```

### Stack Overflow Search

```bash
# Find solutions on Stack Overflow
chico search "javascript promises vs async await" --source stackoverflow

# Examples:
chico search "python list comprehension" --source stackoverflow
chico search "react hooks useEffect" --source stackoverflow
```

### GitHub Code Search

```bash
# Find code examples on GitHub
chico search "rust async implementation" --source github

# Examples:
chico search "python machine learning" --source github
chico search "vue.js components" --source github
```

### Combined with Chat

```bash
# Search first, then ask AI
chico search "docker compose best practices"
chico chat "Based on best practices, create a docker-compose.yml for a Node.js app with PostgreSQL"

# Or use --search flag to do both
chico chat "Create docker-compose for Node.js + PostgreSQL using best practices" --search
```

## Provider Management

### List All Providers

```bash
chico providers

# Output:
# 📋 Available Providers:
# ------------------------------------------------------------
#   • OpenRouter (openrouter)
#     Status: ✓ Configured ✓ Active
#     Default model: anthropic/claude-3.5-sonnet
#
#   • Ollama Cloud (ollama)
#     Status: ✓ Configured
#     Default model: gpt-oss:120b-cloud
```

### Configure Multiple Providers

```bash
# Configure OpenRouter
chico config openrouter --api-key sk-or-v1-YOUR_KEY

# Configure Ollama
chico config ollama --api-key ollama_YOUR_KEY

# Set default models for each
chico config openrouter --api-key YOUR_KEY --default-model "anthropic/claude-3.5-sonnet"
chico config ollama --api-key YOUR_KEY --default-model "gpt-oss:120b-cloud"
```

### Switch Between Providers

```bash
# Switch to Ollama
chico switch ollama

# Use Ollama
chico chat "Hello from Ollama!"

# Switch back to OpenRouter
chico switch openrouter

# Use OpenRouter
chico chat "Hello from OpenRouter!"
```

### List Available Models

```bash
# List models for active provider
chico models

# List models for specific provider
chico models --provider openrouter
chico models --provider ollama
```

### Use Different Providers Without Switching

```bash
# Use OpenRouter temporarily
chico chat "Question" --provider openrouter

# Use Ollama temporarily
chico chat "Question" --provider ollama --model "gpt-oss:120b-cloud"

# Your active provider doesn't change
```

## Advanced Features

### Combining Multiple Flags

```bash
# Chat with all features
chico chat "Explain microservices" \
  --model "anthropic/claude-3.5-sonnet" \
  --search \
  --save

# Interactive with everything
chico interactive \
  --banner \
  --model "anthropic/claude-3.5-sonnet"
```

### Environment Variables

```bash
# Set via environment (Linux/Mac)
export OPENROUTER_API_KEY="sk-or-v1-YOUR_KEY"
chico chat "Hello!"

# Set via environment (Windows)
set OPENROUTER_API_KEY=sk-or-v1-YOUR_KEY
chico chat "Hello!"

# Useful for:
# - CI/CD pipelines
# - Temporary keys
# - Security (no config file)
```

### Non-Streaming Mode

```bash
# Disable streaming (wait for complete response)
chico chat "Tell me a story" --no-stream

# Useful when:
# - Piping output to files
# - Processing complete responses
# - Old terminal emulators
```

### Piping and Output

```bash
# Save output to file
chico chat "Generate Python code for sorting" > sort.py

# Use in scripts
RESPONSE=$(chico chat "Answer in one word: capital of Japan")
echo "The answer is: $RESPONSE"

# Chain commands
chico search "docker tutorial" | grep -i "best practices"
```

## Integration Examples

### WhatsApp Integration

```bash
# Setup WhatsApp
chico whatsapp

# Follow the instructions:
# 1. QR code appears in terminal
# 2. Open WhatsApp on phone
# 3. Go to Settings > Linked Devices
# 4. Scan the QR code
# 5. Connection established!

# Now you can:
# - Send AI responses to WhatsApp
# - Monitor messages from WhatsApp
# - Get notifications
```

### Using with Python Scripts

```python
# example_script.py
import subprocess
import json

def ask_chico(question):
    result = subprocess.run(
        ['chico', 'chat', question, '--no-stream'],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

# Use it
answer = ask_chico("What is 2 + 2?")
print(f"Chico says: {answer}")
```

### Integration with Shell Scripts

```bash
#!/bin/bash
# daily_summary.sh

# Get AI summary of git commits
commits=$(git log --since="1 day ago" --pretty=format:"%s")
summary=$(chico chat "Summarize these git commits: $commits" --no-stream)

echo "Daily Development Summary:"
echo "$summary"

# Send to team channel (example)
# slack-send "$summary"
```

## Tips & Tricks

### Quick Commands

```bash
# Create aliases (Linux/Mac)
alias ask='chico chat'
alias code='chico chat "Generate code for:"'

# Use them
ask "What is Python?"
code "binary search in Java"
```

### PowerShell Functions (Windows)

```powershell
# Add to profile
function ask { chico chat $args }
function code { chico chat "Generate code for: $args" }

# Use them
ask "What is Python?"
code "binary search in Java"
```

### Debugging

```bash
# Check configuration
cat ~/.config/chico-cli/config.json

# Check history database
sqlite3 ~/.config/chico-cli/chat_history.db "SELECT * FROM sessions LIMIT 5;"

# Test connectivity
chico providers
chico models
```

### Best Practices

```bash
# 1. Save important conversations
chico chat "Complex architecture explanation" --save

# 2. Use search for coding questions
chico chat "How to handle errors in async Python?" --search

# 3. Use specific models for specific tasks
chico chat "Write documentation" --model "anthropic/claude-3.5-sonnet"
chico chat "Quick answer" --model "google/gemini-2.0-flash-exp"

# 4. Interactive mode for learning
chico interactive --banner

# 5. Regular updates
cd /path/to/chico-chuwawa-cli && git pull && ./install.sh
```

### Productivity Workflows

```bash
# Code Review Workflow
git diff > changes.txt
chico chat "Review these code changes: $(cat changes.txt)" --save

# Documentation Workflow  
chico chat "Create README for: $(ls -la)" --model "anthropic/claude-3.5-sonnet" > README.md

# Learning Workflow
chico interactive --banner --model "anthropic/claude-3.5-sonnet"
# Ask questions, get explanations, save to history

# Research Workflow
chico search "topic" --source stackoverflow
chico search "topic" --source github
chico chat "Synthesize information about topic" --search --save
```

## Troubleshooting Examples

### API Key Issues

```bash
# Check if configured
chico providers

# Reconfigure
chico config openrouter --api-key sk-or-v1-NEW_KEY

# Use environment variable instead
export OPENROUTER_API_KEY="sk-or-v1-YOUR_KEY"
```

### Model Not Found

```bash
# List available models
chico models

# Use exact model ID from list
chico chat "Hello" --model "exact-model-id-from-list"
```

### Enhanced Features Not Working

```bash
# Install all dependencies
pip install -r requirements.txt

# Or install specific features
pip install pygments  # Syntax highlighting
pip install rich colorama  # Colors
pip install qrcode pillow  # QR codes
pip install duckduckgo-search  # Internet search
```

## More Examples

For more examples and use cases, see:
- [README.md](README.md) - Main documentation
- [INSTALLATION.md](INSTALLATION.md) - Installation guide
- [GitHub Issues](https://github.com/CA0071/chico-chuwawa-cli/issues) - Community examples

---

**Chico Chuwawa AI CLI** - Your comprehensive AI companion! 🐕✨
