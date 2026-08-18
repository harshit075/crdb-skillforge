#!/usr/bin/env python3
import os
import sys
import glob
import yaml
import datetime
from pathlib import Path

REQUIRED_FRONTMATTER_FIELDS = [
    "name",
    "category",
    "description",
    "cockroach_versions",
    "tags",
    "requires_tools",
    "maintainers",
    "last_verified",
    "license",
    "execution_mode",
    "risk_level",
]

ALLOWED_CATEGORIES = [
    "onboarding",
    "query-schema-design",
    "operations",
    "performance",
    "security",
    "observability",
]

ALLOWED_EXECUTION_MODES = ["diagnostic", "recommendation", "setup", "operational"]
ALLOWED_RISK_LEVELS = ["low", "medium", "high"]

def parse_skill_md(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    if not content.startswith("---"):
        return None, content, ["File does not start with YAML frontmatter delimiter (---)."]

    parts = content.split("---", 2)
    if len(parts) < 3:
        return None, content, ["Malformed YAML frontmatter delimiters."]

    try:
        frontmatter = yaml.safe_load(parts[1])
    except Exception as e:
        return None, content, [f"YAML parsing error: {e}"]

    body = parts[2]
    return frontmatter, body, []

def validate_skill_file(file_path, cases_skill_names):
    errors = []
    warnings = []
    frontmatter, body, parse_errors = parse_skill_md(file_path)

    if parse_errors:
        return False, parse_errors, warnings

    # 1. Check required frontmatter fields
    for field in REQUIRED_FRONTMATTER_FIELDS:
        if field not in frontmatter or frontmatter[field] is None:
            errors.append(f"Missing required frontmatter field: '{field}'")

    if errors:
        return False, errors, warnings

    name = frontmatter.get("name")
    category = frontmatter.get("category")
    last_verified = str(frontmatter.get("last_verified"))
    exec_mode = frontmatter.get("execution_mode")
    risk_level = frontmatter.get("risk_level")

    # 2. Check category
    if category not in ALLOWED_CATEGORIES:
        errors.append(f"Invalid category '{category}'. Must be one of {ALLOWED_CATEGORIES}")

    # 3. Check execution mode and risk level
    if exec_mode not in ALLOWED_EXECUTION_MODES:
        errors.append(f"Invalid execution_mode '{exec_mode}'. Must be one of {ALLOWED_EXECUTION_MODES}")

    if risk_level not in ALLOWED_RISK_LEVELS:
        errors.append(f"Invalid risk_level '{risk_level}'. Must be one of {ALLOWED_RISK_LEVELS}")

    # 4. Check last_verified date staleness (> 6 months)
    try:
        verified_date = datetime.datetime.strptime(last_verified, "%Y-%m-%d").date()
        six_months_ago = datetime.date.today() - datetime.timedelta(days=180)
        if verified_date < six_months_ago:
            warnings.append(f"Skill '{name}' is STALE. Last verified on {last_verified} (> 6 months ago).")
    except ValueError:
        errors.append(f"Invalid last_verified date format '{last_verified}'. Must be YYYY-MM-DD.")

    # 5. Check body structure
    required_sections = ["When to Use", "Diagnosis", "Verification"]
    for sec in required_sections:
        if sec.lower() not in body.lower():
            warnings.append(f"Skill '{name}' body missing standard section heading: '{sec}'")

    # 6. Check eval harness case association
    if name not in cases_skill_names:
        warnings.append(f"Skill '{name}' has no matching evaluation case in tools/eval-harness/cases.yaml.")

    is_valid = len(errors) == 0
    return is_valid, errors, warnings

def main():
    root_dir = Path(__file__).resolve().parent.parent
    skills_dir = root_dir / "skills"
    cases_file = root_dir / "tools" / "eval-harness" / "cases.yaml"

    cases_skill_names = set()
    if cases_file.exists():
        try:
            with open(cases_file, "r", encoding="utf-8") as cf:
                eval_data = yaml.safe_load(cf) or []
                for case in eval_data:
                    sk = case.get("skill")
                    if sk:
                        cases_skill_names.add(sk)
        except Exception:
            pass

    skill_files = glob.glob(str(skills_dir / "**" / "SKILL.md"), recursive=True)
    if not skill_files:
        print("ERROR: No SKILL.md files found in skills/ directory.")
        sys.exit(1)

    all_valid = True
    seen_names = {}
    print(f"Scanning and validating {len(skill_files)} canonical skills...\n")

    for file_path in skill_files:
        rel_path = os.path.relpath(file_path, root_dir)
        is_valid, errors, warnings = validate_skill_file(file_path, cases_skill_names)

        frontmatter, _, _ = parse_skill_md(file_path)
        if frontmatter and "name" in frontmatter:
            s_name = frontmatter["name"]
            if s_name in seen_names:
                errors.append(f"Duplicate skill name '{s_name}' also defined in {seen_names[s_name]}")
                is_valid = False
            else:
                seen_names[s_name] = rel_path

        if is_valid:
            print(f"[OK] {s_name} ({rel_path})")
            for w in warnings:
                print(f"  |- WARNING: {w}")
        else:
            all_valid = False
            print(f"[FAIL] {rel_path}")
            for err in errors:
                print(f"  |- ERROR: {err}")
            for w in warnings:
                print(f"  |- WARNING: {w}")

    print("\n" + "=" * 60)
    if all_valid:
        print(f"SUCCESS: All {len(skill_files)} skills are valid!")
        sys.exit(0)
    else:
        print("FAILURE: Validation failed with errors.")
        sys.exit(1)

if __name__ == "__main__":
    main()
