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
