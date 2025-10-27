# Nextcloud Talk Configuration

## Overview

Nextcloud Talk offers audio/video and text chat integrated in Nextcloud. It provides a web interface as well as mobile apps.

You can find out more about Nextcloud Talk [on their website](https://nextcloud.com/talk/).

## Basic Setup

### Prerequisites
- Nextcloud instance (version 20+ recommended)
- Talk app installed and enabled

### Installation
1. Log in to your Nextcloud instance as an administrator
2. Go to **Apps** > **Talk**
3. Click **Download and enable**

### Configuration

#### Server Settings
- **STUN servers**: Configure STUN servers for NAT traversal
- **TURN servers**: Set up TURN servers for reliable connectivity
- **Signaling servers**: Configure high-performance backend for large installations

#### User Settings
- **Notifications**: Configure push notifications
- **Privacy**: Set conversation retention and guest access
- **Moderation**: Enable conversation moderation tools

### API Integration

Nextcloud Talk provides a REST API for integration:

```bash
# Get conversation list
GET /ocs/v2.php/apps/spreed/api/v4/room

# Send message
POST /ocs/v2.php/apps/spreed/api/v1/chat/{token}

# Webhook integration
POST /ocs/v2.php/apps/spreed/api/v1/webhook/{token}
```

### Security Considerations
- Use HTTPS for all connections
- Configure proper CORS settings
- Set up proper authentication tokens
- Enable conversation encryption

### Troubleshooting
- Check server logs for Talk-related errors
- Verify WebRTC connectivity
- Ensure proper firewall settings for STUN/TURN ports
- Update Nextcloud and Talk to latest versions

## Adding Bots to Nextcloud Talk

Nextcloud Talk supports chatbots that can respond to messages, receive webhooks, and interact with conversations. Bots can only be added via OCC (OwnCloud Console) commands - they cannot be configured through the web interface.

### OCC Command Taxonomy

The basic structure for Talk OCC commands is:
```bash
occ talk:<category>:<action> [options] [arguments]
```

Common categories for bots:
- `bot` - Bot management (create, install, setup, remove, uninstall, list, state)
- `room` - Room management (create, add, remove, promote, demote, update, delete)

### Bot Setup Process

1. **Create or Install the Bot** - Register the bot with Nextcloud
2. **Setup in Conversation** - Add the bot to specific chat rooms
3. **Configure Features** - Enable webhook, response, event, or reaction features

### Differences Between NCAIO and Bare Metal

#### Bare Metal Installation
Run OCC commands directly on the server where Nextcloud is installed:

```bash
# Switch to web user (typically www-data or apache)
sudo -u www-data php /path/to/nextcloud/occ talk:bot:create "MinecraftBot" --secret "your-secret-here"
```

Common paths:
- Ubuntu/Debian: `/var/www/nextcloud/occ`
- CentOS/RHEL: `/var/www/html/nextcloud/occ`
- Docker (non-AIO): `docker exec -it nextcloud php occ`

#### Nextcloud All-In-One (NCAIO)
Access the Nextcloud container to run OCC commands:

```bash
# Access the Nextcloud container
docker exec -it nextcloud-aio-nextcloud bash

# Run OCC commands from within the container
occ talk:bot:create "MinecraftBot" --secret "your-secret-here"
```

Or run directly:
```bash
docker exec -it nextcloud-aio-nextcloud occ talk:bot:create "MinecraftBot" --secret "your-secret-here"
```

### Common Bot Commands

#### Create a Bot
```bash
# Bare metal
sudo -u www-data php occ talk:bot:create "BotName" --secret "your-64-char-secret"

# NCAIO
docker exec -it nextcloud-aio-nextcloud occ talk:bot:create "BotName" --secret "your-64-char-secret"
```

#### Install a Bot (Advanced)
```bash
# Bare metal
sudo -u www-data php occ talk:bot:install "BotName" "secret" "https://your-bot-endpoint.com/webhook" --feature response

# NCAIO
docker exec -it nextcloud-aio-nextcloud occ talk:bot:install "BotName" "secret" "https://your-bot-endpoint.com/webhook" --feature response
```

#### Add Bot to Conversation
```bash
# First get conversation token from Nextcloud Talk room URL
# Then add bot to room
sudo -u www-data php occ talk:bot:setup <bot-id> <room-token>
# NCAIO: docker exec -it nextcloud-aio-nextcloud occ talk:bot:setup <bot-id> <room-token>
```

#### List Bots
```bash
# Bare metal
sudo -u www-data php occ talk:bot:list

# NCAIO
docker exec -it nextcloud-aio-nextcloud occ talk:bot:list
```

#### Remove Bot from Conversation
```bash
# Bare metal
sudo -u www-data php occ talk:bot:remove <bot-id> <room-token>

# NCAIO
docker exec -it nextcloud-aio-nextcloud occ talk:bot:remove <bot-id> <room-token>
```

### Bot Features

- **response**: Bot can post messages and reactions as responses
- **webhook**: Bot receives posted chat messages as webhooks
- **event**: Bot reads posted messages from local events
- **reaction**: Bot is notified about adding/removing reactions

### Finding Conversation Tokens

Conversation tokens are found in the Nextcloud Talk room URL:
- URL format: `https://your-nextcloud.com/call/<token>`
- The `<token>` part is what you use in OCC commands

### Troubleshooting Bot Setup

1. **Permission Denied**: Ensure you're running as the correct user (www-data) or in the correct container
2. **Bot Not Appearing**: Check that the bot was created successfully with `talk:bot:list`
3. **Webhook Not Working**: Verify the bot endpoint URL is accessible and returns proper responses
4. **Secret Issues**: Ensure the secret matches between bot creation and webhook validation

For detailed bot API documentation, refer to the [Nextcloud Talk Bot API](https://nextcloud-talk.readthedocs.io/en/latest/bot-api/).

For detailed configuration options, refer to the [Nextcloud Talk documentation](https://docs.nextcloud.com/server/latest/user_manual/en/talk/index.html).
