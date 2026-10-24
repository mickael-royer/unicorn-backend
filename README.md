# unicorn-backend
Backend based on [Dapr](https://dapr.io/) for [Unicorn](https://unicorn.royerm.fr) project (cf. [ADR 0017-distributed-application](https://hugo.royerm.fr/adr/0017-distributed-application/))
## Context
The Unicorn project is designed to streamline the documentation and sharing of architecture artifacts created on a Kindle Scribe. Its primary objective is to enable users to export diagrams and Architecture Decision Records (ADRs) from Kindle Scribe, convert them into Markdown format, and host them on a secure, static website for easy access and collaboration.

[![System Context diagram](context.png "System Context diagram")](https://s.icepanel.io/bLDUeKPM8K9wn6/VUxj)

Interactive C4 System Context diagram on [IcePanel](https://s.icepanel.io/bLDUeKPM8K9wn6/VUxj).

## System Software Overview
The Unicorn system follows a Frontend/Backend pattern. The C4 model is maintained in IcePanel (cf. [ADR 0030-use-icepanel-as-c4-architecture-referential](https://hugo.royerm.fr/adr/0030-use-icepanel-as-c4-architecture-referential/)).
- [Frontend](https://github.com/mickael-royer/unicorn-frontend/): Ionic + React SPA (cf. [ADR 0013-frontend-framework](https://hugo.royerm.fr/adr/0013-frontend-framework/)), hosted on Azure Static Web Apps, with Auth0 sign-in (cf. [ADR 0014-identity-and-access-management](https://hugo.royerm.fr/adr/0014-identity-and-access-management/)).
- [Backend](https://github.com/mickael-royer/unicorn-backend): distributed application on Dapr (cf. [ADR 0017-distributed-application](https://hugo.royerm.fr/adr/0017-distributed-application/)), made of three services:
  - `unicorn-bff` (Node.js / Express, cf. [ADR 0015-backend-framework](https://hugo.royerm.fr/adr/0015-backend-framework/)): backend for the frontend. It lists and downloads the Kindle Scribe exports from Google Drive and publishes a `files` event (cf. [ADR 0020-add-publish-and-subscribe-components](https://hugo.royerm.fr/adr/0020-add-publish-and-subscribe-components/)).
  - `unicorn-process` (Python / FastAPI, cf. [ADR 0019-fastapi-integration](https://hugo.royerm.fr/adr/0019-fastapi-integration/)): subscribes to `files` and synthesises each document with an LLM (cf. [ADR 0023-llm](https://hugo.royerm.fr/adr/0023-llm/)). It uses RAG based on LangChain (cf. [ADR 0025-langchain-integration](https://hugo.royerm.fr/adr/0025-langchain-integration/) and [ADR 0027-integrate-rag-to-llm-request](https://hugo.royerm.fr/adr/0027-integrate-rag-to-llm-request/)) over a Cosmos DB vector store of the C4 model, ingested from IcePanel (cf. [ADR 0026-use-a-vector-database-to-store-c4-diagrams-informations](https://hugo.royerm.fr/adr/0026-use-a-vector-database-to-store-c4-diagrams-informations/)). It stores the result in the `filestore` state store (cf. [ADR 0022-statestore](https://hugo.royerm.fr/adr/0022-statestore/)) and notifies the frontend through Pusher (cf. [ADR 0024-notification](https://hugo.royerm.fr/adr/0024-notification/)).
  - `unicorn-publish` (Go / Gorilla Mux, cf. [ADR 0021-publish-service](https://hugo.royerm.fr/adr/0021-publish-service/)): invoked by `unicorn-process`. It reads the result from `filestore` and pushes the Markdown to the [Hugo site](https://hugo.royerm.fr) repository on GitHub.

[![Container diagram](container.png "Container diagram")](https://s.icepanel.io/bLDUeKPM8K9wn6/85Ju)

Interactive C4 Container diagram on [IcePanel](https://s.icepanel.io/bLDUeKPM8K9wn6/85Ju).

## Build and Run
### Init dapr with Podman
```
dapr init --container-runtime podman
```
