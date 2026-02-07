# Chico Chuwawa CLI - Quick Start with MCP Servers

## What are MCP Servers?

MCP (Model Context Protocol) Servers are integrations that allow Chico Chuwawa CLI to interact with external services like GitHub, Railway, Vercel, Office 365, Browser automation, and Zoho services.

## Quick Setup (5 minutes)

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Choose Your Integration

Pick one or more services to integrate:

#### Option A: GitHub (Easiest to Start)

```bash
# Get a GitHub token from: https://github.com/settings/tokens
python chico-cli.py mcp config github --token YOUR_GITHUB_TOKEN --mode sandbox

# Test it
python chico-cli.py mcp github status
python chico-cli.py mcp github list-repos
```

#### Option B: Browser Automation (No API Keys Needed!)

```bash
# Install Playwright browsers
playwright install

# Configure (no token needed)
python chico-cli.py mcp config browser --mode sandbox

# Test it
python chico-cli.py mcp browser status
```

#### Option C: Railway Deployments

```bash
# Get a Railway token from: https://railway.app/account/tokens
python chico-cli.py mcp config railway --token YOUR_RAILWAY_TOKEN --mode sandbox

# Test it
python chico-cli.py mcp railway status
python chico-cli.py mcp railway list-projects
```

#### Option D: Vercel Deployments

```bash
# Get a Vercel token from: https://vercel.com/account/tokens
python chico-cli.py mcp config vercel --token YOUR_VERCEL_TOKEN --mode sandbox

# Test it
python chico-cli.py mcp vercel status
python chico-cli.py mcp vercel list-projects
```

### 3. List Your Configured Services

```bash
python chico-cli.py mcp list
```

You'll see:
```
📋 MCP Services:
------------------------------------------------------------
  🧪 GITHUB
     Mode: sandbox
     Credentials: ✓ Configured

  🧪 BROWSER
     Mode: sandbox
     Credentials: ✓ Configured
```

## Understanding Modes

### Sandbox Mode (🧪)
- **Safe for testing**
- Simulates destructive operations
- Read operations work normally
- Perfect for learning

### Production Mode (🚀)
- **Use with caution**
- All operations are real
- Changes affect your actual data
- Use only after testing in sandbox

## Common Commands

### GitHub

```bash
# List your repositories
python chico-cli.py mcp github list-repos

# Create a repository (simulated in sandbox)
python chico-cli.py mcp github create-repo test-repo --description "Test repo"

# Get status
python chico-cli.py mcp github status
```

### Browser Automation

```bash
# Launch browser
python chico-cli.py mcp browser launch

# Navigate to a website
python chico-cli.py mcp browser navigate https://github.com

# Take a screenshot
python chico-cli.py mcp browser screenshot /tmp/screenshot.png
```

### Railway

```bash
# List projects
python chico-cli.py mcp railway list-projects

# Get status
python chico-cli.py mcp railway status
```

### Vercel

```bash
# List projects
python chico-cli.py mcp vercel list-projects

# List deployments
python chico-cli.py mcp vercel list-deployments

# Get status
python chico-cli.py mcp vercel status
```

## Switching to Production Mode

After testing in sandbox mode, you can switch to production:

```bash
# Reconfigure with production mode
python chico-cli.py mcp config github --token YOUR_TOKEN --mode production
```

**⚠️ Warning**: In production mode, all operations are real and will affect your actual data!

## Getting Help

### For specific service:
```bash
python chico-cli.py mcp github --help
python chico-cli.py mcp browser --help
```

### For all MCP commands:
```bash
python chico-cli.py mcp --help
```

### Full CLI help:
```bash
python chico-cli.py --help
```

## Troubleshooting

### "Service not configured"
Run the config command first:
```bash
python chico-cli.py mcp config <service> --token YOUR_TOKEN
```

### "Failed to initialize"
- Check your token is valid
- Ensure you have internet connection
- Verify the service is accessible

### Browser automation issues
Install Playwright browsers:
```bash
playwright install
```

## Next Steps

1. ✅ Configure your first service
2. ✅ Test in sandbox mode
3. ✅ Try different operations
4. ✅ Switch to production when ready
5. ✅ Read full guide: [MCP_INTEGRATION_GUIDE.md](MCP_INTEGRATION_GUIDE.md)

## Examples by Use Case

### Developer Workflow
```bash
# Setup GitHub
python chico-cli.py mcp config github --token TOKEN --mode sandbox

# Create repository
python chico-cli.py mcp github create-repo my-project

# List repositories
python chico-cli.py mcp github list-repos
```

### Web Scraping/Testing
```bash
# Setup browser
python chico-cli.py mcp config browser --mode sandbox

# Launch and navigate
python chico-cli.py mcp browser launch
python chico-cli.py mcp browser navigate https://example.com
python chico-cli.py mcp browser screenshot result.png
```

### Deployment Management
```bash
# Setup Railway
python chico-cli.py mcp config railway --token TOKEN --mode sandbox

# List projects and deployments
python chico-cli.py mcp railway list-projects
```

## Tips

1. **Always start with sandbox mode** - Test safely before production
2. **Keep tokens secure** - Never commit them to version control
3. **Use environment variables** - For automation and CI/CD
4. **Check service status** - Use `status` command to verify connectivity
5. **List before you create** - Avoid duplicates

## Need More Help?

- Read the full guide: [MCP_INTEGRATION_GUIDE.md](MCP_INTEGRATION_GUIDE.md)
- Check the main README: [README.md](README.md)
- Review examples in the documentation

---

**Happy automating! 🚀**
