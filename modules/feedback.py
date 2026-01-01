"""
Feedback module for providing user feedback.
"""
import logging

logger = logging.getLogger(__name__)

try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    logger.warning("pyttsx3 not available. Voice feedback disabled.")


class FeedbackProvider:
    def __init__(self, config):
        """
        Initialize feedback provider.
        
        Args:
            config: Configuration dictionary with feedback settings
        """
        self.enable_voice = config.get('enable_voice_feedback', False)
        self.tts_engine = None
        
        if self.enable_voice and TTS_AVAILABLE:
            try:
                self.tts_engine = pyttsx3.init()
                # Set properties
                self.tts_engine.setProperty('rate', 175)  # Speed
                self.tts_engine.setProperty('volume', 0.9)  # Volume
            except Exception as e:
                logger.error(f"Failed to initialize TTS: {e}")
                self.enable_voice = False
    
    def provide_feedback(self, message: str, speak: bool = None):
        """
        Provide feedback to user.
        
        Args:
            message: Feedback message
            speak: Override voice feedback setting
        """
        # Always print to console
        print(f"\n[ASSISTANT] {message}")
        logger.info(f"Feedback: {message}")
        
        # Speak if enabled
        if speak is None:
            speak = self.enable_voice
        
        if speak and self.tts_engine:
            try:
                self.tts_engine.say(message)
                self.tts_engine.runAndWait()
            except Exception as e:
                logger.error(f"TTS error: {e}")
    
    def notify_listening(self):
        """Notify user that system is listening."""
        print("\n🎤 Listening...")
    
    def notify_processing(self):
        """Notify user that command is being processed."""
        print("⚙️  Processing...")
    
    def notify_error(self, error: str):
        """Notify user of an error."""
        print(f"\n❌ Error: {error}")
        logger.error(error)
    
    def notify_success(self, message: str):
        """Notify user of successful command execution."""
        print(f"\n✅ {message}")
