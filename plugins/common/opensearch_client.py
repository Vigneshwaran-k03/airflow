from airflow.sdk.bases.hook import BaseHook
from opensearchpy import OpenSearch


def get_opensearch_client(
    conn_id: str = "opensearch_db", is_local: bool = False
) -> OpenSearch:
    # Fetch connection from Airflow
    conn = BaseHook.get_connection(conn_id)

    # Create OpenSearch client
    client = None
    if is_local:
        client = OpenSearch(
            hosts=[{"host": conn.host, "port": conn.port}],
            http_auth=(conn.login, " D0cker#OpenSearch"),
            use_ssl=True,
            verify_certs=False,
            ssl_assert_hostname=False,
            ssl_show_warn=False,
        )
    else:
        client = OpenSearch(
            hosts=[{"host": conn.host, "port": int(conn.port)}],
            http_auth=(conn.login, conn.password),
            use_ssl=True,
            verify_certs=True,
        )
    return client
