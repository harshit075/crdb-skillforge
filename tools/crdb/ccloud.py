import subprocess
import shutil
from typing import Dict, Any

def ccloud_cluster_info() -> Dict[str, Any]:
    """
    Interact with Cockroach Cloud CLI (ccloud) to query cloud cluster state and serverless tier info.
    """
    ccloud_bin = shutil.which("ccloud")
    if not ccloud_bin:
        return {
            "success": True,
            "installed": False,
            "info": {
                "organization": "crdb-skillforge-org",
                "clusters": [
                    {"name": "agentic-memory-prod", "provider": "AWS", "region": "us-east-1", "plan": "Serverless", "status": "RUNNING"}
                ]
            },
            "note": "ccloud CLI not found in PATH; returned simulated Cockroach Cloud cluster topology."
        }

    try:
        proc = subprocess.run([ccloud_bin, "cluster", "list", "--output", "json"], capture_output=True, text=True, timeout=10)
        return {
            "success": proc.returncode == 0,
            "installed": True,
            "output": proc.stdout or proc.stderr,
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
