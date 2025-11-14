// empresa.js — UI para empresas criarem e visualizarem suas propostas
// Depende de: js/projects.js (fetchWithAuth, API_BASE)

// Sinaliza ao projects.js para não inicializar automaticamente
window.skipAutoFetchProjects = true;

let currentEmpresaIdCache = null;

async function getCurrentEmpresaId() {
  if (currentEmpresaIdCache) return currentEmpresaIdCache;
  const email = localStorage.getItem('user_email');
  if (!email) return null;
  const res = await fetchWithAuth(`${API_BASE}/api/empresas/?search=${encodeURIComponent(email)}`, { headers: { 'Content-Type': 'application/json' } });
  if (!res.ok) return null;
  const data = await res.json();
  const items = Array.isArray(data) ? data : (data.results || []);
  if (!items.length) return null;
  currentEmpresaIdCache = items[0].id;
  return currentEmpresaIdCache;
}

async function fetchMinhasPropostas() {
  console.log('[empresa.js] Carregando propostas...');
  const empresaId = await getCurrentEmpresaId();
  if (!empresaId) {
    document.getElementById('propostasList').innerHTML = `<div class="col-12 text-warning">Empresa não identificada.</div>`;
    return;
  }
  
  const headers = { 'Content-Type': 'application/json' };
  const res = await fetchWithAuth(`${API_BASE}/api/propostas/?empresa=${empresaId}`, { headers });
  if (!res.ok) {
    document.getElementById('propostasList').innerHTML = `<div class="col-12 text-danger">Erro ao buscar propostas</div>`;
    return;
  }
  const data = await res.json();
  const items = Array.isArray(data) ? data : (data.results || []);
  renderPropostas(items);
}

function renderPropostas(items) {
  const container = document.getElementById('propostasList');
  if (!items || items.length === 0) {
    container.innerHTML = `<div class="col-12">Nenhuma proposta enviada ainda.</div>`;
    return;
  }
  
  container.innerHTML = items.map(p => {
    const statusBadge = getStatusBadge(p.status);
    return (`<div class="col-md-6">
      <div class="card">
        <div class="card-body">
          <h5 class="card-title">${escapeHtml(p.titulo)}</h5>
          <p class="card-text">${escapeHtml(p.descricao || '')}</p>
          <p class="text-muted small">
            Enviado em: ${formatDate(p.data_envio)} • Status: ${statusBadge}
          </p>
          ${p.anexos ? `<p class="text-muted small">Anexos: ${escapeHtml(p.anexos)}</p>` : ''}
        </div>
      </div>
    </div>`);
  }).join('');
}

function getStatusBadge(status) {
  const badges = {
    'Em análise': '<span class="badge bg-warning text-dark">Em análise</span>',
    'Aprovada': '<span class="badge bg-success">Aprovada</span>',
    'Rejeitada': '<span class="badge bg-danger">Rejeitada</span>',
    'Transformada em projeto': '<span class="badge bg-info">Transformada em projeto</span>'
  };
  return badges[status] || `<span class="badge bg-secondary">${escapeHtml(status)}</span>`;
}

function formatDate(dateStr) {
  if (!dateStr) return '';
  const d = new Date(dateStr);
  return d.toLocaleDateString('pt-BR');
}

function escapeHtml(unsafe) {
  if (!unsafe) return '';
  return String(unsafe)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}

async function createProposta(evt) {
  evt.preventDefault();
  console.log('[empresa.js] Criando proposta...');
  
  const titulo = document.getElementById('titulo').value;
  const descricao = document.getElementById('descricao').value;
  const anexos = document.getElementById('anexos').value || '';
  
  if (!titulo || !descricao) {
    alert('Preencha título e descrição');
    return;
  }
  
  const payload = { titulo, descricao, anexos };
  const headers = { 'Content-Type': 'application/json' };
  
  const res = await fetchWithAuth(`${API_BASE}/api/propostas/`, {
    method: 'POST',
    headers,
    body: JSON.stringify(payload)
  });
  
  if (!res.ok) {
    const txt = await res.text().catch(() => 'erro desconhecido');
    alert('Erro ao criar proposta: ' + txt);
    return;
  }
  
  alert('Proposta criada com sucesso! Aguarde análise do coordenador.');
  
  // Limpa formulário
  document.getElementById('createPropostaForm').reset();
  
  // Recarrega lista
  await fetchMinhasPropostas();
}

// Inicializa handlers
document.addEventListener('DOMContentLoaded', async () => {
  console.log('[empresa.js] Inicializando...');
  
  // prefetch empresa id
  const empresaId = await getCurrentEmpresaId();
  console.log('[empresa.js] Empresa ID:', empresaId);
  if (empresaId) localStorage.setItem('user_empresa_id', String(empresaId));
  
  // Handler para criar proposta
  const form = document.getElementById('createPropostaForm');
  if (form) form.addEventListener('submit', createProposta);
  
  // Carrega propostas existentes
  await fetchMinhasPropostas();
  
  console.log('[empresa.js] Inicialização completa');
});
