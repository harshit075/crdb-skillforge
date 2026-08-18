#!/usr/bin/env python3
import os
import glob
import yaml
from pathlib import Path

def generate_cursor_rules():
    root_dir = Path(__file__).resolve().parent.parent.parent
    skills_dir = root_dir / "skills"
    output_dir = root_dir / ".cursor" / "rules"
    output_dir.mkdir(parents=True, exist_ok=True)

    skill_files = glob.glob(str(skills_dir / "**" / "SKILL.md"), recursive=True)
    print(f"Converting {len(skill_files)} canonical SKILL.md files into Cursor MDC rules...")

    generated_count = 0
    for s_file in skill_files:
        with open(s_file, "r", encoding="utf-8") as f:
            content = f.read()

        if not content.startswith("---"):
            continue

        parts = content.split("---", 2)
        if len(parts) < 3:
            continue

        try:
            frontmatter = yaml.safe_load(parts[1])
            body = parts[2].strip()
        except Exception as e:
            print(f"Skipping {s_file}: YAML parse error {e}")
            continue

        name = frontmatter.get("name", "unnamed-skill")
        description = frontmatter.get("description", "").strip()
        tags = frontmatter.get("tags", [])
        globs = ["**/*.sql", "**/*.py", "**/*.js", "**/*.ts", "**/*.go", "**/*.java"]

        mdc_content = f"""---
description: {description}
globs: {', '.join(globs)}
tags: {', '.join(tags)}
---

# CockroachDB Skill: {name}

{body}
"""

        out_path = output_dir / f"crdb-{name}.mdc"
        with open(out_path, "w", encoding="utf-8") as out:
            out.write(mdc_content)

        print(f"  |- Generated: {out_path.name}")
        generated_count += 1

    print(f"[OK] Successfully generated {generated_count} Cursor rule files in {output_dir}\n")

if __name__ == "__main__":
    generate_cursor_rules()
