import polars as pl
import json
from datetime import datetime

def build_datetime_object(value):
    if value is None:
        return None

    # value is DATE → "YYYY-MM-DD"
    return {
        "date": f"{value} 00:00:00.000000",
        "timezone_type": 3,
        "timezone": "Europe/Paris",
    }

def transform_pricing_data(lf: pl.LazyFrame) -> pl.LazyFrame:
    """
    Transform pricing data for Typesense indexing.
    
    Handles:
    - JSON translation fields
    - Date formatting
    - Boolean conversions
    - Decimal/numeric formatting
    """
    
    return lf.with_columns([
        # Convert id to string (Typesense requirement)
        pl.col("id").cast(pl.Utf8),

        # VIO Machine (empty object - no table relationship)
        pl.lit(None).alias("vio_machine"),
        
        # Parse JSON translations
        pl.col("name").map_elements(
            lambda x: json.loads(x) if x else {},
            return_dtype=pl.Object
        ),
        
        #dates
        pl.col("start_date").map_elements(
            build_datetime_object,
            return_dtype=pl.Object
        ).alias("start_date"),

        pl.col("end_date").map_elements(
            build_datetime_object,
            return_dtype=pl.Object
        ).alias("end_date"),

        # Parse company JSON object
        pl.col("company").map_elements(
            lambda x: json.loads(x) if x else {},
            return_dtype=pl.Object
        ),
        
        # Parse environment JSON array to list
        pl.col("environment").map_elements(
            lambda x: json.loads(x) if x else [],
            return_dtype=pl.List(pl.Utf8)
        ),
        
        # Convert booleans to proper type
        pl.col("has_free_shipping").cast(pl.Boolean),
        pl.col("is_enabled").cast(pl.Boolean),
        pl.col("has_all_products").cast(pl.Boolean),
        pl.col("has_all_entities").cast(pl.Boolean),
        pl.col("is_shop").cast(pl.Boolean),
        pl.col("is_overriding_fixed_price").cast(pl.Boolean),
        
        # Convert decimals to float
        pl.col("reduction").cast(pl.Float64),
        pl.col("free_shipping_threshold").cast(pl.Float64),
        
        # Ensure numeric fields
        pl.col("company_id").cast(pl.Int32),
        pl.col("vio_machine_id").cast(pl.List(pl.Int32)),
        pl.col("products_threshold").cast(pl.Int32),
    ])
