import polars as pl
import json
from helpers.file_helper import file_to_image_obj, get_current_parent
from helpers.jsonString_json import json_decode

PICTURE_FOLDER = "images/arbre_kit_technique"

def _parse_parent_ids(value):
    """
    Parse parent_ids from database into a list of integers.
    Handles JSON strings, comma-separated strings, or already parsed lists.
    """
    if not value:
        return []
    
    # If it's already a list, return it
    if isinstance(value, list):
        return [int(x) for x in value if x is not None]
    
    if isinstance(value, str):
        # Try JSON parsing first
        try:
            parsed = json.loads(value)
            if isinstance(parsed, list):
                return [int(x) for x in parsed if x is not None]
        except (json.JSONDecodeError, ValueError):
            pass
        
        # Try comma-separated values
        try:
            return [int(x.strip()) for x in value.split(',') if x.strip()]
        except ValueError:
            pass
    
    return []

def _parse_environments(value):
    """
    Parse environments from database into a list of strings.
    Handles JSON arrays or null values.
    """
    if not value:
        return []
    
    # If it's already a list, return it
    if isinstance(value, list):
        return [str(x) for x in value if x is not None]
    
    if isinstance(value, str):
        # Try JSON parsing
        try:
            parsed = json.loads(value)
            if isinstance(parsed, list):
                return [str(x) for x in parsed if x is not None]
        except (json.JSONDecodeError, ValueError):
            pass
    
    return []

def transform_technical_data(lf: pl.LazyFrame) -> pl.LazyFrame:

    lf = lf.with_columns(
        [   
            #translations
            pl.col("name").map_elements(json_decode, return_dtype=pl.Object),
            pl.col("label").map_elements(json_decode, return_dtype=pl.Object),
    
            #booleans
            pl.col("is_consumable").cast(pl.Boolean),
            pl.col("is_accessory").cast(pl.Boolean),
            pl.col("is_other").cast(pl.Boolean),
            pl.col("is_visible").cast(pl.Boolean),

            #floats
            pl.col("weight").cast(pl.Float32),
            pl.col("score").cast(pl.Int32).fill_null(0),

            #environments list
            pl.col("environments").map_elements(_parse_environments, return_dtype=pl.List(pl.Utf8)),
            
            #images
            pl.col("picture")
              .map_elements(lambda x: file_to_image_obj(x, PICTURE_FOLDER) or {}, return_dtype=pl.Object),
            
            # Parse parent_ids from database into array
            pl.col("parent_ids").map_elements(_parse_parent_ids, return_dtype=pl.List(pl.Int32)),
        ]
    )

    # If parent_ids is empty and parent_id exists, use parent_id as fallback
    lf = lf.with_columns(
        pl.when(
            (pl.col("parent_ids").list.len() == 0) & pl.col("parent_id").is_not_null()
        )
        .then(pl.col("parent_id").cast(pl.List(pl.Int32)))
        .otherwise(pl.col("parent_ids"))
        .alias("parent_ids")
    )

    # Build lookup for parent
    lookup_df = lf.select(["id", "name", "label", "picture", "parent_id"]).collect()
    lookup = {row["id"]: row for row in lookup_df.to_dicts()}

    lf = lf.with_columns(
        [
            pl.struct(["parent_id"])
              .map_elements(lambda x: get_current_parent(x["parent_id"], lookup) or {}, return_dtype=pl.Object)
              .alias("parent"),

            pl.col("id").cast(pl.Utf8),
        ]
    )

    return lf
