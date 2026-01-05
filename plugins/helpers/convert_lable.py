import re
import polars as pl

def get_label(name: str) -> str:
    if not name:
        return ""
    s = name.lower()
    s = re.sub(r"[^a-z]+", "-", s)
    return s.strip("-")
