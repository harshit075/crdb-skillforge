---
name: connect-from-app
category: onboarding
description: >
  Use when establishing application or agent database connections to CockroachDB
  using PostgreSQL drivers (psycopg2, psycopg3, pg8000, asyncpg, or node-postgres).
cockroach_versions: ">=23.1"
tags:
  - onboarding
  - connectivity
  - connection-pooling
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

# Connect From Application

## When to Use
- Application or AI agent experiences connection drops, handshake timeouts, or SSL validation errors when connecting to CockroachDB.

## Required Context
- Connection string parameters (`host`, `port`, `user`, `password`, `database`, `sslmode`).
- Application client driver (Python `psycopg`, Node `pg`, Go `pgx`, Java `JDBC`).

## Diagnosis Process
1. Test database connection via parameter validation.
2. Inspect server session settings and current max connections limit.

## Tool Calls & SQL Queries

```sql
-- Step 1: Check session variables and connection limit
SHOW max_connections;
SHOW session_timeout;

-- Step 2: Inspect active sessions
SELECT user_name, client_addr, application_name, phase FROM crdb_internal.node_sessions;
```

## Interpretation Rules
- CockroachDB uses standard PostgreSQL wire protocol (v3.0).
- Always use connection pooling (e.g. PgBouncer, HikariCP, or SQLAlchemy QueuePool) to avoid connection churn overhead.

## Recommended Fix
Use PostgreSQL connection string syntax:
```text
postgresql://user:password@host:26257/defaultdb?sslmode=verify-full
```

## Safety Considerations
- Ensure SSL certificates (`ca.crt`, `client.crt`, `client.key`) are securely permissions-restricted (0600).

## Anti-Patterns
- Opening a new connection per query without pooling.

## Verification Steps
1. Execute `SELECT 1;` using `sql-execution`.
2. Confirm session established cleanly.
