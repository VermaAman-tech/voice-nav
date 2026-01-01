"""
Command executor for performing Windows automation tasks.
"""
import os
import subprocess
import psutil
import pyautogui
import webbrowser
import logging
from pathlib import Path
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class CommandExecutor:
    def __init__(self, config):
        """
        Initialize command executor.
        
        Args:
            config: Configuration dictionary with executor settings
        """
        self.require_confirmation = config.get('require_confirmation_for_destructive', True)
        
        # Configure pyautogui safety
        pyautogui.PAUSE = 0.5
        pyautogui.FAILSAFE = True
    
    def execute(self, command: Dict) -> Dict:
        """
        Execute a parsed command.
        
        Args:
            command: Command dictionary from parser
            
        Returns:
            Result dictionary with success status and message
        """
        if not command:
            return {'success': False, 'message': 'No command provided'}
        
        action = command.get('action')
        logger.info(f"Executing action: {action}")
        
        try:
            # Application commands
            if action == 'open_app':
                return self._open_app(command)
            elif action == 'close_app':
                return self._close_app(command)
            
            # File operations
            elif action == 'create_folder':
                return self._create_folder(command)
            elif action == 'open_folder':
                return self._open_folder(command)
            elif action == 'delete':
                return self._delete(command)
            
            # System controls
            elif action == 'system_volume_up':
                return self._volume_control('up')
            elif action == 'system_volume_down':
                return self._volume_control('down')
            elif action == 'system_mute':
                return self._volume_control('mute')
            elif action == 'system_screenshot':
                return self._screenshot()
            elif action == 'system_lock':
                return self._lock_computer()
            elif action == 'system_shutdown':
                return self._shutdown()
            elif action == 'system_restart':
                return self._restart()
            
            # Web commands
            elif action == 'web_search':
                return self._web_search(command)
            elif action == 'open_url':
                return self._open_url(command)
            
            # Shortcuts
            elif action == 'shortcut_minimize_all':
                return self._minimize_all()
            elif action == 'shortcut_task_view':
                return self._task_view()
            elif action == 'shortcut_switch_window':
                return self._switch_window()
            
            else:
                return {'success': False, 'message': f'Unknown action: {action}'}
        
        except Exception as e:
            logger.error(f"Error executing command: {e}")
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    # Application commands
    def _open_app(self, command: Dict) -> Dict:
        """Open an application."""
        app_path = command.get('app_path')
        app_name = command.get('app_name')
        
        try:
            subprocess.Popen(app_path)
            return {'success': True, 'message': f'Opening {app_name}'}
        except Exception as e:
            return {'success': False, 'message': f'Failed to open {app_name}: {e}'}
    
    def _close_app(self, command: Dict) -> Dict:
        """Close an application."""
        app_name = command.get('app_name')
        
        try:
            # Find and kill process
            killed = False
            for proc in psutil.process_iter(['name']):
                if app_name.lower() in proc.info['name'].lower():
                    proc.terminate()
                    killed = True
            
            if killed:
                return {'success': True, 'message': f'Closed {app_name}'}
            else:
                return {'success': False, 'message': f'{app_name} is not running'}
        except Exception as e:
            return {'success': False, 'message': f'Failed to close {app_name}: {e}'}
    
    # File operations
    def _create_folder(self, command: Dict) -> Dict:
        """Create a new folder."""
        folder_name = command.get('name')
        
        try:
            # Create in Downloads folder by default
            downloads = Path.home() / 'Downloads'
            folder_path = downloads / folder_name
            folder_path.mkdir(parents=True, exist_ok=True)
            return {'success': True, 'message': f'Created folder: {folder_name}'}
        except Exception as e:
            return {'success': False, 'message': f'Failed to create folder: {e}'}
    
    def _open_folder(self, command: Dict) -> Dict:
        """Open a folder in File Explorer."""
        path = command.get('path')
        
        try:
            # Expand path if it's a shortcut
            expanded_path = os.path.expandvars(path)
            
            if os.path.exists(expanded_path):
                os.startfile(expanded_path)
                return {'success': True, 'message': f'Opening folder'}
            else:
                return {'success': False, 'message': f'Folder not found: {path}'}
        except Exception as e:
            return {'success': False, 'message': f'Failed to open folder: {e}'}
    
    def _delete(self, command: Dict) -> Dict:
        """Delete a file or folder (requires confirmation)."""
        target = command.get('target')
        
        # This is a destructive operation - would need user confirmation
        return {'success': False, 'message': 'Delete operation requires manual confirmation'}
    
    # System controls
    def _volume_control(self, action: str) -> Dict:
        """Control system volume."""
        try:
            if action == 'up':
                pyautogui.press('volumeup')
                return {'success': True, 'message': 'Volume increased'}
            elif action == 'down':
                pyautogui.press('volumedown')
                return {'success': True, 'message': 'Volume decreased'}
            elif action == 'mute':
                pyautogui.press('volumemute')
                return {'success': True, 'message': 'Volume muted/unmuted'}
        except Exception as e:
            return {'success': False, 'message': f'Volume control failed: {e}'}
    
    def _screenshot(self) -> Dict:
        """Take a screenshot."""
        try:
            # Save to Pictures folder
            pictures = Path.home() / 'Pictures' / 'Screenshots'
            pictures.mkdir(exist_ok=True)
            
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            screenshot_path = pictures / f'screenshot_{timestamp}.png'
            
            screenshot = pyautogui.screenshot()
            screenshot.save(str(screenshot_path))
            
            return {'success': True, 'message': f'Screenshot saved'}
        except Exception as e:
            return {'success': False, 'message': f'Screenshot failed: {e}'}
    
    def _lock_computer(self) -> Dict:
        """Lock the computer."""
        try:
            subprocess.run(['rundll32.exe', 'user32.dll,LockWorkStation'])
            return {'success': True, 'message': 'Locking computer'}
        except Exception as e:
            return {'success': False, 'message': f'Failed to lock: {e}'}
    
    def _shutdown(self) -> Dict:
        """Shutdown the computer (requires confirmation)."""
        return {'success': False, 'message': 'Shutdown requires manual confirmation'}
    
    def _restart(self) -> Dict:
        """Restart the computer (requires confirmation)."""
        return {'success': False, 'message': 'Restart requires manual confirmation'}
    
    # Web commands
    def _web_search(self, command: Dict) -> Dict:
        """Perform a web search."""
        query = command.get('query')
        
        try:
            search_url = f'https://www.google.com/search?q={query.replace(" ", "+")}'
            webbrowser.open(search_url)
            return {'success': True, 'message': f'Searching for: {query}'}
        except Exception as e:
            return {'success': False, 'message': f'Search failed: {e}'}
    
    def _open_url(self, command: Dict) -> Dict:
        """Open a URL in default browser."""
        url = command.get('url')
        
        try:
            webbrowser.open(url)
            return {'success': True, 'message': f'Opening: {url}'}
        except Exception as e:
            return {'success': False, 'message': f'Failed to open URL: {e}'}
    
    # Shortcuts
    def _minimize_all(self) -> Dict:
        """Minimize all windows (show desktop)."""
        try:
            pyautogui.hotkey('win', 'd')
            return {'success': True, 'message': 'Showing desktop'}
        except Exception as e:
            return {'success': False, 'message': f'Failed: {e}'}
    
    def _task_view(self) -> Dict:
        """Open Task View."""
        try:
            pyautogui.hotkey('win', 'tab')
            return {'success': True, 'message': 'Opening Task View'}
        except Exception as e:
            return {'success': False, 'message': f'Failed: {e}'}
    
    def _switch_window(self) -> Dict:
        """Switch to next window."""
        try:
            pyautogui.hotkey('alt', 'tab')
            return {'success': True, 'message': 'Switching window'}
        except Exception as e:
            return {'success': False, 'message': f'Failed: {e}'}
