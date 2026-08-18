---
name: avoiding-hotspots
category: query-schema-design
description: >
  Use when a user reports uneven load across ranges or nodes, a monotonically
  increasing indexed column, or asks how to prevent CockroachDB hotspots.
cockroach_versions: ">=23.1"
tags:
  - performance
  - schema-design
  - sharding
  - hotspots
requires_tools:
  - sql-execution
  - schema-inspection
  - index-inspection
  - explain-analyze
maintainers:
  - "@crdb-maintainer"
last_verified: "2026-08-18"
license: Apache-2.0
execution_mode: diagnostic
risk_level: low
---

# Avoiding Hotspots

## Trigger Conditions
- Uneven CPU or disk load across nodes in a cluster.
- Sequential primary keys (`INT8` auto-increment, `BIGSERIAL`, sequence, or timestamp PK).
- High range contention or single range leaseholder bottleneck.

## Required Information
- Table schema and primary key definition.
- Current index structure.
- Write pattern volume.

## Diagnosis Process
1. Inspect table primary key definition.
2. Check if primary key or leading index column is monotonically increasing (e.g. `AUTO INCREMENT`, `TIMESTAMP`, sequential `INT`).
3. Check range lease distribution for the target table.

## Tools Required
- `schema-inspection`
- `index-inspection`
- `sql-execution`
- `explain-analyze`

## SQL Queries

```sql
-- Query 1: Inspect primary key columns
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = '%TABLE_NAME%' AND column_name IN (
  SELECT kcu.column_name
  FROM information_schema.table_constraints tc
  JOIN information_schema.key_column_usage kcu
    ON tc.constraint_name = kcu.constraint_name
  WHERE tc.constraint_type = 'PRIMARY KEY' AND tc.table_name = '%TABLE_NAME%'
);

-- Query 2: Inspect Range leaseholders for table
SELECT range_id, lease_holder, start_key, end_key
FROM crdb_internal.ranges_no_leases
WHERE table_name = '%TABLE_NAME%';
```

## Interpretation Rules
- **Monotonic Key Risk**: If PK is sequential (e.g., `id INT DEFAULT unique_rowid()`, `BIGSERIAL`, `now()`), all concurrent inserts attempt to write to the highest key range on a single node leaseholder.
- **Solution 1 (UUID v4)**: Use UUID primary key generated via `gen_random_uuid()`. Distributes keys uniformly across all ranges/nodes.
- **Solution 2 (Hash Sharding)**: If sequential keys must be preserved for ordering, apply `USING HASH WITH (bucket_count = 16)` to the index or primary key.

## Recommended Fixes
Option A (Recommended for new tables):
```sql
ALTER TABLE %TABLE_NAME% ALTER COLUMN id SET DEFAULT gen_random_uuid();
```

Option B (For existing sequential PK tables):
```sql
ALTER TABLE %TABLE_NAME% ALTER PRIMARY KEY USING HASH WITH (bucket_count = 16);
```

## Safety Considerations
- Changing primary key requires rewriting table ranges or performing online schema change.

## Anti-Patterns
- Using sequential integer sequences or timestamps as primary keys in distributed SQL.

## Verification Steps
1. Verify schema change via `schema-inspection`.
2. Execute concurrent test inserts and confirm uniform distribution across range leaseholders via `SELECT lease_holder, count(*) FROM crdb_internal.ranges WHERE table_name = '%TABLE_NAME%' GROUP BY lease_holder;`.
