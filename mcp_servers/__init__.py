"""
MCP (Model Context Protocol) Servers for Chico Chuwawa CLI
Provides integrations with various external services
"""

from .base import BaseMCPServer, MCPServerConfig, EnvironmentMode
from .github_server import GitHubMCPServer
from .railway_server import RailwayMCPServer
from .vercel_server import VercelMCPServer
from .office365_server import Office365MCPServer
from .browser_server import BrowserMCPServer
from .zoho_crm_server import ZohoCRMMCPServer
from .zoho_desk_server import ZohoDeskMCPServer
from .zoho_invoice_server import ZohoInvoiceMCPServer

__all__ = [
    'BaseMCPServer',
    'MCPServerConfig',
    'EnvironmentMode',
    'GitHubMCPServer',
    'RailwayMCPServer',
    'VercelMCPServer',
    'Office365MCPServer',
    'BrowserMCPServer',
    'ZohoCRMMCPServer',
    'ZohoDeskMCPServer',
    'ZohoInvoiceMCPServer',
]
