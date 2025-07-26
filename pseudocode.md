function archive_old_billing_records():
    threshold_date = current_date() - 90 days
    old_records = cosmos.query("SELECT * FROM Billing WHERE created_at < @threshold", threshold_date)

    for record in old_records:
        blob_path = "archive/" + record.id + ".json"
        blob_storage.upload(blob_path, serialize(record))

        cosmos.delete("Billing", record.id)
