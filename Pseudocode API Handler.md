function get_billing_record(record_id):
    record = cosmos.read("Billing", record_id)
    if record:
        return record
    
    blob_path = "archive/" + record_id + ".json"
    if blob_storage.exists(blob_path):
        return blob_storage.download(blob_path)
    
    return "404 Not Found"
