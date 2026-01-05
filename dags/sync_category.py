from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime, timedelta

from services.category.fetch_data import fetch_categories_chunked
from services.category.push_typesense import push_categories_to_typesense

default_args = {
    "owner": "ITJL",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="sync_categories",
    default_args=default_args,
    start_date=datetime(2025, 12, 25),
    schedule="@daily",
    catchup=False,
    max_active_runs=1,
    tags=["categories", "mysql", "parquet", "typesense"],
) as dag:

    # 1️⃣ MySQL → Parquet (FLAT CATEGORY DATA)
    fetch_categories_task = PythonOperator(
        task_id="fetch_categories_to_parquet",
        python_callable=fetch_categories_chunked,
        op_kwargs={
            "output_dir": "/opt/airflow/tmp/categories_chunked",
            "chunk_size": 5_000,
        },
    )

    # 2️⃣ Parquet → Typesense
    push_to_typesense_task = PythonOperator(
        task_id="push_categories_to_typesense",
        python_callable=push_categories_to_typesense,
        op_kwargs={
            "parquet_file": "/opt/airflow/tmp/categories_chunked",
            "collection_name": "categories",
            "batch_size": 5_000,
        },
    )

    fetch_categories_task >> push_to_typesense_task
