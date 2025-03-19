import os
import uuid
from azure.cosmos import CosmosClient
from langchain.text_splitter import MarkdownTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings #or AzureOpenAIEmbeddings
import google.generativeai as genai #for Gemini
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration (Read from environment variables)
cosmos_endpoint = os.getenv("COSMOS_ENDPOINT")
cosmos_key = os.getenv("COSMOS_KEY")
database_name = os.getenv("DATABASE_NAME")
container_name = os.getenv("CONTAINER_NAME")
markdown_directory = os.getenv("MARKDOWN_DIRECTORY")
gemini_api_key = os.getenv("GEMINI_API_KEY")
gemini_embedding_model = os.getenv("GEMINI_EMBEDDING_MODEL")

# Cosmos DB setup
cosmos_client = CosmosClient(url=cosmos_endpoint, credential=cosmos_key)
database = cosmos_client.get_database_client(database_name)
container = database.get_container_client(container_name)

# Embedding model setup
genai.configure(api_key=gemini_api_key) #or openAI config
embeddings = GoogleGenerativeAIEmbeddings(model=gemini_embedding_model, google_api_key=gemini_api_key) #or AzureOpenAIEmbeddings

# Text splitter setup
text_splitter = MarkdownTextSplitter(chunk_size=1000, chunk_overlap=200)

def process_markdown_file(file_path):
    """Processes a single Markdown file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            markdown_content = f.read()

        chunks = text_splitter.split_text(markdown_content)

        for chunk in chunks:
            vector = embeddings.embed_query(chunk)
            item = {
                "id": str(uuid.uuid4()),
                "content": chunk,
                "vector": vector,
                "metadata": {"source": os.path.basename(file_path)},
            }
            container.create_item(body=item)
        print(f"Processed: {file_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def ingest_markdown_files(directory):
    """Ingests all Markdown files from a directory."""
    for filename in os.listdir(directory):
        if filename.endswith(".md"):
            file_path = os.path.join(directory, filename)
            process_markdown_file(file_path)

if __name__ == "__main__":
    ingest_markdown_files(markdown_directory)
    print("Markdown ingestion complete.")