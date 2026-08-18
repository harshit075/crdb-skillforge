#!/usr/bin/env python3
import os
import sys
import argparse
import datetime
from pathlib import Path

SKILL_TEMPLATE = """---
name: {name}
category: {category}

description: >
  [TODO: Add description of when an AI agent should load and execute this skill]

cockroach_versions: ">=23.1"

tags:
  - {category}
  - [TODO: add tags]

requires_tools:
  - sql-execution
  - schema-inspection

maintainers:
  - "@maintainer"

last_verified: "{today}"

license: Apache-2.0

execution_mode: diagnostic

risk_level: low
---

# {title_name}

## Trigger Conditions
- [TODO: Specify exact conditions that trigger this skill]

## Required Context
- [TODO: Specify required input context]

## Diagnosis Process
1. [TODO: Specify diagnostic step 1]

## Tool Calls & SQL Queries

```sql
-- [TODO: Diagnostic query]
SELECT 1;
```

## Recommended Action
- [TODO: Recommended remediation step]

## Verification Steps
1. [TODO: Verification query or check]
"""

def main():
    parser = argparse.ArgumentParser(description="Scaffold a new canonical CockroachDB Agent Skill.")
    parser.add_argument("--category", required=True, help="Skill category (e.g. performance, operations)")
    parser.add_argument("--name", required=True, help="Skill name in kebab-case (e.g. query-plan-regression)")
    args = parser.parse_args()

    root_dir = Path(__file__).resolve().parent.parent
    target_dir = root_dir / "skills" / args.category / args.name
    target_dir.mkdir(parents=True, exist_ok=True)

    examples_dir = target_dir / "examples"
    tests_dir = target_dir / "tests"
    examples_dir.mkdir(exist_ok=True)
    tests_dir.mkdir(exist_ok=True)

    skill_file = target_dir / "SKILL.md"
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    title_str = args.name.replace("-", " ").title()

    content = SKILL_TEMPLATE.format(
        name=args.name,
        category=args.category,
        today=today_str,
        title_name=title_str,
    )

    with open(skill_file, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[OK] Created new skill scaffolding at: {skill_file}")
    print(f"  |- Examples dir: {examples_dir}")
    print(f"  |- Tests dir: {tests_dir}")
    print("\nNote: Run 'python tools/validate-skill.py' to see remaining fields to complete.")

if __name__ == "__main__":
    main()
