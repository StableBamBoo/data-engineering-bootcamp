# Ref: https://cloud.google.com/bigquery/docs/samples/bigquery-load-table-gcs-csv

import json
import os

from google.cloud import bigquery
from google.oauth2 import service_account


keyfile = os.environ.get("KEYFILE_PATH")
service_account_info = json.load(open(keyfile))
credentials = service_account.Credentials.from_service_account_info(service_account_info)
project_id = "skooldio-deb-01-project"
client = bigquery.Client(
    project=project_id,
    credentials=credentials,
)

job_config = bigquery.LoadJobConfig(
    skip_leading_rows=1,
    write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    source_format=bigquery.SourceFormat.CSV,
    autodetect=True,
    time_partitioning=bigquery.TimePartitioning(
        type_=bigquery.TimePartitioningType.DAY,
        field="created_at",
    ),
    clustering_fields=["first_name", "last_name"],
)

# file_path = "data/addresses.csv"
# file_path = "data/events.csv"
# file_path = "data/order_items.csv"
# file_path = "data/orders.csv"
# file_path = "data/products.csv"
# file_path = "data/promos.csv"
file_path = "data/users.csv"

with open(file_path, "rb") as f:
    
    # table_id = f"{project_id}.deb_bootcamp.addresses"
    # table_id = f"{project_id}.deb_bootcamp.events"
    # table_id = f"{project_id}.deb_bootcamp.order_items"
    # table_id = f"{project_id}.deb_bootcamp.orders"
    # table_id = f"{project_id}.deb_bootcamp.products"
    # table_id = f"{project_id}.deb_bootcamp.promos"
    table_id = f"{project_id}.deb_bootcamp.users"
    
    job = client.load_table_from_file(f, table_id, job_config=job_config)
    job.result()

table = client.get_table(table_id)
print(f"Loaded {table.num_rows} rows and {len(table.schema)} columns to {table_id}")