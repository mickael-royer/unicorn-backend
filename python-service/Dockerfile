# Use an official Python runtime as a parent image
FROM python:3.10-slim

ARG GEMINI_API_KEY=${GEMINI_API_KEY}
ENV GEMINI_API_KEY=$GEMINI_API_KEY
ARG PUSHER_SECRET=${PUSHER_SECRET}
ENV PUSHER_SECRET=$PUSHER_SECRET
ARG COSMOS_KEY=${COSMOS_KEY}
ENV COSMOS_KEY=$COSMOS_KEY


# Set the working directory
WORKDIR /app

# Copy the application files
COPY . .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt 
    
# Expose the port FastAPI will run on
EXPOSE 5001

# Define the command to run the application
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "5001"]
