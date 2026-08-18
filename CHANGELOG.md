# Changelog — CrDB SkillForge

All notable changes to **CrDB SkillForge** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-08-18

### Added
- **Canonical Skill Collection**: 21 machine-executable skills across Onboarding, Query/Schema Design, Operations, Performance, Security, and Observability.
- **Tool Execution Layer**: Reusable Python tools for safe SQL execution, EXPLAIN ANALYZE reading, schema inspection, index inspection, vector search, and cluster metadata retrieval.
- **MCP Server**: Real Node.js MCP server exposing `skill://` resources and interactive tools over stdio protocol.
- **Cursor Rule Adapter**: Automatic conversion script (`adapters/cursor/generate.py`) compiling `SKILL.md` files into `.cursor/rules/*.mdc`.
- **LangChain Adapter**: Python package exposing `StructuredTool` wrappers for LangChain agents.
- **AWS Integration**: AWS Bedrock Agent OpenAPI spec generator, serverless AWS Lambda execution handler, and Amazon S3 diagnostic telemetry archiver.
- **Evaluation Harness**: Benchmark harness (`tools/eval-harness/`) with automated scoring, deterministic skill selection, and database diagnostic verification.
- **Skill Validator & Scaffolding**: `tools/validate-skill.py` and `tools/new_skill.py` for skill authoring quality control.
- **End-to-End Demo**: Reproducible performance diagnosis demonstration (`examples/performance-diagnosis/run_demo.py`).
- **CI/CD Workflows**: GitHub Actions workflows for validation, unit tests, evaluation, and nightly staleness detection.
