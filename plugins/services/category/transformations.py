import polars as pl
from helpers.jsonString_json import json_decode


def _get_lang_value(json_str: str, lang: str = "fr") -> str:
    """
    Extract a single language value from a JSON string.
    Flat output only (string).
    """
    if not json_str or not isinstance(json_str, str):
        return ""

    data = json_decode(json_str)
    if not isinstance(data, dict):
        return ""

    return data.get(lang, "") or ""


def transform_category_data(lf: pl.LazyFrame) -> pl.LazyFrame:
    """
    Transform category data for Typesense indexing.
    - Flat fields only
    - No images
    - No nested JSON
    """

    return lf.with_columns(
        [
            # Translations (flattened to single language)
            pl.col("name")
            .map_elements(lambda x: _get_lang_value(x, "fr"), return_dtype=pl.Utf8)
            .alias("name"),

            pl.col("label")
            .map_elements(lambda x: _get_lang_value(x, "fr"), return_dtype=pl.Utf8)
            .alias("label"),

            pl.col("title")
            .map_elements(lambda x: _get_lang_value(x, "fr"), return_dtype=pl.Utf8)
            .alias("title"),

            pl.col("description")
            .map_elements(lambda x: _get_lang_value(x, "fr"), return_dtype=pl.Utf8)
            .alias("description"),

            pl.col("long_description")
            .map_elements(lambda x: _get_lang_value(x, "fr"), return_dtype=pl.Utf8)
            .alias("long_description"),

            pl.col("meta_title")
            .map_elements(lambda x: _get_lang_value(x, "fr"), return_dtype=pl.Utf8)
            .alias("meta_title"),

            pl.col("meta_description")
            .map_elements(lambda x: _get_lang_value(x, "fr"), return_dtype=pl.Utf8)
            .alias("meta_description"),

            # Cast numeric flags explicitly (Polars → Typesense safe)
            pl.col("is_visible").cast(pl.Boolean),
            pl.col("is_enabled").cast(pl.Boolean),
            pl.col("is_clickable").cast(pl.Boolean),
            pl.col("has_pieces_displayed").cast(pl.Int32),
            pl.col("is_reconditioned").cast(pl.Boolean),
            pl.col("is_excluded_from_naming").cast(pl.Boolean),
            pl.col("is_visible_menu").cast(pl.Boolean),
            pl.col("has_generated_children").cast(pl.Boolean),

            # IDs
            pl.col("id").cast(pl.Utf8),
            pl.col("parent_id").cast(pl.Int32),
            pl.col("root_parent_id").cast(pl.Int32),
            pl.col("order").cast(pl.Int32),
        ]
    )
