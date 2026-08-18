# Contributing to CrDB SkillForge

Thank you for your interest in contributing to **CrDB SkillForge**!

We welcome contributions from database engineers, AI developers, and CockroachDB practitioners. Skills in CrDB SkillForge must be **machine-executable** and technically verified against real CockroachDB behavior.

## Core Principle

> **Skills are technically reviewed, not merely prose-reviewed.**

Every skill contribution must include:
1. Valid `SKILL.md` with structured YAML frontmatter.
2. Executable diagnostic SQL queries and tool requirements.
3. Recommended action and verification steps.
4. Evaluation cases in `tools/eval-harness/cases.yaml`.

---

## Development Workflow

### 1. Prerequisites
- Python >= 3.10
- Node.js >= 18
- Docker (optional, for running local CockroachDB node)

### 2. Setup Repository
```bash
git clone https://github.com/harshit075/crdb-skillforge.git
cd crdb-skillforge
make setup
```

### 3. Scaffold a New Skill
Use the scaffolding helper to create a skill directory structure:
```bash
python tools/new_skill.py --category performance --name query-plan-regression
```
or on Linux/macOS:
```bash
./tools/new-skill.sh --category performance --name query-plan-regression
```

### 4. Authoring Guidelines
- Fill in all required frontmatter fields (`name`, `category`, `description`, `cockroach_versions`, `tags`, `requires_tools`, `maintainers`, `last_verified`, `license`, `execution_mode`, `risk_level`).
- Structure the skill workflow clearly:
  - When to use
  - Required context
  - Diagnosis
  - Tool calls & SQL queries
  - Interpretation rules
  - Recommended fix
  - Verification steps

### 5. Running Validation & Tests
Before submitting a pull request, verify your changes pass all validations:
```bash
make validate
make test
make eval
```

---

## Code of Conduct
Please review and adhere to our [Code of Conduct](CODE_OF_CONDUCT.md) in all interactions.

## License
By contributing, you agree that your contributions will be licensed under the project's [Apache-2.0 License](LICENSE).
