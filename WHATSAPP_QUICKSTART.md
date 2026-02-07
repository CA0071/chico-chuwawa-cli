# WhatsApp Integration Quick Start

## What's New in v2.1.0

Chico Chuwawa AI CLI now includes WhatsApp Web integration! You can:
- 📱 Connect to WhatsApp Web via QR code
- 👀 Monitor incoming messages in real-time
- 📤 Send messages to any contact or group
- 🤖 Send AI-generated prompts and responses

## Prerequisites

1. **Install dependencies** (if not already installed):
   ```bash
   pip install -r requirements.txt
   ```

2. **Browser requirement**: Chrome, Firefox, or Edge must be installed on your system.

3. **WhatsApp requirement**: WhatsApp app must be installed on your phone.

## 5-Minute Quick Start

### Step 1: Test Connection

```bash
python chico-cli.py whatsapp connect
```

**What to do:**
1. A browser window will open with WhatsApp Web
2. Scan the QR code using WhatsApp on your phone
3. Wait for "Successfully connected!" message
4. Press Enter to disconnect

**Expected output:**
```
🔗 WhatsApp Web Connection
============================================================
Browser: Chrome
Timeout: 60 seconds

Setting up Chrome browser...
✓ Chrome browser initialized

🔗 Connecting to WhatsApp Web...
📱 Please scan the QR code with your phone when it appears

Waiting for WhatsApp Web to load...

✓ QR code displayed! Please scan with WhatsApp on your phone...
   (You have 60 seconds to scan)

Waiting for QR code scan...

✓ Successfully connected to WhatsApp Web!

✓ Connection successful!
  You can now use 'monitor' or 'send' commands
  Keep this window open to maintain the session

Press Enter to disconnect...
```

### Step 2: Send Your First Message

```bash
python chico-cli.py whatsapp send "YourContact" "Hello from Chico CLI! 🐕"
```

Replace `YourContact` with an actual contact name from your WhatsApp.

**Expected output:**
```
📤 Send Message to WhatsApp
============================================================
Chat: YourContact
Message: Hello from Chico CLI! 🐕

Setting up Chrome browser...
✓ Chrome browser initialized

🔗 Connecting to WhatsApp Web...
📱 Please scan the QR code with your phone when it appears

✓ Already logged in to WhatsApp Web!

✓ Message sent to YourContact

🔌 Disconnecting from WhatsApp Web...
✓ Disconnected successfully
```

### Step 3: Monitor Messages

```bash
python chico-cli.py whatsapp monitor
```

**What happens:**
- Browser opens and connects to WhatsApp
- CLI checks for new messages every 5 seconds
- New messages are displayed with sender name and preview
- Press Ctrl+C to stop

**Expected output:**
```
👀 WhatsApp Message Monitor
============================================================
Browser: Chrome
Check interval: 5 seconds

Setting up Chrome browser...
✓ Chrome browser initialized

🔗 Connecting to WhatsApp Web...
✓ Already logged in to WhatsApp Web!

👀 Monitoring WhatsApp messages...
   Press Ctrl+C to stop monitoring

📩 New message from: John Doe
   Message: Hey, are you there?

📩 New message from: Family Group
   Message: Dinner plans tonight?

^C
⏹ Stopped monitoring

🔌 Disconnecting from WhatsApp Web...
✓ Disconnected successfully
```

## Common Use Cases

### 1. Send Scheduled Reminders

Create a script `reminder.sh`:
```bash
#!/bin/bash
python chico-cli.py whatsapp send "Family Group" "⏰ Reminder: Meeting in 30 minutes!"
```

Schedule with cron (Linux/Mac) or Task Scheduler (Windows).

### 2. Monitor Customer Messages

```bash
# Check for messages every 10 seconds
python chico-cli.py whatsapp monitor --interval 10
```

Use this to monitor customer support chats or group discussions.

### 3. Bulk Message Campaign

Create a script to send to multiple contacts:
```bash
#!/bin/bash
CONTACTS=("Alice" "Bob" "Charlie")
MESSAGE="📣 Important update: New product launch next week!"

for contact in "${CONTACTS[@]}"; do
    python chico-cli.py whatsapp send "$contact" "$MESSAGE"
    sleep 10  # Wait 10 seconds between messages
done
```

### 4. Use Different Browsers

```bash
# Use Firefox instead of Chrome
python chico-cli.py whatsapp connect --browser firefox

# Use Edge (Windows)
python chico-cli.py whatsapp connect --browser edge
```

## Troubleshooting

### Issue: "WebDriver not found"
**Solution:** The CLI automatically downloads the appropriate driver. Check internet connection.

### Issue: QR code won't scan
**Solution:** 
- Make sure your phone has internet
- Update WhatsApp to latest version
- Try increasing timeout: `--timeout 120`

### Issue: Chat not found
**Solution:** 
- Use exact contact name as it appears in WhatsApp
- Check spelling and capitalization
- Make sure contact exists in your WhatsApp

### Issue: Browser crashes
**Solution:**
- Try a different browser: `--browser firefox`
- Update your browser to latest version
- Close other browser instances

## Tips

1. **Session Persistence**: After first connection, you may not need to scan QR code again
2. **Keep Browser Open**: Don't close the browser window while monitoring
3. **Rate Limiting**: Wait a few seconds between messages to avoid being rate-limited
4. **Exact Names**: Use exact contact/group names as they appear in WhatsApp

## Complete Command Reference

```bash
# Connect to WhatsApp Web
python chico-cli.py whatsapp connect
python chico-cli.py whatsapp connect --browser firefox
python chico-cli.py whatsapp connect --timeout 120

# Monitor messages
python chico-cli.py whatsapp monitor
python chico-cli.py whatsapp monitor --interval 10
python chico-cli.py whatsapp monitor --browser firefox

# Send messages
python chico-cli.py whatsapp send "Contact" "Message"
python chico-cli.py whatsapp send "Group" "Hello everyone!"

# Send prompts
python chico-cli.py whatsapp prompt "Contact" "Your message here"
```

## Next Steps

- Read the full documentation: [WHATSAPP_USAGE.md](WHATSAPP_USAGE.md)
- Explore AI features: `python chico-cli.py chat --help`
- Configure AI providers: `python chico-cli.py config --help`

## Support

For issues or questions:
1. Check [WHATSAPP_USAGE.md](WHATSAPP_USAGE.md) for detailed guide
2. Review [README.md](README.md) for general CLI usage
3. Ensure all dependencies are installed: `pip install -r requirements.txt`

---

**Chico Chuwawa AI CLI v2.1.0** - Built by Max van Heerden 🐕✨
