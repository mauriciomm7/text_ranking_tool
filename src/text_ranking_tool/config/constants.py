# src/text_ranking_tool/config/constants.py

import json
import sys
from pathlib import Path
from typing import Dict, Any

# DEBUG FLAG
DEBUG = False

# Simple config file detection - PyInstaller compatible
if getattr(sys, 'frozen', False):
    CONFIG_FILE = Path(sys.executable).parent / "config.json"
else:
    CONFIG_FILE = Path(__file__).parents[3] / "dev_config.json"

def load_config() -> Dict[str, Any]:
    """Load configuration from JSON file - NO DEFAULTS"""
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        raise FileNotFoundError(f"Configuration file {CONFIG_FILE} is required but not found: {e}")

# Load configuration once - FAIL if not found
_config = load_config()

# Install root path (absolute), from config
INSTALL_ROOT = Path(_config["install_root"]).resolve()

def resolve_path(path_str: str) -> Path:
    """Resolves a path relative to INSTALL_ROOT unless it's absolute."""
    path = Path(path_str)
    return path if path.is_absolute() else INSTALL_ROOT / path

# ALL paths from config - FLAT STRUCTURE
EXTERNAL_DATA_DIR = resolve_path(_config["external_data_dir"])
INTERNAL_DATA_DIR = resolve_path(_config["internal_data_dir"])
EXTERNAL_EXPORT_DIR = resolve_path(_config["external_export_dir"])
INTERNAL_EXPORT_DIR = resolve_path(_config["internal_export_dir"])
INTERNAL_USERS_DIR = resolve_path(_config["internal_users_dir"])

# ALL algorithm settings from config - FLAT STRUCTURE
CONFIGURED_ALGORITHM = _config["algorithm"]
AVAILABLE_ALGORITHMS = _config["available_algorithms"]
DEFAULT_ALGORITHM = _config["default_algorithm"]

# ALL user settings from config - NO DEFAULTS
USER_MAPPING = _config["user_mapping"]
USER_COLORS = _config["user_colors"]

# CSV requirements from config - NO DEFAULTS
REQUIRED_COLUMNS = _config["required_columns"]

# Helper functions
def get_user_id(display_name: str) -> str:
    return USER_MAPPING.get(display_name, display_name.replace(" ", ""))

def get_user_color(username: str) -> str:
    return USER_COLORS.get(username, "white")


def set_algorithm(algorithm_name: str) -> bool:
    """
    Set the current algorithm if it's available.
    Returns True if successful, False if algorithm not available.
    """
    global CONFIGURED_ALGORITHM
    if algorithm_name in AVAILABLE_ALGORITHMS:
        CONFIGURED_ALGORITHM = algorithm_name
        return True
    return False

def get_available_algorithms() -> list:
    """Get list of available algorithms."""
    return AVAILABLE_ALGORITHMS.copy()

def get_configured_algorithm() -> str:
    """Get the current configured algorithm - always returns latest value"""
    global CONFIGURED_ALGORITHM
    return CONFIGURED_ALGORITHM


def save_config_to_file():
    """Save current config back to JSON file"""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(_config, f, indent=2)
        return True
    except Exception as e:
        print(f"Warning: Could not save config: {e}")
        return False