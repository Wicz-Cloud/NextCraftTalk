# Contributing to NextCraftTalk

Thank you for your interest in contributing to NextCraftTalk! We welcome contributions from everyone. This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Submitting Changes](#submitting-changes)
- [Reporting Issues](#reporting-issues)
- [Community](#community)

## Code of Conduct

This project adheres to the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to **conduct@wicz.cloud**.

## Getting Started

### Prerequisites

- Python 3.11+
- Docker & Docker Compose (for containerized deployment)
- Git
- Make (optional, for using the Makefile)

### Development Setup

1. **Fork and Clone the Repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/NextCraftTalk.git
   cd NextCraftTalk
   ```

2. **Set up Development Environment**
   ```bash
   # Install all dependencies (recommended)
   make install-all

   # Or install specific modes
   make install-external    # External AI mode only
   make install-selfhosted  # Self-hosted mode only
   make install-dev         # Development dependencies only
   ```

3. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Install Pre-commit Hooks**
   ```bash
   make pre-commit-install
   ```

## Development Workflow

### Branching Strategy

- `main`: Production-ready code
- `develop`: Integration branch for features
- Feature branches: `feature/description-of-feature`
- Bug fix branches: `fix/description-of-bug`
- Release branches: `release/v1.x.x`

### Development Process

1. **Choose an Issue**: Look for issues labeled `good first issue` or `help wanted`
2. **Create a Branch**: `git checkout -b feature/your-feature-name`
3. **Make Changes**: Follow the coding standards below
4. **Run Tests**: Ensure all tests pass
5. **Update Documentation**: If needed
6. **Commit Changes**: Use clear, descriptive commit messages
7. **Create Pull Request**: Follow the PR template

### Commit Message Guidelines

Follow conventional commit format:
```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New features
- `fix`: Bug fixes
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat: add support for xAI Grok API
fix: resolve HTTP timeout issues in Ollama client
docs: update installation instructions
```

## Coding Standards

### Python Code Style

We use several tools to maintain code quality:

- **Black**: Code formatting (line length: 88 characters)
- **isort**: Import sorting
- **flake8**: Linting and style checking
- **mypy**: Static type checking
- **bandit**: Security linting

### Code Quality Checks

Run all quality checks with:
```bash
make check
```

Or run individual tools:
```bash
make lint          # Run linting tools
make format        # Format code with black and isort
make test          # Run tests
```

### Python Best Practices

- Use type hints for all function parameters and return values
- Write docstrings for all public functions, classes, and modules
- Follow PEP 8 style guidelines (enforced by Black and flake8)
- Use descriptive variable and function names
- Keep functions small and focused on a single responsibility
- Write unit tests for new functionality

### Security Considerations

- Never commit sensitive information (API keys, passwords, etc.)
- Use secure coding practices
- Run security scans before submitting PRs
- Report security vulnerabilities through our [Security Policy](SECURITY.md)

## Testing

### Test Structure

- Unit tests: `tests/unit/`
- Integration tests: `tests/integration/`
- End-to-end tests: `tests/e2e/`

### Running Tests

```bash
# Run all tests
make test

# Run tests with coverage
make test-cov

# Run specific test file
pytest tests/unit/test_specific.py

# Run tests in verbose mode
pytest -v
```

### Writing Tests

- Use `pytest` as the testing framework
- Place test files in appropriate directories
- Use descriptive test names: `test_should_do_something_when_condition`
- Include docstrings for complex test scenarios
- Aim for high test coverage (>80%)

### Test Coverage

We use coverage.py to measure test coverage. Ensure your changes maintain or improve coverage.

## Documentation

### Documentation Types

- **README.md**: Project overview and quick start
- **Wiki**: Comprehensive guides and documentation
- **Docstrings**: Inline code documentation
- **CHANGELOG.md**: Version history and release notes

### Documentation Standards

- Use clear, concise language
- Include code examples where helpful
- Keep documentation up-to-date with code changes
- Use proper Markdown formatting

### Updating Documentation

When making changes that affect users or developers:
1. Update relevant documentation
2. Test documentation examples
3. Update CHANGELOG.md for user-facing changes

## Submitting Changes

### Pull Request Process

1. **Ensure your branch is up-to-date**:
   ```bash
   git fetch origin
   git rebase origin/main
   ```

2. **Run quality checks**:
   ```bash
   make check
   make test
   ```

3. **Create a Pull Request**:
   - Use the PR template
   - Provide a clear description of changes
   - Reference related issues
   - Request review from maintainers

4. **Address Review Feedback**:
   - Be responsive to reviewer comments
   - Make requested changes
   - Update PR description if needed

### Pull Request Requirements

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] Documentation updated (if needed)
- [ ] Commit messages follow conventional format
- [ ] Security scans pass
- [ ] No breaking changes without discussion

## Reporting Issues

### Bug Reports

When reporting bugs, please include:

- **Clear title**: Describe the issue concisely
- **Steps to reproduce**: Detailed steps to reproduce the issue
- **Expected behavior**: What should happen
- **Actual behavior**: What actually happens
- **Environment**: Python version, OS, deployment mode
- **Logs**: Relevant error messages or logs
- **Screenshots**: If applicable

### Feature Requests

For feature requests, please include:

- **Clear description**: What feature you want
- **Use case**: Why you need this feature
- **Proposed solution**: How you think it should work
- **Alternatives**: Other solutions you've considered

### Issue Labels

We use labels to categorize issues:
- `bug`: Something isn't working
- `enhancement`: New feature or improvement
- `documentation`: Documentation issues
- `good first issue`: Suitable for newcomers
- `help wanted`: Community contribution needed
- `question`: Questions or discussions

## Community

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General discussions and questions
- **Discord**: Real-time chat and community support

### Getting Help

- Check existing issues and documentation first
- Use clear, descriptive titles for issues
- Be patient and respectful when asking questions
- Help others when you can

### Recognition

Contributors are recognized in:
- CHANGELOG.md for significant contributions
- GitHub's contributor insights
- Release notes

## Additional Resources

- [NextCraftTalk Wiki](https://github.com/Wicz-Cloud/NextCraftTalk/wiki)
- [Makefile Commands & Scenarios](https://github.com/Wicz-Cloud/NextCraftTalk/wiki/Makefile-Commands-&-Scenarios)
- [Development Documentation](https://github.com/Wicz-Cloud/NextCraftTalk/wiki/Project-Documentation)
- [Semantic Versioning Guide](https://github.com/Wicz-Cloud/NextCraftTalk/wiki/Semantic-Versioning-Guide)

Thank you for contributing to NextCraftTalk! 🚀
