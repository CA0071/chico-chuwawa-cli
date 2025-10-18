# Windows Installation Guide

This guide will help you install and set up the AI CLI tool on your Windows PC.

## Quick Start (Recommended for Most Users)

### Step 1: Install Python

1. Download Python from [python.org](https://www.python.org/downloads/)
2. **Important**: During installation, check "Add Python to PATH"
3. Click "Install Now"
4. Verify installation by opening Command Prompt and typing:
   ```
   python --version
   ```

### Step 2: Download and Extract the CLI Tool

1. Download the `windows-cli-api` folder
2. Extract it to a convenient location (e.g., `C:\Tools\windows-cli-api`)

### Step 3: Install Dependencies

1. Open Command Prompt
2. Navigate to the extracted folder:
   ```
   cd C:\Tools\windows-cli-api
   ```
3. Install required packages:
   ```
   pip install -r requirements.txt
   ```

### Step 4: Configure Your API Key

```
python cli.py config --api-key YOUR_API_KEY_HERE
```

Replace `YOUR_API_KEY_HERE` with your actual OpenAI API key.

### Step 5: Test the Installation

```
python cli.py chat "Hello, world!"
```

If you see a response from the AI, the installation was successful! 🎉

## Alternative: Using the Batch File

For easier access, you can use the included batch file:

1. Navigate to the installation folder
2. Run commands using `ai-cli.bat` instead of `python cli.py`:
   ```
   ai-cli.bat chat "Hello!"
   ai-cli.bat interactive
   ```

## Advanced: Building a Standalone Executable

If you want to create a standalone `.exe` file that doesn't require Python:

### Step 1: Run the Build Script

```
cd C:\Tools\windows-cli-api
python build_windows.py
```

### Step 2: Find Your Executable

The executable will be created at:
```
C:\Tools\windows-cli-api\dist\ai-cli.exe
```

### Step 3: Add to PATH (Optional)

To run the CLI from anywhere:

1. Copy `ai-cli.exe` to a permanent location (e.g., `C:\Tools\`)
2. Add that location to your PATH:
   - Right-click "This PC" → Properties
   - Click "Advanced system settings"
   - Click "Environment Variables"
   - Under "System variables", find "Path" and click "Edit"
   - Click "New" and add your folder path (e.g., `C:\Tools\`)
   - Click "OK" on all dialogs
3. Open a new Command Prompt and type:
   ```
   ai-cli --help
   ```

## Troubleshooting

### "python is not recognized"

**Problem**: Python is not in your PATH.

**Solution**:
1. Reinstall Python and check "Add Python to PATH"
2. Or manually add Python to PATH:
   - Find your Python installation (usually `C:\Users\YourName\AppData\Local\Programs\Python\Python3xx\`)
   - Add it to PATH using the steps above

### "pip is not recognized"

**Problem**: pip is not in your PATH.

**Solution**:
```
python -m pip install -r requirements.txt
```

### "No module named 'openai'"

**Problem**: The openai package is not installed.

**Solution**:
```
pip install openai
```

### Windows Defender Blocks the Executable

**Problem**: Windows Defender flags the built executable as potentially harmful.

**Solution**:
1. This is normal for newly created executables
2. Click "More info" → "Run anyway"
3. Or add an exception in Windows Defender for the file

### "No API key found"

**Problem**: You haven't configured your API key yet.

**Solution**:
```
python cli.py config --api-key YOUR_API_KEY
```

## Getting Your API Key

### For OpenAI API:
1. Go to [platform.openai.com](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy and save it securely

### For Other Providers:
Check your specific API provider's documentation for obtaining API keys.

## Usage Examples

### Basic Chat
```
python cli.py chat "What is Python?"
```

### Interactive Mode
```
python cli.py interactive
```

### List Available Models
```
python cli.py models
```

### Use a Specific Model
```
python cli.py chat "Explain AI" --model gpt-4.1-nano
```

## Next Steps

- Read the full [README.md](README.md) for detailed usage instructions
- Try the interactive mode for multi-turn conversations
- Explore different models to find what works best for you

## Support

If you encounter issues not covered here:
1. Check the main README.md file
2. Verify your Python and pip installations
3. Ensure your API key is valid and has credits
4. Check your internet connection

---

**Congratulations!** You're now ready to use the AI CLI tool on your Windows PC! 🚀

