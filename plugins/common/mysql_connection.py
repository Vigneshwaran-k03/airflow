from airflow.sdk.bases.hook import BaseHook
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_mysql_session(conn_id: str):
    conn = BaseHook.get_connection(conn_id)

    engine = create_engine(
        f"mysql+mysqlconnector://{conn.login}:{conn.password}@{conn.host}:{conn.port}/{conn.schema}"
        "?charset=utf8mb4"
    )

    Session = sessionmaker(bind=engine)
    return Session()

def get_mysql_url(conn_id: str):
    conn = BaseHook.get_connection(conn_id)
    return f"mysql://{conn.login}:{conn.password}@{conn.host}:{conn.port}/{conn.schema}" 

def get_mysql_connection(conn_id: str):
    conn = BaseHook.get_connection(conn_id)

    engine = create_engine(
        f"mysql+mysqlconnector://{conn.login}:{conn.password}@{conn.host}:{conn.port}/{conn.schema}"
        "?charset=utf8mb4"
    )
    Connection = engine.connect()
    return Connection
