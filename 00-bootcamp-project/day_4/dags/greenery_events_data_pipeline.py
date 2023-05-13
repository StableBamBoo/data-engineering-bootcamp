from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils import timezone
import configparser
import csv
import requests

# Import modules regarding GCP service account, BigQuery, and GCS 
# Your code here


def _extract_data():
    # Your code below

    parser = configparser.ConfigParser()
    parser.read("/opt/airflow/dags/pipeline.conf")
    host = parser.get("api_config", "host")
    port = parser.get("api_config", "port")

    API_URL = f"http://{host}:{port}"
    DATA_FOLDER = "data"

    ### Events
    data = "events"
    date = "2021-02-10"
    response = requests.get(f"{API_URL}/{data}/?created_at={date}")
    data = response.json()
    with open(f"opt/airflow/dags/events-{date}.csv", "w") as f:
        writer = csv.writer(f)
        header = data[0].keys()
        writer.writerow(header)

        for each in data:
            writer.writerow(each.values())
    pass

def _load_data_to_gcs():
    # Your code below
    pass


def _load_data_from_gcs_to_bigquery():
    # Your code below
    pass


default_args = {
    "owner": "airflow",
		"start_date": timezone.datetime(2023, 5, 1),  # Set an appropriate start date here
}
with DAG(
    dag_id="greenery_events_data_pipeline",  # Replace xxx with the data name
    default_args=default_args,
    schedule="@daily",  # Set your schedule here
    catchup=False,
    tags=["DEB", "2023", "greenery"],
):

    # Extract data from Postgres, API, or SFTP
    extract_data = PythonOperator(
        task_id="extract_data",
        python_callable=_extract_data,
    )

    # Load data to GCS
    load_data_to_gcs = PythonOperator(
        task_id="load_data_to_gcs",
        python_callable=_load_data_to_gcs,
    )

    # Load data from GCS to BigQuery
    load_data_from_gcs_to_bigquery = PythonOperator(
        task_id="load_data_from_gcs_to_bigquery",
        python_callable=_load_data_from_gcs_to_bigquery,
    )

    # Task dependencies
    extract_data >> load_data_to_gcs >> load_data_from_gcs_to_bigquery