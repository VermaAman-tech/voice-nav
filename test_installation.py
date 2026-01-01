"""
Simple test script to verify installation and basic functionality.
"""
import sys
from pathlib import Path

print("="*60)
print("Voice Navigation System - Installation Test")
print("="*60)

# Test imports
print("\n1. Testing imports...")
try:
    import speech_recognition as sr
    print("   ✓ SpeechRecognition")
except ImportError as e:
    print(f"   ✗ SpeechRecognition: {e}")
    sys.exit(1)

try:
    import pyautogui
    print("   ✓ PyAutoGUI")
except ImportError as e:
    print(f"   ✗ PyAutoGUI: {e}")
    sys.exit(1)

try:
    import psutil
    print("   ✓ psutil")
except ImportError as e:
    print(f"   ✗ psutil: {e}")
    sys.exit(1)

try:
    import pyttsx3
    print("   ✓ pyttsx3 (Text-to-Speech)")
except ImportError as e:
    print(f"   ⚠ pyttsx3: {e} (voice feedback will be disabled)")

try:
    from dotenv import load_dotenv
    print("   ✓ python-dotenv")
except ImportError as e:
    print(f"   ✗ python-dotenv: {e}")
    sys.exit(1)

# Test microphone
print("\n2. Testing microphone access...")
try:
    microphones = sr.Microphone.list_microphone_names()
    print(f"   Found {len(microphones)} microphone(s):")
    for i, mic in enumerate(microphones):
        print(f"     [{i}] {mic}")
except Exception as e:
    print(f"   ✗ Error accessing microphones: {e}")
    sys.exit(1)

# Test configuration files
print("\n3. Testing configuration files...")
config_dir = Path(__file__).parent / 'config'
settings_file = config_dir / 'settings.json'
commands_file = config_dir / 'commands.json'

if settings_file.exists():
    print(f"   ✓ settings.json")
else:
    print(f"   ✗ settings.json not found")
    sys.exit(1)

if commands_file.exists():
    print(f"   ✓ commands.json")
else:
    print(f"   ✗ commands.json not found")
    sys.exit(1)

# Test modules
print("\n4. Testing modules...")
try:
    sys.path.append(str(Path(__file__).parent))
    from modules.speech_input import SpeechInput
    from modules.command_parser import CommandParser
    from modules.executor import CommandExecutor
    from modules.feedback import FeedbackProvider
    print("   ✓ All modules import successfully")
except Exception as e:
    print(f"   ✗ Module import error: {e}")
    sys.exit(1)

# Test parser
print("\n5. Testing command parser...")
try:
    parser = CommandParser(commands_file)
    
    test_commands = [
        ("open chrome", "open_app"),
        ("volume up", "system_volume_up"),
        ("search for python", "web_search"),
        ("create folder test", "create_folder")
    ]
    
    for text, expected_action in test_commands:
        result = parser.parse(text)
        if result and result.get('action') == expected_action:
            print(f"   ✓ '{text}' -> {expected_action}")
        else:
            print(f"   ✗ '{text}' -> expected {expected_action}, got {result}")
except Exception as e:
    print(f"   ✗ Parser error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("Installation test complete!")
print("="*60)
print("\nReady to run: python main.py")
print("\nNote: Actual voice recognition requires:")
print("  - A working microphone")
print("  - Internet connection (for Google Speech API)")
print("  - Microphone permissions enabled")
