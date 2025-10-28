# xAI API Usage

## Overview

The xAI API provides access to Grok, xAI's flagship AI model designed to deliver truthful, insightful answers. The API makes it easy to harness Grok's intelligence in your projects.

## Getting Started

### Prerequisites
- xAI API key (get one at [x.ai](https://x.ai))
- HTTP client (curl, requests, etc.)

### API Key Setup
1. Visit [x.ai](https://x.ai) and sign up for an account
2. Generate an API key from your dashboard
3. Store the key securely (never commit to version control)

## Basic Usage

### Authentication
Include your API key in the `Authorization` header:
```
Authorization: Bearer YOUR_API_KEY
```

### Chat Completion
```bash
curl https://api.x.ai/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "model": "grok-2-1212",
    "messages": [
      {
        "role": "user",
        "content": "Explain quantum computing in simple terms"
      }
    ]
  }'
```

### Response Format
```json
{
  "id": "chatcmpl-123",
  "object": "chat.completion",
  "created": 1677652288,
  "model": "grok-2-1212",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Quantum computing uses quantum mechanics..."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 13,
    "completion_tokens": 7,
    "total_tokens": 20
  }
}
```

## Integration with NextCraftTalk

For external AI mode, configure NextCraftTalk to use xAI:

```env
DEPLOYMENT_MODE=external_ai
XAI_API_KEY=your_xai_api_key_here
```

### API Parameters
- **model**: Use "grok-2-1212" for latest Grok model
- **messages**: Array of message objects with `role` and `content`
- **temperature**: Controls randomness (0.0 to 2.0)
- **max_tokens**: Maximum response length
- **stream**: Enable streaming responses

## Advanced Features

### Tool Use (Function Calling)
Grok can perform actions and look up information:

```json
{
  "model": "grok-2-1212",
  "messages": [
    {
      "role": "user",
      "content": "What's the weather in San Francisco?"
    }
  ],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_weather",
        "description": "Get current weather for a location",
        "parameters": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "City name"
            }
          },
          "required": ["location"]
        }
      }
    }
  ]
}
```

### Image Understanding
Grok can analyze images and perform OCR:

```json
{
  "model": "grok-2-1212",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "What's in this image?"
        },
        {
          "type": "image_url",
          "image_url": {
            "url": "https://example.com/image.jpg"
          }
        }
      ]
    }
  ]
}
```

## Rate Limits and Pricing

- **Rate Limits**: Vary by account type
- **Pricing**: Pay-per-token model
- **Free Tier**: Limited requests for new accounts

## Error Handling

### Common HTTP Status Codes
- `200`: Success
- `400`: Bad Request (invalid parameters)
- `401`: Unauthorized (invalid API key)
- `429`: Rate Limited
- `500`: Internal Server Error

### Error Response Format
```json
{
  "error": {
    "message": "Invalid API key",
    "type": "authentication_error",
    "code": 401
  }
}
```

## Content Safety Integration

NextCraftTalk integrates content safety features with xAI API responses to ensure appropriate content for all users.

### Safety Features

- **Profanity Filtering**: Automatic detection and censoring using `profanity-check` library
- **Toxicity Detection**: Google Perspective API integration for comprehensive content analysis
- **Response Filtering**: Unsafe content is filtered before delivery to users
- **Fallback Responses**: Safe alternatives provided when content cannot be made appropriate

### Implementation

```python
# Example safety filter integration
from src.shared.safety_filter import apply_safety_filter

# After receiving xAI response
raw_response = xai_api_response["choices"][0]["message"]["content"]
safe_response, is_safe = apply_safety_filter(raw_response)

if not is_safe:
    # Use safe fallback response
    final_response = "Let's keep it fun and safe! Ask me about building cool Minecraft stuff!"
else:
    final_response = safe_response
```

### Configuration

Control safety features via environment variables:

```env
# Enable/disable safety filtering
ENABLE_SAFETY_FILTER=true

# Detection thresholds (0.0-1.0)
PROFANITY_THRESHOLD=0.6
TOXICITY_THRESHOLD=0.7

# Google Perspective API key for enhanced detection
PERSPECTIVE_API_KEY=your_api_key_here
```

## Best Practices

1. **Secure API Keys**: Never expose keys in client-side code
2. **Error Handling**: Implement proper error handling and retries
3. **Rate Limiting**: Monitor usage and implement backoff strategies
4. **Caching**: Cache responses when appropriate
5. **Prompt Engineering**: Craft clear, specific prompts for best results

## Support

- **Documentation**: [docs.x.ai](https://docs.x.ai/)
- **Support Email**: [support@x.ai](mailto:support@x.ai)
- **Community**: Join discussions on [Grok.com](https://grok.com/)

For NextCraftTalk integration examples, refer to the project's external AI mode documentation.
