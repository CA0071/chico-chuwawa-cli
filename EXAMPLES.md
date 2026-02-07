# Chico Chuwawa CLI - Enhanced Features Examples

## Getting Started

### 1. Welcome Screen
```bash
python chico-cli-enhanced.py welcome
```
Shows a beautiful welcome panel with all available features.

### 2. View AI Providers
```bash
python chico-cli-enhanced.py providers
```
Displays a rich table of AI providers with status and default models.

### 3. Check Integration Status
```bash
python chico-cli-enhanced.py integrations
```
Shows health status of all integrations (Docker, Kubernetes, npm, PyPI, cloud providers).

### 4. MCP Hub Status
```bash
python chico-cli-enhanced.py hub-status
```
Displays overall health of the orchestration hub.

## Docker Integration Examples

### List Containers
```bash
python chico-cli-enhanced.py docker containers
```
Shows all Docker containers in a formatted table.

### List Images
```bash
python chico-cli-enhanced.py docker images
```
Displays all Docker images with size information.

### View Container Logs
```bash
python chico-cli-enhanced.py docker logs <container_id>
```
Shows syntax-highlighted logs for a specific container.

## Kubernetes Integration Examples

### List Pods
```bash
# Default namespace
python chico-cli-enhanced.py k8s pods

# Specific namespace
python chico-cli-enhanced.py k8s pods --namespace production
```

### List Deployments
```bash
python chico-cli-enhanced.py k8s deployments --namespace default
```

### List Services
```bash
python chico-cli-enhanced.py k8s services
```

## Package Management Examples

### npm Registry

#### Search Packages
```bash
python chico-cli-enhanced.py npm search react
python chico-cli-enhanced.py npm search vue
python chico-cli-enhanced.py npm search typescript
```

#### Get Package Info
```bash
python chico-cli-enhanced.py npm info react
python chico-cli-enhanced.py npm info express
python chico-cli-enhanced.py npm info webpack
```

### PyPI

#### Get Package Info
```bash
python chico-cli-enhanced.py pypi info requests
python chico-cli-enhanced.py pypi info django
python chico-cli-enhanced.py pypi info flask
```

## AI Chat Examples

### Quick Chat
```bash
python chico-cli-enhanced.py chat "What is artificial intelligence?"
```

### Chat with Specific Model
```bash
python chico-cli-enhanced.py chat "Explain quantum computing" --model meta-llama/llama-3.3-70b-instruct
```

### Interactive Mode
```bash
python chico-cli-enhanced.py interactive
```

## Configuration Examples

### Configure AI Providers
```bash
# OpenRouter
python chico-cli-enhanced.py config openrouter --api-key YOUR_KEY

# Ollama
python chico-cli-enhanced.py config ollama --api-key YOUR_KEY
```

### Switch Active Provider
```bash
python chico-cli-enhanced.py switch ollama
```

### List Available Models
```bash
# Active provider
python chico-cli-enhanced.py models

# Specific provider
python chico-cli-enhanced.py models --provider openrouter
```

## Integration Configuration

### Docker (Remote)
Edit `~/.config/chico-cli/integrations.json` (Linux/Mac) or `%APPDATA%\ChicoChuwawa-CLI\integrations.json` (Windows):
```json
{
  "docker": {
    "base_url": "tcp://remote-host:2375"
  }
}
```

### Kubernetes (Custom Config)
```json
{
  "kubernetes": {
    "kubeconfig_path": "/path/to/kubeconfig"
  }
}
```

### AWS
```json
{
  "aws": {
    "aws_access_key_id": "YOUR_KEY",
    "aws_secret_access_key": "YOUR_SECRET",
    "region": "us-east-1"
  }
}
```

### GCP
```json
{
  "gcp": {
    "credentials_path": "/path/to/service-account.json"
  }
}
```

### Azure
```json
{
  "azure": {
    "connection_string": "DefaultEndpointsProtocol=https;AccountName=...;AccountKey=...;"
  }
}
```

## Advanced Features

### Auto-Completion
The CLI includes AI-powered auto-completion for commands. Tab completion helps you discover available commands and options.

### Real-Time Monitoring
Monitor integrations in real-time with live dashboards (feature available in monitoring module).

### Smart Defaults
The CLI provides intelligent defaults based on your usage patterns and context.

## Comparison: Original vs Enhanced CLI

### Original CLI
```bash
python chico_cli.py chat "Hello"
# Simple text output
```

### Enhanced CLI
```bash
python chico-cli-enhanced.py welcome
# Rich formatted panel with colors and borders

python chico-cli-enhanced.py providers
# Beautiful table with status indicators

python chico-cli-enhanced.py integrations
# Formatted table showing all integration health
```

## Tips and Tricks

1. **Use the welcome screen** to see all available features at a glance
2. **Check integrations status** regularly to ensure all services are healthy
3. **Use npm/PyPI search** before installing packages to find alternatives
4. **Monitor Docker containers** to track resource usage
5. **Check K8s pods** to ensure deployments are running correctly
6. **Use the MCP hub** to manage all integrations from one place

## Troubleshooting

### Docker Not Working
- Ensure Docker daemon is running
- Check Docker socket permissions
- For remote Docker, verify network connectivity

### Kubernetes Not Working
- Verify kubectl is configured
- Check kubeconfig file location
- Ensure cluster is accessible

### npm/PyPI Search Slow
- These depend on external APIs
- Network latency may affect response time
- Results are cached when possible

### AI Chat Not Working
- Configure API keys first: `python chico-cli-enhanced.py config openrouter --api-key YOUR_KEY`
- Check active provider: `python chico-cli-enhanced.py providers`
- Verify API key is valid

## Next Steps

1. Configure your AI providers
2. Set up integration credentials
3. Explore Docker and Kubernetes features
4. Try package search and info commands
5. Use the MCP hub for orchestration
6. Enjoy the rich terminal UI!
