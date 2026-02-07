# MCP Server Integration Guide

## Overview

Chico Chuwawa CLI now includes MCP (Model Context Protocol) server integrations for multiple external services. Each integration supports both **sandbox** and **production** modes to ensure safe testing before production use.

## Supported Services

1. **GitHub** - Repository management and operations
2. **Railway** - Deployment and project management
3. **Vercel** - Deployment and project management
4. **Office 365** - Email and calendar operations via Microsoft Graph API
5. **Browser** - Browser automation using Playwright
6. **Zoho CRM** - Customer relationship management
7. **Zoho Desk** - Support ticket management
8. **Zoho Invoice** - Invoice and customer management

## Environment Modes

### Sandbox Mode (Default)
- Safe for testing and development
- Simulates destructive operations (create, update, delete)
- Read operations work normally
- Perfect for learning and experimenting

### Production Mode
- Full access to real data and operations
- All operations are executed
- Use with caution
- Recommended only when configuration is tested

## Installation

### Prerequisites

```bash
pip install -r requirements.txt
```

This installs:
- `requests` - HTTP client for API calls
- `playwright` - Browser automation (requires additional setup)

### Playwright Setup (for Browser automation)

```bash
playwright install
```

## Configuration

### General Configuration Command

```bash
python chico-cli.py mcp config <service> [credentials] --mode [sandbox|production]
```

### Service-Specific Configuration

#### 1. GitHub

```bash
# Sandbox mode (default)
python chico-cli.py mcp config github --token YOUR_GITHUB_TOKEN --mode sandbox

# Production mode
python chico-cli.py mcp config github --token YOUR_GITHUB_TOKEN --mode production
```

**Getting a GitHub Token:**
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Select required scopes (repo, admin:org, etc.)
4. Copy the token

#### 2. Railway

```bash
# Sandbox mode
python chico-cli.py mcp config railway --token YOUR_RAILWAY_TOKEN --mode sandbox

# Production mode
python chico-cli.py mcp config railway --token YOUR_RAILWAY_TOKEN --mode production
```

**Getting a Railway Token:**
1. Go to Railway dashboard
2. Click on your profile → Account Settings
3. Go to Tokens section
4. Create new token

#### 3. Vercel

```bash
# Sandbox mode
python chico-cli.py mcp config vercel --token YOUR_VERCEL_TOKEN --mode sandbox

# Production mode
python chico-cli.py mcp config vercel --token YOUR_VERCEL_TOKEN --mode production
```

**Getting a Vercel Token:**
1. Go to Vercel dashboard
2. Settings → Tokens
3. Create new token

#### 4. Office 365

```bash
# Sandbox mode
python chico-cli.py mcp config office365 --access-token YOUR_ACCESS_TOKEN --mode sandbox

# Production mode
python chico-cli.py mcp config office365 --access-token YOUR_ACCESS_TOKEN --mode production
```

**Getting Office 365 Token:**
1. Register app in Azure AD
2. Configure API permissions for Microsoft Graph
3. Generate access token using OAuth 2.0 flow

#### 5. Browser Automation

```bash
# Sandbox mode (simulates actions)
python chico-cli.py mcp config browser --mode sandbox

# Production mode (performs real actions)
python chico-cli.py mcp config browser --mode production
```

**Note:** No credentials needed for browser automation.

#### 6. Zoho CRM

```bash
# Sandbox mode (uses Zoho CRM Sandbox)
python chico-cli.py mcp config zoho-crm --access-token YOUR_TOKEN --mode sandbox

# Production mode (uses production CRM)
python chico-cli.py mcp config zoho-crm --access-token YOUR_TOKEN --mode production
```

**Getting Zoho CRM Token:**
1. Go to Zoho API Console
2. Create Server-based Application
3. Generate access token with required scopes

#### 7. Zoho Desk

```bash
# Sandbox mode
python chico-cli.py mcp config zoho-desk --access-token YOUR_TOKEN --org-id YOUR_ORG_ID --mode sandbox

# Production mode
python chico-cli.py mcp config zoho-desk --access-token YOUR_TOKEN --org-id YOUR_ORG_ID --mode production
```

#### 8. Zoho Invoice

```bash
# Sandbox mode
python chico-cli.py mcp config zoho-invoice --access-token YOUR_TOKEN --org-id YOUR_ORG_ID --mode sandbox

# Production mode
python chico-cli.py mcp config zoho-invoice --access-token YOUR_TOKEN --org-id YOUR_ORG_ID --mode production
```

## Usage Examples

### List Configured Services

```bash
python chico-cli.py mcp list
```

Output:
```
📋 MCP Services:
------------------------------------------------------------
  🧪 GITHUB
     Mode: sandbox
     Credentials: ✓ Configured

  🚀 RAILWAY
     Mode: production
     Credentials: ✓ Configured
```

### GitHub Operations

```bash
# Get status
python chico-cli.py mcp github status

# List repositories
python chico-cli.py mcp github list-repos

# Create repository (simulated in sandbox mode)
python chico-cli.py mcp github create-repo my-new-repo --description "My test repo" --private
```

