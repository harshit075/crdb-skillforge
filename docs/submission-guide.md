# Hackathon Submission Guide & Checklist

## Submission Parameters Summary

1. **Repository URL**: `https://github.com/harshit075/crdb-skillforge.git` (Public Open Source)
2. **License**: Apache 2.0 (Visible at top of repository in `LICENSE`)
3. **CockroachDB Tools Used**:
   - **MCP Server**: Stdio JSON-RPC server exposing database skills & execution tools.
   - **ccloud CLI**: `ccloud` CLI wrapper for cloud cluster topology management.
   - **Distributed Vector Indexing**: `vector_search()` over CockroachDB vector distance operators `<->`.
   - **Agent Skills**: 21 canonical machine-executable `SKILL.md` definitions.
4. **AWS Services Used**:
   - **Amazon Bedrock**: Model reasoning over database diagnostics & vector context.
   - **AWS Lambda**: Serverless event handler for Bedrock Action Groups.
   - **Amazon S3**: Telemetry and diagnostic audit log archival.
5. **Functional Demo App**:
   - `examples/performance-diagnosis/run_demo.py`
   - `examples/agentic-memory-bedrock/run_agentic_memory.py`
6. **Video Script**: See `docs/demo-video-script.md`.
