import os
import shutil


def clear_dir(output_dir: str):
    """
    Safely remove all files and subdirectories inside output_dir.
    """
    if not output_dir:
        raise ValueError("output_dir is empty")

    output_dir = os.path.abspath(output_dir)

    # Safety checks
    if output_dir in ("/", "/root", "/home", "/opt", "/usr"):
        raise ValueError(f"Refusing to clear unsafe directory: {output_dir}")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        return

    for name in os.listdir(output_dir):
        path = os.path.join(output_dir, name)
        if os.path.isfile(path) or os.path.islink(path):
            os.unlink(path)
        else:
            shutil.rmtree(path)
