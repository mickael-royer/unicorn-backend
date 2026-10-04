# unicorn-express-server
BFF for Unicorn App
## Build and Run
### Build Docker image with Podman
```
podman build --build-arg-file=.env -t unicorn-process . 
```
### Run image with Podman
```
podman run -p 3001:3001 unicorn-process
```
### Init dapr with Podman
```
dapr init --container-runtime podman
```
### Run dapr
```
dapr run --app-id unicorn-process \
  --app-port 5001 \
  --dapr-http-port 3501 \
  --dapr-grpc-port 50002 \
  --resources-path ../dapr-components \
  -- uvicorn app.api:app --host 0.0.0.0 --port 5001
```
### RAG Knowledge Base Ingestion
Ingests the C4 model from IcePanel (objects + connections) into the Cosmos DB vector store.
Needs `ICEPANEL_API_KEY` and `ICEPANEL_LANDSCAPE_ID` in `.env` (see `.env.example`).
Re-running updates existing entries in place.
```
pipenv run python -m app.kb
```

One-off: remove the legacy Archi entries (ingested before ADR 0030). Dry run first, then delete:
```
pipenv run python -m app.kb_cleanup
pipenv run python -m app.kb_cleanup --delete
```