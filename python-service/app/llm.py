import logging
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.prompts import PromptTemplate
from dapr.clients import DaprClient
import json
from .config import GEMINI_API_KEY, MODEL_NAME, GEMINI_EMBEDDING_MODEL, DAPR_RAG_STORE #add GEMINI_EMBEDDING_MODEL to config

# Configure logging (if not already done elsewhere)
logging.basicConfig(level=logging.ERROR)  # Or your desired level

dapr_client = DaprClient()
embeddings = GoogleGenerativeAIEmbeddings(model=GEMINI_EMBEDDING_MODEL, google_api_key=GEMINI_API_KEY)

def generate_text_with_gemini(prompt: str) -> str:
    """Generates text using Langchain with Gemini and RAG."""
    try:
        # 1. Generate query embedding
        query_vector = embeddings.embed_query(prompt)
        # 2. Query Cosmos DB via Dapr
        response = dapr_client.invoke_method(
            app_id=DAPR_RAG_STORE, #replace with your cosmosdb dapr app id
            method_name="queryItems",
            data={
                "query": "SELECT * FROM c ORDER BY ARRAY_DISTANCE(c.vector, @queryVector) ASC",
                "parameters": [{"name": "@queryVector", "value": query_vector}],
            },
        )
        cosmos_results = json.loads(response.data.decode("utf-8"))

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