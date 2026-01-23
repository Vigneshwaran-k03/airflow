from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime, timedelta

from services.product.fetch_data import fetch_product_chunked
from services.product.push_typesense import push_product_to_typesense

default_args = {
    "owner": "ITJL",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="sync_product",
    default_args=default_args,
    start_date=datetime(2025, 12, 25),
    schedule="@daily",
    catchup=False,
    max_active_runs=1,
    tags=["product", "mysql", "parquet", "typesense"],
) as dag:

    # 1️⃣ MySQL → Parquet
    fetch_product_task = PythonOperator(
        task_id="fetch_product_to_parquet",
        python_callable=fetch_product_chunked,
        op_kwargs={
            "output_dir": "/opt/airflow/tmp/product_chunked",
            "chunk_size": 10_000,
        },
    )

    # 2️⃣ Parquet → Typesense
    push_to_typesense_task = PythonOperator(
        task_id="push_product_to_typesense",
        python_callable=push_product_to_typesense,
        op_kwargs={
            "parquet_file": "/opt/airflow/tmp/product_chunked",
            "collection_name": "products",
            "batch_size": 5_000,
        },
    )

    fetch_product_task >> push_to_typesense_task
