import requests

# Ollama endpoints
OLLAMA_CHAT = "http://localhost:11434/api/chat"
OLLAMA_EMB = "http://localhost:11434/api/embeddings"

def ollama_chat(model: str, messages: list):
    """Send a chat request to Ollama."""
    payload = {
        "model": model,
        "messages": messages,
        "stream": False
    }
    response = requests.post(OLLAMA_CHAT, json=payload)
    response.raise_for_status()
    return response.json()["message"]["content"]

def ollama_embed(model: str, text: str):
    """Generate embeddings using Ollama."""
    payload = {"model": model, "prompt": text}
    response = requests.post(OLLAMA_EMB, json=payload)
    response.raise_for_status()
    return response.json()["embedding"]