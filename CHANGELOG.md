## 1.1.1 — 2026-10-01

Monthly patch release (Dependabot + maintenance).

- deps(deps): update virtualenv requirement from >=21.7.14 to >=21.12.1 (#73)
- deps(deps): update starlette requirement from >=1.6.0 to >=1.7.0 (#71)
- deps(deps): bump sentence-transformers from 6.0.1 to 6.1.0 (#72)
- deps(deps): update filelock requirement from >=4.0.0 to >=4.0.3 (#74)
- ci(deps): bump actions/checkout from 4 to 7 (#69)
- deps(deps): update filelock requirement from >=3.32.6 to >=4.0.0 (#68)
- deps(deps): update protobuf requirement from >=7.36.1 to >=7.36.2 (#67)
- ci(deps): bump actions/setup-python from 5 to 7 (#70)
- deps(deps): update virtualenv requirement from >=21.7.9 to >=21.7.14 (#66)
- ci: monthly patch release + Dependabot auto-merge (#65)
- deps(deps): update filelock requirement from >=3.32.5 to >=3.32.6 (#64)
- deps(deps): update virtualenv requirement from >=21.7.8 to >=21.7.9 (#63)
- deps(deps): update pillow requirement from >=12.2.0 to >=12.3.0 (#56)
- deps(deps): update virtualenv requirement from >=20.36.1 to >=21.7.8 (#55)
- deps(deps): bump sentence-transformers from 5.2.3 to 6.0.1 (#60)
- deps(deps): update starlette requirement from >=0.49.1 to >=1.6.0 (#53)
- deps(deps): update filelock requirement from >=3.20.3 to >=3.32.5 (#57)
- deps(deps): update protobuf requirement from >=6.33.5 to >=7.36.1 (#58)
- deps(deps): update google-api-python-client requirement (#61)
- ci(deps): bump actions/setup-python from 6 to 7 (#59)
- ci(deps): bump actions/checkout from 6 to 7 (#52)
- deps(deps): bump chromadb from 1.4.0 to 1.5.9 (#62)
- deps(deps): update pyasn1 requirement from >=0.6.3 to >=0.6.4 (#54)
- fix: unblock security CI and pin chromadb to latest available (#51)
- security: batch update vulnerable dependencies (#49)
- fix: remove javascript from CodeQL matrix to prevent false error (#32)
- security: bump vulnerable dependencies (#31)
- deps(deps): bump chromadb from 1.4.0 to 1.5.2 (#30)
- ci(deps): bump actions/upload-artifact from 6 to 7 (#29)
- deps(deps): bump sentence-transformers from 5.2.0 to 5.2.3 (#28)
- deps(deps): bump urllib3 in the pip group across 1 directory (#23)
- deps(deps): bump chromadb from 1.3.7 to 1.4.0 (#22)
- deps(deps): bump urllib3 in the pip group across 1 directory (#17)
- deps(deps): bump urllib3 from 2.5.0 to 2.6.2 (#18)
- deps(deps): bump sentence-transformers from 5.1.2 to 5.2.0 (#19)
- deps(deps): bump chromadb from 1.3.5 to 1.3.7 (#20)
- ci(deps): bump actions/upload-artifact from 5 to 6 (#21)
- deps(deps): bump chromadb from 1.3.4 to 1.3.5 (#16)
- ci(deps): bump actions/checkout from 5 to 6 (#15)
- deps(deps): bump chromadb from 1.2.2 to 1.3.4 (#14)
- docker(deps): bump python in /docker/self_hosted (#13)
- Security: Resolve pip CVE-2025-8869 and enhance CI/CD security
- security: Update FastAPI to version compatible with secure Starlette
- security: Fix Starlette O(n^2) DoS vulnerability in FileResponse
- fix: Downgrade self-hosted Docker to Python 3.13 for chromadb compatibility
- fix: Remove invalid assignees from dependabot.yml
- fix: Remove pip from requirements-external.txt causing Docker build failure
- docker(deps): bump python in /docker/external_ai (#8)
- deps(deps): bump chromadb from 1.2.1 to 1.2.2 (#9)
- ci(deps): bump actions/checkout from 4 to 5 (#11)
- docker(deps): bump python in /docker/self_hosted (#10)
- ci(deps): bump actions/setup-python from 5 to 6 (#12)
- docs: Update documentation to reflect v1.1.0 architecture and features

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
