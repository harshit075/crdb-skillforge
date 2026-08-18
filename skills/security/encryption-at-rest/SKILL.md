---
name: encryption-at-rest
category: security
description: >
  Use when configuring or auditing Encryption at Rest (CCEE) for Pebble storage engine,
  KMS key rotation, or compliance security validation.
cockroach_versions: ">=23.1"
tags:
  - security
  - encryption-at-rest
  - pebble
  - kms
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

# Encryption at Rest

## When to Use
- Enabling hardware/software Encryption at Rest for cluster data stores.
- Integrating AWS KMS or HashiCorp Vault for store encryption keys.

## Required Context
- Cloud provider KMS ARN or Vault configuration endpoint.

## Recommended Action
Configure store flag `--enterprise-encryption` on node start:
```bash
cockroach start \
  --store=path=/mnt/data,attrs=store1,encryption-at-rest-kms-type=aws,encryption-at-rest-kms-aws-key-arn=arn:aws:kms:us-east-1:123456789012:key/abc-123
```

## Verification Steps
1. Verify cluster settings `enterprise.encryption.enabled = true`.
