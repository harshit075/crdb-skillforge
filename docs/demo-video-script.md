# Demo Video Script (Under 3 Minutes)

**Title**: CrDB SkillForge — Executable CockroachDB Expertise & Agentic Memory Layer

## Script Outline

### 0:00 - 0:30 | The Problem: Why Agentic Memory? Why Now?
- "AI agents are moving into production workflows—writing code, running pipelines, and driving massive traffic. But when an agent's memory goes offline, the agent stops."
- "Traditional databases were built for human scale. Agents require memory that never goes down—persisting across regions, failures, and scale with zero downtime."
- "CockroachDB is the system of record for agentic memory."

### 0:30 - 1:15 | Introducing CrDB SkillForge
- Show repository structure, Apache-2.0 license, and 21 machine-executable skills across onboarding, schema design, operations, performance, security, and observability.
- Demonstrate MCP Server, Cursor MDC rules, and LangChain integration.

### 1:15 - 2:15 | Live Demonstration & Diagnostic Flow
- Run `make demo` (`examples/performance-diagnosis/run_demo.py`).
- Show user query: "My query suddenly became slow."
- Show Skill Discovery selecting `explain-analyze-reading`.
- Show tool execution querying CockroachDB `EXPLAIN ANALYZE` -> identifying Full Table Scan -> Amazon Bedrock model recommending covering index -> applying index with safety check -> verifying index scan conversion -> archiving telemetry to Amazon S3.

### 2:15 - 2:50 | AWS Integration & Architecture
- Highlight Amazon Bedrock Action Groups, AWS Lambda handler, and CockroachDB Distributed Vector Indexing.
- Show architectural flow diagram.

### 2:50 - 3:00 | Conclusion & Open Source Link
- "CrDB SkillForge turns static database documentation into machine-executable agent intelligence."
- Link: `https://github.com/harshit075/crdb-skillforge.git`
