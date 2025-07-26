import os, logging
from datetime import datetime, timedelta
import json
import azure.functions as func
from azure.storage.blob import BlobServiceClient
from azure.cosmos import CosmosClient, exceptions

def main(mytimer: func.TimerRequest) -> None:
    cutoff = datetime.utcnow() - timedelta(days=90)
    cosmos = CosmosClient.from_connection_string(os.getenv("COSMOS_URI"))
    container = cosmos.get_database_client(os.getenv("COSMOS_DB")).get_container_client(os.getenv("COSMOS_CONTAINER"))
    blobs = BlobServiceClient.from_connection_string(os.getenv("BLOB_CONN")).get_container_client(os.getenv("BLOB_CONTAINER"))

    query = "SELECT c.id, c.partitionKey, c.createdAt FROM c WHERE c.createdAt < @cutoff"
    params = [{"name":"@cutoff","value":cutoff.isoformat()}]

    for item in container.query_items(query=query, parameters=params, enable_cross_partition_query=True):
        blob_name = f"{item['id']}.json"
        blobs.upload_blob(blob_name, json.dumps(item), overwrite=True)
        container.delete_item(item['id'], partition_key=item['partitionKey'])
        logging.info(f"Archived {item['id']}")



function.json (Timer-trigger):
{
  "bindings": [
    {
      "name": "mytimer",
      "type": "timerTrigger",
      "direction": "in",
      "schedule": "0 0 * * *"  // daily at midnight UTC
    }
  ]
}



requirements.txt:

azure-functions
azure-storage-blob
azure-cosmos
