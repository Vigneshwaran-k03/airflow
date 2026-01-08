import os
import mimetypes

def file_to_image_obj(filename: str, folder: str):
    """
    Convert a filename and folder to an image object dictionary.
    
    Args:
        filename (str): The name of the file.
        folder (str): The local folder path where the file is located.
        
    Returns:
        dict: A dictionary containing file details, or None if filename is invalid.
    """
    if not filename or not filename.strip():
        return None
        
    base_url = "https://files.swap-europe.com"
    url = f"{base_url}/{folder}/{filename}"
    mime_type, _ = mimetypes.guess_type(url) 
    return {
        "folder": folder,
        "file": filename,
        "url": url,
        "size": None,              
        "type": mime_type or "application/octet-stream"  
    }
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

