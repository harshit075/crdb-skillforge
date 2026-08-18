---
name: index-recommendations
category: performance
description: >
  Use when recommending optimal secondary, inverted, or covering indexes for slow queries,
  or identifying unused/duplicate indexes inflating write amplification.
cockroach_versions: ">=23.1"
tags:
  - performance
  - indexing
  - covering-index
  - query-optimization
requires_tools:
  - sql-execution
  - schema-inspection
  - index-inspection
  - explain-analyze
maintainers:
  - "@crdb-maintainer"
last_verified: "2026-08-18"
license: Apache-2.0
execution_mode: recommendation
risk_level: low
---

# Index Recommendations

## When to Use
- Recommending composite secondary indexes, covering indexes using `STORING (...)`, or partial indexes.
- Identifying unused or redundant indexes in CockroachDB tables.

## Required Context
- Table schema and query workload metrics.

## Diagnosis Process
1. Inspect existing table indexes via `index-inspection`.
2. Inspect index usage statistics in `crdb_internal.index_usage_statistics`.

## Tool Calls & SQL Queries

```sql
-- Step 1: Check index usage statistics
SELECT table_name, index_name, total_reads, last_read 
FROM crdb_internal.index_usage_statistics 
WHERE table_name = '%TABLE_NAME%';
```

## Recommended Action
Create covering index:
```sql
CREATE INDEX idx_user_status ON users (status) STORING (email, last_login);
```

Drop unused index (after safety audit):
```sql
DROP INDEX %TABLE_NAME%@%INDEX_NAME%;
```

## Verification Steps
1. Re-query `crdb_internal.index_usage_statistics` to confirm reads hit new index.
