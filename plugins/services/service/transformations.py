import json
import mimetypes
import os
import polars as pl
from helpers.jsonString_json import json_decode
from helpers.file_to_img_obj import file_to_image_obj

ADMIN_AVATAR_FOLDER = "images/admins/avatars"
ADMIN_BG_FOLDER = "images/admins/backgrounds"
FILES_BASE_URL = "https://files.swap-europe.com"

def _parse_json(value):
    """
    Parse JSON string into dict.
    - Return {} instead of None
    - Replace None values with ""
    """
    if not value:
        return {}

    data = json_decode(value)
    if not data or not isinstance(data, dict):
        return {}

    return {k: (v if v is not None else "") for k, v in data.items()}


def transform_data(df: pl.DataFrame) -> pl.DataFrame:
    """
    Transform service data for Typesense indexing
    (same i18n pattern as category)
    """

    df = df.with_columns(
        [
            pl.col("name").map_elements(_parse_json, return_dtype=pl.Object),
            pl.col("title").map_elements(_parse_json, return_dtype=pl.Object),
            pl.col("description").map_elements(_parse_json, return_dtype=pl.Object),
            pl.col("swap_description").map_elements(_parse_json, return_dtype=pl.Object),

            # -------- images --------
            pl.col("image")
            .fill_null("")
            .cast(pl.String)
            .alias("image"),

            pl.col("swap_image")
            .fill_null("")
            .cast(pl.String)
            .alias("swap_image"),


            # -------- booleans → int --------
            pl.col("is_for_particular").cast(pl.Int32),
            pl.col("is_for_repairer").cast(pl.Int32),
            pl.col("is_for_seller").cast(pl.Int32),
            pl.col("is_reserved").cast(pl.Int32),
            pl.col("is_service_ticket").cast(pl.Int32),

            # -------- numeric fields --------
            pl.col("logistic_fee").fill_null(0).cast(pl.Int32),
            pl.col("order").fill_null(0).cast(pl.Int32),
            pl.col("category_id").fill_null(0).cast(pl.Int32),

            # -------- IDs --------
            pl.col("id").cast(pl.Utf8),
        ]
    )

    df = df.with_columns(
        pl.lit(["SWAP"])
        .cast(pl.List(pl.Utf8))
        .alias("environment")
    )

    df = df.with_columns(
        pl.when(
            pl.col("title").map_elements(
                lambda d: isinstance(d, dict)
                and any(isinstance(v, str) and v.strip() for v in d.values()),
                return_dtype=pl.Boolean,
            )
        )
        .then(pl.col("title"))
        .otherwise(pl.col("name"))
        .alias("search_title")
    )

    return df



def _parse_admin_image(value: str, folder: str):
    if not value:
        return None, None, None, None, None

    folder = folder.strip("/")
    relative_path = f"{folder}/{value}"
    absolute_path = f"/opt/airflow/{relative_path}"

    size = os.path.getsize(absolute_path) if os.path.exists(absolute_path) else None
    mime_type, _ = mimetypes.guess_type(value)

    return (
        f"/{folder}",        # folder
        value,               # file
        f"{FILES_BASE_URL}/{relative_path}",  # url
        size,                # size
        mime_type,           # type
    )

def transform_admin(df: pl.DataFrame) -> pl.DataFrame:
    return (
        df.with_columns(
            [
                pl.col("id").cast(pl.Int32),

                pl.col("is_developer").fill_null(False).cast(pl.Boolean),
                pl.col("is_god").fill_null(False).cast(pl.Boolean),

                pl.when(pl.col("avatar").is_not_null())
                .then(
                    pl.struct(
                        [
                            pl.col("avatar").map_elements(
                                lambda v: _parse_admin_image(v, ADMIN_AVATAR_FOLDER)[0],
                                return_dtype=pl.String,
                            ).alias("folder"),

                            pl.col("avatar").map_elements(
                                lambda v: _parse_admin_image(v, ADMIN_AVATAR_FOLDER)[1],
                                return_dtype=pl.String,
                            ).alias("file"),

                            pl.col("avatar").map_elements(
                                lambda v: _parse_admin_image(v, ADMIN_AVATAR_FOLDER)[2],
                                return_dtype=pl.String,
                            ).alias("url"),

                            pl.col("avatar").map_elements(
                                lambda v: _parse_admin_image(v, ADMIN_AVATAR_FOLDER)[3],
                                return_dtype=pl.Int64,
                            ).alias("size"),

                            pl.col("avatar").map_elements(
                                lambda v: _parse_admin_image(v, ADMIN_AVATAR_FOLDER)[4],
                                return_dtype=pl.String,
                            ).alias("type"),
                        ]
                    )
                )
                .otherwise(None)
                .alias("avatar_image"),

                pl.when(pl.col("background").is_not_null())
                .then(
                    pl.struct(
                        [
                            pl.col("background").map_elements(
                                lambda v: _parse_admin_image(v, ADMIN_BG_FOLDER)[0],
                                return_dtype=pl.String,
                            ).alias("folder"),

                            pl.col("background").map_elements(
                                lambda v: _parse_admin_image(v, ADMIN_BG_FOLDER)[1],
                                return_dtype=pl.String,
                            ).alias("file"),

                            pl.col("background").map_elements(
                                lambda v: _parse_admin_image(v, ADMIN_BG_FOLDER)[2],
                                return_dtype=pl.String,
                            ).alias("url"),

                            pl.col("background").map_elements(
                                lambda v: _parse_admin_image(v, ADMIN_BG_FOLDER)[3],
                                return_dtype=pl.Int64,
                            ).alias("size"),

                            pl.col("background").map_elements(
                                lambda v: _parse_admin_image(v, ADMIN_BG_FOLDER)[4],
                                return_dtype=pl.String,
                            ).alias("type"),
                        ]
                    )
                )
                .otherwise(None)
                .alias("background_image"),
            ]
        )
        .select(
            [
                "id",
                "entity_id",
                "mail",
                "pseudo",
                "warehouse_id",
                "service_id",
                "language_id",
                "currency_id",
                "environment_id",
                "is_developer",
                "is_god",
                "avatar_image",
                "background_image",
            ]
        )
    )


def attach_admin_to_services(
    services_df: pl.DataFrame,
    admins_df: pl.DataFrame,
) -> pl.DataFrame:
    admins_df = admins_df.rename({"id": "admin_id"})

    df = services_df.join(
        admins_df,
        on="admin_id",
        how="left",
    )

    df = df.with_columns(
        pl.struct(
            [
                "admin_id",
                "entity_id",
                "mail",
                "pseudo",
                "warehouse_id",
                "service_id",
                "language_id",
                "currency_id",
                "environment_id",
                "is_developer",
                "is_god",
                "avatar_image",
                "background_image",
            ]
        ).alias("admin")
    )

    df = df.drop(
        [
            "entity_id",
            "mail",
            "pseudo",
            "warehouse_id",
            "service_id",
            "language_id",
            "currency_id",
            "environment_id",
            "is_developer",
            "is_god",
            "avatar_image",
            "background_image",
        ]
    )

    return df
