from tools.crdb.client import CRDBClient
from tools.crdb.sql import execute_sql

def test_database_connection_and_table_queries():
    client = CRDBClient()
    conn = client.get_connection()
    assert conn is not None

    res = execute_sql("SELECT count(*) FROM users;", client=client)
    assert res["success"] is True
    assert res["row_count"] >= 1
