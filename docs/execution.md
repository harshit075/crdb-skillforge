# Tool Execution Layer Guide

The tool execution layer (`tools/crdb/`) provides safe Python functions for interacting with CockroachDB instances:

```python
from tools.crdb.sql import execute_sql
from tools.crdb.explain import explain_analyze
from tools.crdb.schema import get_schema
from tools.crdb.indexes import get_indexes
from tools.crdb.cluster import get_cluster_metadata
from tools.crdb.vector import vector_search
```

## Security & Safety Controls

1. **Read-Only Defaults**: Diagnostic tools operate read-only by default.
2. **Mutation Confirmations**: Destructive statements (DROP, ALTER, DELETE) require `read_only=False` and `confirm=True`.
3. **Dual Execution Engine**:
   - Primary: Live PostgreSQL/CockroachDB driver (`psycopg2`/`psycopg3`).
   - Fallback: Embedded in-memory SQL execution engine for offline tests and CI runners.
