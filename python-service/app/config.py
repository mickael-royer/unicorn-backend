import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
MODEL_NAME = "gemini-pro"  # Or "gemini-pro-vision"
PUSHER_SECRET = os.environ.get("PUSHER_SECRET")
DAPR_STATE_STORE = "filestore"
GO_SERVICE_URL = "http://localhost:3500/v1.0/invoke/unicorn-publish/method/github/push-file"