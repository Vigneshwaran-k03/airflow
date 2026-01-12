def typesense_schema(collection_name: str):

    return {
        "name": collection_name,
       
        "fields": [
            # Identifiers
            {"name": "id", "type": "string"},
            {"name": "parent_id", "type": "int32", "optional": True},
            
            #parents
            {"name": "parent", "type": "object"},
            {"name": "parent_ids", "type": "int32[]"},

            #environment
            {"name": "environment", "type": "string"},
            {"name": "id_environment", "type": "int32"},
            
            #linktype
            {"name": "link_type", "type": "string"},

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
            {"name": "alias", "type": "string"},
            {"name": "score", "type": "int32"},
            {"name": "event", "type": "string"},

            # Translations (flattened later in transform step)
            {"name": "name", "type": "object"},
            {"name": "generated_title", "type": "object", "optional": True},
            {"name": "search_title", "type": "object"},
            {"name": "label", "type": "object"},
            {"name": "title", "type": "object"},
            {"name": "description", "type": "object"},
            {"name": "long_description", "type": "object"},
            {"name": "meta_title", "type": "object"},
            {"name": "meta_description", "type": "object"},

            #images 
            {"name": "icon", "type": "object"},
            {"name": "picture", "type": "object"},

        ],
        "enable_nested_fields": True,
    }
