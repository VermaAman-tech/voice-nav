# Voice-Controlled Computer Navigation

A Windows voice assistant that lets you control your computer using natural voice commands. Speak naturally to open applications, manage files, control system settings, and browse the web.

## Features

- 🎤 **Speech Recognition** - Uses Google Speech Recognition for accurate voice-to-text
- 🧠 **Natural Language Processing** - Understands various phrasings of commands
- 🖥️ **Windows Automation** - Controls applications, files, and system settings
- 🌐 **Web Integration** - Search the web and open URLs by voice
- ⚡ **Fast & Responsive** - Real-time command execution
- 🔒 **Safety Features** - Confirmation required for destructive operations

## Installation

### Prerequisites

- Python 3.8 or higher
- Windows 10/11
- Microphone

### Setup Steps

1. **Navigate to project directory**
   ```bash
   cd voice-nav
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   > **Note**: PyAudio installation may require additional steps. If you encounter errors:
   > - Download the appropriate `.whl` file from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)
   > - Install using: `pip install path\to\PyAudio‑0.2.14‑cp311‑cp311‑win_amd64.whl`

4. **Configure settings** (optional)
   ```bash
   copy .env.example .env
   ```
   Edit `.env` and `config/settings.json` to customize behavior

5. **Run the application**
   ```bash
   python main.py
   ```

## Usage

### Basic Commands

**Opening Applications**
- "Open Chrome"
- "Launch Notepad"
- "Start Calculator"

**File Operations**
- "Open Downloads folder"
- "Create folder Project Files"
- "Open Documents"

**Web Browsing**
- "Search for Python tutorials"
- "Google machine learning"
- "Open youtube.com"

**System Controls**
- "Volume up"
- "Volume down"
- "Take screenshot"
- "Show desktop"
- "Lock computer"

**Navigation**
- "Switch window"
- "Task view"
- "Minimize all"

**Exit**
- "Stop listening"
- "Exit"
- "Goodbye"

### Supported Applications

The system comes pre-configured with common applications:
- Chrome, Firefox, Edge
- Notepad, Calculator
- File Explorer
- Microsoft Office (Word, Excel)
- VS Code

To add more applications, edit `config/commands.json` and add the application name and path.

## Configuration

### Settings (`config/settings.json`)

- `recognition_engine`: Speech recognition engine ("google" recommended)
- `confidence_threshold`: Minimum confidence for recognition (0-1)
- `enable_voice_feedback`: Enable text-to-speech responses
- `wake_word_enabled`: Enable wake word detection
- `wake_word`: Custom wake word (e.g., "hey computer")

### Commands (`config/commands.json`)

Customize command patterns, application paths, and folder shortcuts. The configuration uses pattern matching with `{parameter}` placeholders.

Example:
```json
"open_app": [
  "open {app}",
  "launch {app}",
  "start {app}"
]
```

## Troubleshooting

### Microphone Not Working
- Check microphone permissions in Windows Settings
- Run `python -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_names())"` to list devices
- Set `microphone_device_index` in `config/settings.json` if you have multiple microphones

### Recognition Errors
- Ensure you have a stable internet connection (Google Speech API requires internet)
- Speak clearly and avoid background noise
- Adjust `confidence_threshold` in settings

### Application Not Opening
- Verify the application path in `config/commands.json`
- Replace `{username}` placeholder with your actual username
- Use absolute paths for executables

### Permission Errors
- Run as Administrator if controlling system settings
- Some operations may be blocked by Windows security

## Architecture

```
voice-nav/
├── main.py                 # Main orchestration
├── modules/
│   ├── speech_input.py    # Speech recognition
│   ├── command_parser.py  # NLU & pattern matching
│   ├── executor.py        # Windows automation
│   └── feedback.py        # User feedback
├── config/
│   ├── settings.json      # App settings
│   └── commands.json      # Command definitions
└── requirements.txt       # Dependencies
```

## Safety & Privacy

- **Confirmation Required**: Destructive operations (delete, shutdown, etc.) require manual confirmation
- **Local Processing**: Speech recognition uses Google's API (requires internet)
- **No Data Storage**: Commands are not logged or stored (except in `voice_nav.log` for debugging)
- **Fail-Safe**: PyAutoGUI fail-safe enabled - move mouse to corner to stop automation

## Extending Functionality

### Add New Commands

1. Edit `config/commands.json` to add new patterns
2. Implement the action in `modules/executor.py`
3. Add pattern matching in `modules/command_parser.py`

### Add Text-to-Speech

Set `enable_voice_feedback: true` in `config/settings.json` for spoken responses.

### Add Wake Word

Enable wake word detection to avoid accidental command execution:
```json
{
  "wake_word_enabled": true,
  "wake_word": "hey computer"
}
```

## Known Limitations

- Requires internet connection for speech recognition
- Windows-specific (uses Windows APIs and programs)
- PyAudio installation can be tricky on some systems
- Some antivirus software may flag automation tools

## License

MIT License - Feel free to modify and extend!

## Contributing

Contributions welcome! Areas for improvement:
- Offline speech recognition using Whisper
- Additional command types
- Multi-language support
- Context-aware commands
- Command history and learning

---

**Made with ❤️ for hands-free computing**


Future Ideas 

Also integrate voice control 
try to make a wrapper on top of the exisiting pc to do everything with just words in detail 