### Railway Operations

```bash
# Get status
python chico-cli.py mcp railway status

# List projects
python chico-cli.py mcp railway list-projects
```

### Vercel Operations

```bash
# Get status
python chico-cli.py mcp vercel status

# List projects
python chico-cli.py mcp vercel list-projects

# List deployments
python chico-cli.py mcp vercel list-deployments
```

### Office 365 Operations

```bash
# Get status
python chico-cli.py mcp office365 status

# List emails
python chico-cli.py mcp office365 list-emails

# Send email (simulated in sandbox mode)
python chico-cli.py mcp office365 send-email user@example.com "Test Subject" "Email body"
```

### Browser Automation

```bash
# Get status
python chico-cli.py mcp browser status

# Launch browser
python chico-cli.py mcp browser launch --headless

# Navigate to URL
python chico-cli.py mcp browser navigate https://example.com

# Take screenshot
python chico-cli.py mcp browser screenshot /tmp/screenshot.png
```

### Zoho CRM Operations

```bash
# Get status
python chico-cli.py mcp zoho-crm status

# List leads
python chico-cli.py mcp zoho-crm list-leads

# Create lead (uses sandbox if configured)
python chico-cli.py mcp zoho-crm create-lead John Doe john@example.com "Acme Corp"
```

### Zoho Desk Operations

```bash
# Get status
python chico-cli.py mcp zoho-desk status

# List tickets
python chico-cli.py mcp zoho-desk list-tickets
```

### Zoho Invoice Operations

```bash
# Get status
python chico-cli.py mcp zoho-invoice status

# List invoices
python chico-cli.py mcp zoho-invoice list-invoices

# List customers
python chico-cli.py mcp zoho-invoice list-customers
```

## Architecture

### Base MCP Server

All MCP servers inherit from `BaseMCPServer` which provides:
- Authentication handling
- Connection testing
- Status reporting
- Environment mode management

### Configuration Storage

Configurations are stored in:
- **Windows**: `%APPDATA%\ChicoChuwawa-CLI\config.json`
- **Linux/Mac**: `~/.config/chico-cli/config.json`

Example configuration:
```json
{
  "mcp_servers": {
    "github": {
      "credentials": {
        "token": "ghp_xxxxx"
      },
      "mode": "sandbox"
    },
    "railway": {
      "credentials": {
        "token": "xxxxx"
      },
      "mode": "production"
    }
  }
}
```

## Error Handling

All MCP operations include comprehensive error handling:

1. **Authentication Errors**: Clear messages about missing or invalid credentials
2. **Network Errors**: Timeout and connection error handling
3. **API Errors**: HTTP status code interpretation and error messages
4. **Validation Errors**: Input validation with helpful feedback

## Security Best Practices

1. **Use Sandbox Mode First**: Always test with sandbox mode before production
2. **Secure Token Storage**: Keep API tokens secure and never commit them to version control
3. **Rotate Tokens**: Regularly rotate API tokens
4. **Minimal Permissions**: Use tokens with minimal required permissions
5. **Environment Variables**: Consider using environment variables for CI/CD

## Cross-Platform Compatibility

- Works on Windows, macOS, and Linux
- Platform-specific configuration paths handled automatically
- Browser automation supports Chromium, Firefox, and WebKit

## Troubleshooting

### "Service not configured"
**Solution**: Configure the service first:
```bash
python chico-cli.py mcp config <service> [credentials]
```

### "Failed to initialize service"
**Possible causes**:
- Invalid credentials
- Network connectivity issues
- API endpoint changes

**Solution**: Check credentials and network connection

### Browser automation not working
**Solution**: Install Playwright browsers:
```bash
playwright install
```

### Import errors
**Solution**: Install all dependencies:
```bash
pip install -r requirements.txt
```

## API Rate Limits

Be aware of rate limits for each service:
- **GitHub**: 5,000 requests/hour (authenticated)
- **Railway**: Check Railway documentation
- **Vercel**: Check Vercel documentation
- **Office 365**: Varies by endpoint
- **Zoho**: Typically 200 requests/minute per API

## Support and Resources

- **GitHub**: [GitHub API Documentation](https://docs.github.com/en/rest)
- **Railway**: [Railway Documentation](https://docs.railway.app/)
- **Vercel**: [Vercel API Documentation](https://vercel.com/docs/rest-api)
- **Office 365**: [Microsoft Graph Documentation](https://docs.microsoft.com/en-us/graph/)
- **Playwright**: [Playwright Documentation](https://playwright.dev/)
- **Zoho**: [Zoho API Documentation](https://www.zoho.com/crm/developer/docs/api/v3/)

## Future Enhancements

Planned features:
- Additional service integrations
- Webhook support
- Batch operations
- Advanced configuration options
- Integration testing framework

---

**Version**: 2.1.0  
**Last Updated**: February 2026  
**Status**: Production Ready ✅
