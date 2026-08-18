---
name: cert-rotation
category: security
description: >
  Use when rotating TLS node certificates, client certificates, or Root Certificate
  Authorities (CA) in a secure CockroachDB cluster without downtime.
cockroach_versions: ">=23.1"
tags:
  - security
  - tls
  - certificate-rotation
  - mtls
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

# Certificate Rotation

## When to Use
- Rotating expiring node/client TLS certificates or root CA certificates.
- Zero-downtime certificate renewal procedure.

## Required Context
- Location of certificate directory (`--certs-dir`).
- Node certificate expiration dates.

## Diagnosis Process
1. Query active certificate expiration dates in `crdb_internal.node_certificates`.

## Tool Calls & SQL Queries

```sql
-- Step 1: Check node certificate validity & expiration
SELECT node_id, certificate_type, valid_until, issuer 
FROM crdb_internal.node_certificates;
```

## Recommended Action
1. Generate updated node/client certificate signed by active CA.
2. Overwrite certificate file in certs directory on target node.
3. Issue SIGHUP signal or node reload command to reload certificate without restarting process:
```bash
cockroach cert list --certs-dir=certs
```

## Verification Steps
1. Re-query `crdb_internal.node_certificates` to confirm updated `valid_until` timestamp.
