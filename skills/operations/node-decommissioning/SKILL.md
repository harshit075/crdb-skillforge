---
name: node-decommissioning
category: operations
description: >
  Use when safely removing, replacing, or decommissioning a CockroachDB cluster node
  while transferring range replicas and leaseholders to remaining nodes.
cockroach_versions: ">=23.1"
tags:
  - operations
  - node-decommissioning
  - cluster-rebalancing
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

# Node Decommissioning

## When to Use
- Decommissioning a node for hardware replacement or down-scaling cluster capacity.

## Required Context
- Target `node_id` to decommission.
- Total remaining active cluster node count (must satisfy replication factor, e.g. minimum 3 nodes for num_replicas=3).

## Diagnosis Process
1. Inspect node status and range count.
2. Confirm cluster has sufficient capacity on remaining nodes.

## Tool Calls & SQL Queries

```sql
-- Step 1: Check node status
SELECT node_id, is_live, is_decommissioning, ranges 
FROM crdb_internal.gossip_nodes;
```

## Recommended Action
Decommission node via CLI:
```bash
cockroach node decommission <node_id> --insecure
```

## Safety Considerations
- Never decommission multiple nodes simultaneously if doing so drops active live nodes below quorum requirement.

## Verification Steps
1. Query `crdb_internal.gossip_nodes` to confirm `is_decommissioning = true` and `ranges = 0`.
