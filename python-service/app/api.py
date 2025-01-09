import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx
import json
import asyncio
import pusher

from app.gemini import generate_text_with_gemini
from app.dapr_utils import save_state_to_dapr, get_state_from_dapr
from app.utils import decode_base64
from app.notification import send_notification
from app.config import GO_SERVICE_URL

logging.basicConfig(level=logging.INFO)

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dapr Subscriber for "files" topic
@app.get("/dapr/subscribe")
async def get_subscribe():
    """Endpoint to let Dapr know the topics the app is subscribed to."""
    subscriptions = [{
        "pubsubname": "files",
        "topic": "files",
        "route": "files"
    }]
    logging.info(f"Dapr pub/sub is subscribed to: {subscriptions}")
    return JSONResponse(content=subscriptions)


# Process for "files" topic
@app.post("/files")
async def handle_file_message(request: Request):
    """Endpoint to handle messages published to the 'files' topic."""
    try:
        # Retrieve the message sent by the publisher
        message = await request.json()
        logging.info(f"Received message: {message}")

        # Extract the data field, which contains the file information
        data = message.get("data", {})

        # Extract the file content (base64 encoded) and other info
        file_id = data.get("fileId")
        file_name = data.get("fileName")
        mime_type = data.get("mimeType")
        content = data.get("content")

        if content is None:
            raise ValueError("Content is missing or invalid in the message.")

        # If content is base64 encoded, decode it first
        decoded_content_str = decode_base64(content)
        logging.info(f"Received file: {file_name} with MIME type: {mime_type}")
        logging.info(f"File content decoded as: {decoded_content_str}")

         # Generate Synthesis using Gemini
        prompt = f"""
  Analyze the following Architecture Decision Record (ADR) from an Enterprise Architect perspective.

  **Consider:**
  * **Alignment with Enterprise Architecture principles and standards:** Does the decision align with overarching architectural goals, strategies, and best practices? Are there any potential conflicts or inconsistencies?
  * **Impact on other systems and domains:** How does this decision affect other systems, domains, and stakeholders within the enterprise? Are there any potential interoperability issues or dependencies?
  * **Long-term implications:** What are the potential long-term implications of this decision, including maintainability, scalability, security, and cost of ownership?
  * **Risk assessment:** What are the potential risks associated with this decision, and what mitigation strategies are in place?
  * **Decision rationale and justification:** Is the decision rationale clear, well-supported, and adequately justified? Are there any alternative solutions considered and why were they rejected?
  * **Communication and documentation:** Is the ADR well-written, easy to understand, and effectively communicated to relevant stakeholders?

  **Provide a concise and insightful analysis, highlighting any key strengths, weaknesses, opportunities, and threats (SWOT) related to the decision.**

  **ADR Content:**
  {decoded_content_str}
  """
        synthesis = generate_text_with_gemini(prompt)
        logging.info(f"Generated synthesis: {synthesis}")

        # Save the file to Cosmos DB via Dapr.
        file_data = {
            'content': decoded_content_str,  # original content
            'synthesis': synthesis
        }
        save_state_to_dapr(file_id, file_data)

        # Add a delay here
        await asyncio.sleep(2)  # Wait for 2 seconds

        # Call Go Service
        go_service_result = await call_go_service(file_id)
        logging.info(f"Go service result: {go_service_result}")

        send_notification(
            channel='unicorn-notification',
            event='publish',
            data={'message': 'File published successfully with synthesis'}
        )

        return {"message": "File processed successfully with synthesis and go service call",
                "go_service_result" : go_service_result}
    except Exception as e:
        logging.error(f"Error processing message: {e}")
        raise HTTPException(status_code=500, detail="Error processing message")

async def call_go_service(file_id: str) -> dict:
    """Calls the Go service to push the file to Github and returns the result."""
    try:
        async with httpx.AsyncClient() as client:
            payload = {
              "fileId": file_id,
              "message": "Add file via python service",
              }
            response = await client.post(GO_SERVICE_URL, json=payload)
            response.raise_for_status()  # Raise an exception for bad status codes
            
            if response.headers.get("Content-Type") == "application/json":
               return response.json()
            else:
               return {"result" : response.text}
    except httpx.HTTPError as e:
        logging.error(f"HTTP error calling Go service: {e}")
        raise HTTPException(status_code=500, detail=f"Error calling Go service: {e}")
    except Exception as e:
         logging.error(f"Error calling Go service: {e}")
         raise HTTPException(status_code=500, detail=f"Error calling Go service: {e}")