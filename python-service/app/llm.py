import logging
from azure.cosmos import CosmosClient
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.prompts import PromptTemplate
from .config import GEMINI_API_KEY, MODEL_NAME, GEMINI_EMBEDDING_MODEL, COSMOS_ENDPOINT, COSMOS_KEY, DATABASE_NAME, CONTAINER_NAME

# Configure logging (if not already done elsewhere)
logging.basicConfig(level=logging.ERROR)  # Or your desired level

embeddings = GoogleGenerativeAIEmbeddings(model=GEMINI_EMBEDDING_MODEL, google_api_key=GEMINI_API_KEY)
print(f"Cosmos DB Endpoint: {COSMOS_ENDPOINT}")
cosmos_client = CosmosClient(url="https://account-cosmodb-westeurope.documents.azure.com:443/", credential=COSMOS_KEY)
database = cosmos_client.get_database_client(DATABASE_NAME)
container = database.get_container_client(CONTAINER_NAME)


def generate_text_with_gemini(prompt: str) -> str:
    """Generates text using Langchain with Gemini and RAG."""
    try:
        # 1. Generate query embedding
        query_vector = embeddings.embed_query(prompt)

        # 2. Query Cosmos DB via Dapr
        results = container.query_items(
                query="SELECT TOP 3 * FROM c ORDER BY VectorDistance(c.vector, @queryVector)",
                parameters=[{"name": "@queryVector", "value": query_vector}],
                enable_cross_partition_query=True
            )
        cosmos_results = list(results)

        # 3. Construct context-augmented prompt
        context = " ".join([item["content"] for item in cosmos_results[:3]]) #Get top 3 results.
        augmented_prompt = f"Context: {context}\nQuestion: {prompt}\nAnswer:"

        # 4. Invoke Gemini LLM
        llm = ChatGoogleGenerativeAI(model=MODEL_NAME, google_api_key=GEMINI_API_KEY)
        prompt_template = PromptTemplate(input_variables=["prompt"], template="{prompt}")
        final_prompt = prompt_template.format(prompt=augmented_prompt)
        response = llm.invoke(final_prompt)

        if response and response.content:  # Check if response and content are not empty
            return response.content
        else:
            logging.error("Gemini Response was empty.")
            return "Gemini Response was empty."  # More informative than just "failed"

    except Exception as e:
        logging.error(f"Gemini API call error: {e}")
        return f"Error generating text: {e}"