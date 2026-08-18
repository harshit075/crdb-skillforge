# Model Context Protocol (MCP) Server Guide

CrDB SkillForge includes a full Model Context Protocol (MCP) server implementation for Claude, Cursor, and MCP clients.

## Starting the MCP Server

```bash
make mcp
```
or
```bash
cd adapters/mcp-server
npm start
```

## Protocol Endpoints & Exposed Tools

### Resources
- `skill://<skill-name>` — Markdown definition of canonical skill.

### Exposed Tools
- `search_skills`
- `get_skill`
- `execute_sql`
- `explain_analyze`
- `inspect_schema`
- `inspect_indexes`
- `cluster_metadata`
- `vector_search`
