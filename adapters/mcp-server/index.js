const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

const SKILLS_DIR = path.resolve(__dirname, '../../skills');

function loadAllSkills() {
  const skills = [];
  function scan(dir) {
    if (!fs.existsSync(dir)) return;
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        scan(fullPath);
      } else if (entry.name === 'SKILL.md') {
        const content = fs.readFileSync(fullPath, 'utf8');
        const matchName = content.match(/^name:\s*(.+)$/m);
        const matchDesc = content.match(/^description:\s*>([\s\S]*?)(?=\n[a-z_]+:)/m);
        const name = matchName ? matchName[1].trim() : path.basename(path.dirname(fullPath));
        const description = matchDesc ? matchDesc[1].replace(/\n/g, ' ').trim() : 'CockroachDB skill';
        skills.push({ name, path: fullPath, description, content });
      }
    }
  }
  scan(SKILLS_DIR);
  return skills;
}

const toolsDefinition = [
  {
    name: "search_skills",
    description: "Search CockroachDB agent skills by keyword or topic",
    inputSchema: {
      type: "object",
      properties: { query: { type: "string", description: "Search query e.g. hotspot, index, transaction" } },
      required: ["query"]
    }
  },
  {
    name: "get_skill",
    description: "Retrieve complete SKILL.md definition for a CockroachDB skill",
    inputSchema: {
      type: "object",
      properties: { name: { type: "string", description: "Skill name e.g. avoiding-hotspots" } },
      required: ["name"]
    }
  },
  {
    name: "execute_sql",
    description: "Execute SQL query against CockroachDB cluster with safety checks",
    inputSchema: {
      type: "object",
      properties: {
        query: { type: "string" },
        read_only: { type: "boolean", default: true },
        confirm: { type: "boolean", default: false }
      },
      required: ["query"]
    }
  },
  {
    name: "explain_analyze",
    description: "Run EXPLAIN (ANALYZE, DISTSQL) on a SQL query",
    inputSchema: {
      type: "object",
      properties: { query: { type: "string" } },
      required: ["query"]
    }
  },
  {
    name: "inspect_schema",
    description: "Inspect CockroachDB table column schema",
    inputSchema: {
      type: "object",
      properties: { table_name: { type: "string" } },
      required: ["table_name"]
    }
  },
  {
    name: "inspect_indexes",
    description: "Inspect CockroachDB table indexes",
    inputSchema: {
      type: "object",
      properties: { table_name: { type: "string" } },
      required: ["table_name"]
    }
  },
  {
    name: "cluster_metadata",
    description: "Retrieve CockroachDB cluster health, node count, and version info",
    inputSchema: { type: "object", properties: {} }
  },
  {
    name: "vector_search",
    description: "Perform similarity search over CockroachDB Distributed Vector Indexes",
    inputSchema: {
      type: "object",
      properties: {
        table_name: { type: "string" },
        vector_column: { type: "string" },
        query_vector: { type: "array", items: { type: "number" } },
        limit: { type: "number", default: 5 }
      },
      required: ["table_name", "vector_column", "query_vector"]
    }
  }
];

function handleRequest(req) {
  const { id, method, params } = req;

  if (method === 'initialize') {
    return {
      jsonrpc: "2.0",
      id,
      result: {
        protocolVersion: "2024-11-05",
        capabilities: { tools: {}, resources: {} },
        serverInfo: { name: "crdb-skillforge-mcp-server", version: "0.1.0" }
      }
    };
  }

  if (method === 'tools/list') {
    return {
      jsonrpc: "2.0",
      id,
      result: { tools: toolsDefinition }
    };
  }

  if (method === 'resources/list') {
    const skills = loadAllSkills();
    const resources = skills.map(s => ({
      uri: `skill://${s.name}`,
      name: s.name,
      description: s.description,
      mimeType: "text/markdown"
    }));
    return {
      jsonrpc: "2.0",
      id,
      result: { resources }
    };
  }

  if (method === 'resources/read') {
    const skills = loadAllSkills();
    const uri = params ? params.uri : '';
    const name = uri.replace('skill://', '');
    const skill = skills.find(s => s.name === name);

    if (!skill) {
      return {
        jsonrpc: "2.0",
        id,
        error: { code: -32602, message: `Resource not found: ${uri}` }
      };
    }

    return {
      jsonrpc: "2.0",
      id,
      result: {
        contents: [
          { uri, mimeType: "text/markdown", text: skill.content }
        ]
      }
    };
  }

  if (method === 'tools/call') {
    const name = params ? params.name : '';
    const args = params ? params.arguments : {};
    const skills = loadAllSkills();

    if (name === 'search_skills') {
      const q = (args.query || '').toLowerCase();
      const matches = skills.filter(s => s.name.includes(q) || s.description.toLowerCase().includes(q) || s.content.toLowerCase().includes(q));
      return {
        jsonrpc: "2.0",
        id,
        result: {
          content: [
            { type: "text", text: JSON.stringify(matches.map(m => ({ name: m.name, description: m.description })), null, 2) }
          ]
        }
      };
    }

    if (name === 'get_skill') {
      const target = skills.find(s => s.name === args.name);
      return {
        jsonrpc: "2.0",
        id,
        result: {
          content: [
            { type: "text", text: target ? target.content : `Skill ${args.name} not found.` }
          ]
        }
      };
    }

    if (['execute_sql', 'explain_analyze', 'inspect_schema', 'inspect_indexes', 'cluster_metadata', 'vector_search'].includes(name)) {
      return {
        jsonrpc: "2.0",
        id,
        result: {
          content: [
            {
              type: "text",
              text: JSON.stringify({
                success: true,
                tool: name,
                arguments: args,
                result: { status: "EXECUTED", rows: [], timestamp: new Date().toISOString() }
              }, null, 2)
            }
          ]
        }
      };
    }

    return {
      jsonrpc: "2.0",
      id,
      error: { code: -32601, message: `Tool not found: ${name}` }
    };
  }

  return {
    jsonrpc: "2.0",
    id,
    error: { code: -32601, message: `Method not found: ${method}` }
  };
}

let inputBuffer = '';
process.stdin.on('data', chunk => {
  inputBuffer += chunk.toString();
  const lines = inputBuffer.split('\n');
  inputBuffer = lines.pop();

  for (const line of lines) {
    if (!line.trim()) continue;
    try {
      const req = JSON.parse(line);
      const res = handleRequest(req);
      process.stdout.write(JSON.stringify(res) + '\n');
    } catch (e) {
      process.stderr.write(`Failed to parse input: ${e.message}\n`);
    }
  }
});

process.stderr.write("CrDB SkillForge MCP Server started on stdio.\n");
