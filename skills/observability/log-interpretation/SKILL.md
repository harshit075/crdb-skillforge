---
name: log-interpretation
category: observability
description: >
  Use when analyzing CockroachDB log files (cockroach.log, cockroach-sql-exec.log),
  interpreting log channel prefixes (OPS, STORAGE, SQL, SECURITY), or diagnosing crash logs.
cockroach_versions: ">=23.1"
tags:
  - observability
  - log-analysis
  - troubleshooting
  - diagnostics
requires_tools:
  - sql-execution
maintainers:
  - "@crdb-maintainer"
last_verified: "2026-08-18"
license: Apache-2.0
execution_mode: diagnostic
risk_level: low
---

# Log Interpretation

## Trigger Conditions
- CockroachDB node crashes, restarts unexpectedly, or reports internal errors.
- Triaging node stderr or log files in `cockroach-data/logs`.

## Required Information
- Log channel (e.g. `OPS`, `STORAGE`, `SQL`, `SECURITY`).
- Error message pattern or stack trace.

## Interpretation Rules
- `W240818` / `E240818` / `I240818`: Severity indicator (`W` = Warning, `E` = Error, `I` = Info, `F` = Fatal).
- `[STORAGE]`: Pebble storage engine, disk I/O, or SSTable compaction events.
- `[SQL]`: Query execution failures or syntax errors.
- `[OPS]`: Gossip protocol, node health, range rebalancing events.

## Recommended Action
In case of out-of-memory (`OOM` / `F240818` memory budget exceeded), adjust cluster cache/memory budget flags:
```bash
cockroach start --cache=25% --max-sql-memory=25% ...
```

## Verification Steps
1. Inspect live log output to confirm warning/error rate returns to baseline.
