
import polars as pl
from helpers.jsonString_json import json_decode
from helpers.file_helper import file_to_image_obj
from helpers.convert_lable import get_label
def transform_data(df: pl.DataFrame):
    
    return df.with_columns(
        #translations
        pl.col("title").map_elements(lambda x: json_decode(x) if isinstance(x, str) and x.strip() else {}, return_dtype=pl.Object),
        pl.col("description").map_elements(lambda x: json_decode(x) if isinstance(x, str) and x.strip() else {}, return_dtype=pl.Object),
        pl.col("long_description").map_elements(lambda x: json_decode(x) if isinstance(x, str) and x.strip() else {}, return_dtype=pl.Object),
        pl.col("meta").map_elements(lambda x: json_decode(x) if isinstance(x, str) and x.strip() else {}, return_dtype=pl.Object),
        pl.col("description_b2b").map_elements(lambda x: json_decode(x) if isinstance(x, str) and x.strip() else {}, return_dtype=pl.Object),
        
        #images
        pl.col("image").map_elements(lambda x: file_to_image_obj(x, folder="images/marques") if isinstance(x, str) and x.strip() else {}, return_dtype=pl.Object),
        pl.col("background_image").map_elements(lambda x: file_to_image_obj(x, folder="images/marques") if isinstance(x, str) and x.strip() else {}, return_dtype=pl.Object),
        
        #aliases
        pl.when(pl.col("aliases").is_null() | (pl.col("aliases") == ""))
        .then(pl.lit([]).cast(pl.List(pl.Utf8)))
        .otherwise(pl.col("aliases").str.split(",").cast(pl.List(pl.Utf8)))
        .alias("aliases"),

        #environment
        pl.when(pl.col("environment").is_null() | (pl.col("environment") == ""))
        .then(pl.lit([]).cast(pl.List(pl.Utf8)))
        .otherwise(pl.col("environment").str.split(",").cast(pl.List(pl.Utf8)))
        .alias("environment"),

        #label
        pl.col("name").map_elements(lambda x: get_label(x) if isinstance(x, str) and x.strip() else "", return_dtype=pl.Utf8).alias("label"),

        #is_main
        pl.col("is_main").cast(pl.Int32).alias("is_main"),
        #is_seller_brand
        pl.col("is_seller_brand").cast(pl.Int32).alias("is_seller_brand"),
        #is_show_part_brand_search
        pl.col("is_show_part_brand_search").cast(pl.Int32).alias("is_show_part_brand_search"),
        #is_visible
        pl.col("is_visible").cast(pl.Int32).alias("is_visible"),
        #has_parts
        pl.col("has_parts").cast(pl.Int32).alias("has_parts"),

        #id
        pl.col("id").cast(pl.Utf8)
    )