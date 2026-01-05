import os
import polars as pl
from helpers.db_helpers import select_to_polars
from helpers.clear_dir import clear_dir
from services.brand.query import brands_base_query, brands_environment_query


def fetch_brands_chunked(
    output_dir: str,
    chunk_size: int = 100_000,
):
    """
    Export brands in chunks and write multiple Parquet files:
    output_dir/
        part-00000.parquet
        part-00001.parquet
        ...
    """

    os.makedirs(output_dir, exist_ok=True)
    clear_dir(output_dir)

    offset = 0
    part = 0
    total_rows = 0

    while True:
        # Build chunked base query
        base_stmt = brands_base_query(
            limit=chunk_size,
            offset=offset,
        )
        df = select_to_polars(base_stmt)

        if df.is_empty():
            break

        # Fetch env data only for this chunk
        ids = df.select("id").to_series().to_list()

        env_stmt = brands_environment_query(ids=ids)
        df_env = select_to_polars(env_stmt)

        # Join per chunk
        df = df.join(df_env, on="id", how="left")

        # Write chunk
        out_path = os.path.join(
            output_dir,
            f"part-{part:05d}.parquet",
        )
        df.write_parquet(out_path)

        total_rows += df.height
        print(f"[fetch_brands] wrote {df.height} rows → {out_path}")

        offset += chunk_size
        part += 1

    print(f"[fetch_brands] done, total rows: {total_rows}")
