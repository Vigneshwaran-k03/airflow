from sqlalchemy import cast, String, func
from sqlalchemy.sql.elements import ClauseElement


def json_as_string(expr: ClauseElement, label: str):
    """
    Force JSON expressions to STRING for Polars-safe ingestion.
    """
    return cast(expr, String).label(label)


def group_concat_as_string(expr: ClauseElement, label: str):
    """
    Force GROUP_CONCAT expressions to STRING for Polars-safe ingestion.
    """
    return cast(func.group_concat(expr), String).label(label)
