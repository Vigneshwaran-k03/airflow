from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime, timedelta
 
from services.service.fetch_data import fetch_services_chunked
from services.service.push_typesense import push_services_to_typesense
 
default_args = {
    "owner": "ITJL",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}
 
with DAG(
    dag_id="sync_service",
    default_args=default_args,
    start_date=datetime(2025, 12, 25),
    schedule="@daily",
    catchup=False,
    max_active_runs=1,
    tags=["service", "mysql", "parquet", "typesense"],
) as dag:
 
    # 1️⃣ MySQL → Parquet
    fetch_services_task = PythonOperator(
        task_id="fetch_services_to_parquet",
        python_callable=fetch_services_chunked,
        op_kwargs={
            "output_dir": "/opt/airflow/tmp/services_chunked",
            "chunk_size": 1_000,
        },
    )
 
    # 2️⃣ Parquet → Typesense
    push_to_typesense_task = PythonOperator(
        task_id="push_services_to_typesense",
        python_callable=push_services_to_typesense,
        op_kwargs={
            "parquet_file": "/opt/airflow/tmp/services_chunked",
            "collection_name": "service",
            "batch_size": 200,
        },
    )
 
    fetch_services_task >> push_to_typesense_task