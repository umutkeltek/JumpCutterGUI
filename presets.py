"""
Preset configurations for different types of content and use cases.
"""

from typing import Dict, Any

# Default presets for different content types
PRESETS = {
    "podcast": {
        "name": "Podcast",
        "description": "Optimized for podcast content with speech",
        "magnitude_threshold_ratio": 0.02,
        "duration_threshold": 0.8,
        "failure_tolerance_ratio": 0.05,
        "space_on_edges": 0.1,
        "silence_part_speed": 1.0,
        "min_loud_part_duration": 0.3,
        "cut": "silent"
    },
    "lecture": {
        "name": "Lecture/Educational",
        "description": "For educational content with longer pauses",
        "magnitude_threshold_ratio": 0.025,
        "duration_threshold": 1.2,
        "failure_tolerance_ratio": 0.07,
        "space_on_edges": 0.15,
        "silence_part_speed": 1.0,
        "min_loud_part_duration": 0.5,
        "cut": "silent"
    },
    "tutorial": {
        "name": "Tutorial/Demo",
        "description": "For screen recordings and tutorials",
        "magnitude_threshold_ratio": 0.015,
        "duration_threshold": 0.6,
        "failure_tolerance_ratio": 0.04,
        "space_on_edges": 0.08,
        "silence_part_speed": 1.0,
        "min_loud_part_duration": 0.2,
        "cut": "silent"
    },
    "meeting": {
        "name": "Meeting/Interview",
        "description": "For meetings and interviews with multiple speakers",
        "magnitude_threshold_ratio": 0.03,
        "duration_threshold": 1.0,
        "failure_tolerance_ratio": 0.08,
        "space_on_edges": 0.2,
        "silence_part_speed": 1.0,
        "min_loud_part_duration": 0.4,
        "cut": "silent"
    },
    "aggressive": {
        "name": "Aggressive Cutting",
        "description": "Maximum silence removal for very tight editing",
        "magnitude_threshold_ratio": 0.01,
        "duration_threshold": 0.3,
        "failure_tolerance_ratio": 0.02,
        "space_on_edges": 0.05,
        "silence_part_speed": 1.0,
        "min_loud_part_duration": 0.1,
        "cut": "silent"
    },
    "conservative": {
        "name": "Conservative",
        "description": "Gentle silence removal preserving natural flow",
        "magnitude_threshold_ratio": 0.05,
        "duration_threshold": 2.0,
        "failure_tolerance_ratio": 0.1,
        "space_on_edges": 0.3,
        "silence_part_speed": 1.0,
        "min_loud_part_duration": 0.8,
        "cut": "silent"
    }
}

# Platform-specific export presets
EXPORT_PRESETS = {
    "youtube": {
        "name": "YouTube",
        "description": "Optimized for YouTube upload",
        "codec": "libx264",
        "bitrate": "5000k",
        "suggested_settings": {
            "magnitude_threshold_ratio": 0.02,
            "duration_threshold": 0.7,
        }
    },
    "instagram": {
        "name": "Instagram",
        "description": "Optimized for Instagram videos",
        "codec": "libx264",
        "bitrate": "3500k",
        "suggested_settings": {
            "magnitude_threshold_ratio": 0.015,
            "duration_threshold": 0.5,
        }
    },
    "tiktok": {
        "name": "TikTok",
        "description": "Optimized for TikTok short videos",
        "codec": "libx264",
        "bitrate": "2500k",
        "suggested_settings": {
            "magnitude_threshold_ratio": 0.01,
            "duration_threshold": 0.3,
        }
    },
    "twitter": {
        "name": "Twitter",
        "description": "Optimized for Twitter videos",
        "codec": "libx264",
        "bitrate": "2000k",
        "suggested_settings": {
            "magnitude_threshold_ratio": 0.02,
            "duration_threshold": 0.6,
        }
    }
}

def get_preset(preset_name: str) -> Dict[str, Any]:
    """Get a preset configuration by name."""
    return PRESETS.get(preset_name, {})

def get_export_preset(preset_name: str) -> Dict[str, Any]:
    """Get an export preset configuration by name."""
    return EXPORT_PRESETS.get(preset_name, {})

def list_presets() -> Dict[str, str]:
    """List all available presets with their descriptions."""
    return {name: config["description"] for name, config in PRESETS.items()}

def list_export_presets() -> Dict[str, str]:
    """List all available export presets with their descriptions."""
    return {name: config["description"] for name, config in EXPORT_PRESETS.items()}