import os
import polars as pl

from helpers.db_helpers import select_to_polars
from helpers.clear_dir import clear_dir
from services.teract_translations.query import teract_translations_query

def fetch_teract_translations_chunked(
    output_dir: str,
    chunk_size: int = 5_000,
):
    """
    Export teract translations in chunks and write multiple Parquet files
    """

    os.makedirs(output_dir, exist_ok=True)
    clear_dir(output_dir)

    offset = 0
    part = 0
    total_rows = 0

    while True:
        # Build chunked query
        stmt = teract_translations_query(
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
        print(f"[fetch_teract_translations] wrote {df.height} rows → {out_path}")

        offset += chunk_size
        part += 1

    print(f"[fetch_teract_translations] done, total rows: {total_rows}")
