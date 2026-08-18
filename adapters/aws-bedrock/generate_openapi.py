#!/usr/bin/env python3
import json
from pathlib import Path

def generate_bedrock_openapi_spec():
    root_dir = Path(__file__).resolve().parent.parent.parent
    output_file = root_dir / "adapters" / "aws-bedrock" / "bedrock_action_group.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)

    spec = {
        "openapi": "3.0.1",
        "info": {
            "title": "CrDB SkillForge Agent Tools API",
            "description": "Amazon Bedrock Action Group API for executing CockroachDB diagnostic and agentic memory skills.",
            "version": "1.0.0"
        },
        "paths": {
            "/execute_sql": {
                "post": {
                    "summary": "Execute SQL against CockroachDB",
                    "operationId": "executeSql",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "query": {"type": "string"},
                                        "read_only": {"type": "boolean", "default": True}
                                    },
                                    "required": ["query"]
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {"description": "Query execution result"}
                    }
                }
            },
            "/explain_analyze": {
                "post": {
                    "summary": "Run EXPLAIN ANALYZE on query",
                    "operationId": "explainAnalyze",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "query": {"type": "string"}
                                    },
                                    "required": ["query"]
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {"description": "Execution plan diagnostics"}
                    }
                }
            },
            "/vector_search": {
                "post": {
                    "summary": "Distributed Vector Index search in CockroachDB",
                    "operationId": "vectorSearch",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "table_name": {"type": "string"},
                                        "vector_column": {"type": "string"},
                                        "query_vector": {"type": "array", "items": {"type": "number"}}
                                    },
                                    "required": ["table_name", "vector_column", "query_vector"]
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {"description": "Nearest vector matches"}
                    }
                }
            }
        }
    }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(spec, f, indent=2)

    print(f"[OK] Successfully generated Amazon Bedrock Action Group OpenAPI spec at: {output_file}")

if __name__ == "__main__":
    generate_bedrock_openapi_spec()
