import os, json
import azure.functions as func
from azure.cosmos import CosmosClient, exceptions
from azure.storage.blob import BlobServiceClient

cosmos = CosmosClient.from_connection_string(os.getenv("COSMOS_URI"))
container = cosmos.get_database_client(os.getenv("COSMOS_DB")).get_container_client(os.getenv("COSMOS_CONTAINER"))
blobs = BlobServiceClient.from_connection_string(os.getenv("BLOB_CONN")).get_container_client(os.getenv("BLOB_CONTAINER"))

def main(req: func.HttpRequest) -> func.HttpResponse:
    record_id = req.route_params.get("id")
    partition_key = req.headers.get("x-partition-key")
    try:
        rec = container.read_item(record_id, partition_key)
        return func.HttpResponse(json.dumps(rec), mimetype="application/json")
    except exceptions.CosmosResourceNotFoundError:
        blob = blobs.get_blob_client(f"{record_id}.json")
        if blob.exists():
            return func.HttpResponse(blob.download_blob().readall(), mimetype="application/json")
        return func.HttpResponse("Not Found", status_code=404)


requirements.txt:
azure-functions
azure-cosmos
azure-storage-blob
