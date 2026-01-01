"""
Speech input module for capturing and transcribing voice commands.
"""
import speech_recognition as sr
import logging

logger = logging.getLogger(__name__)


class SpeechInput:
    def __init__(self, config):
        """
        Initialize speech recognition.
        
        Args:
            config: Configuration dictionary with recognition settings
        """
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone(
            device_index=config.get('microphone_device_index')
        )
        self.engine = config.get('recognition_engine', 'google')
        self.confidence_threshold = config.get('confidence_threshold', 0.7)
        
        # Adjust for ambient noise
        logger.info("Calibrating microphone for ambient noise...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        logger.info("Microphone calibrated")
    
    def listen(self, timeout=5, phrase_time_limit=5):
        """
        Listen for voice input and convert to text.
        
        Args:
            timeout: Maximum time to wait for speech to start (seconds)
            phrase_time_limit: Maximum time for phrase (seconds)
            
        Returns:
            str: Transcribed text or None if recognition failed
        """
        try:
            with self.microphone as source:
                logger.info("Listening...")
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
                
            logger.info("Processing speech...")
            
            # Use selected recognition engine
            if self.engine == 'google':
                text = self.recognizer.recognize_google(audio)
            elif self.engine == 'sphinx':
                text = self.recognizer.recognize_sphinx(audio)
            else:
                logger.error(f"Unknown recognition engine: {self.engine}")
                return None
            
            logger.info(f"Recognized: {text}")
            return text.lower()
            
        except sr.WaitTimeoutError:
            logger.warning("No speech detected within timeout")
            return None
        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            return None
        except sr.RequestError as e:
            logger.error(f"Recognition service error: {e}")
            return None
        except Exception as e:
            logger.error(f"Error in speech recognition: {e}")
            return None
    
    def listen_for_wake_word(self, wake_word, timeout=None):
        """
        Continuously listen for a wake word.
        
        Args:
            wake_word: The wake word to listen for
            timeout: Maximum time to wait (None for indefinite)
            
        Returns:
            bool: True if wake word detected, False otherwise
        """
        text = self.listen(timeout=timeout if timeout else 10)
        if text and wake_word.lower() in text:
            logger.info(f"Wake word '{wake_word}' detected")
            return True
        return False
    
    @staticmethod
    def list_microphones():
        """List all available microphone devices."""
        return sr.Microphone.list_microphone_names()
