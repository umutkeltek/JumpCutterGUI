"""
Utilities and helper functions for Jump Cutter GUI.
"""

import os
import sys
from pathlib import Path
from typing import List, Tuple, Optional, Dict, Any
import json


class ConfigManager:
    """Manages application configuration and user settings."""
    
    def __init__(self, config_dir: Optional[str] = None):
        if config_dir is None:
            config_dir = self._get_default_config_dir()
        
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config_file = self.config_dir / "jumpcut_config.json"
        
        self.default_config = {
            "last_input_dir": str(Path.home()),
            "last_output_dir": str(Path.home()),
            "last_preset": "podcast",
            "last_export_preset": "",
            "window_geometry": None,
            "recent_files": [],
            "max_recent_files": 10
        }
        
    def _get_default_config_dir(self) -> str:
        """Get the default configuration directory for the current platform."""
        if sys.platform == "win32":
            return os.path.join(os.environ.get("APPDATA", ""), "JumpCutter")
        elif sys.platform == "darwin":
            return os.path.join(os.path.expanduser("~"), "Library", "Application Support", "JumpCutter")
        else:
            return os.path.join(os.path.expanduser("~"), ".config", "jumpcut")
            
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                # Merge with defaults to handle new settings
                return {**self.default_config, **config}
            except (json.JSONDecodeError, IOError):
                pass
        return self.default_config.copy()
        
    def save_config(self, config: Dict[str, Any]) -> None:
        """Save configuration to file."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except IOError:
            pass  # Fail silently if we can't save config
            
    def add_recent_file(self, file_path: str, config: Dict[str, Any]) -> None:
        """Add a file to the recent files list."""
        recent = config.get("recent_files", [])
        
        # Remove if already exists
        if file_path in recent:
            recent.remove(file_path)
            
        # Add to front
        recent.insert(0, file_path)
        
        # Limit to max files
        max_files = config.get("max_recent_files", 10)
        config["recent_files"] = recent[:max_files]


class FileValidator:
    """Validates file paths and types."""
    
    SUPPORTED_VIDEO_EXTENSIONS = {
        '.mp4', '.avi', '.mkv', '.mov', '.flv', '.wmv', '.webm', '.m4v', '.3gp'
    }
    
    SUPPORTED_AUDIO_EXTENSIONS = {
        '.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a'
    }
    
    @classmethod
    def is_video_file(cls, file_path: str) -> bool:
        """Check if the file is a supported video format."""
        return Path(file_path).suffix.lower() in cls.SUPPORTED_VIDEO_EXTENSIONS
        
    @classmethod
    def is_audio_file(cls, file_path: str) -> bool:
        """Check if the file is a supported audio format."""
        return Path(file_path).suffix.lower() in cls.SUPPORTED_AUDIO_EXTENSIONS
        
    @classmethod
    def is_supported_file(cls, file_path: str) -> bool:
        """Check if the file is supported (video or audio)."""
        return cls.is_video_file(file_path) or cls.is_audio_file(file_path)
        
    @classmethod
    def validate_input_file(cls, file_path: str) -> Tuple[bool, str]:
        """Validate an input file and return (is_valid, error_message)."""
        if not file_path:
            return False, "No file selected"
            
        path = Path(file_path)
        
        if not path.exists():
            return False, f"File does not exist: {file_path}"
            
        if not path.is_file():
            return False, f"Path is not a file: {file_path}"
            
        if not cls.is_supported_file(file_path):
            return False, f"Unsupported file format: {path.suffix}"
            
        return True, ""
        
    @classmethod
    def validate_output_path(cls, file_path: str) -> Tuple[bool, str]:
        """Validate an output file path and return (is_valid, error_message)."""
        if not file_path:
            return False, "No output path specified"
            
        path = Path(file_path)
        
        # Check if parent directory exists or can be created
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
        except (OSError, PermissionError):
            return False, f"Cannot create output directory: {path.parent}"
            
        # Check if we can write to the location
        if path.exists() and not os.access(path, os.W_OK):
            return False, f"No write permission for: {file_path}"
            
        if not cls.is_video_file(file_path):
            return False, f"Output must be a video file format"
            
        return True, ""


class ParameterValidator:
    """Validates processing parameters."""
    
    @staticmethod
    def validate_magnitude_threshold(value: float) -> Tuple[bool, str]:
        """Validate magnitude threshold ratio."""
        if not 0.001 <= value <= 0.5:
            return False, "Magnitude threshold must be between 0.001 and 0.5"
        return True, ""
        
    @staticmethod
    def validate_duration_threshold(value: float) -> Tuple[bool, str]:
        """Validate duration threshold."""
        if not 0.1 <= value <= 10.0:
            return False, "Duration threshold must be between 0.1 and 10.0 seconds"
        return True, ""
        
    @staticmethod
    def validate_failure_tolerance(value: float) -> Tuple[bool, str]:
        """Validate failure tolerance ratio."""
        if not 0.01 <= value <= 0.5:
            return False, "Failure tolerance must be between 0.01 and 0.5"
        return True, ""
        
    @staticmethod
    def validate_space_on_edges(value: float, duration_threshold: float) -> Tuple[bool, str]:
        """Validate space on edges parameter."""
        if not 0.0 <= value <= 2.0:
            return False, "Space on edges must be between 0.0 and 2.0 seconds"
            
        if value >= duration_threshold / 2:
            return False, "Space on edges should be less than half the duration threshold to avoid overlaps"
            
        return True, ""
        
    @staticmethod
    def validate_min_loud_duration(value: float) -> Tuple[bool, str]:
        """Validate minimum loud part duration."""
        if not 0.0 <= value <= 10.0:
            return False, "Minimum loud duration must be between 0.0 and 10.0 seconds"
        return True, ""


def format_duration(seconds: float) -> str:
    """Format duration in seconds to human-readable format."""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        remaining_seconds = seconds % 60
        return f"{minutes}m {remaining_seconds:.1f}s"
    else:
        hours = int(seconds // 3600)
        remaining_minutes = int((seconds % 3600) // 60)
        remaining_seconds = seconds % 60
        return f"{hours}h {remaining_minutes}m {remaining_seconds:.1f}s"


def estimate_processing_time(input_duration: float, complexity_factor: float = 1.0) -> str:
    """Estimate processing time based on input duration."""
    # Very rough estimation: processing typically takes 0.1x to 0.5x of video duration
    # depending on video complexity and hardware
    estimated_seconds = input_duration * 0.2 * complexity_factor
    return format_duration(estimated_seconds)


def generate_output_filename(input_path: str, suffix: str = "_processed") -> str:
    """Generate a default output filename based on input path."""
    input_path_obj = Path(input_path)
    return str(input_path_obj.parent / f"{input_path_obj.stem}{suffix}{input_path_obj.suffix}")


def sanitize_filename(filename: str) -> str:
    """Sanitize filename by removing invalid characters."""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename


class BatchProcessor:
    """Handles batch processing operations."""
    
    def __init__(self):
        self.files = []
        self.completed = []
        self.failed = []
        
    def add_file(self, file_path: str) -> bool:
        """Add a file to the batch processing queue."""
        is_valid, _ = FileValidator.validate_input_file(file_path)
        if is_valid and file_path not in self.files:
            self.files.append(file_path)
            return True
        return False
        
    def remove_file(self, file_path: str) -> bool:
        """Remove a file from the batch processing queue."""
        if file_path in self.files:
            self.files.remove(file_path)
            return True
        return False
        
    def clear(self):
        """Clear all files from the queue."""
        self.files.clear()
        self.completed.clear()
        self.failed.clear()
        
    def get_progress(self) -> Tuple[int, int, int]:
        """Get progress as (completed, failed, total)."""
        return len(self.completed), len(self.failed), len(self.files)
        
    def mark_completed(self, file_path: str):
        """Mark a file as completed."""
        if file_path in self.files and file_path not in self.completed:
            self.completed.append(file_path)
            
    def mark_failed(self, file_path: str):
        """Mark a file as failed."""
        if file_path in self.files and file_path not in self.failed:
            self.failed.append(file_path)


def create_desktop_shortcut(app_path: str, shortcut_path: str) -> bool:
    """Create a desktop shortcut (Windows only for now)."""
    try:
        if sys.platform == "win32":
            import winshell
            from win32com.client import Dispatch
            
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = app_path
            shortcut.WorkingDirectory = str(Path(app_path).parent)
            shortcut.IconLocation = app_path
            shortcut.save()
            return True
    except ImportError:
        pass  # winshell not available
    except Exception:
        pass  # Other error creating shortcut
        
    return False