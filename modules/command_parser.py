"""
Command parser for interpreting voice commands and extracting intent.
"""
import json
import re
import os
import logging
from typing import Dict, Optional, Tuple

logger = logging.getLogger(__name__)


class CommandParser:
    def __init__(self, commands_config_path):
        """
        Initialize command parser with command patterns.
        
        Args:
            commands_config_path: Path to commands.json configuration file
        """
        with open(commands_config_path, 'r') as f:
            self.config = json.load(f)
        
        self.applications = self.config.get('applications', {})
        self.command_patterns = self.config.get('command_patterns', {})
        self.folder_shortcuts = self.config.get('folder_shortcuts', {})
        
        # Replace {username} placeholder with actual username
        username = os.getenv('USERNAME') or os.getenv('USER') or 'User'
        self.applications = {k: v.replace('{username}', username) 
                           for k, v in self.applications.items()}
        self.folder_shortcuts = {k: v.replace('{username}', username) 
                                for k, v in self.folder_shortcuts.items()}
    
    def parse(self, text: str) -> Optional[Dict]:
        """
        Parse voice command text into structured command.
        
        Args:
            text: Voice command text (lowercase)
            
        Returns:
            Dictionary with command details or None if not recognized
        """
        if not text:
            return None
        
        text = text.strip().lower()
        
        # Try to match command patterns
        command = None
        
        # Check application commands
        command = self._parse_app_command(text)
        if command:
            return command
        
        # Check file operations
        command = self._parse_file_operation(text)
        if command:
            return command
        
        # Check system controls
        command = self._parse_system_control(text)
        if command:
            return command
        
        # Check web commands
        command = self._parse_web_command(text)
        if command:
            return command
        
        # Check shortcuts
        command = self._parse_shortcut(text)
        if command:
            return command
        
        logger.warning(f"Could not parse command: {text}")
        return None
    
    def _parse_app_command(self, text: str) -> Optional[Dict]:
        """Parse application open/close commands."""
        # Open app
        for pattern in self.command_patterns.get('open_app', []):
            match = self._match_pattern(pattern, text)
            if match:
                app_name = match.get('app', '').lower()
                app_path = self.applications.get(app_name)
                if app_path:
                    return {
                        'action': 'open_app',
                        'app_name': app_name,
                        'app_path': app_path
                    }
        
        # Close app
        for pattern in self.command_patterns.get('close_app', []):
            match = self._match_pattern(pattern, text)
            if match:
                app_name = match.get('app', '').lower()
                return {
                    'action': 'close_app',
                    'app_name': app_name
                }
        
        return None
    
    def _parse_file_operation(self, text: str) -> Optional[Dict]:
        """Parse file operation commands."""
        file_ops = self.command_patterns.get('file_operations', {})
        
        # Create folder
        for pattern in file_ops.get('create_folder', []):
            match = self._match_pattern(pattern, text)
            if match:
                return {
                    'action': 'create_folder',
                    'name': match.get('name', 'New Folder')
                }
        
        # Open folder
        for pattern in file_ops.get('open_folder', []):
            match = self._match_pattern(pattern, text)
            if match:
                folder = match.get('folder', '').lower()
                folder_path = self.folder_shortcuts.get(folder, folder)
                return {
                    'action': 'open_folder',
                    'path': folder_path
                }
        
        # Delete
        for pattern in file_ops.get('delete', []):
            match = self._match_pattern(pattern, text)
            if match:
                return {
                    'action': 'delete',
                    'target': match.get('target', ''),
                    'requires_confirmation': True
                }
        
        return None
    
    def _parse_system_control(self, text: str) -> Optional[Dict]:
        """Parse system control commands."""
        sys_controls = self.command_patterns.get('system_controls', {})
        
        for action, patterns in sys_controls.items():
            if any(pattern in text for pattern in patterns):
                return {
                    'action': f'system_{action}',
                    'requires_confirmation': action in ['shutdown', 'restart']
                }
        
        return None
    
    def _parse_web_command(self, text: str) -> Optional[Dict]:
        """Parse web-related commands."""
        web_cmds = self.command_patterns.get('web', {})
        
        # Search
        for pattern in web_cmds.get('search', []):
            match = self._match_pattern(pattern, text)
            if match:
                return {
                    'action': 'web_search',
                    'query': match.get('query', '')
                }
        
        # Open URL
        for pattern in web_cmds.get('open_url', []):
            match = self._match_pattern(pattern, text)
            if match:
                url = match.get('url', '')
                # Add https:// if not present
                if not url.startswith('http'):
                    url = 'https://' + url
                return {
                    'action': 'open_url',
                    'url': url
                }
        
        return None
    
    def _parse_shortcut(self, text: str) -> Optional[Dict]:
        """Parse keyboard shortcut commands."""
        shortcuts = self.command_patterns.get('shortcuts', {})
        
        for action, patterns in shortcuts.items():
            if any(pattern in text for pattern in patterns):
                return {
                    'action': f'shortcut_{action}'
                }
        
        return None
    
    def _match_pattern(self, pattern: str, text: str) -> Optional[Dict]:
        """
        Match a pattern template against text and extract parameters.
        
        Args:
            pattern: Pattern template with {param} placeholders
            text: Text to match against
            
        Returns:
            Dictionary of extracted parameters or None
        """
        # Convert pattern to regex
        regex_pattern = pattern
        params = re.findall(r'\{(\w+)\}', pattern)
        
        for param in params:
            regex_pattern = regex_pattern.replace(f'{{{param}}}', f'(?P<{param}>.+)')
        
        regex_pattern = '^' + regex_pattern + '$'
        
        match = re.match(regex_pattern, text)
        if match:
            return match.groupdict()
        
        return None
