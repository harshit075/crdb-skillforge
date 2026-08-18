#!/usr/bin/env python3
import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(root_dir))

from tools.crdb.client import CRDBClient
from tools.crdb.sql import execute_sql

def main():
    print("Resetting CockroachDB test schema and data...")
    db = CRDBClient()
    reset_sql = """
    DROP TABLE IF EXISTS orders;
    DROP TABLE IF EXISTS users;
    DROP TABLE IF EXISTS agent_memory;
    CREATE TABLE users (id TEXT PRIMARY KEY, name TEXT, email TEXT, status TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
    CREATE TABLE orders (id TEXT PRIMARY KEY, user_id TEXT, total_amount DECIMAL, status TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
    CREATE TABLE agent_memory (id TEXT PRIMARY KEY, agent_id TEXT, memory_key TEXT, content TEXT, embedding TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
    INSERT INTO users VALUES ('u1', 'Alice', 'alice@example.com', 'active', CURRENT_TIMESTAMP);
    INSERT INTO orders VALUES ('o1', 'u1', 149.99, 'completed', CURRENT_TIMESTAMP);
    INSERT INTO agent_memory VALUES ('m1', 'agent-alpha', 'checkpoint-1', 'State initialized cleanly', '[0.12, 0.45, 0.88]', CURRENT_TIMESTAMP);
    """
    res = execute_sql(reset_sql, read_only=False, confirm=True, client=db)
    if res.get("success"):
        print("✓ Successfully reset database schema and sample data.")
    else:
        print(f"✗ Failed to reset database: {res.get('error')}")

if __name__ == "__main__":
    main()
