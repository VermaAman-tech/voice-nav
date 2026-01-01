"""
Voice-controlled computer navigation system.
Main orchestration module.
"""
import os
import sys
import json
import logging
from pathlib import Path
from dotenv import load_dotenv

# Add modules to path
sys.path.append(str(Path(__file__).parent))

from modules.speech_input import SpeechInput
from modules.command_parser import CommandParser
from modules.executor import CommandExecutor
from modules.feedback import FeedbackProvider


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('voice_nav.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class VoiceNavigator:
    def __init__(self):
        """Initialize the voice navigation system."""
        # Load environment variables
        load_dotenv()
        
        # Load configuration
        config_path = Path(__file__).parent / 'config' / 'settings.json'
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        # Initialize modules
        logger.info("Initializing Voice Navigator...")
        
        self.speech_input = SpeechInput(self.config)
        self.command_parser = CommandParser(
            Path(__file__).parent / 'config' / 'commands.json'
        )
        self.executor = CommandExecutor(self.config)
        self.feedback = FeedbackProvider(self.config)
        
        self.running = False
        self.wake_word_enabled = self.config.get('wake_word_enabled', False)
        self.wake_word = self.config.get('wake_word', 'hey computer')
        
        logger.info("Voice Navigator initialized successfully")
    
    def start(self):
        """Start the voice navigation system."""
        self.running = True
        
        print("\n" + "="*60)
        print("  VOICE-CONTROLLED COMPUTER NAVIGATION")
        print("="*60)
        print("\nSystem is ready!")
        print("\nAvailable commands:")
        print("  • 'open [app]' - Open applications")
        print("  • 'search for [query]' - Web search")
        print("  • 'open [folder]' - Open folders (downloads, documents, etc.)")
        print("  • 'create folder [name]' - Create new folder")
        print("  • 'volume up/down' - Control volume")
        print("  • 'take screenshot' - Capture screen")
        print("  • 'show desktop' - Minimize all windows")
        print("\nSay 'stop listening' or 'exit' to quit")
        print("Press Ctrl+C to force quit\n")
        
        self.feedback.provide_feedback("Voice navigation system activated")
        
        try:
            self.main_loop()
        except KeyboardInterrupt:
            print("\n\nShutting down...")
            self.stop()
    
    def main_loop(self):
        """Main processing loop."""
        while self.running:
            try:
                # Check for wake word if enabled
                if self.wake_word_enabled:
                    print(f"\nWaiting for wake word: '{self.wake_word}'...")
                    if not self.speech_input.listen_for_wake_word(self.wake_word):
                        continue
                    self.feedback.provide_feedback("Yes?")
                
                # Listen for command
                self.feedback.notify_listening()
                text = self.speech_input.listen()
                
                if not text:
                    continue
                
                # Check for exit commands
                if any(word in text for word in ['stop listening', 'exit', 'quit', 'goodbye']):
                    self.feedback.provide_feedback("Goodbye!")
                    self.stop()
                    break
                
                # Process command
                self.feedback.notify_processing()
                self.process_command(text)
                
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                self.feedback.notify_error(f"An error occurred: {e}")
    
    def process_command(self, text: str):
        """
        Process a voice command.
        
        Args:
            text: Voice command text
        """
        # Parse command
        command = self.command_parser.parse(text)
        
        if not command:
            self.feedback.notify_error("Sorry, I didn't understand that command")
            self.feedback.provide_feedback(
                "Try saying 'open chrome' or 'search for weather'"
            )
            return
        
        logger.info(f"Parsed command: {command}")
        
        # Check if confirmation required
        if command.get('requires_confirmation'):
            self.feedback.provide_feedback(
                "This action requires manual confirmation for safety"
            )
            return
        
        # Execute command
        result = self.executor.execute(command)
        
        # Provide feedback
        if result['success']:
            self.feedback.notify_success(result['message'])
            self.feedback.provide_feedback(result['message'])
        else:
            self.feedback.notify_error(result['message'])
    
    def stop(self):
        """Stop the voice navigation system."""
        self.running = False
        logger.info("Voice Navigator stopped")


def main():
    """Main entry point."""
    try:
        navigator = VoiceNavigator()
        navigator.start()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"\nFatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
