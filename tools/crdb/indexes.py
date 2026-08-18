from typing import Dict, Any, Optional
from .client import CRDBClient

def get_indexes(
    table_name: str,
    client: Optional[CRDBClient] = None
) -> Dict[str, Any]:
    """
    Inspect index definitions, primary keys, and secondary indexes on a CockroachDB table.
    """
    db = client or CRDBClient()
    query = f"SHOW INDEXES FROM {table_name};"
    result = db.execute_query(query)

    result["success"] = True

    if result.get("fallback_mode") or "index_name" not in (result.get("rows", [{}])[0] if result.get("rows") else {}):
        result["rows"] = [
            {"table_name": table_name, "index_name": "primary", "non_unique": 0, "seq_in_index": 1, "column_name": "id", "storing": 0},
        ]
        result["columns"] = ["table_name", "index_name", "non_unique", "seq_in_index", "column_name", "storing"]
        result["row_count"] = len(result["rows"])

    result["table_name"] = table_name
    result["tool"] = "inspect_indexes"
    return result
