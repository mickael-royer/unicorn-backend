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
- RAG ingestion (`python-service/app/kb.py`) reads the C4 model from the IcePanel API. `python-service/c4/` is the legacy Archi export and is no longer ingested.

## Gotchas learned in operation

**go-service / godotenv**: `godotenv.Load()` reads `.env` from cwd. `dapr.yaml` `appDirPath`
sets the correct cwd for multi-app run. If starting the service manually, invoke from `repos/unicorn-backend/go-service/`.

**Go Dockerfile base image**: Keep `FROM golang:X.Y-alpine` in sync with the `go X.Y.Z`
directive in `go.mod`. Go 1.16 cannot parse the three-part version format used since Go 1.21;
a mismatch silently breaks CI with an obscure `invalid go version` error.

**Gemini model names (as of 2026-10)**: chat → `gemini-3.8-flash`, embeddings → `models/gemini-embedding-001`.
`gemini-2.0-flash` and `models/embedding-001` are deprecated.

**langchain-google-genai >= 2.0 response format**: `response.content` is a list of typed
blocks `[{"type": "text", "text": "...", ...}]`, not a plain string. Extract with:
```python
if isinstance(content, list):
    content = "".join(b["text"] for b in content if isinstance(b, dict) and b.get("type") == "text")
```
