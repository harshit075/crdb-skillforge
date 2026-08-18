---
name: rbac-setup
category: security
description: >
  Use when configuring Role-Based Access Control (RBAC), creating database users,
  roles, granting fine-grained privileges, or enforcing column-level security.
cockroach_versions: ">=23.1"
tags:
  - security
  - rbac
  - permissions
  - privileges
requires_tools:
  - sql-execution
maintainers:
  - "@crdb-maintainer"
last_verified: "2026-08-18"
license: Apache-2.0
execution_mode: operational
risk_level: medium
---

# RBAC Setup

## When to Use
- Setting up least-privilege roles for application microservices or AI agents.
- Granting `SELECT`, `INSERT`, `UPDATE` privileges on specific database schemas.

## Required Context
- Target database, schema, table names.
- Role/User names (e.g. `agent_readonly_role`, `app_writer`).

## Diagnosis Process
1. Inspect existing users, roles, and table privileges.

## Tool Calls & SQL Queries

```sql
-- Step 1: Check existing roles
SELECT role_name FROM information_schema.applicable_roles;

-- Step 2: Inspect table privileges
SELECT grantee, table_name, privilege_type 
FROM information_schema.table_privileges 
WHERE table_name = '%TABLE_NAME%';
```

## Recommended Action
Create least-privilege agent role:
```sql
CREATE ROLE agent_executor;
GRANT CONNECT ON DATABASE defaultdb TO agent_executor;
GRANT USAGE ON SCHEMA public TO agent_executor;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO agent_executor;
CREATE USER agent_bot WITH PASSWORD 'StrongSecretPass123!';
GRANT agent_executor TO agent_bot;
```

## Safety Considerations
- Never grant `root` or `admin` superuser privileges to application agents.

## Verification Steps
1. Execute `SHOW GRANTS FOR agent_bot;` via `sql-execution`.
2. Confirm user privileges strictly match intended role scope.
