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

For detailed configuration options, refer to the [Nextcloud Talk documentation](https://docs.nextcloud.com/server/latest/user_manual/en/talk/index.html).
