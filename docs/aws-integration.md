# AWS Service Integration Guide

CrDB SkillForge natively integrates with AWS services to deploy serverless AI agents powered by CockroachDB agentic memory.

## AWS Services Used

1. **Amazon Bedrock**: Foundation model reasoning (Claude v2 / Bedrock Agents) over CockroachDB diagnostic outputs and vector memory.
2. **AWS Lambda**: Serverless execution layer hosting Bedrock Action Group handlers (`adapters/aws-lambda/lambda_function.py`).
3. **Amazon S3**: Telemetry and diagnostic audit log archival (`tools/aws/s3.py`).

## Generating Bedrock Action Group OpenAPI Spec

```bash
python adapters/aws-bedrock/generate_openapi.py
```
Outputs `adapters/aws-bedrock/bedrock_action_group.json`.
