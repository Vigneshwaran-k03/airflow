import polars as pl
from helpers.file_to_img_obj import file_to_image_obj
from helpers.jsonString_json import json_decode
from helpers.product_extensions_transform import _transform_extensions
from services.pricing.transformations import build_datetime_object
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

def _clean_characteristics(value):
    data = _parse_json(value)
    if not data:
        return []

    cleaned = []
    for item in data:
        if not isinstance(item, dict):
            continue

        if "value_tr" in item and isinstance(item["value_tr"], str):
            try:
                decoded = json_decode(item["value_tr"])
                if isinstance(decoded, dict):
                    item["value_tr"] = {
                        k: (v if v is not None else "")
                        for k, v in decoded.items()
                    }
            except Exception:
                item["value_tr"] = None
                
        # Remove keys with None values
        item = {k: v for k, v in item.items() if v is not None}

        cleaned.append(item)

    return cleaned

def _transform_suppliers(value):
    data = _parse_json(value)
    if not data:
        return []

    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                 # Transform date
                if "update_date" in item:
                    item["update_date"] = build_datetime_object(item["update_date"])
                
                # Ensure fields are present as per user request (though query handles most)
                # But JSON from SQL might have nulls where we want specific defaults? 
                # User didn't specify defaults effectively, but let's trust SQL for now.
                pass
    return data

def _transform_images(value):
    data = _parse_json(value)
    if not data:
        return []

    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                # Transform file path to image object
                if "file" in item and item["file"]:
                     item["file"] = file_to_image_obj(item["file"], PHOTO_FOLDER) or {}
                else:
                    item["file"] = {} # ensure empty object if no file

    return data


def _transform_videos(value):
    data = _parse_json(value)
    if not data:
        return []

    cleaned = []
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                # Process title translation if it exists
                if "title" in item and isinstance(item["title"], str):
                    try:
                        decoded = json_decode(item["title"])
                        if isinstance(decoded, dict):
                            item["title"] = {
                                k: (v if v is not None else "")
                                for k, v in decoded.items()
                            }
                    except Exception:
                        item["title"] = None
                
                # Replace None with "" for all other fields
                item = {k: (v if v is not None else "") for k, v in item.items()}
                cleaned.append(item)
    
    return cleaned


def _transform_refurbished(data):
    if not data:
        return None
    
    id_machine = data.get("id_machine") or 0
    id_piece = data.get("id_piece") or 0
    
    if id_machine > 0 and id_piece > 0:
        ref = data.get("ref") or ""
        # Check first letter
        first_char = ref[0] if ref else ""
        grade = " "
        if first_char in ['X', 'Y', 'Z', 'R']:
            grade = first_char
        
        original_product = data.get("original_product_id")
        if original_product is None:
            original_product = ""
            
        return {
            "grade": grade,
            "original_product": original_product
        }
    
    return None


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
            pl.when((pl.col("id_machine").cast(pl.Int64) > 0) & (pl.col("id_piece").cast(pl.Int64) == 0))
            .then(pl.lit("machine"))
            .when((pl.col("id_machine").cast(pl.Int64) == 0) & (pl.col("id_piece").cast(pl.Int64) > 0))
            .then(pl.lit("piece"))
            .when((pl.col("id_machine").cast(pl.Int64) > 0) & (pl.col("id_piece").cast(pl.Int64) > 0))
            .then(pl.lit("refurbished"))
            .otherwise(
                pl.col("type").str.to_lowercase()
            )
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
            ),
            
            pl.col("image")
            .map_elements(
                lambda x: file_to_image_obj(x, PHOTO_FOLDER) or {}, return_dtype=pl.Object
            ).alias("best_image"),

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

            #machine_characteristics
            pl.col("machine_characteristics").map_elements(_clean_characteristics, return_dtype=pl.Object),

            #piece_characteristics
            pl.col("piece_characteristics").map_elements(_clean_characteristics, return_dtype=pl.Object),

            #suppliers
            pl.col("suppliers").map_elements(_transform_suppliers, return_dtype=pl.Object),

            # in_stock
            pl.col("in_stock").cast(pl.Boolean).fill_null(False),

            # resupplies
            pl.col("resupplies").map_elements(lambda x: _parse_json(x) or [], return_dtype=pl.Object),

            # images
            pl.col("images").map_elements(_transform_images, return_dtype=pl.Object),

            # accessories
            pl.col("accessories").map_elements(lambda x: _parse_json(x) or [], return_dtype=pl.Object),

            # alternatives
            pl.col("alternatives").map_elements(lambda x: _parse_json(x) or [], return_dtype=pl.Object),

    # videos
            pl.col("videos").map_elements(_transform_videos, return_dtype=pl.Object),

            # refurbished
            pl.struct(["id_machine", "id_piece", "ref", "original_product_id"])
            .map_elements(_transform_refurbished, return_dtype=pl.Object)
            .alias("refurbished"),

            # best_brand
            pl.lit("", dtype=pl.Utf8).alias("best_brand"),

            # aliases
            pl.col("aliases").map_elements(lambda x: _parse_json(x) or [], return_dtype=pl.Object),
            
            # search_aliases
            pl.col("aliases")
            .map_elements(lambda x: _parse_json(x) or [], return_dtype=pl.Object)
            .map_elements(
                lambda aliases: " ".join([a.get("alias", "") for a in aliases if isinstance(a, dict) and a.get("alias")]),
                return_dtype=pl.Utf8
            )
            .fill_null(" ")
            .alias("search_aliases"),

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
        "best_image",
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
        "stocks",
        "machine_characteristics",
        "piece_characteristics",
        "suppliers",
        "in_stock",
        "resupplies",
        "images",
        "accessories",
        "alternatives",
        "videos",
        "refurbished",
        "best_brand",
        "aliases",
        "search_aliases"
    ]
    
    lf = lf.select(final_cols)

    return lf
