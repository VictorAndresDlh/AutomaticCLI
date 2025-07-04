"""
Environment configuration utilities
Loads environment variables from .env file
"""

import os
from pathlib import Path


def load_env_file(env_path: str = ".env") -> dict:
    """Load environment variables from .env file"""
    env_vars = {}
    env_file = Path(env_path)
    
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    env_vars[key] = value
                    os.environ[key] = value
    
    return env_vars


def check_api_keys() -> dict:
    """Check which API keys are configured"""
    keys_status = {
        'openai': bool(os.environ.get('OPENAI_API_KEY')),  # Required for Codex and evaluation
        'anthropic': bool(os.environ.get('ANTHROPIC_API_KEY')),  # Optional - Claude Code works without it
        'gemini': True,  # Gemini CLI works without API key (free tier with Google auth)
        'claude_code': True  # Claude Code works without API key
    }
    return keys_status


# Load .env file automatically when this module is imported
load_env_file()
