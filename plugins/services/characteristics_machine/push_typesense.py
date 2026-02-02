import polars as pl
from typesense.exceptions import ObjectNotFound

from common.typesense_client import get_typesense_client
from services.characteristics_machine.schema_typesense import characteristics_machine_schema
from services.characteristics_machine.transformations import transform_characteristics_machine_data


def push_characteristics_machine_to_typesense(
    parquet_file: str,
    collection_name: str,
    batch_size: int = 10_000,
):
    """
    Stream characteristics_machine Parquet files into Typesense safely.

    """

    client = get_typesense_client("typesense_conn")

    # Ensure collection exists
    schema = characteristics_machine_schema(collection_name)
    try:
        client.collections[collection_name].retrieve()
    except ObjectNotFound:
        client.collections.create(schema)

    total_imported = 0
    total_failed = 0

    # Lazy scan (does NOT load all data into memory)
    lf = pl.scan_parquet(f"{parquet_file}/*.parquet")

    # Apply flat transformations
    lf = transform_characteristics_machine_data(lf)

    print(f"[Typesense] Starting import to '{collection_name}'...")
    
    # Stream in batches
    for batch_df in lf.collect(streaming=True).iter_slices(batch_size):
        records = batch_df.to_dicts()

        results = client.collections[
            collection_name
        ].documents.import_(
            records,
            {"action": "upsert"},
        )
        for r in results:
          if not r.get("success"):
           print("Typesense error:", r)
           break

        failed = [r for r in results if not r.get("success")]
        total_failed += len(failed)
        total_imported += len(records) - len(failed)

    print(
        f"[Typesense] Imported {total_imported} documents "
        f"(failed: {total_failed}) into '{collection_name}'"
    )
