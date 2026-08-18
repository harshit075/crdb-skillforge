.PHONY: setup install validate test integration eval crdb-up crdb-down crdb-reset mcp cursor langchain demo clean help

PYTHON ?= python
NPM ?= npm

help:
	@echo "CrDB SkillForge — Executable CockroachDB Agent Skills Platform"
	@echo "Available commands:"
	@echo "  make setup        Install all dependencies (Python & Node)"
	@echo "  make install      Install Python package in editable mode"
	@echo "  make validate     Validate all canonical SKILL.md files"
	@echo "  make test         Run Python & MCP unit test suites"
	@echo "  make integration  Run database integration tests"
	@echo "  make eval         Run skill discovery & diagnosis evaluation harness"
	@echo "  make crdb-up      Start local CockroachDB container"
	@echo "  make crdb-down    Stop local CockroachDB container"
	@echo "  make crdb-reset   Reset local CockroachDB test data"
	@echo "  make mcp          Start MCP server"
	@echo "  make cursor       Generate Cursor rule files (.cursor/rules/)"
	@echo "  make langchain    Build & verify LangChain StructuredTools package"
	@echo "  make app          Start interactive web application studio (http://localhost:8080)"
	@echo "  make demo         Run end-to-end performance diagnosis demonstration"
	@echo "  make clean        Clean build artifacts and temporary files"

setup: install
	@echo "Setting up Node.js dependencies for MCP server..."
	@cd adapters/mcp-server && $(NPM) install

install:
	@echo "Installing Python dependencies..."
	@$(PYTHON) -m pip install -e .[dev,langchain,aws]

validate:
	@echo "Validating canonical skills..."
	@$(PYTHON) tools/validate-skill.py

test: validate
	@echo "Running unit test suites..."
	@$(PYTHON) -m pytest tests/unit tests/skills tests/adapters
	@cd adapters/mcp-server && $(NPM) test

integration:
	@echo "Running integration tests..."
	@$(PYTHON) -m pytest tests/integration

eval:
	@echo "Running evaluation harness..."
	@$(PYTHON) tools/eval-harness/run.py

crdb-up:
	@echo "Starting CockroachDB single-node container..."
	@docker-compose -f docker/cockroach/docker-compose.yml up -d || docker run -d --name crdb-skillforge-node -p 26257:26257 -p 8080:8080 cockroachdb/cockroach:v24.1.0 start-single-node --insecure

crdb-down:
	@echo "Stopping CockroachDB container..."
	@docker-compose -f docker/cockroach/docker-compose.yml down || docker stop crdb-skillforge-node && docker rm crdb-skillforge-node

crdb-reset:
	@echo "Resetting CockroachDB test schema and data..."
	@$(PYTHON) tools/scripts/reset_db.py

mcp:
	@echo "Starting CrDB SkillForge MCP Server..."
	@cd adapters/mcp-server && $(NPM) start

cursor:
	@echo "Generating Cursor rule files..."
	@$(PYTHON) adapters/cursor/generate.py

langchain:
	@echo "Generating and testing LangChain adapter tools..."
	@$(PYTHON) -c "from adapters.langchain.src import load_skills; skills = load_skills(); print(f'Successfully loaded {len(skills)} LangChain StructuredTools')"

app:
	@echo "Starting CrDB SkillForge Web Application on http://localhost:8080..."
	@$(PYTHON) app/server.py

demo:
	@echo "Executing end-to-end performance diagnosis demo..."
	@$(PYTHON) examples/performance-diagnosis/run_demo.py

clean:
	@echo "Cleaning temporary files..."
	@rm -rf build dist *.egg-info .pytest_cache .coverage htmlcov .cursor/rules/*.mdc
