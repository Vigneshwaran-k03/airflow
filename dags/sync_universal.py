from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime, timedelta

from services.universal.fetch_data import fetch_universal_chunked
from services.universal.push_typesense import push_universal_to_typesense

default_args = {
    "owner": "ITJL",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="sync_universal",
    default_args=default_args,
    start_date=datetime(2025, 12, 25),
    schedule="@daily",
    catchup=False,
) as dag:

    fetch_universal_task = PythonOperator(
        task_id="fetch_universal_to_parquet",
        python_callable=fetch_universal_chunked,
        op_kwargs={
            "output_dir": "/opt/airflow/tmp/universal",
        },
    )

    push_to_typesense_task = PythonOperator(
        task_id="push_universal_to_typesense",
        python_callable=push_universal_to_typesense,
        op_kwargs={
            "parquet_file": "/opt/airflow/tmp/universal",
            "collection_name": "universal_branches",
            "batch_size": 5_000,
        },
    )

    fetch_universal_task >> push_to_typesense_task
