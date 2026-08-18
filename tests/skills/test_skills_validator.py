import os
from pathlib import Path
from tools.validate_skill import parse_skill_md, validate_skill_file

def test_validator_on_canonical_skills():
    root_dir = Path(__file__).resolve().parent.parent.parent
    avoiding_hotspots = root_dir / "skills" / "query-schema-design" / "avoiding-hotspots" / "SKILL.md"

    assert avoiding_hotspots.exists()
    is_valid, errors, warnings = validate_skill_file(str(avoiding_hotspots), {"avoiding-hotspots"})
    assert is_valid is True
    assert len(errors) == 0

def test_validator_rejects_missing_fields(tmp_path=None):
    if tmp_path is None:
        tmp_path = Path(__file__).resolve().parent / "tmp_test"
        tmp_path.mkdir(exist_ok=True)
    invalid_skill = tmp_path / "SKILL.md"
    invalid_skill.write_text("""---
name: invalid-skill
category: invalid-category
---
# Invalid Skill
""", encoding="utf-8")
    is_valid, errors, warnings = validate_skill_file(str(invalid_skill), set())
    assert is_valid is False
    assert len(errors) > 0
    if invalid_skill.exists():
        invalid_skill.unlink()
