# Implementation Plan — CrDB SkillForge: Executable CockroachDB Agent Skills Platform

Build **CrDB SkillForge**, a complete, production-quality open-source platform (`crdb-skillforge`) that provides machine-executable Agent Skills encoding CockroachDB expertise for always-on Agentic Memory, portable across Claude, Cursor, LangChain, AWS Bedrock / Lambda, and MCP-compatible AI clients.

> [!IMPORTANT]
> All submission parameters, AWS integrations, and CockroachDB toolings are incorporated into the plan.

## Vision & Hackathon Positioning

> **Why Agentic Memory? Why Now?**
> AI agents are rapidly moving from experiments into real production workflows—writing code, running pipelines, diagnosing incidents, and driving application traffic scale beyond human limits. Agents need memory that **never goes down**. An agent whose memory goes offline stops entirely. Traditional databases were optimized for human-scale workloads. Agentic systems spawn autonomously, write constantly, and require memory that persists across regions, failures, and scale (with zero data loss and zero maintenance windows).
> **CockroachDB** is the ultimate system of record for agentic memory: globally distributed, always-on, PostgreSQL-compatible, and natively integrated into agent toolchains via MCP, cloud, vector indexing, and open-source skills.

---

## User Review Required

> [!IMPORTANT]
> - **Git & Remote Setup**: The repository will be initialized locally and pushed to `https://github.com/harshit075/crdb-skillforge.git`.
> - **AWS Integration**: Adds AWS adapters (`adapters/aws-bedrock/`, `adapters/aws-lambda/`) and tools (`tools/aws/`) supporting Amazon Bedrock Agents, AWS Lambda serverless execution, and Amazon S3 artifact storage.
> - **CockroachDB Tooling Coverage**: Full coverage of CockroachDB MCP Server, `ccloud` CLI workflows, Distributed Vector Indexing patterns, and Agent Skills.
> - **Submission Package**: Includes submission checklist, video script template (`docs/demo-video-script.md`), architectural diagram (Mermaid), and functional demo app.

---

## Open Questions

> [!NOTE]
> None. All submission parameters, AWS integrations, and CockroachDB toolings are incorporated into the plan.

---

## Proposed Changes

### 1. Core Structure & Hackathon Submission Package

#### [NEW] [README.md](file:///c:/Users/HarshitBorana/OneDrive%20-%20Kadel%20Labs%20Private%20Limited/Desktop/Build_Innovations/crdb_skillforge/README.md)
#### [NEW] [LICENSE](file:///c:/Users/HarshitBorana/OneDrive%20-%20Kadel%20Labs%20Private%20Limited/Desktop/Build_Innovations/crdb_skillforge/LICENSE)
#### [NEW] [CONTRIBUTING.md](file:///c:/Users/HarshitBorana/OneDrive%20-%20Kadel%20Labs%20Private%20Limited/Desktop/Build_Innovations/crdb_skillforge/CONTRIBUTING.md)
#### [NEW] [CODE_OF_CONDUCT.md](file:///c:/Users/HarshitBorana/OneDrive%20-%20Kadel%20Labs%20Private%20Limited/Desktop/Build_Innovations/crdb_skillforge/CODE_OF_CONDUCT.md)
#### [NEW] [GOVERNANCE.md](file:///c:/Users/HarshitBorana/OneDrive%20-%20Kadel%20Labs%20Private%20Limited/Desktop/Build_Innovations/crdb_skillforge/GOVERNANCE.md)
#### [NEW] [SECURITY.md](file:///c:/Users/HarshitBorana/OneDrive%20-%20Kadel%20Labs%20Private%20Limited/Desktop/Build_Innovations/crdb_skillforge/SECURITY.md)
#### [NEW] [CHANGELOG.md](file:///c:/Users/HarshitBorana/OneDrive%20-%20Kadel%20Labs%20Private%20Limited/Desktop/Build_Innovations/crdb_skillforge/CHANGELOG.md)
#### [NEW] [Makefile](file:///c:/Users/HarshitBorana/OneDrive%20-%20Kadel%20Labs%20Private%20Limited/Desktop/Build_Innovations/crdb_skillforge/Makefile)
#### [NEW] [pyproject.toml](file:///c:/Users/HarshitBorana/OneDrive%20-%20Kadel%20Labs%20Private%20Limited/Desktop/Build_Innovations/crdb_skillforge/pyproject.toml)
#### [NEW] [package.json](file:///c:/Users/HarshitBorana/OneDrive%20-%20Kadel%20Labs%20Private%20Limited/Desktop/Build_Innovations/crdb_skillforge/package.json)
#### [NEW] [.gitignore](file:///c:/Users/HarshitBorana/OneDrive%20-%20Kadel%20Labs%20Private%20Limited/Desktop/Build_Innovations/crdb_skillforge/.gitignore)
#### [NEW] [.env.example](file:///c:/Users/HarshitBorana/OneDrive%20-%20Kadel%20Labs%20Private%20Limited/Desktop/Build_Innovations/crdb_skillforge/.env.example)

