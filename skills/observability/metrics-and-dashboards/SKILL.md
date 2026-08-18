---
name: metrics-and-dashboards
category: observability
description: >
  Use when configuring Prometheus metrics scrapers, DB Console dashboards,
  or monitoring core cluster health indicators (QPS, Latency, CPU, Disk, Memory).
cockroach_versions: ">=23.1"
tags:
  - observability
  - metrics
  - prometheus
  - dashboards
requires_tools:
  - sql-execution
  - cluster-metadata
maintainers:
  - "@crdb-maintainer"
last_verified: "2026-08-18"
license: Apache-2.0
execution_mode: diagnostic
risk_level: low
---

# Metrics & Dashboards

## When to Use
- Setting up Prometheus endpoint monitoring (`/_status/vars`).
- Monitoring key database health signals (SQL Latency p99, Range Quorum status, CPU usage).

## Required Context
- Prometheus scrape configuration.
- DB Console endpoint (`http://localhost:8080`).

## Diagnosis Process
1. Query key cluster metrics and node session statistics.

## Tool Calls & SQL Queries

```sql
-- Step 1: Query query latency and execution metrics
SELECT * FROM crdb_internal.node_metrics WHERE name IN ('sql.exec.latency-p99', 'sql.conns');
```

## Interpretation Rules
- Key Prometheus Metrics:
  - `sql_conns`: Total open application SQL connections.
  - `sql_exec_latency_nanos`: Query execution latency distribution.
  - `ranges_underreplicated`: Number of ranges below replica quorum (Alert if > 0).
  - `ranges_unavailable`: Number of ranges with no active leaseholder (Critical alert if > 0).

## Verification Steps
1. Fetch `http://<node-host>:8080/_status/vars` and confirm valid Prometheus metric output.
