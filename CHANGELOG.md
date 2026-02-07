# Changelog

All notable changes to Chico Chuwawa AI CLI will be documented in this file.

## [3.0.0] - 2026-02-07

### 🎉 Major Release - Complete Overhaul

This release represents a comprehensive enhancement of the Chico CLI with modularity, visual improvements, integrations, and cross-platform support.

### ✨ Added

#### Core Features
- **Modular Architecture**: Clean separation into `chico.core`, `chico.ui`, `chico.utils`, and `chico.integrations`
- **Enhanced Error Handling**: Comprehensive error handling across all modules
- **Graceful Degradation**: Core features work even without optional dependencies

#### Visual Enhancements
- **ASCII Chihuahua Animation**: Animated mascot on startup with `--banner` flag
- **ASCII Art Logo**: Beautiful Chico logo display
- **Coding-Themed Loading Messages**: 20+ fun developer-focused waiting messages
- **Syntax Highlighting**: Automatic code block highlighting using Pygments
- **Loading Spinner**: Animated spinner with themed messages
- **Rich Console Output**: Colorful, beautiful terminal interface using Rich library

#### Persistent Features
- **SQLite Chat History**: All conversations automatically saved to database
- **Session Management**: Create, view, and resume chat sessions
- **Builder Markers**: Mark important points in conversations
- **History Search**: Search through previous conversations by content
- **Message Timestamps**: Track when messages were sent

#### Command Line Interface
- **`history` Command**: View recent chat sessions
- **`search` Command**: Search for coding solutions on the internet
- **`whatsapp` Command**: Setup WhatsApp integration via QR code
- **`--search` Flag**: Enable internet search for chat commands
- **`--save` Flag**: Save single messages to history
- **`--banner` Flag**: Show welcome animation in interactive mode
- **`--no-save` Flag**: Disable history saving in interactive mode

#### Internet Search
- **DuckDuckGo Integration**: Search the web for coding solutions
- **Stack Overflow Search**: Targeted Stack Overflow queries
- **GitHub Search**: Find code examples on GitHub
- **Automatic Context**: Search results included in AI prompts for better answers

#### MCP Server Integrations
- **GitHub Integration**: Repository management, issue creation, PR operations
- **Railway Integration**: Deployment automation
- **Vercel Integration**: Hosting and deployment
- **Office 365 Integration**: Email and calendar access
- **Zoho CRM Integration**: Customer relationship management
- **Zoho Desk Integration**: Support ticket management
- **Zoho Invoice Integration**: Billing and invoicing
- **Sandbox Mode**: Safe testing mode for all integrations
- **MCP Server Manager**: Centralized management of all integrations

#### Desktop App Connections
- **Manus AI Connection**: Connect to Manus AI desktop app
- **DeepSeek Connection**: Connect to DeepSeek desktop app
- **Claude AI Connection**: Connect to Claude desktop app
- **ChatGPT Connection**: Connect to ChatGPT desktop app
- **Read/Write Support**: Full bidirectional communication
- **Connection Manager**: Manage multiple app connections
- **Health Checks**: Verify app connectivity before sending messages

#### WhatsApp Integration
- **QR Code Generation**: Generate QR codes for WhatsApp Web connection
- **ASCII QR Display**: Display QR codes in terminal
- **Connection Management**: Establish and maintain WhatsApp connections
- **Message Monitoring**: Listen for incoming WhatsApp messages
- **AI Response Forwarding**: Send AI responses via WhatsApp
- **Session Persistence**: Maintain active WhatsApp sessions

#### Installation & Distribution
- **Linux/Unix Install Script** (`install.sh`): One-line installation for Unix systems
- **PowerShell Install Script** (`install.ps1`): Enhanced Windows installation
- **Global Command**: `chico` command available system-wide
- **PATH Configuration**: Automatic PATH setup on all platforms
- **pip Installation**: Install via `pip install` from GitHub
- **setup.py**: Proper Python package structure
- **Cross-Platform Support**: Windows, macOS, Linux, Ubuntu, Debian compatibility

#### Documentation
- **Comprehensive README**: Updated with all v3.0 features
- **Installation Guide** (`INSTALLATION.md`): Detailed platform-specific instructions
- **Changelog** (`CHANGELOG.md`): Track all changes
- **Examples Guide**: (Coming soon) Extensive usage examples

### 🔧 Changed

- **Main CLI File**: Completely rewritten with modular imports
- **Configuration Structure**: Enhanced to support integrations
- **Requirements**: Added pygments, colorama, rich, qrcode, pillow, duckduckgo-search
- **Version Numbering**: Updated to 3.0.0 to reflect major changes
- **Error Messages**: More user-friendly and actionable
- **Help Text**: Enhanced with better examples and descriptions

### 🐛 Fixed

- **Import Error Handling**: Graceful degradation when optional packages missing
- **Cross-Platform Paths**: Proper path handling for Windows/Unix systems
- **Streaming Fallback**: Better handling of models that don't support streaming
- **Model Listing**: Improved fallback when API doesn't support model listing

### 🔒 Security

- **Sandbox Mode**: Test integrations safely without making real API calls
- **Config File Protection**: Warnings about securing API keys
- **Environment Variables**: Support for environment-based configuration
- **No Hardcoded Secrets**: All credentials externalized

### 📦 Dependencies

#### New Dependencies
- `pygments>=2.15.0` - Code syntax highlighting
- `colorama>=0.4.6` - Cross-platform colored output
- `rich>=13.0.0` - Beautiful terminal formatting
- `pyfiglet>=0.8.0` - ASCII art generation (optional)
- `qrcode>=7.4.0` - QR code generation
- `pillow>=10.0.0` - Image processing for QR codes
- `duckduckgo-search>=3.8.0` - Internet search capability

#### Existing Dependencies (Unchanged)
- `openai>=1.0.0` - OpenRouter API client
- `ollama>=0.1.0` - Ollama Cloud client
- `requests>=2.31.0` - HTTP library

### 🚀 Performance

- **Lazy Loading**: Optional modules only loaded when needed
- **Efficient Database**: SQLite for fast history storage
- **Streaming Support**: Real-time response streaming where available
- **Minimal Overhead**: Core features remain fast even with enhancements

### 📊 Statistics

- **Lines of Code**: ~2,000+ new lines
- **New Files**: 18 new files added
- **Modules**: 4 main module categories (ui, utils, integrations, core)
- **New Commands**: 3 new top-level commands
- **New Flags**: 4 new command-line flags
- **Integrations**: 9 service integrations
- **Desktop Apps**: 4 app connections

## [2.0.0] - 2025-10-XX

### Added
- OpenRouter and Ollama Cloud provider support
- Multi-provider architecture
- Provider switching
- Interactive chat mode
- Streaming responses
- Configuration management
- Model listing

### Changed
- Complete rewrite from v1.0
- New provider system
- Enhanced configuration storage

## [1.0.0] - 2025-10-XX

### Added
- Initial release
- Basic OpenAI API integration
- Simple chat functionality
- Windows batch file wrapper

---

## Version Naming Convention

We use [Semantic Versioning](https://semver.org/):
- **Major** (X.0.0): Breaking changes or major new features
- **Minor** (0.X.0): New features, backward compatible
- **Patch** (0.0.X): Bug fixes, backward compatible

## Links

- **Repository**: https://github.com/CA0071/chico-chuwawa-cli
- **Issues**: https://github.com/CA0071/chico-chuwawa-cli/issues
- **Releases**: https://github.com/CA0071/chico-chuwawa-cli/releases
