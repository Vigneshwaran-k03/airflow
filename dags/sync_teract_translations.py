from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime, timedelta

from services.teract_translations.fetch_data import fetch_teract_translations_chunked
from services.teract_translations.push_typesense import push_teract_translations_to_typesense

default_args = {
    "owner": "ITJL",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="sync_teract_translations",
    default_args=default_args,
    start_date=datetime(2025, 12, 25),
    schedule="@daily",
    catchup=False,
    max_active_runs=1,
    tags=["teract_translations", "mysql", "parquet", "typesense"],
) as dag:

    # 1️⃣ MySQL → Parquet
    fetch_teract_translations_task = PythonOperator(
        task_id="fetch_teract_translations_to_parquet",
        python_callable=fetch_teract_translations_chunked,
        op_kwargs={
            "output_dir": "/opt/airflow/tmp/teract_translations_chunked",
            "chunk_size": 5_000,
        },
    )

    # 2️⃣ Parquet → Typesense
    push_to_typesense_task = PythonOperator(
        task_id="push_teract_translations_to_typesense",
        python_callable=push_teract_translations_to_typesense,
        op_kwargs={
            "parquet_file": "/opt/airflow/tmp/teract_translations_chunked",
            "collection_name": "teract_translations",
            "batch_size": 5_000,
        },
    )

    fetch_teract_translations_task >> push_to_typesense_task
