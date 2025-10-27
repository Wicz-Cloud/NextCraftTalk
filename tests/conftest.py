"""
NextCraftTalk Test Configuration and Fixtures

Shared test fixtures and configuration for pytest.
"""

import os
import tempfile
from pathlib import Path
from typing import Generator

import pytest


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)


@pytest.fixture
def mock_env_file(temp_dir: Path) -> Generator[Path, None, None]:
    """Create a mock .env file for testing."""
    env_file = temp_dir / ".env"
    env_content = """
DEPLOYMENT_MODE=external_ai
WEBHOOK_PORT=8080
LOG_LEVEL=INFO
"""
    env_file.write_text(env_content)
    # Change to temp directory so relative paths work
    original_cwd = os.getcwd()
    os.chdir(temp_dir)
    try:
        yield env_file
    finally:
        os.chdir(original_cwd)


@pytest.fixture
def external_ai_env(temp_dir: Path) -> Generator[Path, None, None]:
    """Create environment for external AI mode testing."""
    env_file = temp_dir / ".env"
    env_content = """
DEPLOYMENT_MODE=external_ai
WEBHOOK_PORT=8080
LOG_LEVEL=INFO
XAI_API_KEY=test_key
"""
    env_file.write_text(env_content)
    original_cwd = os.getcwd()
    os.chdir(temp_dir)
    try:
        yield env_file
    finally:
        os.chdir(original_cwd)


@pytest.fixture
def self_hosted_env(temp_dir: Path) -> Generator[Path, None, None]:
    """Create environment for self-hosted mode testing."""
    env_file = temp_dir / ".env"
    env_content = """
DEPLOYMENT_MODE=self_hosted
WEBHOOK_PORT=8081
LOG_LEVEL=INFO
OLLAMA_BASE_URL=http://localhost:11434
CHROMA_HOST=localhost
CHROMA_PORT=8001
"""
    env_file.write_text(env_content)
    original_cwd = os.getcwd()
    os.chdir(original_cwd)
    try:
        yield env_file
    finally:
        os.chdir(original_cwd)


@pytest.fixture(autouse=True)
def clean_env():
    """Clean environment variables before each test."""
    # Remove any NextCraftTalk related env vars
    env_vars_to_remove = [
        "DEPLOYMENT_MODE",
        "WEBHOOK_PORT",
        "LOG_LEVEL",
        "XAI_API_KEY",
        "OLLAMA_BASE_URL",
        "CHROMA_HOST",
        "CHROMA_PORT",
    ]
    for var in env_vars_to_remove:
        os.environ.pop(var, None)
    yield
