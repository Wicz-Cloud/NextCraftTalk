# Makefile Commands & Scenarios

This guide explains the Makefile commands available in NextCraftTalk and provides scenarios for when to use each command versus the deployment script.

## 📋 Available Make Commands

### Installation Commands
```bash
make install          # Install production dependencies
make install-dev      # Install development dependencies
make install-external # Install external AI mode dependencies
make install-selfhosted # Install self-hosted mode dependencies
make install-all      # Install all dependencies (dev + all modes)
```

### Testing Commands
```bash
make test        # Run all tests
make test-cov    # Run tests with coverage report
make test-fast   # Run tests without coverage (faster)
```

### Code Quality Commands
```bash
make lint     # Run all linting tools (flake8, mypy, bandit)
make format   # Format code with black and isort
make check    # Run all quality checks (lint + format check) - ignores line length limits
```

### Development Server Commands
```bash
make serve              # Start development server (auto-reload)
make serve-external     # Start development server in external AI mode
make serve-selfhosted   # Start development server in self-hosted mode
make stop               # Stop development server
```

### Docker Commands
```bash
make docker-build-external   # Build external AI Docker image
make docker-build-selfhosted # Build self-hosted Docker image
make docker-run-external     # Run external AI containers
make docker-run-selfhosted   # Run self-hosted containers
make docker-stop-external    # Stop external AI containers
make docker-stop-selfhosted  # Stop self-hosted containers
```

### Deployment Commands
```bash
make deploy-external    # Deploy external AI mode
make deploy-selfhosted  # Deploy self-hosted mode
```

### Pre-commit Commands
```bash
make pre-commit-install  # Install pre-commit hooks
make pre-commit-run      # Run pre-commit on all files
```

## 🎯 Makefile vs deploy.sh

### When to Use Makefile
Use `make` commands for:
- **Development workflow** - Quick testing, linting, formatting
- **Local development** - Starting/stopping dev servers
- **Code quality checks** - Automated quality assurance
- **Simple Docker operations** - Building and running containers
- **Dependency management** - Installing packages for different modes

### When to Use deploy.sh
Use `./scripts/deploy.sh` for:
- **Production deployment** - Full deployment with environment validation
- **Network configuration** - Docker network setup and Nextcloud connectivity
- **Bot setup assistance** - Automated Nextcloud Talk bot configuration
- **Advanced deployment options** - Status checking, restart, direct Python mode
- **Comprehensive setup** - Directory creation, dependency installation, validation

## 📚 Common Scenarios

### Scenario 1: First-Time Setup (Development)
```bash
# Clone and setup
git clone https://github.com/Wicz-Cloud/NextCraftTalk.git
cd NextCraftTalk
cp .env.example .env

# Install all dependencies (includes pre-commit setup)
make install-all

# Run tests to verify setup
make test

# Start development server
make serve-external  # or make serve-selfhosted
```

### Scenario 2: Code Development Workflow
```bash
# Make code changes...

# Format and check code quality
make format
make check

# Run tests
make test

# Start dev server to test changes
make serve-external
```

### Scenario 3: Docker Development
```bash
# Build and run containers
make docker-build-external
make docker-run-external

# Test the running containers
curl http://localhost:8080/health

# Stop when done
make docker-stop-external
```

### Scenario 4: Production Deployment
```bash
# For production deployment, use deploy.sh
./scripts/deploy.sh start

# Or use the Makefile shortcut
make deploy-external  # or make deploy-selfhosted
```

### Scenario 5: CI/CD Pipeline
```bash
# Install dependencies
make install-all

# Run quality checks
make check

# Run tests with coverage
make test-cov

# Build Docker images
make docker-build-external
make docker-build-selfhosted
```

### Scenario 6: Pre-commit Setup and Usage
```bash
# Pre-commit hooks are automatically installed with make install-all

# Run pre-commit manually on all files (optional)
make pre-commit-run

# Or let pre-commit run automatically on git commits
git add .
git commit -m "Your commit message"
# Pre-commit hooks will run automatically
```

### Scenario 6: Maintenance & Cleanup
```bash
# Update dependencies
make deps-update

# Clean temporary files
make clean

# Full cleanup (including virtual env)
make clean-all
```

## 🔧 Command Categories

### 🚀 Development Workflow
- `make install-all` - Get started quickly
- `make test` - Verify code works
- `make check` - Ensure code quality
- `make serve-*` - Test locally

### 🐳 Docker Operations
- `make docker-build-*` - Create container images
- `make docker-run-*` - Start containers
- `make docker-stop-*` - Stop containers

### 🚢 Deployment
- `make deploy-*` - Quick deployment (calls deploy.sh)
- `./scripts/deploy.sh start` - Full production deployment

### 🧹 Maintenance
- `make clean` - Remove temporary files
- `make deps-update` - Update packages
- `make env-check` - Verify configuration
- `make pre-commit-install` - Setup git hooks
- `make pre-commit-run` - Manual pre-commit check

## 💡 Pro Tips

1. **Use `make help`** to see all available commands with descriptions
2. **Combine commands**: `make format && make test` for quick checks
3. **Use shortcuts**: `make deploy-external` instead of remembering deploy.sh syntax
4. **Development mode**: Use `make serve-*` for auto-reloading during development
5. **Production**: Always use `deploy.sh` or `make deploy-*` for production deployments
6. **Clean regularly**: Run `make clean` to keep your workspace tidy
7. **Line length**: `make check` ignores line length limits (E501) for readability
8. **Pre-commit**: Automatically installed with `make install-all`, runs on every commit

## ⚠️ Current Status

### ✅ Working Features
- All tests pass (22/23, 1 skipped due to dynamic import mocking)
- Full development workflow with Makefile
- Docker containerization for both modes
- Comprehensive deployment with deploy.sh

### 🔧 Known Issues
The `make check` command currently ignores line length limits but catches other code quality issues:
- **Unused global variables** (F824): `global xai_pipeline` declarations
- **Whitespace issues** (E203): Spaces before colons in type hints
- **Unused imports** (F401): Some test imports not currently used

These are minor issues that don't affect functionality but could be addressed in future cleanup.
