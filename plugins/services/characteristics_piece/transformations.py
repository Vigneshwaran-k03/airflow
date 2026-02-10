import polars as pl
import json

def transform_characteristics_piece_data(lf: pl.LazyFrame) -> pl.LazyFrame:
    """
    Transform characteristics piece data for Typesense indexing.
    
    Handles:
    - JSON translation fields
    - Boolean conversions
    - Numeric formatting
    """
    
    return lf.with_columns([
        # Convert id to string (Typesense requirement)
        pl.col("id").cast(pl.Utf8),
        
        # Parse JSON translations
        pl.col("name").map_elements(
            lambda x: json.loads(x) if x else {},
            return_dtype=pl.Object
        ),

        pl.col("unit").map_elements(
            lambda x: json.loads(x) if x else {},
            return_dtype=pl.Object
        ),
        
        # Other string fields
        pl.col("type").cast(pl.Utf8),
        pl.col("symbol").cast(pl.Utf8).fill_null(""),

        # Integer fields
        pl.col("technical_branch_id").cast(pl.Utf8),

        # Parse JSON products ids array
        pl.col("products_ids").map_elements(
            lambda x: [str(i) for i in json.loads(x)] if x else [],
            return_dtype=pl.List(pl.Utf8)
        ),
    ])
