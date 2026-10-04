# unicorn-backend

Distributed backend on Dapr (ADR 0017). Services:
- `node-service/`   Express (ADR 0015)
- `python-service/` FastAPI, dependencies in Pipfile
- `go-service/`     Gorilla Mux
- `dapr-components/` Dapr component YAML; `deploy/` deployment/IaC; `.github/workflows/` CI

LLM + RAG with LangChain on a Cosmos DB vector store holding C4 info (ADR 0025-0027).

## Commands
- Init Dapr: `dapr init --container-runtime podman`
- Node type-check: `npx tsc --noEmit` (no test suite yet)
- Go: `go vet ./... && go test ./...`
- Python: `pipenv run pytest -q`
- Run all: `make up` from workspace root (uses `dapr.yaml` + `dapr-components-local/`)

| App ID | Port | Dapr HTTP | Dapr gRPC |
|---|---|---|---|
| unicorn-bff (node) | 3001 | 3500 | 50001 |
| unicorn-process (python) | 5001 | 3501 | 50002 |
| unicorn-publish (go) | 8050 | 3502 | 50003 |

## Rules
- Dapr component names must match between `dapr-components/` and Azure; only types/metadata differ.
- Keep pub/sub topics and payload shapes backward compatible; change them together across services.
- Follow-up: RAG ingestion of C4 info should read the IcePanel export once IcePanel replaces Archi.
