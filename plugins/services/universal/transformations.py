import polars as pl
import json
from helpers.file_to_img_obj import file_to_image_obj
from helpers.get_current_parent import get_current_parent
from helpers.jsonString_json import json_decode

IMAGE_FOLDER = "documents/arborescence/img"
DEFAULT_MACHINE_FOLDER = "documents/arborescence/img"

def _parse_parent_ids(value):
    if not value:
        return []
    
    ids = []
    if isinstance(value, list):
        ids = [int(x) for x in value if x is not None]
    else:
        try:
            ids = [int(x) for x in json.loads(value)]
        except Exception:
            return []

    return list(dict.fromkeys(ids))

def transform_universal_data(lf: pl.LazyFrame) -> pl.LazyFrame:

    lf = lf.with_columns(
        [
            # ---- TRANSLATIONS (JSON → object) ----
            pl.col("name").map_elements(
                json_decode,
                return_dtype=pl.Object,
            ),
            pl.col("label").map_elements(
                json_decode,
                return_dtype=pl.Object,
            ),
            pl.col("summary").map_elements(
                json_decode,
                return_dtype=pl.Object,
            ),
            pl.col("alias").map_elements(
                json_decode,
                return_dtype=pl.Object,
            ),

            # ---- ALIAS SLUGIFIED (French value, lowercase, spaces to underscores) ----
            pl.col("alias").map_elements(
                lambda x: (
                    decoded.get("fr", "").lower().replace(" ", "_")
                    if x and (decoded := json_decode(x)) and isinstance(decoded, dict) and decoded.get("fr")
                    else ""
                ),
                return_dtype=pl.Utf8,
            ).alias("alias_slugified"),

            # ---- ENVIRONMENT (JSON ARRAY → list[str]) ----
           pl.col("environment").map_elements(
           lambda x: [
                     str(v)
                    for v in (json.loads(x)
                    if isinstance(x, str)
                     else (x or []))
                    if v is not None
            ],
            return_dtype=pl.List(pl.Utf8),
            ),


            # ---- IMAGES ----
            pl.col("img").map_elements(
                lambda x: file_to_image_obj(x, IMAGE_FOLDER) or {},
                return_dtype=pl.Object,
            ).alias("image"),

            # Keep default_machine_img as raw string value from table (convert None to empty string)
            pl.col("default_machine_img").map_elements(
                lambda x: str(x) if x is not None else "",
                return_dtype=pl.Utf8,
            ),

            pl.col("background").map_elements(
                lambda x: file_to_image_obj(x, IMAGE_FOLDER) or {},
                return_dtype=pl.Object,
            ),

            pl.col("icon").map_elements(
                lambda x: file_to_image_obj(x, IMAGE_FOLDER) or {},
                return_dtype=pl.Object,
            ),

            # ---- PARENT IDS ----
            pl.col("parent_ids").map_elements(
                _parse_parent_ids,
                return_dtype=pl.List(pl.Int32),
            ),
            pl.col("depreciation_rate").cast(pl.Float64).fill_null(0.0),
        ]
    )

    # ---- FALLBACK parent_ids ----
    lf = lf.with_columns(
        pl.when(
            (pl.col("parent_ids").list.len() == 0)
            & pl.col("parent_id").is_not_null()
        )
        .then(pl.col("parent_id").cast(pl.List(pl.Int32)))
        .otherwise(pl.col("parent_ids"))
        .alias("parent_ids")
    )

    # ---- BUILD PARENT LOOKUP (EAGER, SAFE) ----
    lookup_df = lf.select(
        ["id", "name", "label",pl.col("image").alias("picture"), "parent_id"]
    ).collect()

    lookup = {row["id"]: row for row in lookup_df.to_dicts()}

    # ---- CURRENT PARENT OBJECT ----
    lf = lf.with_columns(
        pl.struct(["parent_id"])
        .map_elements(
            lambda x: get_current_parent(x["parent_id"], lookup) or {},
            return_dtype=pl.Object,
        )
        .alias("parent"),

        pl.col("id").cast(pl.Utf8),
    )
    lf = lf.drop("img")

    return lf
