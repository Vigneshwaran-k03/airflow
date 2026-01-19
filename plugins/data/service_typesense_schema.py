SERVICE_SCHEMA = {
    "name": "services",
    "fields": [
        {"name": "id", "type": "string"},
        {"name": "admin_id", "type": "int32", "optional": True},
        {"name": "title", "type": "string"},
        {"name": "description", "type": "string", "optional": True},
        {"name": "is_for_particular", "type": "bool"},
        {"name": "is_for_repairer", "type": "bool"},
        {"name": "is_for_seller", "type": "bool"},
        {"name": "logistic_fee", "type": "float", "optional": True},
        {"name": "is_reserved", "type": "bool"},
        {"name": "order", "type": "int32", "optional": True},
        {"name": "is_service_ticket", "type": "bool"},
        {"name": "image", "type": "string", "optional": True},
        {"name": "category_id", "type": "int32", "optional": True},
        {"name": "landing", "type": "string", "optional": True},
        {"name": "name", "type": "string"},
        {"name": "swap_description", "type": "string", "optional": True},
        {"name": "swap_image", "type": "string", "optional": True},
        {"name": "environment", "type": "string[]"},
        {"name": "search_title", "type": "string", "optional": True},
        {"name": "translations_fr", "type": "string", "optional": True},
        {"name": "translations_en", "type": "string", "optional": True}
    ],
    #"default_sorting_field": "id"
}
