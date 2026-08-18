from tools.crdb.client import CRDBClient
from tools.crdb.sql import execute_sql
from tools.crdb.explain import explain_analyze
from tools.crdb.schema import get_schema
from tools.crdb.indexes import get_indexes
from tools.crdb.cluster import get_cluster_metadata
from tools.crdb.vector import vector_search

def test_execute_sql_readonly():
    res = execute_sql("SELECT 1;", read_only=True)
    assert res["success"] is True
    assert res["tool"] == "execute_sql"

def test_execute_sql_mutation_blocked_without_confirm():
    res = execute_sql("DROP TABLE users;", read_only=False, confirm=False)
    assert res["success"] is False
    assert "Safety Confirmation Required" in res["error"]

def test_execute_sql_mutation_allowed_with_confirm():
    res = execute_sql("CREATE TABLE IF NOT EXISTS test_t (id INT);", read_only=False, confirm=True)
    assert res["success"] is True

def test_explain_analyze():
    res = explain_analyze("SELECT * FROM users WHERE id = 'u1';")
    assert res["success"] is True
    assert res["tool"] == "explain_analyze"
    assert "rows" in res

def test_get_schema():
    res = get_schema("users")
    assert res["success"] is True
    assert res["table_name"] == "users"

def test_get_indexes():
    res = get_indexes("users")
    assert res["success"] is True
    assert res["table_name"] == "users"

def test_get_cluster_metadata():
    res = get_cluster_metadata()
    assert res["success"] is True
    assert "cluster_info" in res

def test_vector_search():
    res = vector_search("agent_memory", "embedding", [0.1, 0.2, 0.3])
    assert res["success"] is True
    assert res["tool"] == "vector_search"
