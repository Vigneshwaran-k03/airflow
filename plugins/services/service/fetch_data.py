import os
import json
import polars as pl

from helpers.db_helpers import select_to_polars
from helpers.clear_dir import clear_dir

from services.service.transformations import (
    transform_data,
    transform_admin,
    attach_admin_to_services,
)

from services.service.query import (
    services_base_query,
    services_admin_query,
)

def fetch_services_chunked(
    output_dir: str,
    chunk_size: int = 100_000,
):
    """
    Export services in chunks and write multiple Parquet files:
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
        base_stmt = services_base_query(
            limit=chunk_size,
            offset=offset,
        )
        df = select_to_polars(base_stmt)

        if df.is_empty():
            break

        df = transform_data(df)

        admin_ids = (
            df.select("admin_id")
            .unique()
            .drop_nulls()
            .to_series()
            .to_list()
        )

        if admin_ids:
            admin_stmt = services_admin_query(admin_ids=admin_ids)
            df_admin = select_to_polars(admin_stmt)

            df_admin = transform_admin(df_admin)

            df = attach_admin_to_services(df, df_admin)

        out_path = os.path.join(
            output_dir,
            f"part-{part:05d}.parquet",
        )
        df = sanitize_for_parquet(df)

        df.write_parquet(out_path)

        total_rows += df.height
        print(f"[fetch_services] wrote {df.height} rows → {out_path}")

        offset += chunk_size
        part += 1

    print(f"[fetch_services] done, total rows: {total_rows}")

def sanitize_for_parquet(df: pl.DataFrame) -> pl.DataFrame:
    exprs = []

    for name, dtype in df.schema.items():
        if dtype == pl.Object:
            exprs.append(
                pl.col(name)
                .map_elements(
                    lambda v: json.dumps(v) if v is not None else "{}",
                    return_dtype=pl.String,
                )
                .alias(name)
            )

    if exprs:
        df = df.with_columns(exprs)

    return df
