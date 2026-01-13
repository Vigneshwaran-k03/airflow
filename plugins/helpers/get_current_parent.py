import os
import mimetypes

def get_current_parent(parent_id, lookup):
    '''
    Return ONLY the immediate parent details. 

    Args:
        parent_id (int): The ID of the parent.
        lookup (dict): A dictionary of parent details.
        
    Returns:
        dict: A dictionary containing the parent details, or None if parent_id is invalid.
    '''
    if not parent_id:
        return None

    parent = lookup.get(parent_id)
    if not parent:
        return None

    return {
        "id": parent["id"],
        "name": parent["name"],
        "label": parent["label"],
        "picture": parent["picture"],
    }

