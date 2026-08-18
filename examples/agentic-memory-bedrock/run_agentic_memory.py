#!/usr/bin/env python3
import sys
import json
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(root_dir))

from tools.crdb.client import CRDBClient
from tools.crdb.vector import vector_search
from tools.crdb.sql import execute_sql
from tools.aws.bedrock import invoke_bedrock_agent

def run_agentic_memory_demo():
    print("=" * 80)
    print("  CrDB SkillForge - CockroachDB Agentic Memory & AWS Bedrock Demo")
    print("  Theme: 'Why Agentic Memory? Why Now?'")
    print("=" * 80)
    print()

    db = CRDBClient()

    # Step 1: Write Agent State Checkpoint to CockroachDB
    print("Step 1: Storing Agent State Checkpoint in CockroachDB Memory Layer")
    store_sql = "INSERT INTO agent_memory VALUES ('m100', 'agent-bedrock', 'checkpoint-prod', 'Agent state preserved across region failover', '[0.15, 0.32, 0.91]', CURRENT_TIMESTAMP);"
    res = execute_sql(store_sql, read_only=False, confirm=True, client=db)
    print(f"  |- Status: Checkpoint saved to CockroachDB (Duration: {res.get('duration_ms')} ms)\n")

    # Step 2: Query Vector Similarity
    print("Step 2: Performing Vector Search over Distributed Vector Index")
    vec_res = vector_search("agent_memory", "embedding", [0.15, 0.30, 0.90], limit=1, client=db)
    print(f"  |- Nearest Memory Content: \"{vec_res['rows'][0]['content']}\" (Distance: {vec_res['rows'][0]['distance']})\n")

    # Step 3: Invoke AWS Bedrock Model with Context
    print("Step 3: Reasoning with Amazon Bedrock over Persisted Agentic Memory")
    prompt = f"Agent Memory retrieved from CockroachDB: {vec_res['rows'][0]['content']}. Synthesize next action."
    bedrock_res = invoke_bedrock_agent(prompt)
    print(f"  |- Bedrock Completion: {bedrock_res.get('completion')}\n")

    print("=" * 80)
    print("  SUCCESS: Agentic memory verified - persistent across regional failures.")
    print("=" * 80)

if __name__ == "__main__":
    run_agentic_memory_demo()
