---
name: multi-region-table-design
category: query-schema-design
description: >
  Use when designing or optimizing tables across multi-region CockroachDB clusters
  using REGIONAL BY ROW, REGIONAL BY TABLE, or GLOBAL tables for low latency.
cockroach_versions: ">=23.1"
tags:
  - multi-region
  - locality
  - schema-design
requires_tools:
  - sql-execution
  - schema-inspection
  - cluster-metadata
maintainers:
  - "@crdb-maintainer"
last_verified: "2026-08-18"
license: Apache-2.0
execution_mode: recommendation
risk_level: medium
---

# Multi-Region Table Design

## When to Use
- Deploying tables across multiple cloud regions (e.g. `us-east-1`, `us-west-2`, `eu-west-1`).
- Optimizing table locality patterns for fast local reads and compliant data residency.

## Required Context
- Table read/write access patterns per region.
- Database regions configuration (`SHOW REGIONS FROM DATABASE`).

## Diagnosis Process
1. Inspect database regions.
2. Check table locality setting.

## Tool Calls & SQL Queries

```sql
-- Step 1: Check database regions
SHOW REGIONS FROM DATABASE;

-- Step 2: Check table locality
SHOW CREATE TABLE %TABLE_NAME%;
```

## Interpretation Rules
- `REGIONAL BY ROW`: Best for multi-tenant data where rows belong to specific regions (e.g. `crdb_region`). Gives local read/write latency.
- `GLOBAL`: Best for read-heavy reference tables updated infrequently. Gives sub-millisecond reads anywhere.
- `REGIONAL BY TABLE`: Pins entire table data to the primary region of the database or table.

## Recommended Fix
Configure row locality:
```sql
ALTER TABLE user_profiles SET LOCALITY REGIONAL BY ROW AS crdb_region;
```
Or set GLOBAL for reference data:
```sql
ALTER TABLE currency_rates SET LOCALITY GLOBAL;
```

## Safety Considerations
- Changing table locality reorganizes leaseholders and ranges across regions, incurring background network traffic during rebalancing.

## Verification Steps
1. Execute `SHOW CREATE TABLE %TABLE_NAME%;`.
2. Confirm table locality clause.
