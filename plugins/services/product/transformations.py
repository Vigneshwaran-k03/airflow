import polars as pl
from helpers.file_to_img_obj import file_to_image_obj
from helpers.jsonString_json import json_decode
from helpers.product_extensions_transform import _transform_extensions
import json

PHOTO_FOLDER = "photos"
EXPLODED_VIEW_FOLDER = "images/produits/vues_eclatees"
DOCUMENTS_FOLDER = "documents/produits"


def _parse_json(value):
    if not value:
        return None

    try:
        data = json_decode(value)
    except Exception:
        # If it's not valid JSON, it might be a simple string (e.g. for url)
        # But for translations which are typically objects, falling back to None or empty dict is safer.
        # However, for 'url' if it is a plain string, we might want to keep it?
        # Given the schema expects objects for these fields, returning None or empty dict is best to avoid type errors.
        return None

    if not data:
        return None

    # Replace None with "" in the dictionary
    if isinstance(data, dict):
        data = {k: (v if v is not None else "") for k, v in data.items()}

    return data
#exploded view for the machine field
def _map_exploded_view(machine: dict):
    if not machine:
        return None

    # drop fully empty machine
    if not machine.get("id"):
        return None

    if machine.get("exploded_view"):
        machine["exploded_view"] = file_to_image_obj(
            machine["exploded_view"],
            EXPLODED_VIEW_FOLDER
        ) or {}

    return machine

def _transform_packaging(value):
    data = _parse_json(value)
    if not data:
        return None
    
    if isinstance(data, dict):
        # Round float values to 2 decimal places
        for k, v in data.items():
            if isinstance(v, float):
                data[k] = round(v, 2)
    
    return data


def _transform_documents(value):
    data = _parse_json(value)
    if not data:
        return []
    
    if isinstance(data, list):
        for doc in data:
            if isinstance(doc, dict) and doc.get("file"):
                current_folder = DOCUMENTS_FOLDER
                if doc.get("dossier"):
                    current_folder = f"{DOCUMENTS_FOLDER}/{doc['dossier']}"
                    # remove dossier field as it is not needed in final output
                    del doc["dossier"]
                
                doc["file"] = file_to_image_obj(doc["file"], current_folder)
            else:
                 pass
    return data


def transform_product_data(lf: pl.LazyFrame) -> pl.LazyFrame:
    """
    Apply transformations to Product data.
    """
    lf = lf.with_columns(
        [
            # Objects (Translations)
            pl.col("name").map_elements(_parse_json, return_dtype=pl.Object),
            pl.col("short_description").map_elements(_parse_json, return_dtype=pl.Object),
            pl.col("long_description").map_elements(_parse_json, return_dtype=pl.Object),
            pl.col("meta_title").map_elements(_parse_json, return_dtype=pl.Object),
            pl.col("meta_description").map_elements(_parse_json, return_dtype=pl.Object),
            pl.col("original_references").map_elements(_parse_json, return_dtype=pl.Object),
            pl.col("url").cast(pl.Utf8).fill_null(""),

            # Booleans
            pl.col("is_visible").cast(pl.Boolean),
            pl.col("is_obsolete").cast(pl.Boolean),

            # Integers
            pl.col("id").cast(pl.Int32),
            pl.col("brand").cast(pl.Utf8).fill_null(""),

            # Floats
            pl.col("weight").cast(pl.Float64),

            # Strings
            pl.col("customs_code").cast(pl.Utf8).fill_null(""),
            pl.col("ref").cast(pl.Utf8).fill_null(""),
            pl.col("barcode").cast(pl.Utf8).fill_null(""),
            pl.col("comment").cast(pl.Utf8).fill_null(""),
            pl.col("hs_code").cast(pl.Utf8).fill_null(""),

            #type
            pl.when(pl.col("type") == "KIT")
            .then(pl.lit("piece"))
            .otherwise(pl.col("type"))
            .cast(pl.Utf8)
            .fill_null("")
            .alias("type"),


            #d3e
            pl.col("d3e").map_elements(_parse_json, return_dtype=pl.Object),
            #machine
           pl.col("machine")
            .map_elements(_parse_json, return_dtype=pl.Object)
            .map_elements(_map_exploded_view, return_dtype=pl.Object),

            #Piece
            pl.col("piece").map_elements(_parse_json, return_dtype=pl.Object),

            # Image
            pl.col("image")
            .map_elements(
                lambda x: file_to_image_obj(x, PHOTO_FOLDER) or {}, return_dtype=pl.Object
            )
            .alias("image"),

            # EXTENSIONS
            pl.col("extensions")
            .map_elements(_transform_extensions, return_dtype=pl.Object),

            #Categories
            pl.col("categories").map_elements(_parse_json, return_dtype=pl.Object),

            #machines, pieces and parts
             pl.col("machines").map_elements(_parse_json, return_dtype=pl.Object),
            pl.col("pieces").map_elements(_parse_json, return_dtype=pl.Object),
            pl.col("parts").map_elements(lambda x: _parse_json(x) or [], return_dtype=pl.Object),

            #packaging
            pl.col("packaging").map_elements(_transform_packaging, return_dtype=pl.Object),

            #documents
            pl.col("documents").map_elements(_transform_documents, return_dtype=pl.Object),

            #environment
            pl.col("environment").map_elements(lambda x: _parse_json(x) or [], return_dtype=pl.Object),

            #pricing
            pl.col("pricing").map_elements(_parse_json, return_dtype=pl.Object),

            #stocks
            pl.col("stocks").map_elements(lambda x: _parse_json(x) or [], return_dtype=pl.Object),




        ]
    )

    # Convert ID to string if needed for Typsense ID (Category does pl.col("id").cast(pl.Utf8) at the end)
    lf = lf.with_columns([
        pl.col("id").cast(pl.Utf8)
    ])

    # Select final columns
    final_cols = [
        "id", 
        "type", 
        "customs_code", 
        "ref", 
        "weight", 
        "barcode", 
        "comment", 
        "name", 
        "short_description", 
        "long_description", 
        "is_visible", 
        "is_obsolete", 
        "image", 
        "hs_code", 
        "meta_title", 
        "meta_description", 
        "original_references", 
        "d3e",
        "machine",
        "piece",
        "url",
        "brand",
        "categories",
        "extensions",
        "machines",
        "pieces",
        "parts",
        "packaging",
        "documents",
        "environment",
        "pricing",
        "stocks"
    ]
    
    lf = lf.select(final_cols)

    return lf
