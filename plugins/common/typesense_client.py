from airflow.sdk.bases.hook import BaseHook
import typesense


def get_typesense_client(conn_id: str = "typesense_conn") -> typesense.Client:
    # Fetch connection from Airflow
    conn = BaseHook.get_connection(conn_id)

    # Create Typesense client
    client = typesense.Client(
        {
            "nodes": [
                {
                    "host": conn.host,
                    "port": int(conn.port),
                    "protocol": "http",
                }
            ],
            "api_key": conn.password,
            "connection_timeout_seconds": 10,
        }
    )

    return client
