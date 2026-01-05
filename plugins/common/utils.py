import shutil
import os

def delete_directory_by_path(dir_path):
    try:
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
            print(f"Successfully deleted directory: {dir_path}")
        else:
            print(f"Directory does not exist: {dir_path}")
    except PermissionError:
        print(f"Permission denied: {dir_path}")
    except OSError as e:
        print(f"✗ Error deleting {dir_path}: {e}")