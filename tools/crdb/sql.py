from typing import Dict, Any, Optional, Tuple
from .client import CRDBClient

def execute_sql(
    query: str,
    params: Optional[Tuple[Any, ...]] = None,
    read_only: bool = True,
    confirm: bool = False,
    client: Optional[CRDBClient] = None
) -> Dict[str, Any]:
    """
    Execute SQL against CockroachDB with safety checks.
    Mutating statements (DROP, DELETE, TRUNCATE, ALTER) require confirm=True.
    """
    normalized = query.strip().upper()
    is_mutation = any(normalized.startswith(kw) for kw in ["DROP", "DELETE", "TRUNCATE", "ALTER", "UPDATE"])

    if is_mutation and read_only:
        return {
            "success": False,
            "error": "Security Restriction: Read-only execution mode is enabled. Set read_only=False and confirm=True to execute mutating SQL statements.",
            "tool": "execute_sql",
        }

    if is_mutation and not confirm:
        return {
            "success": False,
            "error": "Safety Confirmation Required: Mutating SQL operations require explicit confirmation parameter (confirm=True).",
            "tool": "execute_sql",
        }

    db = client or CRDBClient()
    result = db.execute_query(query, params)
    result["tool"] = "execute_sql"
    return result
