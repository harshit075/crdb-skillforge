# Evaluation Harness Guide

CrDB SkillForge features an automated benchmark harness (`tools/eval-harness/`) to evaluate skill discovery precision and real database diagnostic accuracy.

## Running Evaluation

```bash
make eval
```
or
```bash
python tools/eval-harness/run.py
```

## Adding Evaluation Cases

Add test cases to `tools/eval-harness/cases.yaml`:

```yaml
- name: sequential-primary-key-hotspot
  skill: avoiding-hotspots
  prompt: >
    Our CockroachDB cluster has uneven load across nodes and our primary key
    column is monotonically increasing. How should we fix it?
  expected_skill:
    - avoiding-hotspots
  expected_behaviors:
    - identify-monotonic-key
    - explain-hotspot-risk
    - recommend-mitigation
  database_required: true
  verification: "SELECT column_name FROM information_schema.columns WHERE table_name = 'orders';"
```
