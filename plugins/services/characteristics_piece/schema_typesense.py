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
            {"name": "technical_branch_id", "type": "int32","reference": "technical_branches.id"},
            {"name": "type", "type": "string"},
            {"name": "symbol", "type": "string", "optional": True},
            
            # Arrays (Lists)
            {"name": "products_ids", "type": "int32[]", "optional": True,"reference": "products.id"},
            
            # Translation objects
            {"name": "name", "type": "object", "optional": True},
            {"name": "unit", "type": "object", "optional": True},
        ],
    }
