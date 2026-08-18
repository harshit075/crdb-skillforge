#!/usr/bin/env python3
import os
import sys
import json
import yaml
import glob
import importlib.util
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from pathlib import Path

# Add root directory to sys.path
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))

from tools.crdb.client import CRDBClient
from tools.crdb.sql import execute_sql
from tools.crdb.explain import explain_analyze
from tools.crdb.schema import get_schema
from tools.crdb.indexes import get_indexes
from tools.crdb.cluster import get_cluster_metadata
from tools.crdb.vector import vector_search
from tools.aws.bedrock import invoke_bedrock_agent
from tools.aws.s3 import archive_telemetry_to_s3

# Import eval-harness runner
spec = importlib.util.spec_from_file_location("eval_runner", root_dir / "tools" / "eval-harness" / "run.py")
eval_runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(eval_runner)

discover_skill_for_prompt = eval_runner.discover_skill_for_prompt
load_skills_data = eval_runner.load_skills_data

PORT = int(os.getenv("PORT", 8080))
STATIC_DIR = Path(__file__).resolve().parent / "static"

class CrDBSkillForgeHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(STATIC_DIR), **kwargs)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/health":
            self.send_json_response({"status": "HEALTHY", "platform": "CrDB SkillForge Web App", "version": "0.1.0"})
        elif parsed.path == "/api/skills":
            skills = load_skills_data(root_dir / "skills")
            clean_skills = [
                {
                    "name": s.get("name"),
                    "category": s.get("category"),
                    "description": s.get("description", "").strip(),
                    "cockroach_versions": s.get("cockroach_versions"),
                    "tags": s.get("tags", []),
                    "requires_tools": s.get("requires_tools", []),
                    "last_verified": str(s.get("last_verified")),
                    "risk_level": s.get("risk_level"),
                }
                for s in skills
            ]
            self.send_json_response({"skills": clean_skills, "count": len(clean_skills)})
        elif parsed.path == "/api/cluster-info":
            meta = get_cluster_metadata()
            self.send_json_response(meta)
        else:
            super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        content_len = int(self.headers.get("Content-Length", 0))
        post_body = self.rfile.read(content_len).decode("utf-8") if content_len > 0 else "{}"
        
        try:
            data = json.loads(post_body)
        except Exception:
            data = {}

        if parsed.path == "/api/discover":
            prompt = data.get("prompt", "")
            skills = load_skills_data(root_dir / "skills")
            skill_name, score = discover_skill_for_prompt(prompt, skills)
            matched = next((s for s in skills if s.get("name") == skill_name), {})
            self.send_json_response({
                "skill": skill_name,
                "score": round(score, 2),
                "category": matched.get("category"),
                "description": matched.get("description", "").strip(),
                "requires_tools": matched.get("requires_tools", []),
                "content": matched.get("content", "")
            })

        elif parsed.path == "/api/diagnose":
            prompt = data.get("prompt", "My query suddenly became slow.")
            skills = load_skills_data(root_dir / "skills")
            skill_name, score = discover_skill_for_prompt(prompt, skills)

            db = CRDBClient()
            schema_res = get_schema("orders", client=db)
            indexes_res = get_indexes("orders", client=db)
            before_explain = explain_analyze("SELECT * FROM orders WHERE status = 'pending' ORDER BY created_at DESC;", client=db)
            
            bedrock_res = invoke_bedrock_agent(f"Diagnose slow query for CockroachDB table 'orders'. Prompt: '{prompt}'")
            
            # Apply fix
            fix_res = execute_sql("CREATE INDEX idx_orders_status_created ON orders (status, created_at DESC);", read_only=False, confirm=True, client=db)
            after_explain = explain_analyze("SELECT * FROM orders WHERE status = 'pending' ORDER BY created_at DESC; -- indexed", client=db)

            s3_res = archive_telemetry_to_s3({
                "prompt": prompt,
                "skill": skill_name,
                "score": score,
                "status": "RESOLVED"
            })

            self.send_json_response({
                "success": True,
                "prompt": prompt,
                "skill": skill_name,
                "score": round(score, 2),
                "schema": schema_res,
                "indexes": indexes_res,
                "before_explain": before_explain,
                "bedrock": bedrock_res,
                "fix": fix_res,
                "after_explain": after_explain,
                "s3": s3_res
            })

        elif parsed.path == "/api/vector-search":
            query_vec = data.get("vector", [0.15, 0.30, 0.90])
            table = data.get("table", "agent_memory")
            res = vector_search(table, "embedding", query_vec)
            self.send_json_response(res)

        elif parsed.path == "/api/execute-sql":
            sql_str = data.get("query", "SELECT version();")
            confirm = data.get("confirm", False)
            read_only = data.get("read_only", True)
            res = execute_sql(sql_str, read_only=read_only, confirm=confirm)
            self.send_json_response(res)

        else:
            self.send_json_response({"error": "Unknown API endpoint"}, status=404)

    def send_json_response(self, data, status=200):
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

def main():
    print(f"Starting CrDB SkillForge Web App Server on http://localhost:{PORT}")
    server = HTTPServer(("0.0.0.0", PORT), CrDBSkillForgeHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down web server.")
        server.server_close()

if __name__ == "__main__":
    main()
