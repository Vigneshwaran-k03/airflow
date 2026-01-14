def typesense_schema(collection_name: str = "service") -> dict:
    return {
        "name": collection_name,
        "fields": [
            {"name": "id", "type": "string"},
            {"name": "admin_id", "type": "int32"},

            {"name": "name", "type": "object"},
            {"name": "title", "type": "object"},
            {"name": "description", "type": "object"},
            {"name": "search_title", "type": "object"},

            {"name": "swap_description", "type": "object", "optional": True},

            {"name": "is_for_particular", "type": "int32"},
            {"name": "is_for_repairer", "type": "int32"},
            {"name": "is_for_seller", "type": "int32"},
            {"name": "logistic_fee", "type": "int32"},
            {"name": "is_reserved", "type": "int32"},
            {"name": "order", "type": "int32"},
            {"name": "is_service_ticket", "type": "int32"},

            {"name": "image", "type": "string", "optional": True},
            {"name": "swap_image", "type": "string", "optional": True},
            {"name": "admin", "type": "object", "optional": True},

            {"name": "category_id", "type": "int32"},
            {"name": "landing", "type": "string", "optional": True},
            {"name": "environment", "type": "string[]"},
        ],
        "default_sorting_field": "order",
        "enable_nested_fields": True,
    }
