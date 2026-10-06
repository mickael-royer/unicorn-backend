import os
import httpx
from azure.cosmos import CosmosClient
from langchain_text_splitters import MarkdownTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings #or AzureOpenAIEmbeddings
from dotenv import load_dotenv
from .config import GEMINI_EMBEDDING_MODEL

# Load environment variables from .env file
load_dotenv()

# Configuration (Read from environment variables)
cosmos_endpoint = os.getenv("COSMOS_ENDPOINT")
cosmos_key = os.getenv("COSMOS_KEY")
database_name = os.getenv("DATABASE_NAME")
container_name = os.getenv("CONTAINER_NAME")
gemini_api_key = os.getenv("GEMINI_API_KEY")
icepanel_api_key = os.getenv("ICEPANEL_API_KEY")
icepanel_landscape_id = os.getenv("ICEPANEL_LANDSCAPE_ID")
icepanel_version_id = os.getenv("ICEPANEL_VERSION_ID", "latest")

ICEPANEL_API_URL = "https://api.icepanel.io/v1"

# Text splitter setup
text_splitter = MarkdownTextSplitter(chunk_size=1000, chunk_overlap=200)


def fetch_icepanel(resource, key):
    """Fetches every page of a model resource (objects or connections) from the IcePanel API."""
    url = f"{ICEPANEL_API_URL}/landscapes/{icepanel_landscape_id}/versions/{icepanel_version_id}/model/{resource}"
    headers = {"X-API-Key": icepanel_api_key}
    params = {"expand": "technologies"}
    items = []
    while True:
        response = httpx.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        body = response.json()
        items.extend(body.get(key, []))
        if not body.get("nextCursor"):
            return items
        params["cursor"] = body["nextCursor"]


def _technology_names(entity):
    return [t.get("name") for t in (entity.get("technologies") or {}).values() if t.get("name")]


def _connection_line(connection, other, arrow):
    line = f"- {arrow} **{other}**: {connection.get('name', '')}"
    technologies = _technology_names(connection)
    if technologies:
        line += f" ({', '.join(technologies)})"
    if connection.get("description"):
        line += f" — {connection['description']}"
    return line


def render_model_object(obj, objects_by_id, connections):
    """Renders one IcePanel model object and its connections as a Markdown document."""
    lines = [f"# {obj['name']} ({obj['type']})", ""]
    parent = objects_by_id.get(obj.get("parentId"))
    if parent and parent["type"] != "root":
        lines.append(f"- Part of: {parent['name']} ({parent['type']})")
    if obj.get("caption"):
        lines.append(f"- Caption: {obj['caption']}")
    lines.append(f"- External: {'yes' if obj.get('external') else 'no'}")
    lines.append(f"- Status: {obj.get('status', 'live')}")
    technologies = _technology_names(obj)
    if technologies:
        lines.append(f"- Technologies: {', '.join(technologies)}")
    children = [o["name"] for o in objects_by_id.values() if o.get("parentId") == obj["id"]]
    if children:
        lines.append(f"- Contains: {', '.join(sorted(children))}")
    if obj.get("description"):
        lines += ["", obj["description"]]

    name_of = lambda object_id: objects_by_id.get(object_id, {}).get("name", object_id)
    outgoing = [_connection_line(c, name_of(c["targetId"]), "→") for c in connections if c["originId"] == obj["id"]]
    incoming = [_connection_line(c, name_of(c["originId"]), "←") for c in connections if c["targetId"] == obj["id"]]
    if outgoing or incoming:
        lines += ["", "## Connections", *outgoing, *incoming]
    return "\n".join(lines) + "\n"


def build_documents(objects, connections):
    """Returns (source, markdown) pairs for every live model object, skipping the landscape root."""
    objects = [o for o in objects if o.get("status") != "removed"]
    connections = [c for c in connections if c.get("status") != "removed"]
    objects_by_id = {o["id"]: o for o in objects}
    return [
        (f"icepanel-{o['id']}", render_model_object(o, objects_by_id, connections))
        for o in objects
        if o["type"] != "root"
    ]


def process_document(container, embeddings, source, markdown_content):
    """Chunks, embeds and upserts one document. Ids are deterministic so re-ingestion updates in place."""
    chunks = text_splitter.split_text(markdown_content)
    for index, chunk in enumerate(chunks):
        vector = embeddings.embed_query(chunk)
        item = {
            "id": f"{source}-{index}",
            "content": chunk,
            "vector": vector,
            "metadata": {"source": source},
        }
        container.upsert_item(body=item)
    print(f"Processed: {source} ({len(chunks)} chunks)")


def ingest_icepanel_model():
    """Ingests the IcePanel C4 model (objects + connections) into the Cosmos DB vector store."""
    objects = fetch_icepanel("objects", "modelObjects")
    connections = fetch_icepanel("connections", "modelConnections")

    cosmos_client = CosmosClient(url=cosmos_endpoint, credential=cosmos_key)
    container = cosmos_client.get_database_client(database_name).get_container_client(container_name)
    embeddings = GoogleGenerativeAIEmbeddings(model=GEMINI_EMBEDDING_MODEL, google_api_key=gemini_api_key) #or AzureOpenAIEmbeddings

    for source, markdown_content in build_documents(objects, connections):
        try:
            process_document(container, embeddings, source, markdown_content)
        except Exception as e:
            print(f"Error processing {source}: {e}")


if __name__ == "__main__":
    ingest_icepanel_model()
    print("IcePanel ingestion complete.")
