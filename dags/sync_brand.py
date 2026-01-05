from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime, timedelta

from services.brand.fetch_data import fetch_brands_chunked
from services.brand.push_typesense import push_brands_to_typesense

default_args = {
    "owner": "ITJL",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="sync_brands",
    default_args=default_args,
    start_date=datetime(2025, 12, 25),
    schedule="@daily",
    catchup=False,
    max_active_runs=1,
    tags=["brands", "mysql", "parquet", "typesense"],
) as dag:

    # 1️⃣ MySQL → Parquet
    fetch_brands_task = PythonOperator(
        task_id="fetch_brands_to_parquet",
        python_callable=fetch_brands_chunked,
        op_kwargs={
            "output_dir": "/opt/airflow/tmp/marques_chunked",
            "chunk_size": 1_000,
        },
    )

    # 2️⃣ Parquet → Typesense
    push_to_typesense_task = PythonOperator(
        task_id="push_brands_to_typesense",
        python_callable=push_brands_to_typesense,
        op_kwargs={
            "parquet_file": "/opt/airflow/tmp/marques_chunked",
            "collection_name": "brands",
            "batch_size": 200,
        },
    )

    fetch_brands_task >> push_to_typesense_task