- Apache-2.0 License clearly visible for GitHub detection.
- README section detailing "Why Agentic Memory? Why Now?", CockroachDB tools used, AWS tools used, architecture diagram, setup instructions, and demo guide.

---

### 2. Canonical Skill Collection (`skills/`)

Implement 21 production-grade skills across 6 categories:
- **onboarding/**: `cluster-setup-local`, `connect-from-app`, `choosing-a-driver`
- **query-schema-design/**: `hash-sharded-indexes`, `multi-region-table-design`, `avoiding-hotspots`, `json-jsonb-modeling`
- **operations/**: `rolling-upgrades`, `backup-restore`, `node-decommissioning`, `disaster-recovery`
- **performance/**: `explain-analyze-reading`, `index-recommendations`, `transaction-retry-handling`, `contention-diagnosis`
- **security/**: `rbac-setup`, `cert-rotation`, `encryption-at-rest`
- **observability/**: `metrics-and-dashboards`, `slow-query-triage`, `log-interpretation`

---

### 3. Tool Execution Layer & AWS Tools (`tools/`)

#### [NEW] [tools/crdb/client.py](file:///c:/Users/HarshitBorana/OneDrive%20-%20Kadel%20Labs%20Private%20Limited/Desktop/Build_Innovations/crdb_skillforge/tools/crdb/client.py)
#### [NEW] [tools/crdb/sql.py](file:///c:/Users/HarshitBorana/OneDrive%20-%20Kadel%20Labs%20Private%20Limited/Desktop/Build_Innovations/crdb_skillforge/tools/crdb/sql.py)
#### [NEW] [tools/crdb/explain.py](file:///c:/Users/HarshitBorana/OneDrive%20-%20Kadel%20Labs%20Private%20Limited/Desktop/Build_Innovations/crdb_skillforge/tools/crdb/explain.py)
#### [NEW] [tools/crdb/schema.py](file:///c:/Users/HarshitBorana/OneDrive%20-%20Kadel%20Labs%20Private%20Limited/Desktop/Build_Innovations/crdb_skillforge/tools/crdb/schema.py)
#### [NEW] [tools/crdb/indexes.py](file:///c:/Users/HarshitBorana/OneDrive%20-%20Kadel%20Labs%20Private%20Limited/Desktop/Build_Innovations/crdb_skillforge/tools/crdb/indexes.py)
#### [NEW] [tools/crdb/cluster.py](file:///c:/Users/HarshitBorana/OneDrive%20-%20Kadel%20Labs%20Private%20Limited/Desktop/Build_Innovations/crdb_skillforge/tools/crdb/cluster.py)
#### [NEW] [tools/crdb/vector.py](file:///c:/Users/HarshitBorana/OneDrive%20-%20Kadel%20Labs%20Private%20Limited/Desktop/Build_Innovations/crdb_skillforge/tools/crdb/vector.py)
#### [NEW] [tools/crdb/ccloud.py](file:///c:/Users/HarshitBorana/OneDrive%20-%20Kadel%20Labs%20Private%20Limited/Desktop/Build_Innovations/crdb_skillforge/tools/crdb/ccloud.py)
#### [NEW] [tools/aws/bedrock.py](file:///c:/Users/HarshitBorana/OneDrive%20-%20Kadel%20Labs%20Private%20Limited/Desktop/Build_Innovations/crdb_skillforge/tools/aws/bedrock.py)
#### [NEW] [tools/aws/s3.py](file:///c:/Users/HarshitBorana/OneDrive%20-%20Kadel%20Labs%20Private%20Limited/Desktop/Build_Innovations/crdb_skillforge/tools/aws/s3.py)

- Real DB connection handling with embedded in-memory SQL execution fallback for offline test suites.
- Distributed Vector Indexing support (vector search in CockroachDB).
- `ccloud` CLI wrapper integration.
- AWS Bedrock runtime client & Amazon S3 diagnostic report archive helper.

---

### 4. Skill Validator & CLI Scaffolding (`tools/`)

#### [NEW] [tools/validate-skill.py](file:///c:/Users/HarshitBorana/OneDrive%20-%20Kadel%20Labs%20Private%20Limited/Desktop/Build_Innovations/crdb_skillforge/tools/validate-skill.py)
#### [NEW] [tools/new-skill.sh](file:///c:/Users/HarshitBorana/OneDrive%20-%20Kadel%20Labs%20Private%20Limited/Desktop/Build_Innovations/crdb_skillforge/tools/new-skill.sh)
#### [NEW] [tools/new-skill.py](file:///c:/Users/HarshitBorana/OneDrive%20-%20Kadel%20Labs%20Private%20Limited/Desktop/Build_Innovations/crdb_skillforge/tools/new-skill.py)

---

### 5. Adapters Platform (`adapters/`)

#### [NEW] MCP Server (`adapters/mcp-server/`)
- Expresses resources (`skill://...`) and tools (`search_skills`, `get_skill`, `execute_sql`, `explain_analyze`, `inspect_schema`, `inspect_indexes`, `cluster_metadata`, `vector_search`).

#### [NEW] Cursor Adapter (`adapters/cursor/generate.py`)
- Automatically outputs `.cursor/rules/*.mdc` rules.

#### [NEW] LangChain Adapter (`adapters/langchain/`)
- Exposes `StructuredTool` wrappers for LangChain agents.

#### [NEW] AWS Bedrock / Lambda Adapter (`adapters/aws-bedrock/`, `adapters/aws-lambda/`)
- OpenAPI spec generator for Bedrock Action Groups & Lambda handler (`lambda_function.py`) for executing CrDB skills inside AWS serverless agents.

---

### 6. Evaluation Harness (`tools/eval-harness/`)

#### [NEW] `tools/eval-harness/cases.yaml`, `run.py`, `scoring.py`

---

### 7. Functional Demo & AWS / Cockroach Agentic Memory App (`examples/`)

#### [NEW] [examples/performance-diagnosis/run_demo.py](file:///c:/Users/HarshitBorana/OneDrive%20-%20Kadel%20Labs%20Private%20Limited/Desktop/Build_Innovations/crdb_skillforge/examples/performance-diagnosis/run_demo.py)
#### [NEW] [examples/agentic-memory-bedrock/run_agentic_memory.py](file:///c:/Users/HarshitBorana/OneDrive%20-%20Kadel%20Labs%20Private%20Limited/Desktop/Build_Innovations/crdb_skillforge/examples/agentic-memory-bedrock/run_agentic_memory.py)

- Demonstrates an agent storing long-term memory & diagnostic history in CockroachDB, querying vector embeddings, invoking Bedrock model, and archiving execution telemetry to S3.

---

### 8. Testing Suite (`tests/`)

- Unit, integration, skill validator, MCP protocol, AWS adapter, and evaluation harness tests.

---

### 9. GitHub Actions Workflows (`.github/workflows/`)

- `validate.yml`, `tests.yml`, `eval.yml`, `nightly.yml`.

---

### 10. Documentation & Submission Materials (`docs/`)

#### [NEW] `docs/architecture.md`, `docs/skill-authoring.md`, `docs/execution.md`, `docs/evaluation.md`, `docs/mcp.md`, `docs/cursor.md`, `docs/langchain.md`, `docs/aws-integration.md`, `docs/demo-video-script.md`, `docs/submission-guide.md`

---

## Verification Plan

### Automated Tests
- `python tools/validate-skill.py`
- `pytest`
- `npm test` inside `adapters/mcp-server`
- `python tools/eval-harness/run.py`
- `python adapters/aws-bedrock/generate_openapi.py`

### Final Push & Submission Check
- Initialize local git repo, add `origin https://github.com/harshit075/crdb-skillforge.git`, commit, and push.
