# Project Documentation

## Full Documentation Links

### NextCraftTalk Documentation
- [Main README](https://github.com/Wicz-Cloud/NextCraftTalk/blob/main/README.md) - Complete project overview
- [External AI README](https://github.com/Wicz-Cloud/NextCraftTalk/blob/main/docs/external_ai_readme.md) - Detailed external AI setup
- [API Documentation](https://github.com/Wicz-Cloud/NextCraftTalk/blob/main/docs/api.md) - API reference
- [Deployment Guide](https://github.com/Wicz-Cloud/NextCraftTalk/blob/main/docs/deployment.md) - Full deployment instructions
- [Migration Guide](https://github.com/Wicz-Cloud/NextCraftTalk/blob/main/docs/migration.md) - Migration between modes

### External Resources
- [Nextcloud Talk User Manual](https://docs.nextcloud.com/server/latest/user_manual/en/talk/index.html)
- [Ollama Documentation](https://github.com/ollama/ollama)
- [xAI API Documentation](https://docs.x.ai/)

## Architecture Documentation

### Core Components
- **Bot Logic**: Handles chat integration and response generation
- **Mode Management**: Switches between external AI and self-hosted modes
- **Configuration**: Environment-based settings management
- **Docker Integration**: Containerized deployment support

### Data Flow
1. Nextcloud Talk webhook receives message
2. Bot processes message and determines intent
3. AI model (xAI or Ollama) generates response
4. Response formatted and sent back to chat

## Development Resources

### Code Quality
- **Linting**: flake8 for Python code quality
- **Type Checking**: mypy for static type analysis
- **Testing**: pytest for unit and integration tests
- **Formatting**: black for code formatting

### CI/CD Pipeline
- **GitHub Actions**: Automated testing and deployment
- **Security Scanning**: TruffleHog for secrets detection
- **Dependency Review**: Automated dependency analysis
- **CodeQL**: Static analysis for security vulnerabilities

## Security Considerations

### API Security
- Secure API key storage and rotation
- HTTPS enforcement for all communications
- Input validation and sanitization
- Rate limiting and abuse prevention

### Data Privacy
- Minimal data collection and storage
- User message encryption in transit
- Compliance with privacy regulations
- Transparent data handling policies

## Troubleshooting Guide

### Common Issues
1. **Connection Problems**: Check network connectivity and API endpoints
2. **Authentication Errors**: Verify API keys and permissions
3. **Performance Issues**: Monitor resource usage and optimize configurations
4. **Integration Problems**: Validate webhook URLs and message formats

### Debug Mode
Enable debug logging for detailed troubleshooting:
```bash
export LOG_LEVEL=DEBUG
```

### Support Channels
- [GitHub Issues](https://github.com/Wicz-Cloud/NextCraftTalk/issues) - Bug reports and feature requests
- [Discord Community](https://discord.gg/D2vFfQW4Nm) - Real-time help and discussions
- [Security Issues](https://github.com/Wicz-Cloud/NextCraftTalk/security) - Security vulnerability reports

## Contributing Guidelines

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Set up development environment
4. Run tests and linting
5. Submit pull request

### Code Standards
- Follow PEP 8 style guidelines
- Write comprehensive tests
- Document new features
- Update changelog for changes

### Release Process
- Semantic versioning (MAJOR.MINOR.PATCH)
- Automated releases via GitHub Actions
- Changelog updates with each release
- Security updates prioritized

For more detailed information, explore the full documentation in the repository.
