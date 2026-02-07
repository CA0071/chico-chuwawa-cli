# WhatsApp Integration Usage Guide

This document provides detailed instructions on using the WhatsApp integration features of Chico Chuwawa AI CLI.

## Prerequisites

1. **Browser**: You need one of the following browsers installed:
   - Google Chrome (default)
   - Mozilla Firefox
   - Microsoft Edge

2. **WhatsApp**: You must have WhatsApp installed on your phone and be able to scan QR codes.

3. **Dependencies**: All required dependencies will be automatically installed when you first use a WhatsApp command.

## Quick Start

### 1. Connect to WhatsApp Web

The first step is to establish a connection to WhatsApp Web by scanning a QR code:

```bash
python chico-cli.py whatsapp connect
```

**What happens:**
1. A browser window opens displaying WhatsApp Web
2. A QR code appears on the screen
3. Open WhatsApp on your phone
4. Go to Settings > Linked Devices > Link a Device
5. Scan the QR code displayed in the browser
6. Once scanned, the connection is established
7. Press Enter to disconnect and close the browser

**Advanced options:**
```bash
# Use Firefox instead of Chrome
python chico-cli.py whatsapp connect --browser firefox

# Increase QR scan timeout to 2 minutes
python chico-cli.py whatsapp connect --timeout 120

# Use Edge browser
python chico-cli.py whatsapp connect --browser edge
```

### 2. Monitor Incoming Messages

Once connected, you can monitor incoming messages in real-time:

```bash
python chico-cli.py whatsapp monitor
```

**What happens:**
1. Browser opens and connects to WhatsApp Web
2. The CLI starts checking for new messages every 5 seconds (default)
3. When a new message arrives, it displays:
   - Sender's name
   - Message preview
4. Press Ctrl+C to stop monitoring

**Advanced options:**
```bash
# Check for new messages every 10 seconds
python chico-cli.py whatsapp monitor --interval 10

# Monitor with Firefox
python chico-cli.py whatsapp monitor --browser firefox
```

**Example output:**
```
👀 WhatsApp Message Monitor
============================================================
Browser: Chrome
Check interval: 5 seconds

Monitoring WhatsApp messages...
   Press Ctrl+C to stop monitoring

📩 New message from: John Doe
   Message: Hey, are you available?

📩 New message from: Family Group
   Message: Dinner at 7pm tonight!
```

### 3. Send Messages

Send a message to any contact or group:

```bash
python chico-cli.py whatsapp send "John Doe" "Hello from CLI!"
```

**What happens:**
1. Browser opens and connects to WhatsApp Web
2. Searches for the specified contact/group
3. Opens the chat
4. Sends the message
5. Closes the browser

**Examples:**
```bash
# Send to a contact
python chico-cli.py whatsapp send "Jane Smith" "Meeting at 3pm"

# Send to a group
python chico-cli.py whatsapp send "Work Team" "Project deadline extended"

# Multi-line message (use quotes)
python chico-cli.py whatsapp send "John" "Line 1
Line 2
Line 3"

# Send with Firefox
python chico-cli.py whatsapp send "Alice" "Hello" --browser firefox
```

### 4. Send AI Prompts

Send AI-generated prompts or responses to chats:

```bash
python chico-cli.py whatsapp prompt "John Doe" "What's the weather today?"
```

**Note:** Currently, this command sends the message directly. In future versions, it could be enhanced to:
- Generate AI responses based on chat context
- Use AI to craft personalized messages
- Integrate with the CLI's AI models for automated responses

**Examples:**
```bash
# Send a prompt
python chico-cli.py whatsapp prompt "Alice" "Can you help me with Python?"

# Send to a group
python chico-cli.py whatsapp prompt "Study Group" "Question about quantum physics"

# With Firefox
python chico-cli.py whatsapp prompt "Bob" "Project update needed" --browser firefox
```

## Tips and Best Practices

### Session Persistence

The CLI saves your WhatsApp session locally, so you won't need to scan the QR code every time:

- **Session location:**
  - Windows: `%APPDATA%\ChicoChuwawa-CLI\whatsapp-session`
  - Linux/Mac: `~/.config/chico-cli/whatsapp-session`

- **If you need to reset:** Delete the session folder and reconnect

### Automation Examples

#### 1. Scheduled Message Sending

Create a script to send messages at specific times:

```bash
#!/bin/bash
# Send morning reminder
python chico-cli.py whatsapp send "Family" "Good morning everyone! 🌅"
```

#### 2. Message Monitoring with Actions

Create a monitoring script that responds to keywords:

