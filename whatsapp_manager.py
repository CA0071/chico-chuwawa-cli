"""
WhatsApp Manager Module
Handles WhatsApp Web automation using Selenium for QR code scanning,
message monitoring, and sending AI-generated responses.
"""

import os
import sys
import time
import json
from pathlib import Path
from typing import Optional, List, Dict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService


class WhatsAppManager:
    """Manages WhatsApp Web automation and AI integration"""
    
    # WhatsApp Web selectors (these may need updates if WhatsApp changes their UI)
    SELECTORS = {
        'qr_code': 'canvas[aria-label="Scan this QR code to link a device!"]',
        'search_box': 'div[contenteditable="true"][data-tab="3"]',
        'chat_list': 'div[aria-label*="Chat list"]',
        'message_input': 'div[contenteditable="true"][data-tab="10"]',
        'send_button': 'button[aria-label="Send"]',
        'messages': 'div[class*="message"]',
        'unread_messages': 'span[aria-label*="unread message"]'
    }
    
    def __init__(self, browser: str = 'chrome', headless: bool = False):
        """
        Initialize WhatsApp Manager
        
        Args:
            browser: Browser to use ('chrome', 'firefox', 'edge')
            headless: Whether to run browser in headless mode
        """
        self.browser = browser.lower()
        self.headless = headless
        self.driver = None
        self.connected = False
        self.session_dir = self._get_session_dir()
        
    def _get_session_dir(self) -> Path:
        """Get directory for storing browser session data"""
        if os.name == 'nt':
            session_dir = Path(os.environ.get('APPDATA', '')) / 'ChicoChuwawa-CLI' / 'whatsapp-session'
        else:
            session_dir = Path.home() / '.config' / 'chico-cli' / 'whatsapp-session'
        
        session_dir.mkdir(parents=True, exist_ok=True)
        return session_dir
    
    def _setup_driver(self):
        """Setup Selenium WebDriver based on selected browser"""
        print(f"Setting up {self.browser.capitalize()} browser...")
        
        options = None
        service = None
        
        try:
            if self.browser == 'chrome':
                from selenium.webdriver.chrome.options import Options
                options = Options()
                options.add_argument(f'user-data-dir={self.session_dir}')
                options.add_argument('--disable-blink-features=AutomationControlled')
                options.add_experimental_option('excludeSwitches', ['enable-automation'])
                options.add_experimental_option('useAutomationExtension', False)
                
                if self.headless:
                    options.add_argument('--headless=new')
                    options.add_argument('--window-size=1920,1080')
                
                service = ChromeService(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=options)
                
            elif self.browser == 'firefox':
                from selenium.webdriver.firefox.options import Options
                options = Options()
                
                # Firefox profile for session persistence
                profile = webdriver.FirefoxProfile()
                profile.set_preference('dom.webdriver.enabled', False)
                profile.set_preference('useAutomationExtension', False)
                
                if self.headless:
                    options.add_argument('--headless')
                
                service = FirefoxService(GeckoDriverManager().install())
                self.driver = webdriver.Firefox(service=service, options=options, firefox_profile=profile)
                
            elif self.browser == 'edge':
                from selenium.webdriver.edge.options import Options
                options = Options()
                options.add_argument(f'user-data-dir={self.session_dir}')
                options.add_argument('--disable-blink-features=AutomationControlled')
                options.add_experimental_option('excludeSwitches', ['enable-automation'])
                options.add_experimental_option('useAutomationExtension', False)
                
                if self.headless:
                    options.add_argument('--headless')
                    options.add_argument('--window-size=1920,1080')
                
                service = EdgeService(EdgeChromiumDriverManager().install())
                self.driver = webdriver.Edge(service=service, options=options)
                
            else:
                raise ValueError(f"Unsupported browser: {self.browser}")
            
            print(f"✓ {self.browser.capitalize()} browser initialized")
            
        except Exception as e:
            print(f"Error setting up browser: {e}")
            print(f"Make sure {self.browser} is installed on your system.")
            raise
    
    def connect(self, timeout: int = 60):
        """
        Connect to WhatsApp Web and handle QR code scanning
        
        Args:
            timeout: Maximum time to wait for QR code scan (seconds)
        """
        if self.driver is None:
            self._setup_driver()
        
        print("\n🔗 Connecting to WhatsApp Web...")
        print("📱 Please scan the QR code with your phone when it appears")
        
        try:
            # Navigate to WhatsApp Web
            self.driver.get('https://web.whatsapp.com')
            
            # Wait for either QR code or chat interface (if already logged in)
            print("\nWaiting for WhatsApp Web to load...")
            
            # Check if already logged in
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, self.SELECTORS['search_box']))
                )
                print("\n✓ Already logged in to WhatsApp Web!")
                self.connected = True
                return True
            except TimeoutException:
                pass
            
            # Wait for QR code to appear
            try:
                qr_element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, self.SELECTORS['qr_code']))
                )
                print("\n✓ QR code displayed! Please scan with WhatsApp on your phone...")
                print(f"   (You have {timeout} seconds to scan)")
            except TimeoutException:
                print("Warning: Could not detect QR code element. It may still be visible.")
            
            # Wait for successful login (QR code disappears and chat interface appears)
            print("\nWaiting for QR code scan...")
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.SELECTORS['search_box']))
            )
            
            print("\n✓ Successfully connected to WhatsApp Web!")
            self.connected = True
            return True
            
        except TimeoutException:
            print(f"\n✗ Connection timeout. QR code was not scanned within {timeout} seconds.")
            return False
        except Exception as e:
            print(f"\n✗ Connection error: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from WhatsApp Web and close browser"""
        if self.driver:
            print("\n🔌 Disconnecting from WhatsApp Web...")
            self.driver.quit()
            self.driver = None
            self.connected = False
            print("✓ Disconnected successfully")
    
    def get_unread_chats(self) -> List[Dict[str, str]]:
        """
        Get list of chats with unread messages
        
        Returns:
            List of dicts with chat info: {'name': str, 'last_message': str}
        """
        if not self.connected:
            print("Error: Not connected to WhatsApp Web")
            return []
        
        unread_chats = []
        
        try:
            # Find all chat elements with unread indicators
            chat_elements = self.driver.find_elements(By.CSS_SELECTOR, 'div[role="listitem"]')
            
            for chat in chat_elements:
                try:
                    # Check if chat has unread messages
                    unread_badge = chat.find_elements(By.CSS_SELECTOR, 'span[aria-label*="unread"]')
                    
                    if unread_badge:
                        # Get chat name
                        name_element = chat.find_element(By.CSS_SELECTOR, 'span[dir="auto"][title]')
                        name = name_element.get_attribute('title')
                        
                        # Get last message preview
                        message_elements = chat.find_elements(By.CSS_SELECTOR, 'span.selectable-text')
                        last_message = message_elements[-1].text if message_elements else ""
                        
                        unread_chats.append({
                            'name': name,
                            'last_message': last_message
                        })
                except (NoSuchElementException, IndexError):
                    continue
            
            return unread_chats
            
        except Exception as e:
            print(f"Error getting unread chats: {e}")
            return []
    
    def monitor_messages(self, callback=None, interval: int = 5):
        """
        Monitor incoming messages continuously
        
        Args:
            callback: Function to call when new message is detected
            interval: Check interval in seconds
        """
        if not self.connected:
            print("Error: Not connected to WhatsApp Web")
            return
        
        print("\n👀 Monitoring WhatsApp messages...")
        print("   Press Ctrl+C to stop monitoring\n")
        
        last_unread_count = 0
        
        try:
            while True:
                unread_chats = self.get_unread_chats()
                current_count = len(unread_chats)
                
                if current_count > last_unread_count:
                    # New messages detected
                    new_chats = unread_chats[last_unread_count:]
                    
                    for chat in new_chats:
                        print(f"\n📩 New message from: {chat['name']}")
                        print(f"   Message: {chat['last_message']}")
                        
                        if callback:
                            callback(chat['name'], chat['last_message'])
                
                last_unread_count = current_count
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n\n⏹ Stopped monitoring")
    
    def send_message(self, chat_name: str, message: str) -> bool:
        """
        Send a message to a specific chat
        
        Args:
            chat_name: Name of the contact or group
            message: Message text to send
            
        Returns:
            True if message was sent successfully, False otherwise
        """
        if not self.connected:
            print("Error: Not connected to WhatsApp Web")
            return False
        
        try:
            # Search for the chat
            search_box = self.driver.find_element(By.CSS_SELECTOR, self.SELECTORS['search_box'])
            search_box.clear()
            search_box.click()
            search_box.send_keys(chat_name)
            time.sleep(2)  # Wait for search results
            
            # Click on the first result
            chat_result = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f'//span[@title="{chat_name}"]'))
            )
            chat_result.click()
            time.sleep(1)
            
            # Find message input and send message
            message_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.SELECTORS['message_input']))
            )
            
            # Split message by lines and send each line
            lines = message.split('\n')
            for i, line in enumerate(lines):
                message_box.send_keys(line)
                if i < len(lines) - 1:
                    # Shift+Enter for new line
                    from selenium.webdriver.common.keys import Keys
                    message_box.send_keys(Keys.SHIFT + Keys.ENTER)
            
            # Click send button
            send_button = self.driver.find_element(By.CSS_SELECTOR, self.SELECTORS['send_button'])
            send_button.click()
            
            print(f"\n✓ Message sent to {chat_name}")
            return True
            
        except TimeoutException:
            print(f"\n✗ Could not find chat: {chat_name}")
            return False
        except Exception as e:
            print(f"\n✗ Error sending message: {e}")
            return False
    
    def send_ai_prompt(self, chat_name: str, prompt: str, ai_client=None) -> bool:
        """
        Generate AI response and send to chat
        
        Args:
            chat_name: Name of the contact or group
            prompt: Prompt to send to AI
            ai_client: AICLI instance for generating response
            
        Returns:
            True if successful, False otherwise
        """
        if not ai_client:
            print("Error: AI client not provided")
            return False
        
        # For now, just send the prompt directly
        # In a more advanced implementation, this could:
        # 1. Read the chat history
        # 2. Use AI to generate a contextual response
        # 3. Send the AI-generated response
        
        return self.send_message(chat_name, prompt)
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - cleanup"""
        self.disconnect()
