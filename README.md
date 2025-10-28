# NextCraftTalk

🤖 **Unified AI Chatbot for Nextcloud Talk** - Supporting both self-hosted and external AI deployment modes.

## 🌟 Features

- **Dual Deployment Modes**:
  - **External AI Mode**: Uses x.ai for AI responses (lightweight, cloud-based)
  - **Self-Hosted Mode**: Full local AI stack with Ollama, ChromaDB, and RAG pipeline

- **Nextcloud Talk Integration**: Seamless webhook-based chat integration
- **Mode Switching**: Simple `.env` configuration to switch between modes
- **Docker Support**: Containerized deployment for both modes
- **Content Safety**: Built-in profanity filtering and toxicity detection

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Docker & Docker Compose (for containerized deployment)
- Nextcloud instance with Talk enabled

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Wicz-Cloud/NextCraftTalk.git
   cd NextCraftTalk
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Deploy**
   ```bash
   # Using Docker (recommended)
   ./scripts/deploy.sh start

   # Or run directly with Python
   ./scripts/deploy.sh python
   ```

## ⚙️ Configuration

Edit `.env` to configure:

```env
# Deployment mode: 'external_ai' or 'self_hosted'
DEPLOYMENT_MODE=external_ai

# Nextcloud configuration
NEXTCLOUD_URL=https://your-nextcloud.com
NEXTCLOUD_USERNAME=bot-user
NEXTCLOUD_PASSWORD=your-password
TALK_ROOM_TOKEN=room-token

# External AI mode
XAI_API_KEY=your-xai-key

# Self-hosted mode (when DEPLOYMENT_MODE=self_hosted)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2
CHROMA_DB_PATH=./data/chroma_db
```

## 🏗️ Architecture

```
NextCraftTalk/
├── src/
│   ├── core/          # Configuration & shared logic
│   ├── modes/         # Mode-specific implementations
│   │   ├── external_ai/    # x.ai integration
│   │   └── self_hosted/    # Local AI stack
│   ├── shared/        # Common utilities
│   └── bot/           # Core bot logic
├── docker/            # Container configurations
├── scripts/           # Deployment scripts
└── tests/             # Test suite
```

## 📋 Deployment Modes

### External AI Mode
- Lightweight deployment using x.ai API
- No local AI infrastructure required
- Perfect for cloud deployments

### Self-Hosted Mode
- Full local AI stack with Ollama
- Vector database (ChromaDB) for knowledge base
- Web scraping capabilities
- RAG pipeline for enhanced responses

## 🛠️ Development

### Setup Development Environment
```bash
# Install all dependencies (recommended)
make install-all

# Or install specific modes
make install-external    # External AI mode only
make install-selfhosted  # Self-hosted mode only
make install-dev         # Development dependencies only
```

### Development Workflow
```bash
# Run all tests
make test

# Run tests with coverage
make test-cov

# Code quality checks
make lint          # Run linting tools
make format        # Format code
make check         # Run all quality checks

# Pre-commit hooks
make pre-commit-install  # Install pre-commit hooks
make pre-commit-run      # Run pre-commit on all files

# Development server
make serve-external     # Start external AI mode server
make serve-selfhosted   # Start self-hosted mode server
make stop               # Stop development server

# Docker operations
make docker-build-external    # Build external AI Docker image
make docker-build-selfhosted  # Build self-hosted Docker image
make docker-run-external      # Run external AI containers
make docker-run-selfhosted    # Run self-hosted containers
make docker-stop-external     # Stop external AI containers
make docker-stop-selfhosted   # Stop self-hosted containers

# Deployment
make deploy-external     # Deploy external AI mode
make deploy-selfhosted   # Deploy self-hosted mode

# Cleanup
make clean         # Clean temporary files
make clean-all     # Clean everything including virtual env
```

### Manual Commands (Legacy)
For manual setup without Makefile:
```bash
# For external AI mode
pip install -r requirements-external.txt

# For self-hosted mode
pip install -r requirements-selfhosted.txt
```

## 📚 Documentation

