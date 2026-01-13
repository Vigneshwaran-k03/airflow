import polars as pl
from helpers.file_to_img_obj import file_to_image_obj
from helpers.get_current_parent import get_current_parent
from helpers.jsonString_json import json_decode
import json

ICON_FOLDER = "images/catman_swap"
PICTURE_FOLDER = "images/catman_swap"


def _parse_json(value):
    if not value:
        return None

    data = json_decode(value)
    if not data:
        return None

    # Replace None with "" in the dictionary
    if isinstance(data, dict):
        data = {k: (v if v is not None else "") for k, v in data.items()}

    return data


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


def transform_category_data(lf: pl.LazyFrame) -> pl.LazyFrame:
    # Base Transformations
    lf = lf.with_columns(
        [   
            
            # Objects
            pl.col("name").map_elements(_parse_json, return_dtype=pl.Object),
            pl.col("label").map_elements(_parse_json, return_dtype=pl.Object),
            pl.col("title").map_elements(_parse_json, return_dtype=pl.Object),
            pl.col("description").map_elements(_parse_json, return_dtype=pl.Object),
            pl.col("long_description").map_elements(_parse_json, return_dtype=pl.Object),
            pl.col("meta_title").map_elements(_parse_json, return_dtype=pl.Object),
            pl.col("meta_description").map_elements(_parse_json, return_dtype=pl.Object),
            pl.col("generated_title").map_elements(_parse_json, return_dtype=pl.Object),
            pl.col("content").map_elements(_parse_json, return_dtype=pl.Object),
            pl.col("redirection_url").map_elements(_parse_json, return_dtype=pl.Object),

            #colour
            pl.col("primary_color").cast(pl.Utf8).fill_null(""),


            # Booleans
            pl.col("is_visible").cast(pl.Boolean),
            pl.col("is_enabled").cast(pl.Boolean),
            pl.col("is_clickable").cast(pl.Boolean),
            pl.col("is_reconditioned").cast(pl.Boolean),
            pl.col("is_excluded_from_naming").cast(pl.Boolean),
            pl.col("is_visible_menu").cast(pl.Boolean),
            pl.col("has_generated_children").cast(pl.Boolean),
            pl.col("display_brand_filter").cast(pl.Boolean),

            # Integers
            pl.col("has_pieces_displayed").cast(pl.Int32),
            pl.col("parent_id").cast(pl.Int32),
            pl.col("order").cast(pl.Int32),

            # Strings & Fills
            pl.col("alias").cast(pl.Utf8).fill_null(""),
            pl.col("score").cast(pl.Int32).fill_null(0),
            pl.col("event").cast(pl.Utf8).fill_null(""),

            # environment
            pl.col("environment").cast(pl.Utf8).fill_null(""),
            pl.col("id_environment").cast(pl.Int32).fill_null(0), 

            # linktype
            pl.col("link_type").cast(pl.Utf8).fill_null(""),

            # parent_ids - parse into list of integers
            pl.col("parent_ids").map_elements(_parse_parent_ids, return_dtype=pl.List(pl.Int32)),
            
            # Branches - parse into list of integers
            pl.col("technical_branches").map_elements(_parse_parent_ids, return_dtype=pl.List(pl.Int32)),
            pl.col("universal_branches").map_elements(_parse_parent_ids, return_dtype=pl.List(pl.Int32)),
            
            # shop_filters - parse into list of strings
            pl.col("shop_filters").map_elements(
                lambda x: json.loads(x) if x and isinstance(x, str) else (x if isinstance(x, list) else []),
                return_dtype=pl.List(pl.Utf8)
            ),
            
            # images
            pl.col("icon")
            .map_elements(
                lambda x: file_to_image_obj(x, ICON_FOLDER) or {}, return_dtype=pl.Object
            )
            .alias("icon"),
            pl.col("picture")
            .map_elements(
                lambda x: file_to_image_obj(x, PICTURE_FOLDER) or {}, return_dtype=pl.Object
            )
            .alias("picture"),
           

        ]
    )

    # Build Lookup Table to collect parent chain
    lookup_df = lf.select(["id", "name", "label", "picture", "parent_id"]).collect()
    lookup = {row["id"]: row for row in lookup_df.to_dicts()}

    lf = lf.with_columns(
    [
        # parent ONLY
        pl.struct(["parent_id"])
        .map_elements(
            lambda x: get_current_parent(x["parent_id"], lookup) or {},
            return_dtype=pl.Object,
        )
        .alias("parent"),

        pl.col("id").cast(pl.Utf8),
    ]
)
    lf = lf.with_columns(
    [
        pl.when(
            pl.col("generated_title").is_not_null()
            & pl.col("generated_title").map_elements(
                lambda d: (
                    isinstance(d, dict)
                    and any(
                        isinstance(v, str) and v.strip() != ""
                        for v in d.values()
                    )
                ),
                return_dtype=pl.Boolean,
            )
        )
        .then(pl.col("generated_title"))
        .otherwise(pl.col("name"))
        .alias("search_title")
    ]
)




    # select only the desired columns
    final_cols = [
        "id", "name","label", "title", "description", "long_description",
        "meta_title", "meta_description","search_title", "generated_title",
        "content", "redirection_url",
        "is_visible", "is_enabled", "is_clickable", "is_reconditioned", 
        "is_excluded_from_naming", "is_visible_menu", "has_generated_children",
        "has_pieces_displayed", "parent_id", "order",
        "alias", "score", "event", "environment", "id_environment", "link_type",
        "icon", "picture", 
        "primary_color","display_brand_filter","shop_filters",
        "parent","parent_ids",
        "technical_branches", "universal_branches"
    ]
    
    lf = lf.select(final_cols)

    return lf
