import sys
from pathlib import Path

# Add parent directory to sys.path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

# Import symbols from tools/validate-skill.py script file
import importlib.util
spec = importlib.util.spec_from_file_location("validate_skill_mod", root_dir / "tools" / "validate-skill.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

parse_skill_md = mod.parse_skill_md
validate_skill_file = mod.validate_skill_file
main = mod.main

if __name__ == "__main__":
    main()