For comprehensive documentation, visit our [GitHub Wiki](https://github.com/Wicz-Cloud/NextCraftTalk/wiki):

### Quick Reference Guides
- [NextCraftTalk Overview](https://github.com/Wicz-Cloud/NextCraftTalk/wiki/NextCraftTalk-Overview) - Project description and features
- [Makefile Commands & Scenarios](https://github.com/Wicz-Cloud/NextCraftTalk/wiki/Makefile-Commands-&-Scenarios) - Development workflow and deployment scenarios
- [Nextcloud Talk Configuration](https://github.com/Wicz-Cloud/NextCraftTalk/wiki/Nextcloud-Talk-Configuration) - Setting up Nextcloud Talk and adding bots
- [Ollama Setup Guide](https://github.com/Wicz-Cloud/NextCraftTalk/wiki/Ollama-Setup-Guide) - Installing and configuring Ollama
- [xAI API Usage](https://github.com/Wicz-Cloud/NextCraftTalk/wiki/xAI-API-Usage) - Using xAI's Grok API
- [Project Documentation](https://github.com/Wicz-Cloud/NextCraftTalk/wiki/Project-Documentation) - Full docs and development resources
- **[Semantic Versioning Guide](https://github.com/Wicz-Cloud/NextCraftTalk/wiki/Semantic-Versioning-Guide)** - Version management and release process
- **[Release Automation Guide](https://github.com/Wicz-Cloud/NextCraftTalk/wiki/Release-Automation-Guide)** - Automated releases and Discord notifications

### External Resources
- [Nextcloud Talk Official Documentation](https://docs.nextcloud.com/server/latest/user_manual/en/talk/index.html)
- [Ollama Official Site](https://ollama.com/)
- [xAI API Documentation](https://docs.x.ai/)

## 🏷️ Versioning

NextCraftTalk follows [Semantic Versioning 2.0.0](https://semver.org/). For details on our versioning strategy and release process, see our [Semantic Versioning Guide](https://github.com/Wicz-Cloud/NextCraftTalk/wiki/Semantic-Versioning-Guide).

### Current Version
[![Version](https://img.shields.io/badge/version-1.0.2-blue.svg)](https://github.com/Wicz-Cloud/NextCraftTalk/releases)

### Release History
See [CHANGELOG.md](CHANGELOG.md) for detailed release notes and version history.

## 🔒 Security

NextCraftTalk takes security seriously with comprehensive automated security scanning and best practices.

### Security Features
- **Automated Security Scanning**: Weekly security audits with multiple tools (Bandit, Safety, pip-audit, Trivy)
- **Container Security**: Alpine Linux base images with Trivy vulnerability scanning
- **Dependency Monitoring**: Automated dependency updates and vulnerability detection
- **Secure Defaults**: Localhost-only server bindings by default
- **SARIF Integration**: Security findings uploaded to GitHub Security tab
- **Content Safety**: Profanity filtering and toxicity detection for kid-friendly responses

### Security Scanning
The project includes automated security scanning via GitHub Actions:
- **Code Security**: Bandit static analysis for Python security issues
- **Dependency Security**: Safety and pip-audit for vulnerable dependencies
- **Container Security**: Trivy scans for Docker image vulnerabilities
- **Weekly Audits**: Automated security scans every Monday

### Content Safety
NextCraftTalk includes built-in content safety features to ensure appropriate responses:
- **Profanity Filtering**: Automatic detection and censoring using `profanity-check` library
- **Toxicity Detection**: Google Perspective API integration for comprehensive content analysis
- **Configurable Thresholds**: Adjustable sensitivity levels via environment variables
- **Safe Fallbacks**: Kid-friendly alternative responses when unsafe content is detected
- **Environment Controls**: Enable/disable features with `ENABLE_SAFETY_FILTER` variable

### Security Best Practices
- **Server Binding**: Default to `127.0.0.1` instead of `0.0.0.0` for local access only
- **HTTP Timeouts**: Proper timeout handling for API calls (30s for tags, 300s for model pulls)
- **Dependency Pinning**: Secure versions of dependencies with vulnerability fixes
- **Container Hardening**: Non-root users and minimal attack surface

### Reporting Security Issues
Please report security vulnerabilities responsibly. See our [Security Policy](SECURITY.md) for details.

## 🤝 Contributing

We welcome contributions from the community! Please see our [Contributing Guidelines](CONTRIBUTING.md) for detailed information on:

- Development setup and workflow
- Coding standards and best practices
- Testing requirements
- Pull request process
- Issue reporting

### Quick Start for Contributors

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/NextCraftTalk.git`
3. Set up development environment: `make install-all`
4. Create a feature branch: `git checkout -b feature/your-feature`
5. Make your changes following our [coding standards](CONTRIBUTING.md#coding-standards)
6. Run tests: `make test`
7. Submit a pull request

## 📋 Community Standards

- **[Code of Conduct](CODE_OF_CONDUCT.md)**: Our community guidelines and standards
- **[Security Policy](SECURITY.md)**: How to report security vulnerabilities
- **[License](LICENSE)**: MIT License terms and conditions

## 🏷️ Versioning

Join our Discord server for discussions, support, and to connect with other users: https://discord.gg/D2vFfQW4Nm

## �📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Nextcloud Talk for the chat platform
- x.ai for AI capabilities
- Ollama for local LLM hosting
- ChromaDB for vector storage
