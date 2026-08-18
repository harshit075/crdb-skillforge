# Skill Authoring Guide

Learn how to author executable CockroachDB skills for CrDB SkillForge.

## Scaffolding a Skill

Run the scaffolding tool:
```bash
python tools/new_skill.py --category performance --name query-plan-regression
```

This creates:
```text
skills/performance/query-plan-regression/
├── SKILL.md
├── examples/
└── tests/
```

## Mandatory Frontmatter Schema

Every `SKILL.md` must begin with YAML frontmatter:

```yaml
---
name: query-plan-regression
category: performance
description: Use when query plans regress following major release upgrades or statistics updates.
cockroach_versions: ">=23.1"
tags:
  - performance
  - query-plan
requires_tools:
  - sql-execution
  - explain-analyze
maintainers:
  - "@maintainer"
last_verified: "2026-08-18"
license: Apache-2.0
execution_mode: diagnostic
risk_level: low
---
```

## Validation & Quality Verification

Run validation before committing:
```bash
python tools/validate-skill.py
```
