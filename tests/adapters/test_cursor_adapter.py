from pathlib import Path
from adapters.cursor.generate import generate_cursor_rules

def test_cursor_rule_generation():
    root_dir = Path(__file__).resolve().parent.parent.parent
    rules_dir = root_dir / ".cursor" / "rules"

    generate_cursor_rules()
    assert rules_dir.exists()
    rule_files = list(rules_dir.glob("*.mdc"))
    assert len(rule_files) >= 21
