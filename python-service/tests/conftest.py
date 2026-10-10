"""Stub the clients app.llm builds at import time, so tests need no Azure/Gemini credentials."""

from unittest.mock import MagicMock, patch

_patches = [
    patch("azure.cosmos.CosmosClient", MagicMock()),
    patch("langchain_google_genai.GoogleGenerativeAIEmbeddings", MagicMock()),
    patch("langchain_google_genai.ChatGoogleGenerativeAI", MagicMock()),
]
for p in _patches:
    p.start()
