import polars as pl
import gc
import time
import glob
import os
import psutil

from typesense.exceptions import ObjectNotFound, TypesenseClientError
from requests.exceptions import ConnectionError, RequestException

from common.typesense_client import get_typesense_client
from services.product.schema_typesense import product_schema
from services.product.transformations import transform_product_data


def check_typesense_health(client, collection_name: str, max_retries: int = 3) -> bool:
    """
    Check if Typesense is responsive before processing.
    """
    for attempt in range(1, max_retries + 1):
        try:
            client.collections[collection_name].retrieve()
            return True
        except (ConnectionError, RequestException, TypesenseClientError) as e:
            print(f"[Typesense] Health check failed ({attempt}/{max_retries}): {e}")
            if attempt < max_retries:
                wait_time = 2 ** attempt
                print(f"[Typesense] Waiting {wait_time}s before retry...")
                time.sleep(wait_time)
            else:
                return False
    return False


def import_batch_with_retry(
    client,
    collection_name: str,
    records: list,
    max_retries: int = 5,
    initial_delay: float = 2.0,
):
    """
    Import a batch with retry + exponential backoff.
    """
    for attempt in range(1, max_retries + 1):
        try:
            return client.collections[collection_name].documents.import_(
                records,
                {"action": "upsert", "return": False},
            )
        except (ConnectionError, RequestException, TypesenseClientError) as e:
            print(f"[Typesense] Batch import failed ({attempt}/{max_retries}): {e}")

            if attempt < max_retries:
                wait_time = initial_delay * (2 ** (attempt - 1))
                print(f"[Typesense] Retrying in {wait_time}s...")
                time.sleep(wait_time)

                if isinstance(e, (ConnectionError, RequestException)):
                    print("[Typesense] Recreating client connection...")
                    client = get_typesense_client("typesense_conn")
            else:
                raise


def push_product_to_typesense(
    parquet_file: str,
    collection_name: str,
    batch_size: int = 10_000,
    delay_between_batches: float = 1.5,
    delay_between_files: float = 3.0,
):
    """
    Import Parquet files into Typesense safely, one file at a time,
    with clean memory handling and NO RSS log spam.
    """

    client = get_typesense_client("typesense_conn")

    # Ensure collection exists
    schema = product_schema(collection_name)
    try:
        client.collections[collection_name].retrieve()
        print(f"[Typesense] Collection '{collection_name}' found")
    except ObjectNotFound:
        print(f"[Typesense] Creating collection '{collection_name}'...")
        client.collections.create(schema)

    parquet_files = sorted(glob.glob(f"{parquet_file}/*.parquet"))
    print(f"[Typesense] Found {len(parquet_files)} parquet files")

    process = psutil.Process(os.getpid())

    for file_idx, pq_file in enumerate(parquet_files, 1):
        print(f"[Typesense] Processing file {file_idx}/{len(parquet_files)}: {pq_file}")

        # Health check before each file
        if not check_typesense_health(client, collection_name):
            raise Exception("[Typesense] Service not responsive. Aborting import.")

        # Read ONE parquet file
        lf = pl.scan_parquet(pq_file)
        lf = transform_product_data(lf)
        df = lf.collect()

        total_rows = len(df)
        print(f"[Typesense] Loaded {total_rows} rows into memory")

        # Batch import
        for start in range(0, total_rows, batch_size):
            end = min(start + batch_size, total_rows)
            batch_df = df[start:end]
            records = batch_df.to_dicts()

            import_batch_with_retry(client, collection_name, records)
            print(f"[Typesense] Imported rows {start} → {end}")

            time.sleep(delay_between_batches)

        # HARD memory cleanup
        del df
        del lf
        gc.collect()

        # Log RSS ONCE (no repetition)
        rss_mb = process.memory_info().rss / 1024 / 1024
        print(f"[Memory] RSS after cleanup: {rss_mb:.2f} MB")

        # Optional short pause if memory is high (single wait only)
        if rss_mb > 1500:
            time.sleep(2)

        print(f"[Typesense] Completed file {file_idx}/{len(parquet_files)}")
        print(f"[Typesense] Waiting {delay_between_files}s before next file...")
        time.sleep(delay_between_files)

    print("[Typesense] ✅ Import completed successfully for all parquet files")
