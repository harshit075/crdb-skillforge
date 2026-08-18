---
name: rolling-upgrades
category: operations
description: >
  Use when performing zero-downtime rolling upgrades across CockroachDB cluster nodes,
  checking cluster binary version compatibility, or finalizing cluster version upgrades.
cockroach_versions: ">=23.1"
tags:
  - operations
  - rolling-upgrade
  - cluster-version
requires_tools:
  - sql-execution
  - cluster-metadata
maintainers:
  - "@crdb-maintainer"
last_verified: "2026-08-18"
license: Apache-2.0
execution_mode: operational
risk_level: medium
---

# Rolling Upgrades

## When to Use
- Upgrading CockroachDB nodes to a new major/minor release without cluster downtime.
- Verifying upgrade state and setting cluster version finalization setting `cluster.preserve_downgrade_option`.

## Required Context
- Current running binary versions across cluster nodes.
- Target release version.

## Diagnosis Process
1. Query node versions and cluster settings.
2. Check cluster readiness and drain status before restarting each node.

## Tool Calls & SQL Queries

```sql
-- Step 1: Check versions across all nodes
SELECT node_id, address, build_tag FROM crdb_internal.node_build_info;

-- Step 2: Check cluster upgrade setting
SHOW CLUSTER SETTING cluster.preserve_downgrade_option;
```

## Interpretation Rules
- Upgrades must proceed one major version at a time (e.g. v23.1 -> v23.2 -> v24.1).
- Restart nodes sequentially, allowing range leaseholders to transfer cleanly before stopping the next node.

## Recommended Fix
Finalize upgrade after all nodes run the target binary:
```sql
RESET CLUSTER SETTING cluster.preserve_downgrade_option;
```

## Safety Considerations
- Never upgrade across multiple major version jumps in a single step.

## Verification Steps
1. Verify `SELECT DISTINCT build_tag FROM crdb_internal.node_build_info;` returns single target version.
