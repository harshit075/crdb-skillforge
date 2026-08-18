---
name: disaster-recovery
category: operations
description: >
  Use when planning or executing disaster recovery procedures, handling multi-region failover,
  or recovering from regional outages with zero data loss.
cockroach_versions: ">=23.1"
tags:
  - operations
  - disaster-recovery
  - failover
  - high-availability
requires_tools:
  - sql-execution
  - cluster-metadata
maintainers:
  - "@crdb-maintainer"
last_verified: "2026-08-18"
license: Apache-2.0
execution_mode: operational
risk_level: high
---

# Disaster Recovery

## When to Use
- A full cloud region suffers an outage and range leaseholders must failover to surviving regions.
- Recovering data state using point-in-time recovery (PITR) or cluster backups.

## Required Context
- Cluster topology across availability zones and regions.
- Target RPO (Recovery Point Objective) and RTO (Recovery Time Objective).

## Diagnosis Process
1. Query node health status across regions.
2. Check range lease distribution and unavailable range count.

## Tool Calls & SQL Queries

```sql
-- Step 1: Inspect node availability by region
SELECT node_id, locality, is_live 
FROM crdb_internal.gossip_nodes;

-- Step 2: Check for unavailable ranges
SELECT count(*) FROM crdb_internal.ranges WHERE array_length(unreachable_replicas, 1) > 0;
```

## Recommended Action
In a multi-region cluster with survival goals (`ZONE` or `REGION`), CockroachDB automatically transfers leaseholders away from dead nodes to surviving regions without manual intervention.

If forcing primary region change for database:
```sql
ALTER DATABASE defaultdb PRIMARY REGION "us-west-2";
```

## Verification Steps
1. Verify `SELECT count(*) FROM crdb_internal.ranges WHERE is_healthy = false;` returns 0.
