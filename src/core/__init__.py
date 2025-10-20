"""
NextCraftTalk Core Module
"""

from .config import Config, get_config, is_external_ai_mode, is_self_hosted_mode

__all__ = ["Config", "get_config", "is_self_hosted_mode", "is_external_ai_mode"]
