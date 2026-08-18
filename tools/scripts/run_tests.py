#!/usr/bin/env python3
import sys
import traceback
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(root_dir))

def run_all_tests():
    print("Running CrDB SkillForge Test Suite...\n")
    passed = 0
    failed = 0

    test_modules = [
        ("tests.unit.test_crdb_tools", "Unit Tools Test"),
        ("tests.skills.test_skills_validator", "Skills Validator Test"),
        ("tests.adapters.test_cursor_adapter", "Cursor Adapter Test"),
        ("tests.adapters.test_langchain_adapter", "LangChain Adapter Test"),
        ("tests.integration.test_database_integration", "Database Integration Test"),
    ]

    for mod_name, label in test_modules:
        try:
            mod = __import__(mod_name, fromlist=["*"])
            test_funcs = [getattr(mod, fn) for fn in dir(mod) if fn.startswith("test_") and callable(getattr(mod, fn))]
            print(f"[{label}] Found {len(test_funcs)} test functions in {mod_name}:")
            for tf in test_funcs:
                try:
                    tf()
                    print(f"  [OK] {tf.__name__}")
                    passed += 1
                except Exception as e:
                    print(f"  [FAIL] {tf.__name__}: {e}")
                    traceback.print_exc()
                    failed += 1
        except Exception as e:
            print(f"  [FAIL] Failed to import module {mod_name}: {e}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"TEST SUMMARY: {passed} passed, {failed} failed.")
    if failed == 0:
        print("SUCCESS: All tests passed!")
        sys.exit(0)
    else:
        print("FAILURE: Some tests failed.")
        sys.exit(1)

if __name__ == "__main__":
    run_all_tests()
