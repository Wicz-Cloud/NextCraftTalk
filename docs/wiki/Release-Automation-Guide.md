# Release Automation Guide

This guide covers automated release processes for NextCraftTalk, including version management, GitHub releases, and Discord notifications.

## Overview

NextCraftTalk uses automated workflows to streamline the release process:

- **Semantic Versioning**: Automated version bumping and tagging
- **GitHub Releases**: Automated release creation with PyPI publishing
- **Docker Images**: Automated container image building and publishing
- **Discord Notifications**: Automatic release announcements

## Version Management

### Using the Version Manager Script

The `scripts/version_manager.py` script handles all version operations:

```bash
# Check current version
./scripts/version_manager.py current

# Bump versions
./scripts/version_manager.py bump --type patch    # 1.0.0 → 1.0.1
./scripts/version_manager.py bump --type minor    # 1.0.0 → 1.1.0
./scripts/version_manager.py bump --type major    # 1.0.0 → 2.0.0

# Create and push tags
./scripts/version_manager.py tag
./scripts/version_manager.py push

# View recent commits for changelog
./scripts/version_manager.py changelog
```

### Makefile Integration

Version commands are also available through Makefile:

```bash
make version              # Show current version
make version-bump-patch   # Bump patch version
make version-bump-minor   # Bump minor version
make version-bump-major   # Bump major version
make version-tag         # Create git tag
make version-push        # Push tag to remote
make version-release     # Complete release workflow
```

## GitHub Releases Automation

### Automated Release Workflow

When you push a version tag (e.g., `v1.0.0`), the release workflow automatically:

1. **Builds Python Package**: Creates distribution files
2. **Publishes to PyPI**: Uploads package to Python Package Index
3. **Builds Docker Images**: Creates and pushes container images
4. **Creates GitHub Release**: Generates release with changelog

### Release Process

1. **Prepare Release**:
   ```bash
   make check              # Run all quality checks
   make test              # Run test suite
   make version-bump-patch # Bump version (adjust type as needed)
   ```

2. **Create Tag and Push**:
   ```bash
   make version-tag       # Create annotated tag
   make version-push      # Push to remote repository
   ```

3. **GitHub Release**:
   - Go to repository → Releases → Draft new release
   - Select the new tag
   - Copy changelog content from `CHANGELOG.md`
   - Publish release

The automation handles the rest automatically.

## Discord Release Notifications

### Setup Process

#### 1. Create Discord Webhook

1. Open your Discord server settings
2. Navigate to **Integrations** → **Webhooks**
3. Click **New Webhook**
4. Configure:
   - **Name**: "NextCraftTalk Releases"
   - **Channel**: Select your releases/announcements channel
   - **Avatar**: Optional - use repository logo
5. Copy the **Webhook URL**

#### 2. Add GitHub Secret

1. Go to your repository on GitHub
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Configure:
   - **Name**: `DISCORD_WEBHOOK_URL`
   - **Value**: Paste your webhook URL
5. Click **Add secret**

#### 3. Test the Integration

1. Create a test release on GitHub
2. Check your Discord channel for the notification
3. Verify the embed formatting and content

### Testing Discord Notifications

For testing Discord notifications without affecting main branch versioning:

1. **Create Test Branch**:
   ```bash
   git checkout -b test-discord-notifications
   ```

2. **Create Test Tag**:
   ```bash
   ./scripts/version_manager.py bump --type patch
   ./scripts/version_manager.py tag --message "test: Discord notification test"
   ./scripts/version_manager.py push
   ```

3. **Check Discord**: Verify the notification appears in your channel

4. **Clean Up**:
   ```bash
   git checkout main
   git branch -D test-discord-notifications
   git tag -d v1.x.x  # Delete test tag locally
   git push origin :refs/tags/v1.x.x  # Delete test tag remotely
   ```

This approach keeps your main branch version history clean while allowing thorough testing of notification workflows.

### Discord Embed Features

The automated Discord posts include:

- **Rich Embeds**: Formatted messages with titles, descriptions, and fields
- **Release Information**: Title, tag, and direct links to GitHub
- **Full Release Notes**: Complete changelog with Markdown formatting (truncated to 2000 chars)
- **Custom Branding**: NextCraftTalk colors and avatar
- **Timestamps**: Automatic timestamp formatting
- **Dual Triggers**: Works for both GitHub releases and version tags

### Workflow Triggers

The Discord notification workflow triggers on:
- **Release Publication**: When you publish a release via GitHub's Releases page
- **Version Tag Push**: When you push a tag matching `v*.*.*` (for testing and automated workflows)

This dual-trigger system ensures notifications work whether you're using manual releases or automated tagging.

### Troubleshooting

**Webhook Not Working**:
- Verify the webhook URL is correct and active
- Check that the Discord channel permissions allow webhooks
- Ensure the GitHub secret is properly configured

**Embed Formatting Issues**:
- Release notes longer than 2000 characters are automatically truncated
- Discord has a 4096 character limit for embed descriptions
- Use proper Markdown formatting in release notes for best results

**Workflow Not Triggering**:
- Ensure releases are published (not just created as drafts)
- Check the Actions tab for workflow run status
- Verify the webhook secret exists and is accessible

## Release Checklist

Before publishing a release:

- [ ] All tests pass (`make test`)
- [ ] Code quality checks pass (`make check`)
- [ ] Documentation is updated
- [ ] Changelog is current (`CHANGELOG.md`)
- [ ] Version is bumped appropriately
- [ ] Branch is up to date with main
- [ ] Pre-commit hooks pass

## Release Types

### Patch Releases (x.x.Z)
- Bug fixes and security patches
- Documentation updates
- Dependency updates
- Minor performance improvements

### Minor Releases (x.Y.0)
- New features (backward compatible)
- Enhancements to existing features
- New configuration options
- API additions

### Major Releases (X.0.0)
- Breaking changes
- Major architectural changes
- API modifications
- Significant feature additions

## Automation Benefits

- **Consistency**: Standardized release process
- **Speed**: Automated building and publishing
- **Reliability**: Reduced manual errors
- **Visibility**: Automatic notifications to stakeholders
- **Security**: Automated security scanning and updates

## Advanced Configuration

### Custom Release Scripts

You can extend the release process with custom scripts in `scripts/release/`.

### Multiple Discord Channels

Add multiple webhooks for different audiences:
- `DISCORD_WEBHOOK_DEV` - Development team notifications
- `DISCORD_WEBHOOK_COMMUNITY` - Community announcements

### Custom Docker Registries

Modify the release workflow to push to additional registries (AWS ECR, Google GCR, etc.).

## Support

For issues with release automation:
1. Check the Actions tab for workflow logs
2. Review Discord webhook configuration
3. Verify GitHub secrets and permissions
4. Consult the troubleshooting section above

For questions about versioning or releases, see the [Semantic Versioning Guide](Semantic-Versioning-Guide.md).
