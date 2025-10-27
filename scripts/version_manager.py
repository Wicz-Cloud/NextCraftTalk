#!/usr/bin/env python3
"""
NextCraftTalk Version Management Script

This script provides utilities for managing semantic versioning in the NextCraftTalk project.
"""

import argparse
import re
import subprocess
from pathlib import Path
from typing import Tuple


class VersionManager:
    """Manages semantic versioning for NextCraftTalk."""

    def __init__(self, repo_path: Path = None):
        self.repo_path = repo_path or Path(__file__).parent.parent
        self.version_file = self.repo_path / "VERSION"

    def get_current_version(self) -> str:
        """Get the current version from VERSION file."""
        if not self.version_file.exists():
            raise FileNotFoundError(f"VERSION file not found at {self.version_file}")

        return self.version_file.read_text().strip()

    def parse_version(self, version: str) -> Tuple[int, int, int]:
        """Parse semantic version string into components."""
        match = re.match(r"^(\d+)\.(\d+)\.(\d+)$", version)
        if not match:
            raise ValueError(f"Invalid semantic version format: {version}")

        return tuple(int(x) for x in match.groups())

    def format_version(self, major: int, minor: int, patch: int) -> str:
        """Format version components into semantic version string."""
        return f"{major}.{minor}.{patch}"

    def bump_version(self, bump_type: str) -> str:
        """Bump version according to semantic versioning rules."""
        current = self.get_current_version()
        major, minor, patch = self.parse_version(current)

        if bump_type == "major":
            major += 1
            minor = 0
            patch = 0
        elif bump_type == "minor":
            minor += 1
            patch = 0
        elif bump_type == "patch":
            patch += 1
        else:
            raise ValueError(f"Invalid bump type: {bump_type}. Must be 'major', 'minor', or 'patch'")

        new_version = self.format_version(major, minor, patch)
        self.version_file.write_text(new_version)
        return new_version

    def create_git_tag(self, version: str, message: str = None) -> None:
        """Create a git tag for the current commit."""
        if message is None:
            message = f"Release version {version}"

        # Create annotated tag
        subprocess.run(["git", "tag", "-a", version, "-m", message], check=True)

    def push_tag(self, version: str) -> None:
        """Push the version tag to remote repository."""
        subprocess.run(["git", "push", "origin", version], check=True)

    def get_commit_messages_since_tag(self, tag: str = None) -> list[str]:
        """Get commit messages since the last tag."""
        if tag:
            cmd = ["git", "log", "--oneline", f"{tag}..HEAD"]
        else:
            cmd = ["git", "log", "--oneline"]

        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip().split("\n") if result.stdout.strip() else []


def main():
    parser = argparse.ArgumentParser(description="NextCraftTalk Version Manager")
    parser.add_argument("action", choices=["current", "bump", "tag", "push", "changelog"], help="Action to perform")
    parser.add_argument(
        "--type", choices=["major", "minor", "patch"], help="Version bump type (required for bump action)"
    )
    parser.add_argument("--message", help="Tag message (for tag action)")
    parser.add_argument("--since-tag", help="Tag to compare against for changelog")

    args = parser.parse_args()
    manager = VersionManager()

    if args.action == "current":
        print(manager.get_current_version())

    elif args.action == "bump":
        if not args.type:
            parser.error("--type is required for bump action")
        new_version = manager.bump_version(args.type)
        print(f"Version bumped to {new_version}")

    elif args.action == "tag":
        current_version = manager.get_current_version()
        manager.create_git_tag(current_version, args.message)
        print(f"Created tag {current_version}")

    elif args.action == "push":
        current_version = manager.get_current_version()
        manager.push_tag(current_version)
        print(f"Pushed tag {current_version}")

    elif args.action == "changelog":
        commits = manager.get_commit_messages_since_tag(args.since_tag)
        print("Recent commits:")
        for commit in commits:
            if commit.strip():
                print(f"  {commit}")


if __name__ == "__main__":
    main()
