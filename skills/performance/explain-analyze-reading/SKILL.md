---
name: explain-analyze-reading
category: performance
description: >
  Use when analyzing SQL query performance regressions, reading EXPLAIN (ANALYZE) plans,
  detecting full table scans, or identifying memory spilling and cross-region latencies.
cockroach_versions: ">=23.1"
tags:
  - performance
  - explain-analyze
  - query-tuning
  - query-plan
requires_tools:
  - sql-execution
  - explain-analyze
  - schema-inspection
  - index-inspection
maintainers:
  - "@crdb-maintainer"
last_verified: "2026-08-18"
license: Apache-2.0
execution_mode: diagnostic
risk_level: low
---

# Reading EXPLAIN ANALYZE

## When to Use
- User asks why a query is slow or requests analysis of execution plan output.
- Performance triage reveals high execution times or unexpected memory usage.

## Required Context
- Target SQL query statement.
- Relevant table schemas and indexes.

## Diagnosis Process
1. Execute `EXPLAIN (ANALYZE, DISTSQL) <query>` via `explain-analyze` tool.
2. Scan physical plan tree for red flags:
   - `scan` method = `full` (Full Table Scan instead of Index Scan).
   - `spilled` = `true` (Sort or HashJoin ran out of RAM and spilled to disk).
   - `cross-region` RPC count > 0 (Network latency bottleneck between nodes).

## Tool Calls & SQL Queries

```sql
EXPLAIN (ANALYZE, DISTSQL) SELECT * FROM orders WHERE customer_id = 'c123' ORDER BY created_at DESC LIMIT 10;
```

## Interpretation Rules
- **Full Scan Flag**: If plan displays `render -> scan orders (full scan)`, no usable index matched `customer_id`. Create secondary index on `(customer_id)`.
- **Index Scan + Covering**: If plan displays `scan orders @ idx_cust_created (index scan, covering)`, all required columns reside in the index without primary key lookup fanout.

## Recommended Fix
Add a covering secondary index matching filter and sort order:
```sql
CREATE INDEX idx_orders_customer_created ON orders (customer_id, created_at DESC) STORING (total_amount, status);
```

## Verification Steps
1. Re-run `EXPLAIN (ANALYZE, DISTSQL)` on target query.
2. Confirm plan scan method changes from `full scan` to `index scan (covering)`.
3. Compare execution time reduction.
