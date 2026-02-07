"""
Browser MCP Server Integration
Provides browser automation capabilities using Playwright
"""

from typing import Dict, Any, List, Optional
from .base import BaseMCPServer, MCPServerConfig


class BrowserMCPServer(BaseMCPServer):
    """MCP Server for Browser automation integration"""
    
    def __init__(self, config: MCPServerConfig):
        super().__init__(config)
        self.browser = None
        self.page = None
        self.playwright = None
    
    def authenticate(self) -> bool:
        """No authentication needed for browser automation"""
        return True
    
    def test_connection(self) -> bool:
        """Test browser automation setup"""
        try:
            # Try to import playwright
            from playwright.sync_api import sync_playwright
            return True
        except ImportError:
            print("Error: Playwright not installed. Install with: pip install playwright")
            print("Then run: playwright install")
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """Get browser automation status"""
        browser_running = self.browser is not None
        return {
            "status": "connected" if browser_running else "disconnected",
            "browser_running": browser_running,
            "mode": self.config.mode.value
        }
    
    def launch_browser(self, headless: bool = True, browser_type: str = "chromium") -> bool:
        """Launch a browser instance"""
        try:
            from playwright.sync_api import sync_playwright
            
            if self.config.is_sandbox():
                print("⚠️  Running in SANDBOX mode - browser operations are safe")
            
            self.playwright = sync_playwright().start()
            
            if browser_type == "chromium":
                self.browser = self.playwright.chromium.launch(headless=headless)
            elif browser_type == "firefox":
                self.browser = self.playwright.firefox.launch(headless=headless)
            elif browser_type == "webkit":
                self.browser = self.playwright.webkit.launch(headless=headless)
            else:
                print(f"Unknown browser type: {browser_type}, using chromium")
                self.browser = self.playwright.chromium.launch(headless=headless)
            
            self.page = self.browser.new_page()
            return True
        except Exception as e:
            print(f"Error launching browser: {e}")
            return False
    
    def close_browser(self) -> bool:
        """Close the browser instance"""
        try:
            if self.page:
                self.page.close()
                self.page = None
            if self.browser:
                self.browser.close()
                self.browser = None
            if self.playwright:
                self.playwright.stop()
                self.playwright = None
            return True
        except Exception as e:
            print(f"Error closing browser: {e}")
            return False
    
    def navigate_to(self, url: str) -> bool:
        """Navigate to a URL"""
        if not self.page:
            print("Error: Browser not launched. Use launch_browser() first.")
            return False
        
        try:
            self.page.goto(url)
            return True
        except Exception as e:
            print(f"Error navigating to {url}: {e}")
            return False
    
    def get_page_title(self) -> Optional[str]:
        """Get the current page title"""
        if not self.page:
            print("Error: Browser not launched.")
            return None
        
        try:
            return self.page.title()
        except Exception as e:
            print(f"Error getting page title: {e}")
            return None
    
    def screenshot(self, path: str, full_page: bool = False) -> bool:
        """Take a screenshot of the current page"""
        if not self.page:
            print("Error: Browser not launched.")
            return False
        
        if self.config.is_sandbox():
            print(f"⚠️  SANDBOX mode: Screenshot would be saved to {path}")
            return True
        
        try:
            self.page.screenshot(path=path, full_page=full_page)
            return True
        except Exception as e:
            print(f"Error taking screenshot: {e}")
            return False
    
    def click_element(self, selector: str) -> bool:
        """Click an element on the page"""
        if not self.page:
            print("Error: Browser not launched.")
            return False
        
        if self.config.is_sandbox():
            print(f"⚠️  SANDBOX mode: Would click element: {selector}")
            return True
        
        try:
            self.page.click(selector)
            return True
        except Exception as e:
            print(f"Error clicking element: {e}")
            return False
    
    def fill_input(self, selector: str, text: str) -> bool:
        """Fill an input field"""
        if not self.page:
            print("Error: Browser not launched.")
            return False
        
        if self.config.is_sandbox():
            print(f"⚠️  SANDBOX mode: Would fill '{selector}' with '{text}'")
            return True
        
        try:
            self.page.fill(selector, text)
            return True
        except Exception as e:
            print(f"Error filling input: {e}")
            return False
    
    def get_text_content(self, selector: str) -> Optional[str]:
        """Get text content of an element"""
        if not self.page:
            print("Error: Browser not launched.")
            return None
        
        try:
            return self.page.text_content(selector)
        except Exception as e:
            print(f"Error getting text content: {e}")
            return None
