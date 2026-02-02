def characteristics_machine_schema(collection_name: str) -> dict:
    """
    Typesense schema for the characteristics_machine collection.
    """
    return {
        "name": collection_name,
        "enable_nested_fields": True,
        "fields": [
            # Primary ID (Typesense requires string type for id)
            {"name": "id", "type": "string"},
            
            # Standard fields
            {"name": "type", "type": "string"},
            {"name": "symbol", "type": "string"},
            
            # Arrays (Lists)
            {"name": "product_ids", "type": "string[]"},
            
            # Translation objects
            {"name": "name", "type": "object"},
            {"name": "unit", "type": "object"},
        ],
    }
