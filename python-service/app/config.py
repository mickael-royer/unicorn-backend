import os
from dotenv import load_dotenv

load_dotenv()

# Gemini LLM Configuration
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
MODEL_NAME = "gemini-2.0-flash"  # Or "gemini-pro-vision"
GEMINI_EMBEDDING_MODEL = "models/embedding-001"

# Cosmos DB Configuration
COSMOS_ENDPOINT = os.getenv("COSMOS_ENDPOINT")
COSMOS_KEY = os.getenv("COSMOS_KEY")
DATABASE_NAME = "filesDB"
CONTAINER_NAME = "c4"

# Pusher Configuration
PUSHER_SECRET = os.environ.get("PUSHER_SECRET")

# Dapr Configuration
DAPR_STATE_STORE = "filestore"

# Go Service Configuration
GO_SERVICE_URL = "http://localhost:3500/v1.0/invoke/unicorn-publish/method/github/push-file"