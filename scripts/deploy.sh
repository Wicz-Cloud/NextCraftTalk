#!/bin/bash
# NextCraftTalk Unified Deployment Script
# Supports both self-hosted and external AI modes

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if .env file exists
check_env() {
    if [ ! -f ".env" ]; then
        log_error ".env file not found. Please copy .env.example to .env and configure it."
        exit 1
    fi
}

# Detect deployment mode from .env
get_deployment_mode() {
    if [ -f ".env" ]; then
        grep "^DEPLOYMENT_MODE=" .env | cut -d'=' -f2 | tr -d ' '
    else
        echo "external_ai"  # Default mode
    fi
}

# Install Python dependencies
install_dependencies() {
    log_info "Installing Python dependencies..."
    pip install -r requirements.txt

    MODE=$(get_deployment_mode)
    if [ "$MODE" = "external_ai" ]; then
        log_info "Installing external AI dependencies..."
        # Add external AI specific packages if needed
        # pip install openai
    elif [ "$MODE" = "self_hosted" ]; then
        log_info "Installing self-hosted dependencies..."
        # Add self-hosted specific packages
        # pip install chromadb ollama beautifulsoup4
    fi
}

# Setup directories
setup_directories() {
    log_info "Setting up directories..."
    mkdir -p logs data

    MODE=$(get_deployment_mode)
    if [ "$MODE" = "self_hosted" ]; then
        mkdir -p data/chroma_db
    fi
}

# Deploy using Docker
deploy_docker() {
    MODE=$(get_deployment_mode)
    COMPOSE_FILE="docker/${MODE}/docker-compose.yml"

    if [ -f "$COMPOSE_FILE" ]; then
        log_info "Deploying with Docker Compose (${MODE} mode)..."
        docker-compose -f "$COMPOSE_FILE" up -d
    else
        log_warning "Docker Compose file not found: $COMPOSE_FILE"
        log_info "Falling back to direct Python execution..."
        deploy_python
    fi
}

# Deploy using Python directly
deploy_python() {
    log_info "Starting NextCraftTalk with Python..."
    python main.py
}

# Stop deployment
stop_deployment() {
    MODE=$(get_deployment_mode)
    COMPOSE_FILE="docker/${MODE}/docker-compose.yml"

    if [ -f "$COMPOSE_FILE" ]; then
        log_info "Stopping Docker containers..."
        docker-compose -f "$COMPOSE_FILE" down
    else
        log_warning "No Docker Compose file found. Manual cleanup may be needed."
    fi
}

# Show status
show_status() {
    MODE=$(get_deployment_mode)
    log_info "Deployment Mode: $MODE"

    COMPOSE_FILE="docker/${MODE}/docker-compose.yml"
    if [ -f "$COMPOSE_FILE" ]; then
        log_info "Docker containers status:"
        docker-compose -f "$COMPOSE_FILE" ps
    else
        log_info "Running in direct Python mode"
        # Check if process is running
        if pgrep -f "python main.py" > /dev/null; then
            log_success "NextCraftTalk is running"
        else
            log_warning "NextCraftTalk is not running"
        fi
    fi
}

# Main deployment logic
main() {
    COMMAND=${1:-"start"}

    case $COMMAND in
        "start")
            check_env
            setup_directories
            install_dependencies
            deploy_docker
            ;;
        "stop")
            stop_deployment
            ;;
        "restart")
            stop_deployment
            sleep 2
            check_env
            setup_directories
            deploy_docker
            ;;
        "status")
            show_status
            ;;
        "python")
            check_env
            setup_directories
            install_dependencies
            deploy_python
            ;;
        *)
            echo "Usage: $0 {start|stop|restart|status|python}"
            echo "  start   - Start deployment (default)"
            echo "  stop    - Stop deployment"
            echo "  restart - Restart deployment"
            echo "  status  - Show deployment status"
            echo "  python  - Run directly with Python (no Docker)"
            exit 1
            ;;
    esac
}

main "$@"
