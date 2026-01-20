def pricing_schema(collection_name: str) -> dict:
    """
    Typesense schema for the pricing collection.
    
    Based on the tarifs table structure with fields for searching and filtering.
    """
    return {
        "name": collection_name,
        "enable_nested_fields": True,
        "fields": [
            # Primary ID (Typesense requires string type for id)
            {"name": "id", "type": "string"},
            
            # Foreign keys and identifiers
            {"name": "company_id", "type": "int32"},
            {"name": "vio_machine_id", "type": "int32"},
            {"name": "code", "type": "string"},
            
            # Pricing and thresholds
            {"name": "reduction", "type": "float"},
            {"name": "free_shipping_threshold", "type": "float"},
            {"name": "products_threshold", "type": "int32"},
            
            # Boolean flags
            {"name": "has_free_shipping", "type": "bool"},
            {"name": "is_enabled", "type": "bool"},
            {"name": "has_all_products", "type": "bool"},
            {"name": "has_all_entities", "type": "bool"},
            {"name": "is_shop", "type": "bool"},
            {"name": "is_overriding_fixed_price", "type": "bool"},
            
            # Enum fields (stored as strings)
            {"name": "products_type", "type": "string"},
            {"name": "entities_type", "type": "string"},
            {"name": "query", "type": "string"},
            
            # Translation object
            {"name": "name", "type": "object"},
            
            # Company details object
            {"name": "company", "type": "object"},
            
            # Environment array
            {"name": "environment", "type": "string[]"},

            # VIO Machine
            {"name": "vio_machine", "type": "int32"},

            #dates
            {"name": "start_date", "type": "object"},
            {"name": "end_date", "type": "object"},


        ],
        
    }
    
