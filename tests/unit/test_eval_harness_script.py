import subprocess
import sys
from pathlib import Path


def test_eval_harness_script_runs_successfully():
    root_dir = Path(__file__).resolve().parents[2]
    result = subprocess.run(
        [sys.executable, "tools/eval-harness/run.py"],
        cwd=root_dir,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "SUCCESS: All evaluation cases passed!" in result.stdout