```bash
# This would be implemented in a future version with callback support
python chico-cli.py whatsapp monitor
```

#### 3. Bulk Message Sending

Send the same message to multiple contacts:

```bash
#!/bin/bash
CONTACTS=("Alice" "Bob" "Charlie")
MESSAGE="Meeting reminder: Tomorrow at 10am"

for contact in "${CONTACTS[@]}"; do
    python chico-cli.py whatsapp send "$contact" "$MESSAGE"
    sleep 5  # Wait 5 seconds between messages
done
```

## Troubleshooting

### Browser Issues

**Problem:** Browser doesn't open or crashes
**Solution:**
1. Make sure the browser is installed
2. Try a different browser with `--browser` flag
3. Update your browser to the latest version

**Problem:** "WebDriver not found"
**Solution:**
- The CLI automatically downloads the appropriate WebDriver
- If it fails, check your internet connection
- Try running with administrator/sudo privileges

### Connection Issues

**Problem:** QR code doesn't appear
**Solution:**
1. Increase timeout: `--timeout 120`
2. Try a different browser
3. Clear browser cache and cookies
4. Check internet connection

**Problem:** QR code won't scan
**Solution:**
1. Make sure your phone has internet connection
2. Check WhatsApp is up to date on your phone
3. Try logging out of other WhatsApp Web sessions
4. Make sure the QR code is clearly visible

**Problem:** Connection drops frequently
**Solution:**
1. Keep the browser window open
2. Check your internet stability
3. Don't manually close WhatsApp Web tabs

### Message Sending Issues

**Problem:** Chat not found
**Solution:**
1. Make sure the contact/group name is exactly correct
2. Check spelling and capitalization
3. The contact must exist in your WhatsApp contacts

**Problem:** Message not sending
**Solution:**
1. Check internet connection
2. Verify WhatsApp Web is connected
3. Make sure you haven't been restricted by WhatsApp

## Limitations

1. **WhatsApp Web Dependency**: This integration uses WhatsApp Web, so it inherits all its limitations
2. **Phone Connection Required**: Your phone must be connected to the internet
3. **Rate Limiting**: WhatsApp may rate-limit automated messages
4. **Session Management**: Sessions expire after a period of inactivity
5. **No Media Support**: Currently only text messages are supported

## Future Enhancements

Potential improvements being considered:

1. **AI Integration**: Full AI-powered automated responses
2. **Media Support**: Send images, videos, and documents
3. **Group Management**: Create groups, add/remove members
4. **Message History**: Read and search message history
5. **Status Updates**: Post and view WhatsApp statuses
6. **Callback Support**: Custom callback functions for message events
7. **Webhook Integration**: Integration with webhooks for automation

## Security and Privacy

### Important Notes

1. **Session Data**: Your WhatsApp session is stored locally on your computer
2. **No Cloud Storage**: Session data is never uploaded to any cloud service
3. **API Keys**: No API keys are required for WhatsApp functionality
4. **Official API**: This uses WhatsApp Web, not unofficial APIs
5. **Terms of Service**: Make sure your usage complies with WhatsApp's Terms of Service

### Best Practices

1. **Don't share session folder**: Keep your session data private
2. **Logout when done**: Use `connect` command and disconnect when finished
3. **Avoid spam**: Don't send automated messages to strangers
4. **Respect privacy**: Don't monitor conversations without consent
5. **Rate limiting**: Avoid sending too many messages too quickly

## Support

If you encounter issues:

1. Check this guide first
2. Review the main README.md
3. Make sure all dependencies are installed
4. Try with a different browser
5. Check your internet connection
6. Ensure WhatsApp is working normally on your phone

## Examples

### Example 1: Simple Connection Test

```bash
# Connect and verify WhatsApp Web works
python chico-cli.py whatsapp connect
# Scan QR code
# Wait for "Successfully connected" message
# Press Enter to disconnect
```

### Example 2: Monitor for 1 Hour

```bash
# Start monitoring and let it run
python chico-cli.py whatsapp monitor --interval 10
# Press Ctrl+C after an hour to stop
```

### Example 3: Send Daily Reminder

Create a file `daily_reminder.sh`:
```bash
#!/bin/bash
MESSAGE="Daily standup at 10am! 📅"
python chico-cli.py whatsapp send "Work Team" "$MESSAGE"
```

Make it executable and schedule with cron:
```bash
chmod +x daily_reminder.sh
# Add to crontab: 0 9 * * * /path/to/daily_reminder.sh
```

---

**Built by Max van Heerden**  
**Part of Chico Chuwawa AI CLI v2.0.0**
