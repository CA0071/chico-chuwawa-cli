#!/usr/bin/env python3
"""
Test script for MCP Server integrations
Demonstrates the functionality without requiring real API keys
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mcp_servers import (
    MCPServerConfig, EnvironmentMode,
    GitHubMCPServer, RailwayMCPServer, VercelMCPServer,
    Office365MCPServer, BrowserMCPServer, ZohoCRMMCPServer,
    ZohoDeskMCPServer, ZohoInvoiceMCPServer
)


def test_base_functionality():
    """Test base MCP server functionality"""
    print("=" * 60)
    print("Testing Base MCP Server Functionality")
    print("=" * 60)
    
    # Test configuration
    config = MCPServerConfig("test-service", EnvironmentMode.SANDBOX)
    config.set_credential("test_key", "test_value")
    config.set_setting("test_setting", "test_value")
    
    assert config.get_credential("test_key") == "test_value"
    assert config.get_setting("test_setting") == "test_value"
    assert config.is_sandbox() == True
    assert config.is_production() == False
    
    print("✓ Configuration management works correctly")
    
    # Test production mode
    prod_config = MCPServerConfig("test-service", EnvironmentMode.PRODUCTION)
    assert prod_config.is_production() == True
    assert prod_config.is_sandbox() == False
    
    print("✓ Environment mode switching works correctly")
    print()


def test_github_server():
    """Test GitHub MCP server (without real credentials)"""
    print("=" * 60)
    print("Testing GitHub MCP Server")
    print("=" * 60)
    
    config = MCPServerConfig("github", EnvironmentMode.SANDBOX)
    server = GitHubMCPServer(config)
    
    # Test without authentication
    assert server.authenticate() == False  # Should fail without token
    print("✓ GitHub server correctly requires authentication")
    
    # Add mock token
    config.set_credential("token", "mock_token_for_testing")
    assert server.authenticate() == True
    print("✓ GitHub server accepts token configuration")
    
    # Test environment info
    env_info = server.get_environment_info()
    assert env_info["mode"] == "sandbox"
    assert env_info["name"] == "github"
    print("✓ GitHub server provides correct environment info")
    print()


def test_browser_server():
    """Test Browser MCP server"""
    print("=" * 60)
    print("Testing Browser MCP Server")
    print("=" * 60)
    
    config = MCPServerConfig("browser", EnvironmentMode.SANDBOX)
    server = BrowserMCPServer(config)
    
    # Test authentication (no credentials needed)
    assert server.authenticate() == True
    print("✓ Browser server doesn't require authentication")
    
    # Test environment info
    env_info = server.get_environment_info()
    assert env_info["mode"] == "sandbox"
    print("✓ Browser server provides correct environment info")
    print()


def test_railway_server():
    """Test Railway MCP server (without real credentials)"""
    print("=" * 60)
    print("Testing Railway MCP Server")
    print("=" * 60)
    
    config = MCPServerConfig("railway", EnvironmentMode.SANDBOX)
    server = RailwayMCPServer(config)
    
    # Test without authentication
    assert server.authenticate() == False
    print("✓ Railway server correctly requires authentication")
    
    # Add mock token
    config.set_credential("token", "mock_token")
    assert server.authenticate() == True
    print("✓ Railway server accepts token configuration")
    print()


def test_vercel_server():
    """Test Vercel MCP server (without real credentials)"""
    print("=" * 60)
    print("Testing Vercel MCP Server")
    print("=" * 60)
    
    config = MCPServerConfig("vercel", EnvironmentMode.SANDBOX)
    server = VercelMCPServer(config)
    
    # Test without authentication
    assert server.authenticate() == False
    print("✓ Vercel server correctly requires authentication")
    
    # Add mock token
    config.set_credential("token", "mock_token")
    assert server.authenticate() == True
    print("✓ Vercel server accepts token configuration")
    print()


def test_office365_server():
    """Test Office 365 MCP server (without real credentials)"""
    print("=" * 60)
    print("Testing Office 365 MCP Server")
    print("=" * 60)
    
    config = MCPServerConfig("office365", EnvironmentMode.SANDBOX)
    server = Office365MCPServer(config)
    
    # Test without authentication
    assert server.authenticate() == False
    print("✓ Office 365 server correctly requires authentication")
    
    # Add mock token
    config.set_credential("access_token", "mock_token")
    assert server.authenticate() == True
    print("✓ Office 365 server accepts access token configuration")
    print()


def test_zoho_servers():
    """Test Zoho MCP servers (without real credentials)"""
    print("=" * 60)
    print("Testing Zoho MCP Servers")
    print("=" * 60)
    
    # Test Zoho CRM
    crm_config = MCPServerConfig("zoho-crm", EnvironmentMode.SANDBOX)
    crm_server = ZohoCRMMCPServer(crm_config)
    
    assert crm_server.authenticate() == False
    crm_config.set_credential("access_token", "mock_token")
    assert crm_server.authenticate() == True
    print("✓ Zoho CRM server authentication works correctly")
    
    # Test Zoho Desk
    desk_config = MCPServerConfig("zoho-desk", EnvironmentMode.SANDBOX)
    desk_server = ZohoDeskMCPServer(desk_config)
    
    assert desk_server.authenticate() == False
    desk_config.set_credential("access_token", "mock_token")
    desk_config.set_credential("org_id", "mock_org")
    assert desk_server.authenticate() == True
    print("✓ Zoho Desk server authentication works correctly")
    
    # Test Zoho Invoice
    invoice_config = MCPServerConfig("zoho-invoice", EnvironmentMode.SANDBOX)
    invoice_server = ZohoInvoiceMCPServer(invoice_config)
    
    assert invoice_server.authenticate() == False
    invoice_config.set_credential("access_token", "mock_token")
    invoice_config.set_credential("organization_id", "mock_org")
    assert invoice_server.authenticate() == True
    print("✓ Zoho Invoice server authentication works correctly")
    print()


def run_all_tests():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("MCP SERVER INTEGRATION TESTS")
    print("=" * 60 + "\n")
    
    try:
        test_base_functionality()
        test_github_server()
        test_browser_server()
        test_railway_server()
        test_vercel_server()
        test_office365_server()
        test_zoho_servers()
        
        print("=" * 60)
        print("ALL TESTS PASSED ✅")
        print("=" * 60)
        print()
        print("Summary:")
        print("  ✓ Base MCP server functionality")
        print("  ✓ GitHub integration")
        print("  ✓ Railway integration")
        print("  ✓ Vercel integration")
        print("  ✓ Office 365 integration")
        print("  ✓ Browser automation integration")
        print("  ✓ Zoho CRM integration")
        print("  ✓ Zoho Desk integration")
        print("  ✓ Zoho Invoice integration")
        print()
        print("Next steps:")
        print("  1. Configure real credentials for services you want to use")
        print("  2. Test with real API calls in sandbox mode")
        print("  3. Switch to production mode when ready")
        print()
        
        return 0
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
