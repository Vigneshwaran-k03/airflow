from sqlalchemy.sql import Select
from sqlalchemy.dialects import mysql
import polars as pl
from common.mysql_connection import get_mysql_url


def select_to_polars(stmt: Select) -> pl.DataFrame:
    compiled = stmt.compile(
        dialect=mysql.dialect(),
        compile_kwargs={"literal_binds": True}
    )

    return pl.read_database_uri(
        query=str(compiled),
        uri=get_mysql_url("BOB_DB"),
    )
