"""SDE Team Project - AI Engineering Team"""
import os
from dotenv import load_dotenv
from ollama import Client

# Load environment variables from .env file
load_dotenv()

client = None


def get_client():
    """Get or initialize the Ollama client."""
    global client
    if client is not None:
        return client
    newClient = Client(
        host="https://ollama.com",
        headers={'Authorization': 'Bearer ' + os.environ.get('OLLAMA_API_KEY')}
    )
    client = newClient
    return client


# Initialize client on module import
get_client()

__all__ = ["client", "get_client"]
