import json
import logging
from tools.crdb.sql import execute_sql
from tools.crdb.explain import explain_analyze
from tools.crdb.vector import vector_search

logger = logging.getLogger("crdb_skillforge_lambda")
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    AWS Lambda handler servicing Amazon Bedrock Agent action group requests
    against CockroachDB agentic memory & diagnostic endpoints.
    """
    logger.info(f"Received Bedrock Agent Event: {json.dumps(event)}")

    action_group = event.get("actionGroup", "CrDBSkillForgeActionGroup")
    api_path = event.get("apiPath", "/execute_sql")
    http_method = event.get("httpMethod", "POST")
    request_body = event.get("requestBody", {}).get("content", {}).get("application/json", {}).get("properties", [])

    body_params = {p["name"]: p["value"] for p in request_body} if isinstance(request_body, list) else {}

    result_data = {}
    if api_path == "/execute_sql":
        query = body_params.get("query", "SELECT version();")
        result_data = execute_sql(query, read_only=True)
    elif api_path == "/explain_analyze":
        query = body_params.get("query", "SELECT * FROM users LIMIT 10;")
        result_data = explain_analyze(query)
    elif api_path == "/vector_search":
        table = body_params.get("table_name", "agent_memory")
        col = body_params.get("vector_column", "embedding")
        vec = body_params.get("query_vector", [0.1, 0.2, 0.3])
        result_data = vector_search(table, col, vec)
    else:
        result_data = {"error": f"Unsupported API path: {api_path}"}

    response_body = {
        "application/json": {
            "body": json.dumps(result_data)
        }
    }

    action_response = {
        "actionGroup": action_group,
        "apiPath": api_path,
        "httpMethod": http_method,
        "httpStatusCode": 200,
        "responseBody": response_body
    }

    return {
        "messageVersion": "1.0",
        "response": action_response
    }
