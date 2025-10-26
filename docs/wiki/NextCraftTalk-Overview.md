# NextCraftTalk Overview

## What is NextCraftTalk?

🤖 **Unified AI Chatbot for Nextcloud Talk** - Supporting both self-hosted and external AI deployment modes.

NextCraftTalk is a Minecraft knowledge chatbot that integrates with Nextcloud Talk to provide AI-powered responses about Minecraft in a kid-friendly manner.

## Features

- **🤖 Direct x.ai Integration** - Uses x.ai's Grok model directly for all responses
- **🚫 No Local Storage** - No vector database or scraped data required
- **👶 Kid-Friendly** - Simple language and clear steps suitable for children
- **☁️ Cloud AI** - Leverages x.ai's powerful language model
- **💬 Nextcloud Talk Integration** - Responds naturally in chat conversations
- **⚡ Fast Setup** - One-command deployment with Docker
- **🎭 Dynamic Prompts** - Edit bot personality without container restarts
- **👀 Auto-Reload** - Prompt changes detected automatically via file watching
- **🔊 Configurable Logging** - Control verbosity levels for monitoring

## Deployment Modes

### External AI Mode
- Uses x.ai for AI responses (lightweight, cloud-based)
- No local AI infrastructure required
- Perfect for cloud deployments

### Self-Hosted Mode
- Full local AI stack with Ollama, ChromaDB, and RAG pipeline
- Vector database (ChromaDB) for knowledge base
- Web scraping capabilities
- RAG pipeline for enhanced responses

## Quick Start

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

## Architecture

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

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## License

This project is licensed under the MIT License.
