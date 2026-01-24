from helpers.jsonString_json import json_decode
from helpers.file_to_img_obj import file_to_image_obj
PHOTO_FOLDER = "photos"


def _parse_json(value):
    if not value:
        return None

    try:
        data = json_decode(value)
    except Exception:
        return None

    if not data:
        return None

    # Replace None with "" in the dictionary
    if isinstance(data, dict):
        data = {k: (v if v is not None else "") for k, v in data.items()}

    return data

def _transform_extensions(value):
    if not value:
        return None
    
    try:
        data_list = json_decode(value)
    except Exception:
        return None
        
    if not data_list or not isinstance(data_list, list):
        return None
        
    result = {}
    
    for item in data_list:
        label = item.get("label")
        raw_data = item.get("data")
        
        if not label or not raw_data:
            continue
            
        clean_data = {}
        
        # Simple fields (Direct copy if not empty)
        for field in ["reference", "currency_id", "url", "score", "review_count", "average_rating", "default_category_id", "forced_sale_duration"]:
            val = raw_data.get(field)
            if val is not None and str(val) != "": 
                clean_data[field] = val
                
        # Booleans (Keep explicit True/False)
        for field in ["is_visible", "has_forced_price"]:
            val = raw_data.get(field)
            if val is not None:
                clean_data[field] = bool(val)

        # Dates (Keep as string if present)
        for field in ["discount_start_date", "discount_end_date"]:
            val = raw_data.get(field)
            if val:
                clean_data[field] = str(val)

        # Price Calculation
        price = raw_data.get("price")
        tax_rate = raw_data.get("tax_rate") or 0
        discount_price = raw_data.get("discount_price")
        
        if price is not None:
            clean_data["price"] = float(price)
            # price_taxed
            try:
                tax_mult = 1 + (float(tax_rate) / 100)
                clean_data["price_taxed"] = float(price) * tax_mult
            except:
                pass
                
        if discount_price is not None:
            clean_data["discount_price"] = float(discount_price)
            # discount_price_taxed
            try:
                tax_mult = 1 + (float(tax_rate) / 100)
                clean_data["discount_price_taxed"] = float(discount_price) * tax_mult
            except:
                pass

        # Image
        img_val = raw_data.get("img")
        if img_val:
            img_obj = file_to_image_obj(img_val, PHOTO_FOLDER)
            if img_obj:
                clean_data["img"] = img_obj
                
        # Translations - KEEP AS OBJECTS but clean empty keys
        translation_fields = ["name", "meta_title", "meta_description", "short_description", "long_description", "specificities", "original_references"]
        
        name_obj_for_search = None
        
        for field in translation_fields:
            t_val_str = raw_data.get(field)
            parsed_t = _parse_json(t_val_str) # Returns dict {fr:"", en:""...} or None
            
            if parsed_t and isinstance(parsed_t, dict):
                # Clean empty keys
                cleaned_t = {k: v for k, v in parsed_t.items() if v and str(v).strip()}
                
                if cleaned_t:
                    clean_data[field] = cleaned_t
                    if field == "name":
                        name_obj_for_search = cleaned_t

        # Search Title Construction (String)
        reference = raw_data.get("reference") or ""
        search_title_parts = []
        
        if name_obj_for_search:
            # Extract best name for search title string: fr > en > first
            best_str = name_obj_for_search.get("fr") or name_obj_for_search.get("en")
            if not best_str:
                 for val in name_obj_for_search.values():
                     if val:
                         best_str = val
                         break
            if best_str:
                search_title_parts.append(str(best_str).strip())
        
        if reference and str(reference).strip():
            search_title_parts.append(str(reference).strip())
            
        search_title = " ".join(search_title_parts)
        if search_title.strip():
             clean_data["search_title"] = f" {search_title} " 
        
        # Final cleanup for this label group
        final_block = {k: v for k, v in clean_data.items() if v not in [None, ""]}
        final_block = {k: v for k, v in final_block.items() if not (isinstance(v, dict) and not v)}

        if final_block:
            result[label] = final_block

    return result or None
