import json
def json_decode(json_str):
    if not json_str:
        return None
    return json.loads(json_str)