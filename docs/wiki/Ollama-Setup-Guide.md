# Ollama Setup Guide

## What is Ollama?

Ollama is a lightweight, extensible framework for building and running language models on the local machine. It provides a simple API for creating, running, and managing models, as well as a library of pre-built models.

## Installation

### macOS
```bash
# Download and install
curl -fsSL https://ollama.com/install.sh | sh
```

### Windows
Download the installer from [ollama.com/download/OllamaSetup.exe](https://ollama.com/download/OllamaSetup.exe)

### Linux
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### Docker
```bash
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

## Quick Start

### Run a Model
```bash
# Run Gemma 3 (recommended for NextCraftTalk)
ollama run gemma3

# Other popular models
ollama run llama3.2
ollama run mistral
```

### Pull a Model
```bash
ollama pull llama3.2
```

### List Models
```bash
ollama list
```

### Stop a Model
```bash
ollama stop llama3.2
```

## Model Library

Popular models for NextCraftTalk:
- **Gemma 3**: 1B, 4B, 12B, 27B parameters
- **Llama 3.2**: 1B, 3B parameters (good for resource-constrained systems)
- **Mistral**: 7B parameters
- **Phi 4**: 14B parameters

## REST API

Ollama provides a REST API on `http://localhost:11434`:

### Generate Response
```bash
curl http://localhost:11434/api/generate -d '{
  "model": "gemma3",
  "prompt": "Why is the sky blue?"
}'
```

### Chat Interface
```bash
curl http://localhost:11434/api/chat -d '{
  "model": "gemma3",
  "messages": [
    {"role": "user", "content": "Hello"}
  ]
}'
```

### List Running Models
```bash
curl http://localhost:11434/api/ps
```

## Configuration

### Environment Variables
```bash
export OLLAMA_HOST=0.0.0.0:11434  # Allow external connections
export OLLAMA_MODELS=/path/to/models  # Custom model directory
```

### System Requirements
- **RAM**: At least 8GB for 7B models, 16GB for 13B+, 32GB for 33B+
- **Storage**: 4-50GB depending on model size
- **GPU**: NVIDIA GPU recommended for better performance

## Integration with NextCraftTalk

For self-hosted mode, configure NextCraftTalk to use Ollama:

```env
DEPLOYMENT_MODE=self_hosted
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=gemma3
```

## Troubleshooting

### Common Issues
1. **Port already in use**: Change the port with `OLLAMA_HOST=0.0.0.0:8080`
2. **Model download fails**: Check internet connection and disk space
3. **GPU not detected**: Install NVIDIA drivers and CUDA
4. **Memory issues**: Use smaller models or increase RAM

### Performance Tuning
- Use GPU acceleration when available
- Adjust model parameters (temperature, context length)
- Use model quantization for better performance

For more information, visit [ollama.com](https://ollama.com/) or the [GitHub repository](https://github.com/ollama/ollama).
