def universal_schema(collection_name: str):
    return {
        "name": collection_name,
        "fields": [
            {"name": "id", "type": "string"},

            {"name": "parent_id", "type": "int32", "optional": True},
            {"name": "parent", "type": "object", "optional": True},
            {"name": "parent_ids", "type": "int32[]", "optional": True},

            {"name": "name", "type": "object"},
            {"name": "label", "type": "object"},
            {"name": "summary", "type": "object", "optional": True},
            {"name": "alias", "type": "object", "optional": True},
            {"name": "alias_slugified", "type": "string", "optional": True},

            {"name": "image", "type": "object", "optional": True},
            {"name": "default_machine_img", "type": "string", "optional": True},

            {"name": "background", "type": "object", "optional": True},
            {"name": "icon", "type": "object", "optional": True},

            {"name": "customs_code", "type": "string", "optional": True},
            {"name": "average_weight", "type": "float", "optional": True},
            {"name": "has_battery", "type": "bool"},
            {"name": "depreciation_rate", "type": "float"},
            {"name": "is_visible_front", "type": "bool"},

            {"name": "environment", "type": "string[]", "optional": True},
        ],
        "enable_nested_fields": True,
    }
