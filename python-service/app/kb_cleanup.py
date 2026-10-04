"""Removes the legacy Archi-derived entries from the Cosmos DB C4 vector store.

Before ADR 0030, app/kb.py ingested the Archi Markdown export with random ids and
metadata.source set to the file name (e.g. "context.md"). IcePanel entries use
metadata.source "icepanel-<objectId>" and are left untouched.

Dry run by default; pass --delete to actually remove the entries.
"""
import argparse
import os
from collections import Counter

from azure.cosmos import CosmosClient
from azure.cosmos.partition_key import NonePartitionKeyValue
from dotenv import load_dotenv

load_dotenv()

cosmos_endpoint = os.getenv("COSMOS_ENDPOINT")
cosmos_key = os.getenv("COSMOS_KEY")
database_name = os.getenv("DATABASE_NAME")
container_name = os.getenv("CONTAINER_NAME")

LEGACY_QUERY = "SELECT * FROM c WHERE ENDSWITH(c.metadata.source, '.md')"


def partition_key_value(item, partition_key_path):
    """Returns the item's partition key value for a path like "/id" or "/a/b"."""
    value = item
    for part in partition_key_path.strip("/").split("/"):
        if not isinstance(value, dict) or part not in value:
            return NonePartitionKeyValue
        value = value[part]
    return value


def cleanup_legacy_entries(delete):
    cosmos_client = CosmosClient(url=cosmos_endpoint, credential=cosmos_key)
    container = cosmos_client.get_database_client(database_name).get_container_client(container_name)
    partition_key_path = container.read()["partitionKey"]["paths"][0]

    items = list(container.query_items(query=LEGACY_QUERY, enable_cross_partition_query=True))
    for source, count in sorted(Counter(i["metadata"]["source"] for i in items).items()):
        print(f"{source}: {count} entries")
    print(f"Total legacy entries: {len(items)} (partition key {partition_key_path})")

    if not delete:
        print("Dry run: nothing deleted. Re-run with --delete to remove them.")
        return

    for item in items:
        container.delete_item(item=item["id"], partition_key=partition_key_value(item, partition_key_path))
    print(f"Deleted {len(items)} legacy entries.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--delete", action="store_true", help="delete the entries instead of listing them")
    cleanup_legacy_entries(parser.parse_args().delete)
