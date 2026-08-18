const { spawn } = require('child_process');
const path = require('path');

console.log("Running MCP Protocol Unit Test Suite...");

const serverPath = path.join(__dirname, 'index.js');
const child = spawn('node', [serverPath], { stdio: ['pipe', 'pipe', 'inherit'] });

let output = '';

child.stdout.on('data', data => {
  output += data.toString();
});

const reqs = [
  { jsonrpc: "2.0", id: 1, method: "initialize", params: {} },
  { jsonrpc: "2.0", id: 2, method: "tools/list", params: {} },
  { jsonrpc: "2.0", id: 3, method: "resources/list", params: {} },
  { jsonrpc: "2.0", id: 4, method: "resources/read", params: { uri: "skill://avoiding-hotspots" } },
  { jsonrpc: "2.0", id: 5, method: "tools/call", params: { name: "search_skills", arguments: { query: "hotspot" } } },
  { jsonrpc: "2.0", id: 6, method: "tools/call", params: { name: "get_skill", arguments: { name: "avoiding-hotspots" } } },
  { jsonrpc: "2.0", id: 7, method: "tools/call", params: { name: "execute_sql", arguments: { query: "SELECT version();" } } }
];

for (const r of reqs) {
  child.stdin.write(JSON.stringify(r) + '\n');
}

setTimeout(() => {
  child.stdin.end();
  child.kill();

  const lines = output.trim().split('\n').filter(Boolean);
  console.log(`Received ${lines.length} protocol response lines.`);

  let allPassed = true;
  for (let i = 0; i < lines.length; i++) {
    try {
      const res = JSON.parse(lines[i]);
      if (res.error) {
        console.error(`❌ Request ${res.id} failed:`, res.error);
        allPassed = false;
      } else {
        console.log(`✓ Request ${res.id} (${reqs[i].method}) passed.`);
      }
    } catch (e) {
      console.error(`❌ Failed to parse response line ${i}: ${lines[i]}`);
      allPassed = false;
    }
  }

  if (allPassed && lines.length >= 7) {
    console.log("SUCCESS: All MCP protocol level tests passed!");
    process.exit(0);
  } else {
    console.error("FAILURE: MCP tests failed.");
    process.exit(1);
  }
}, 1500);
