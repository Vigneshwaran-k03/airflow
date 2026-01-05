def typesense_schema(collection_name: str):

    return {
        "name": collection_name,
        "fields": [
            # Identifiers
            {"name": "id", "type": "int32"},
            {"name": "parent_id", "type": "int32", "optional": True},
            {"name": "root_parent_id", "type": "int32", "optional": True},

            # Ordering
            {"name": "order", "type": "int32"},

            # Flags
            {"name": "is_visible", "type": "bool"},
            {"name": "is_enabled", "type": "bool"},
            {"name": "is_clickable", "type": "bool"},
            {"name": "has_pieces_displayed", "type": "int32"},
            {"name": "is_reconditioned", "type": "bool"},
            {"name": "is_excluded_from_naming", "type": "bool"},
            {"name": "is_visible_menu", "type": "bool"},
            {"name": "has_generated_children", "type": "bool"},

            # Misc fields
            {"name": "alias", "type": "string", "optional": True},
            {"name": "score", "type": "int32", "optional": True},
            {"name": "event", "type": "string", "optional": True},

            # Translations (flattened later in transform step)
            {"name": "name", "type": "string"},
            {"name": "label", "type": "string"},
            {"name": "title", "type": "string"},
            {"name": "description", "type": "string"},
            {"name": "long_description", "type": "string"},
            {"name": "meta_title", "type": "string"},
            {"name": "meta_description", "type": "string"},
        ],
        "default_sorting_field": "order",
    }
