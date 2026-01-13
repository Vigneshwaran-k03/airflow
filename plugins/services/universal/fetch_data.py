import os
import polars as pl

from helpers.db_helpers import select_to_polars
from helpers.clear_dir import clear_dir
from services.universal.query import universal_base_query
from helpers.debug_df import debug_df

def fetch_universal_chunked(
    output_dir: str,
    chunk_size: int = 5_000,
):
    """
    Export universal data in chunks and write multiple Parquet files:
    output_dir/
        part-00000.parquet
        part-00001.parquet
        part-00002.parquet
    """

    os.makedirs(output_dir, exist_ok=True)
    clear_dir(output_dir)

    offset = 0
    part = 0
    total_rows = 0

    while True:
        # Build chunked universal query
        stmt = universal_base_query(
            limit=chunk_size,
            offset=offset,
        )

        df = select_to_polars(stmt)


        if df.is_empty():
            break

        out_path = os.path.join(
            output_dir,
            f"part-{part:05d}.parquet",
        )
        df.write_parquet(out_path)

        total_rows += df.height
        print(f"[fetch_universal] wrote {df.height} rows → {out_path}")

        offset += chunk_size
        part += 1

    print(f"[fetch_universal] done, total rows: {total_rows}")
