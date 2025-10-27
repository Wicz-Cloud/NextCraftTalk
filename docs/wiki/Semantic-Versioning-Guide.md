# Semantic Versioning Guide

This document outlines NextCraftTalk's semantic versioning strategy and release process.

## Overview

NextCraftTalk follows [Semantic Versioning 2.0.0](https://semver.org/) (SemVer) to clearly communicate the nature of changes in each release.

## Version Format

Versions follow the format: `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes that are not backward compatible
- **MINOR**: New features that are backward compatible
- **PATCH**: Bug fixes and small improvements that are backward compatible

## Version Classification Guidelines

### Major Version (X.0.0)

**Breaking Changes** - Increment when you make incompatible API changes:

- **API Changes**: Modifications to public APIs, function signatures, or configuration formats
- **Architecture Changes**: Major restructuring that affects how the application is deployed or configured
- **Dependency Changes**: Updating to incompatible versions of core dependencies
- **Feature Removal**: Removing existing features or capabilities
- **Security Changes**: Changes that require user action for security compliance

**Examples from NextCraftTalk:**
- Repository modernization (moving from single file to structured package)
- Major integration changes (merging NextCraftTalk-EXT codebase)
- Breaking API changes in core functionality

### Minor Version (x.Y.0)

**New Features** - Increment when you add functionality in a backwards compatible manner:

- **New Features**: Adding new capabilities or endpoints
- **Enhancements**: Significant improvements to existing features
- **Configuration Options**: New configuration parameters (with defaults)
- **Integration Features**: New third-party integrations
- **UI/UX Improvements**: New user interface elements or workflows

**Examples from NextCraftTalk:**
- Adding Nextcloud Talk bot detection and setup automation
- Implementing comprehensive pre-commit code quality tooling
- Adding configurable Docker network support
- Adding prompt template mounting and file watching support

### Patch Version (x.x.Z)

**Bug Fixes & Maintenance** - Increment when you make backwards compatible bug fixes:

- **Bug Fixes**: Resolving issues, crashes, or incorrect behavior
- **Security Patches**: Security vulnerability fixes without breaking changes
- **Documentation Updates**: README, wiki, and code documentation improvements
- **Dependency Updates**: Updating dependencies to newer compatible versions
- **Performance Improvements**: Optimizations that don't change functionality
- **Code Quality**: Linting fixes, refactoring without functional changes

**Examples from NextCraftTalk:**
- Updating dependency versions for security/stability
- Fixing CI/CD workflow issues
- Adding documentation and wiki content
- Resolving linting and code quality issues
- Updating Docker base images to newer patch versions

## Release Process

### 1. Commit Classification

All commits should be prefixed with appropriate type indicators:

- `feat:` - New features (minor version bump)
- `fix:` - Bug fixes (patch version bump)
- `docs:` - Documentation changes (patch version bump)
- `deps:` - Dependency updates (patch version bump)
- `ci:` - CI/CD changes (patch version bump)
- `refactor:` - Code refactoring (patch version bump)
- `BREAKING CHANGE:` - Breaking changes (major version bump)

### 2. Version Bumping

Use the version management script to handle versioning:

```bash
# Check current version
./scripts/version_manager.py current

# Bump patch version (e.g., 1.0.0 -> 1.0.1)
./scripts/version_manager.py bump --type patch

# Bump minor version (e.g., 1.0.0 -> 1.1.0)
./scripts/version_manager.py bump --type minor

# Bump major version (e.g., 1.0.0 -> 2.0.0)
./scripts/version_manager.py bump --type major
```

### 3. Release Creation

1. Ensure all changes are committed and tested
2. Run full test suite: `make test`
3. Run code quality checks: `make check`
4. Update VERSION file using version manager
5. Create git tag: `./scripts/version_manager.py tag`
6. Push tag: `./scripts/version_manager.py push`
7. Create GitHub release with release notes

### 4. Release Notes

Release notes should include:

- **Summary**: Brief overview of the release
- **Breaking Changes**: List of breaking changes (major versions)
- **New Features**: List of new features (minor versions)
- **Bug Fixes**: List of bug fixes (patch versions)
- **Dependencies**: Notable dependency updates
- **Migration Guide**: Instructions for upgrading (if needed)

## Automated Versioning

The project includes automated versioning tools:

- **Version Manager**: `scripts/version_manager.py` for version operations
- **VERSION File**: Current version tracking
- **Makefile Integration**: Version commands in development workflow
- **GitHub Actions**: Automated releases with PyPI publishing and Docker image builds
- **Discord Notifications**: Automatic release announcements to Discord channels

### Discord Release Notifications

When you publish a release on GitHub, release notes are automatically posted as formatted embed messages to Discord channels.

#### Setup Instructions

1. **Create Discord Webhook**:
   - Open your Discord server settings
   - Navigate to **Integrations** → **Webhooks**
   - Create a new webhook for your releases channel
   - Copy the **Webhook URL**

2. **Add GitHub Secret**:
   - Go to repository Settings → Secrets and variables → Actions
   - Create new secret: `DISCORD_WEBHOOK_URL`
   - Paste your webhook URL as the value

3. **Automatic Posting**:
   - Triggers on release publication OR version tag pushes
   - Posts formatted embeds with release title, notes, and links
   - Includes custom branding and footer messages

#### Discord Embed Features

- **Title**: Release name with link to GitHub release/tag
- **Description**: Full release notes with Markdown formatting
- **Color**: Green theme for successful releases
- **Footer**: Custom message with update notification
- **Avatar**: NextCraftTalk branding

The Discord workflow runs automatically on both GitHub releases and version tag pushes.

### Testing Notifications

To test Discord notifications without affecting main branch versioning:

1. **Create Test Branch**: `git checkout -b test-discord-notifications`
2. **Create Test Tag**: Use version manager to bump and tag
3. **Push Tag**: Triggers Discord notification workflow
4. **Verify**: Check Discord channel for notification
5. **Clean Up**: Delete test branch and tags when done

This keeps your main branch version history clean for testing.

## Branching Strategy

- `main`: Production-ready code, tagged releases
- `develop`: Integration branch for features
- Feature branches: `feature/feature-name`
- Hotfix branches: `hotfix/issue-number`

## Version History

See [CHANGELOG.md](../CHANGELOG.md) for detailed version history and release notes.

## Contributing

When contributing:

1. Follow commit message conventions
2. Update documentation for new features
3. Ensure backward compatibility for non-major changes
4. Test thoroughly before submitting PRs

For questions about versioning, contact the maintainers or open an issue.
