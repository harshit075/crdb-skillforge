# Cursor Adapter Guide

The Cursor rule generator converts canonical `SKILL.md` files into Cursor rules (`.cursor/rules/*.mdc`).

## Generating Cursor Rules

```bash
make cursor
```
or
```bash
python adapters/cursor/generate.py
```

Rule files are placed in `.cursor/rules/crdb-*.mdc` and automatically loaded by Cursor IDE when editing SQL or database code.
