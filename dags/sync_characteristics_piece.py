from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime, timedelta

from services.characteristics_piece.fetch_data import fetch_characteristics_piece_chunked
from services.characteristics_piece.push_typesense import push_characteristics_piece_to_typesense

default_args = {
    "owner": "ITJL",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="sync_characteristics_piece",
    default_args=default_args,
    start_date=datetime(2025, 12, 25),
    schedule="@daily",
    catchup=False,
    max_active_runs=1,
    tags=["characteristics_piece", "mysql", "parquet", "typesense"],
) as dag:

    # 1️⃣ MySQL → Parquet
    fetch_characteristics_piece_task = PythonOperator(
        task_id="fetch_characteristics_piece_to_parquet",
        python_callable=fetch_characteristics_piece_chunked,
        op_kwargs={
            "output_dir": "/opt/airflow/tmp/characteristics_piece_chunked",
            "chunk_size": 10_000,
        },
    )

    # 2️⃣ Parquet → Typesense
    push_to_typesense_task = PythonOperator(
        task_id="push_characteristics_piece_to_typesense",
        python_callable=push_characteristics_piece_to_typesense,
        op_kwargs={
            "parquet_file": "/opt/airflow/tmp/characteristics_piece_chunked",
            "collection_name": "characteristics_piece",
            "batch_size": 10_000,
        },
    )

    fetch_characteristics_piece_task >> push_to_typesense_task
