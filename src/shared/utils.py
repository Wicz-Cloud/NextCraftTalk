"""
Shared utilities for NextCraftTalk
"""

import logging
from pathlib import Path

from ..core.config import get_config


def setup_logging() -> None:
    """Setup logging configuration"""
    config = get_config()
    logging.basicConfig(
        level=getattr(logging, config.logging.level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(config.logging.file), logging.StreamHandler()],
    )


def ensure_directories() -> None:
    """Ensure all required directories exist"""
    dirs = [
        Path("logs"),
        Path("data"),
    ]

    # Add mode-specific directories
    config = get_config()
    if config.self_hosted:
        dirs.append(Path(config.self_hosted.chroma_db_path).parent)

    for dir_path in dirs:
        dir_path.mkdir(parents=True, exist_ok=True)


def get_project_root() -> Path:
    """Get the project root directory"""
    return Path(__file__).parent.parent.parent


def load_env_file(env_file: str = ".env") -> None:
    """Load environment variables from file"""
    from dotenv import load_dotenv

    env_path = get_project_root() / env_file
    if env_path.exists():
        load_dotenv(env_path)
