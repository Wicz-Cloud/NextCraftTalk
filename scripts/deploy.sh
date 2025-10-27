#!/bin/bash
# NextCraftTalk Unified Deployment Script
# Supports both self-hosted and external AI modes

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

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

# Get deployment mode from .env
get_deployment_mode() {
    if [ -f ".env" ]; then
        MODE=$(grep "^DEPLOYMENT_MODE=" .env | cut -d'=' -f2 | tr -d ' ')
        echo -e "${BLUE}[INFO]${NC} Found .env, MODE: '$MODE'" >&2
        echo "$MODE"
    else
        echo -e "${YELLOW}[WARNING]${NC} .env file not found, defaulting to external_ai" >&2
        echo "external_ai"
    fi
}

# Install Python dependencies
install_dependencies() {
    MODE=$(get_deployment_mode)
    log_info "Installing Python dependencies for $MODE mode..."

    if [ "$MODE" = "external_ai" ]; then
        pip install -r requirements-external.txt
    elif [ "$MODE" = "self_hosted" ]; then
        pip install -r requirements-selfhosted.txt
    else
        log_error "Unknown deployment mode: $MODE"
        exit 1
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

# Configure Docker network in compose file
configure_docker_network() {
    MODE=$(get_deployment_mode)
    COMPOSE_FILE="docker/${MODE}/docker-compose.yml"

    if [ ! -f "$COMPOSE_FILE" ]; then
        return
    fi

    # Get network name from .env
    NETWORK_NAME=$(grep "^DOCKER_NETWORK=" .env | cut -d'=' -f2 | tr -d ' ')

    if [ -z "$NETWORK_NAME" ]; then
        log_warning "DOCKER_NETWORK not set in .env, using default 'nextcraft'"
        NETWORK_NAME="nextcraft"
    fi

    log_info "Configuring Docker network: $NETWORK_NAME"

    # Update the networks section in docker-compose.yml
    # Replace the network name in the networks section
    sed -i "s/nextcraft:/${NETWORK_NAME}:/g" "$COMPOSE_FILE"

    # Update the service network reference
    sed -i "s/- nextcraft/- ${NETWORK_NAME}/g" "$COMPOSE_FILE"
}

# Check Nextcloud connectivity and provide bot setup instructions
check_nextcloud_setup() {
    NETWORK_NAME=$(grep "^DOCKER_NETWORK=" .env | cut -d'=' -f2 | tr -d ' ' || echo "nextcloud-aio")

    log_info "Checking Nextcloud connectivity on network: $NETWORK_NAME"

    # Check if Nextcloud containers are accessible
    if docker network ls | grep -q "$NETWORK_NAME"; then
        log_info "✓ Docker network '$NETWORK_NAME' exists"

        # Try to detect Nextcloud containers on the network
        NEXTCLOUD_CONTAINERS=$(docker ps --filter "network=$NETWORK_NAME" --format "{{.Names}}" | grep -E "(nextcloud|apache)" | head -1)

        if [ -n "$NEXTCLOUD_CONTAINERS" ]; then
            log_success "✓ Found Nextcloud container(s) on network: $NEXTCLOUD_CONTAINERS"
            log_info ""
            log_info "🤖 Nextcloud Talk Bot Setup:"
            log_info "=========================="

            # Check if MinecraftBot is already installed
            BOT_EXISTS=$(docker exec nextcloud-aio-nextcloud php occ talk:bot:list --output=json 2>/dev/null | jq -r '.[] | select(.name=="MinecraftBot") | .id' 2>/dev/null || echo "")

            if [ -n "$BOT_EXISTS" ]; then
                log_info "✓ MinecraftBot found (ID: $BOT_EXISTS)"
                log_warning "⚠️  Bot may need webhook URL reconfiguration"
                log_info ""
                log_info "To update the webhook URL, run these commands:"
                log_info "docker exec nextcloud-aio-nextcloud php occ talk:bot:uninstall $BOT_EXISTS"
                log_info "docker exec nextcloud-aio-nextcloud php occ talk:bot:install MinecraftBot '' 'http://external_ai_nextcraft-external_1:8080/webhook' 'Minecraft knowledge bot for kids'"
            else
                log_info "❌ MinecraftBot not found"
                log_info ""
                log_info "To install the bot, run this command:"
                log_info "docker exec nextcloud-aio-nextcloud php occ talk:bot:install MinecraftBot '' 'http://external_ai_nextcraft-external_1:8080/webhook' 'Minecraft knowledge bot for kids'"
            fi

            log_info ""
            log_info "After configuring the bot:"
            log_info "1. Add the bot to conversations: docker exec nextcloud-aio-nextcloud php occ talk:bot:setup $BOT_EXISTS <conversation-token>"
            log_info "2. Test by mentioning @MinecraftBot in a Talk conversation"
            log_info ""
            log_warning "⚠️  Bot webhook URL must be accessible from Nextcloud container!"
        else
            log_warning "⚠️  No Nextcloud containers found on network '$NETWORK_NAME'"
            log_info "Make sure Nextcloud AIO is running and connected to the same network"
        fi
    else
        log_warning "⚠️  Docker network '$NETWORK_NAME' not found"
        log_info "The bot may not be able to communicate with Nextcloud"
    fi
}

# Deploy using Docker
deploy_docker() {
    MODE=$(get_deployment_mode)
    COMPOSE_FILE="docker/${MODE}/docker-compose.yml"

    log_info "Deployment mode: $MODE"
    log_info "Compose file: $COMPOSE_FILE"

    if [ -f "$COMPOSE_FILE" ]; then
        log_info "Configuring Docker network..."
        configure_docker_network

        log_info "Deploying with Docker Compose (${MODE} mode)..."
        docker-compose -f "$COMPOSE_FILE" up -d

        # Check Nextcloud setup after successful deployment
        check_nextcloud_setup
    else
        log_error "Docker Compose file not found: $COMPOSE_FILE"
        log_error "Cannot deploy without Docker Compose configuration."
        exit 1
    fi
}

# Deploy using Python directly
deploy_python() {
    MODE=$(get_deployment_mode)
    REQUIREMENTS_FILE="requirements-${MODE}.txt"

    log_info "Setting up Python virtual environment..."
    if [ ! -d "venv" ]; then
        python3 -m venv venv
    fi
    export PATH="$PWD/venv/bin:$PATH"

    log_info "Installing Python dependencies for ${MODE} mode..."
    if [ -f "$REQUIREMENTS_FILE" ]; then
        pip install -r "$REQUIREMENTS_FILE"
    else
        log_warning "Requirements file not found: $REQUIREMENTS_FILE"
        pip install -r requirements.txt
    fi

    log_info "Starting NextCraftTalk with Python..."
    python src/main.py
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
        if pgrep -f "python src/main.py" > /dev/null; then
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
