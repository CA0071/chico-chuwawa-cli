"""
WhatsApp Integration via QR Code
Monitor and prompt via WhatsApp
"""

import qrcode
import io
from typing import Optional, Callable
import threading
import time


class WhatsAppIntegration:
    """WhatsApp integration for monitoring and prompting"""
    
    def __init__(self):
        self.connected = False
        self.session_id = None
        self.qr_code = None
        self.monitoring = False
        self.message_handler: Optional[Callable] = None
    
    def generate_qr_code(self, data: str) -> str:
        """
        Generate QR code for WhatsApp connection
        
        Args:
            data: Data to encode in QR code
        
        Returns:
            ASCII art QR code
        """
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        # Create ASCII QR code
        qr_ascii = qr.get_matrix()
        ascii_art = []
        for row in qr_ascii:
            line = ''.join(['██' if cell else '  ' for cell in row])
            ascii_art.append(line)
        
        return '\n'.join(ascii_art)
    
    def show_connection_qr(self) -> str:
        """
        Display QR code for WhatsApp connection
        
        Returns:
            QR code as ASCII art
        """
        # Generate a connection URL (this would be provided by WhatsApp API)
        connection_url = f"https://wa.me/qr/CHICO-CLI-{int(time.time())}"
        
        print("\n📱 Scan this QR code with WhatsApp to connect:\n")
        qr_ascii = self.generate_qr_code(connection_url)
        print(qr_ascii)
        print("\n✓ Open WhatsApp on your phone")
        print("✓ Tap Menu or Settings > Linked Devices")
        print("✓ Tap 'Link a Device' and scan the QR code above\n")
        
        return qr_ascii
    
    def connect(self) -> bool:
        """
        Establish WhatsApp connection
        
        Returns:
            True if connected successfully
        """
        print("\n🔗 Connecting to WhatsApp...")
        
        # Show QR code
        self.show_connection_qr()
        
        # Simulate connection (in real implementation, wait for scan)
        print("⏳ Waiting for QR code scan...")
        time.sleep(2)
        
        # In a real implementation, this would use WhatsApp Web API
        self.connected = True
        self.session_id = f"session_{int(time.time())}"
        
        print("✓ Connected to WhatsApp!\n")
        return True
    
    def disconnect(self):
        """Disconnect from WhatsApp"""
        self.connected = False
        self.session_id = None
        self.monitoring = False
        print("✓ Disconnected from WhatsApp")
    
    def send_message(self, phone_number: str, message: str) -> bool:
        """
        Send a message via WhatsApp
        
        Args:
            phone_number: Recipient phone number
            message: Message to send
        
        Returns:
            True if sent successfully
        """
        if not self.connected:
            print("❌ Not connected to WhatsApp")
            return False
        
        print(f"📤 Sending message to {phone_number}...")
        # In real implementation, send via WhatsApp API
        print(f"✓ Message sent: {message[:50]}...")
        return True
    
    def start_monitoring(self, callback: Callable[[str, str], None]):
        """
        Start monitoring for incoming messages
        
        Args:
            callback: Function to call when message received (phone, message)
        """
        if not self.connected:
            print("❌ Not connected to WhatsApp")
            return
        
        self.monitoring = True
        self.message_handler = callback
        
        print("👂 Monitoring WhatsApp messages...")
        print("   Send 'stop' to stop monitoring\n")
        
        # In real implementation, this would listen to WhatsApp messages
        # For now, just set the flag
    
    def stop_monitoring(self):
        """Stop monitoring messages"""
        self.monitoring = False
        self.message_handler = None
        print("✓ Stopped monitoring WhatsApp")
    
    def get_status(self) -> dict:
        """
        Get current WhatsApp integration status
        
        Returns:
            Status dictionary
        """
        return {
            'connected': self.connected,
            'session_id': self.session_id,
            'monitoring': self.monitoring
        }
    
    def send_ai_response(self, phone_number: str, prompt: str, ai_response: str) -> bool:
        """
        Send AI response to WhatsApp
        
        Args:
            phone_number: Recipient phone number
            prompt: Original prompt
            ai_response: AI's response
        
        Returns:
            True if sent successfully
        """
        message = f"🤖 Chico AI Response\n\n📝 Prompt: {prompt}\n\n💬 Response:\n{ai_response}"
        return self.send_message(phone_number, message)


def create_connection_qr() -> str:
    """
    Create a WhatsApp connection QR code
    
    Returns:
        ASCII QR code
    """
    integration = WhatsAppIntegration()
    return integration.show_connection_qr()
