# Changelog

All notable changes to NextCraftTalk will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive semantic versioning system
- Version management script (`scripts/version_manager.py`)
- Semantic versioning documentation in wiki

### Changed
- Repository structure modernized with professional Python standards

## [1.1.0] - 2025-10-27

### Added
- **Content Safety Filtering**: Comprehensive profanity and toxicity detection for external AI mode
- **Profanity Detection**: Automatic inappropriate language filtering using `profanity-check` library
- **Toxicity Analysis**: Google Perspective API integration for advanced content safety
- **Configurable Safety Settings**: Environment variable controls for sensitivity thresholds
- **Safe Fallback Responses**: Kid-friendly alternatives when unsafe content is detected
- **Safety Filter Module**: Shared `src/shared/safety_filter.py` for consistent content filtering

### Changed
- **External AI Pipeline**: Enhanced with safety filtering for all x.ai responses
- **Dependencies**: Added `profanity-check` and `google-api-python-client` to external requirements
- **Documentation**: Updated README, external AI docs, and xAI API wiki with safety features
- **Environment Configuration**: New safety-related environment variables

### Technical Details
- **Safety Thresholds**: Configurable profanity (default: 0.6) and toxicity (default: 0.7) levels
- **Graceful Degradation**: Safety features work without optional dependencies
- **Performance**: Minimal overhead with efficient filtering algorithms
- **Extensibility**: Modular design for future safety enhancements

## [1.0.2] - 2025-10-26

### Security
- **SARIF Upload Reliability**: Fixed JSON syntax errors in GitHub Actions security audit workflow
- **Container Security Scanning**: Enhanced Trivy integration with automatic SARIF validation and fallback
- **Vulnerability Mitigation**: Resolved urllib3 redirect vulnerabilities (CVE-2025-50181, CVE-2025-50182)
- **Server Binding Security**: Changed default server bindings from 0.0.0.0 to 127.0.0.1 for localhost-only access

### Fixed
- **CI/CD Pipeline**: Resolved SARIF file generation failures preventing security results upload
- **HTTP Timeouts**: Added proper timeout handling for Ollama API calls (30s tags, 300s model pulls)
- **Security Scanning**: Fixed Bandit security linter issues and dependency vulnerability detection
- **Workflow Reliability**: Enhanced error handling in security audit workflows with debug logging

### Added
- **Automated Security Validation**: jq-based SARIF file validation with minimal fallback structures
- **Debug Logging**: Enhanced Trivy scan result inspection for troubleshooting
- **Graceful Degradation**: Security workflows continue execution even with individual scan failures

## [1.0.0] - 2025-10-26

### Added
- **Complete Repository Modernization**: Migrated from single-file script to professional Python package structure
- **Comprehensive Test Suite**: Added pytest framework with 22/23 tests passing
- **Automated Code Quality**: Implemented pre-commit hooks with black, isort, flake8, mypy
- **Modern Packaging**: Added pyproject.toml with complete dependency management
- **Docker Optimization**: Updated to Python 3.11-slim with .dockerignore
- **Development Tools**: Added Makefile with automated workflows (build, test, check, format, lint)
- **GitHub Wiki Documentation**: Complete guides for Nextcloud Talk, Ollama, xAI API, and development
- **CI/CD Pipeline**: GitHub Actions with security scanning, dependency review, and code quality checks
- **Security Features**: Comprehensive vulnerability scanning and security advisories
- **Pre-commit Tooling**: Automated code formatting and quality checks

### Changed
- **Project Structure**: Moved from `main.py` to `src/` layout with proper package organization
- **Dependencies**: Updated to LTS versions with security patches
- **Docker Images**: Migrated to Python 3.11-slim base images
- **Configuration**: Centralized configuration management with Pydantic v2
- **Documentation**: Updated README to reference comprehensive wiki documentation

### Fixed
- **Security Vulnerabilities**: Resolved urllib3 and other dependency security issues
- **CI/CD Issues**: Fixed workflow triggers and TruffleHog configuration
- **Code Quality**: Resolved all linting issues and type errors
- **Import Issues**: Fixed relative import problems and module organization

### Security
- **Dependency Updates**: Pinned vulnerable packages to secure versions
- **Security Scanning**: Implemented comprehensive vulnerability detection
- **Advisory System**: Added automated security advisory creation

## [0.3.0] - 2025-10-25

### Added
- **Comprehensive Security Features**: GitHub security advisories and vulnerability reporting
- **Security Policy**: Detailed vulnerability reporting guidelines and SLO compliance
- **Security Monitoring**: Email-based security alert system

### Changed
- **CI/CD Pipeline**: Enhanced with security scanning and automated advisories
- **Dependencies**: Updated GitHub Actions to latest versions for security

### Fixed
- **Shellcheck Warnings**: Resolved shell script linting issues

## [0.2.0] - 2025-10-21

### Added
- **Nextcloud Talk Bot Detection**: Automated bot setup and detection
- **Prompt Template Support**: File watching and mounting for templates
- **Pre-commit Code Quality**: Comprehensive linting and formatting tools
- **Enhanced Docker Configuration**: Improved container networking and health checks

### Changed
- **Environment Configuration**: Updated .env.example with better model selection
- **Development Workflow**: Added comprehensive pre-commit tooling

### Fixed
- **Container Health Checks**: Corrected port binding for health monitoring

## [0.1.0] - 2025-10-19

### Added
- Initial Nextcloud Talk integration
- Basic bot functionality for external AI mode
- Docker containerization for both deployment modes
- Basic configuration management
- Initial documentation and setup guides
- Phase 1 basic structure and NextCraftTalk-EXT integration

### Changed
- Separated requirements files for different deployment modes
- Added configurable Docker network support
- Implemented prompt template mounting and file watching

### Fixed
- Container port binding issues
- Shellcheck warnings
- Basic functionality bugs

---

## Release Notes Template

When creating a new release, copy this template and fill in the details:

```markdown
## [VERSION] - YYYY-MM-DD

### Added
- New features and capabilities

### Changed
- Modifications to existing functionality

### Deprecated
- Features scheduled for removal

### Removed
- Removed features and capabilities

### Fixed
- Bug fixes and issue resolutions

### Security
- Security-related changes and vulnerability fixes
```

### Version Classification Checklist

**Major Version (X.0.0)**:
- [ ] Breaking API changes
- [ ] Major architectural changes
- [ ] Incompatible dependency updates
- [ ] Feature removal

**Minor Version (x.Y.0)**:
- [ ] New features (backward compatible)
- [ ] Significant enhancements
- [ ] New configuration options
- [ ] New integrations

**Patch Version (x.x.Z)**:
- [ ] Bug fixes
- [ ] Security patches
- [ ] Documentation updates
- [ ] Compatible dependency updates
- [ ] Performance improvements
- [ ] Code quality improvements
