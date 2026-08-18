---
name: slow-query-triage
category: observability
description: >
  Use when triaging slow SQL queries, querying crdb_internal.node_statement_statistics,
  enabling statement logging, or finding resource-intensive queries.
cockroach_versions: ">=23.1"
tags:
  - observability
  - slow-query
  - statement-stats
  - performance-triage
requires_tools:
  - sql-execution
  - explain-analyze
maintainers:
  - "@crdb-maintainer"
last_verified: "2026-08-18"
license: Apache-2.0
execution_mode: diagnostic
risk_level: low
---

# Slow Query Triage

## Trigger Conditions
- Overall database query response times increase.
- High CPU utilization without an obvious hardware cause.

## Required Information
- Minimum execution time threshold for slow statement logging (default 100ms).

## Diagnosis Process
1. Query `crdb_internal.node_statement_statistics` sorted by mean service latency or total execution count.
2. Filter for queries performing full table scans.

## Tool Calls & SQL Queries

```sql
-- Step 1: Find top 5 slowest statements by mean latency
SELECT 
  statement, 
  count, 
  mean_service_latency, 
  rows_read_mean, 
  full_scan
FROM crdb_internal.node_statement_statistics
WHERE count > 5
ORDER BY mean_service_latency DESC
LIMIT 5;
```

## Recommended Action
1. Extract statement string from stats.
2. Invoke `explain-analyze-reading` skill to generate index recommendations.
3. Enable cluster slow statement logging:
```sql
SET CLUSTER SETTING sql.log.slow_query.threshold = '100ms';
```

## Verification Steps
1. Re-query statement stats after indexing to verify `mean_service_latency` reduction.
