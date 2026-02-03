def product_schema(collection_name: str):
    return {
        "name": collection_name,
        "fields": [
            # ID
            {"name": "id", "type": "string", "index": True},
            
            # Basic Fields
            {"name": "type", "type": "string", "index": False},
            {"name": "customs_code", "type": "string", "index": False},
            {"name": "ref", "type": "string", "index": False},
            {"name": "weight", "type": "float", "index": False},
            {"name": "barcode", "type": "string", "index": False},
            {"name": "comment", "type": "string", "index": False},
            {"name": "hs_code", "type": "string", "optional": True, "index": False},
            {"name":"brand","type":"string","index":False},

            # Booleans
            {"name": "is_visible", "type": "bool", "index": False},
            {"name": "is_obsolete", "type": "bool", "index": False},

            # Translations (Objects)
            {"name": "name", "type": "object", "index": True},
            {"name": "short_description", "type": "object", "index": False},
            {"name": "long_description", "type": "object", "index": False},
            {"name": "meta_title", "type": "object", "index": True},
            {"name": "meta_description", "type": "object", "index": False},
            {"name": "original_references", "type": "object", "index": False},
            {"name": "url", "type": "string", "optional": True, "index": False},

            # Image (Object)
            {"name": "image", "type": "object", "index": False},

            #d3e,machine and piece
            {"name": "d3e", "type": "object","index":False },
            {"name": "machine", "type": "object", "index":False},
            {"name": "piece", "type": "object", "index": False},
            
            # Extensions
            {"name": "extensions", "type": "object", "index": False},

            #Categories
            {"name": "categories", "type": "int32[]", "index": False},

            #Machines, pieces, parts
            {"name": "machines", "type": "int32[]", "index": False},
            {"name": "pieces", "type": "int32[]", "index": False},
            {"name": "parts", "type": "int32[]", "index": False},

            # Packaging
            {"name": "packaging", "type": "object", "index": False},

            # Documents
            {"name": "documents", "type": "object", "index": False , "optional": True},

            # Environment
            {"name": "environment", "type": "string[]", "index": False},

            #Pricing
            {"name": "pricing", "type": "object", "index": False},

            #Stocks
            {"name": "stocks", "type": "object[]", "index": False},

            #Machine characteristics
            {"name": "machine_characteristic", "type": "object[]", "index": False},






        ],
        "enable_nested_fields": True,
    }
