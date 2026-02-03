def technical_schema(collection_name: str):
    return {
        "name": collection_name,
        "fields": [
            {"name": "id", "type": "string"},
            {"name": "parent_id", "type": "int32", "optional": True},
            {"name": "parent", "type": "object", "optional": True},
            {"name": "parent_ids", "type": "int32[]", "optional": True},
            {"name": "environments", "type": "string[]", "optional": True},

            {"name": "name", "type": "object"},
            {"name": "url", "type": "object"},
            {"name": "label", "type": "object"},

            {"name": "weight", "type": "float"},
            {"name": "is_consumable", "type": "bool"},
            {"name": "is_accessory", "type": "bool"},
            {"name": "is_other", "type": "bool"},
            {"name": "packaging", "type": "string", "optional": True},
            {"name": "is_visible", "type": "bool"},

            {"name": "hs_code", "type": "string", "optional": True},
            {"name": "score", "type": "int32"},

            {"name": "image", "type": "object"},
            {"name": "picture", "type": "object"},
        ],
        "enable_nested_fields": True,
    }
