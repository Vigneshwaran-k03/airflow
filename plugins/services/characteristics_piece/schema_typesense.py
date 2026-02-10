def characteristics_piece_schema(collection_name: str) -> dict:
    """
    Typesense schema for the characteristics_piece collection.
    """
    return {
        "name": collection_name,
        "enable_nested_fields": True,
        "fields": [
            # Primary ID (Typesense requires string type for id)
            {"name": "id", "type": "string"},
            
            # Standard fields
            {"name": "technical_branch_id", "type": "string", "reference": "technical_branches.id"},
            {"name": "type", "type": "string"},
            {"name": "symbol", "type": "string"},
            
            # Arrays (Lists)
            {"name": "products_ids", "type": "string[]","reference": "products.id"},
            
            # Translation objects
            {"name": "name", "type": "object"},
            {"name": "unit", "type": "object"},
        ],
    }
