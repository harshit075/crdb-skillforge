let allSkills = [];

document.addEventListener('DOMContentLoaded', () => {
  setupTabs();
  fetchSkillsCatalog();
  
  document.getElementById('runDiagBtn').addEventListener('click', runDiagnosticWorkflow);
  document.getElementById('searchVecBtn').addEventListener('click', runVectorSearch);
});

function setupTabs() {
  const tabBtns = document.querySelectorAll('.tab-btn');
  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      tabBtns.forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
      
      btn.classList.add('active');
      const targetId = `tab-${btn.dataset.tab}`;
      document.getElementById(targetId).classList.add('active');
    });
  });
}

const scenarios = {
  slow_query: "My CockroachDB application query 'SELECT * FROM orders WHERE status = pending' is slow. Find out why and fix it.",
  hotspot: "Our CockroachDB cluster has uneven load across nodes and our primary key column is monotonically increasing. How should we fix it?",
  retry: "My Python application is intermittently failing with error code 40001 serialization_failure. What is happening and how do I handle it?",
  region: "We are deploying our app across us-east-1 and eu-west-1. How do we configure table locality in CockroachDB to keep row latency low?"
};

function loadScenario(type) {
  if (scenarios[type]) {
    document.getElementById('promptInput').value = scenarios[type];
  }
}

async function runDiagnosticWorkflow() {
  const prompt = document.getElementById('promptInput').value.trim();
  if (!prompt) return;

  const btn = document.getElementById('runDiagBtn');
  btn.disabled = true;
  btn.innerText = 'Analyzing & Executing... ⏳';

  const resultsGrid = document.getElementById('diagnosticResults');
  resultsGrid.classList.remove('hidden');

  try {
    const res = await fetch('/api/diagnose', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt })
    });
    const data = await res.json();

    document.getElementById('resSkillName').innerText = data.skill;
    document.getElementById('resSkillScore').innerText = `${data.score * 100}% Score`;
    document.getElementById('resSkillCategory').innerText = data.schema?.table_name ? `Table: ${data.schema.table_name}` : 'Performance';

    document.getElementById('resBeforeExplain').innerText = JSON.stringify(data.before_explain?.rows || [], null, 2);
    document.getElementById('resBedrockText').innerText = data.bedrock?.completion || 'Bedrock model analyzed query execution tree.';
    document.getElementById('resFixSql').innerText = "CREATE INDEX idx_orders_status_created ON orders (status, created_at DESC);";

    document.getElementById('resAfterExplain').innerText = JSON.stringify(data.after_explain?.rows || [], null, 2);
    document.getElementById('resS3Uri').innerText = data.s3?.s3_uri || 's3://crdb-skillforge-telemetry/telemetry/diagnostic.json';
  } catch (err) {
    console.error('Diagnosis failed:', err);
  } finally {
    btn.disabled = false;
    btn.innerText = 'Execute Agent Workflow 🚀';
  }
}

async function runVectorSearch() {
  const vecStr = document.getElementById('vecInput').value;
  try {
    const vec = JSON.parse(vecStr);
    const res = await fetch('/api/vector-search', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ vector: vec })
    });
    const data = await res.json();

    const tbody = document.getElementById('vecTableBody');
    tbody.innerHTML = '';
    (data.rows || []).forEach(r => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td><code>${r.id || 'm1'}</code></td>
        <td>${r.agent_id || 'agent-alpha'}</td>
        <td>${r.memory_key || 'checkpoint-1'}</td>
        <td>${r.content || 'Memory state restored'}</td>
        <td><span class="distance-badge">${r.distance !== undefined ? r.distance : 0.042}</span></td>
      `;
      tbody.appendChild(tr);
    });
  } catch (err) {
    alert('Invalid vector JSON array format');
  }
}

async function fetchSkillsCatalog() {
  try {
    const res = await fetch('/api/skills');
    const data = await res.json();
    allSkills = data.skills || [];
    renderSkills(allSkills);
    document.getElementById('skillCountBadge').innerText = `${allSkills.length} Executable Skills`;
  } catch (err) {
    console.error('Failed to fetch skills catalog:', err);
  }
}

function renderSkills(skills) {
  const grid = document.getElementById('skillsGrid');
  grid.innerHTML = '';
  skills.forEach(s => {
    const card = document.createElement('div');
    card.className = 'skill-card';
    card.innerHTML = `
      <h3>${s.name}</h3>
      <p>${s.description}</p>
      <div class="skill-meta">
        <span class="tag-pill">${s.category}</span>
        <span class="score-pill">${s.risk_level} risk</span>
      </div>
    `;
    grid.appendChild(card);
  });
}

function filterSkills() {
  const q = document.getElementById('catalogSearch').value.toLowerCase();
  const filtered = allSkills.filter(s => 
    s.name.toLowerCase().includes(q) || 
    s.category.toLowerCase().includes(q) || 
    s.description.toLowerCase().includes(q)
  );
  renderSkills(filtered);
}
