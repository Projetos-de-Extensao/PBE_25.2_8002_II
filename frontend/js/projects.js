const API_BASE = 'http://127.0.0.1:8000';

function getAuthHeader() {
  const access = localStorage.getItem('access');
  return access ? { 'Authorization': `Bearer ${access}` } : {};
}

// fetchWithAuth: adiciona Authorization automaticamente, tenta refresh em 401 e re-tenta
async function refreshAccess() {
  const refresh = localStorage.getItem('refresh');
  if (!refresh) return false;
  try {
    const res = await fetch(`${API_BASE}/api/token/refresh/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh })
    });
    if (!res.ok) return false;
    const data = await res.json();
    if (data.access) localStorage.setItem('access', data.access);
    return true;
  } catch (err) {
    console.error('Refresh token failed', err);
    return false;
  }
}

async function fetchWithAuth(url, options = {}, tryRefresh = true) {
  options.headers = options.headers || {};
  const access = localStorage.getItem('access');
  if (access) options.headers['Authorization'] = `Bearer ${access}`;
  const res = await fetch(url, options);
  if (res.status === 401 && tryRefresh) {
    const ok = await refreshAccess();
    if (ok) {
      // retry once with new access
      options.headers['Authorization'] = `Bearer ${localStorage.getItem('access')}`;
      return fetch(url, options);
    }
    // refresh failed: clear tokens and redirect to login
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
    window.location.href = 'index.html';
    return res;
  }
  return res;
}

async function fetchProjects() {
  const headers = { 'Content-Type': 'application/json' };
  const res = await fetchWithAuth(`${API_BASE}/api/projetos/`, { headers });
  if (res.status === 401) {
    // token inválido ou expirado
    alert('Token inválido ou expirado. Faça login novamente.');
    window.location.href = 'index.html';
    return;
  }
  if (!res.ok) {
    document.getElementById('projectsList').innerHTML = `<div class="col-12 text-danger">Erro ao buscar projetos</div>`;
    return;
  }
  const data = await res.json();
  // Suporta resposta paginada do DRF ({count,next,previous,results:[]})
  const items = Array.isArray(data) ? data : (data.results || []);
  renderProjects(items);
  // Detecta papel do usuário e atualiza título
  detectRoleAndSetTitle();
}

async function detectRoleAndSetTitle() {
  const email = localStorage.getItem('user_email');
  const header = getAuthHeader();
  let role = 'Usuário';
  if (!email) {
    document.getElementById('roleTitle').textContent = 'Sou ' + role;
    return;
  }
  try {
    // Tenta identificar pela ordem: Coordenador, Professor, Empresa
    const endpoints = [
      { url: `${API_BASE}/api/coordenadores/?search=${encodeURIComponent(email)}`, label: 'Coordenador' },
      { url: `${API_BASE}/api/professores/?search=${encodeURIComponent(email)}`, label: 'Professor' },
      { url: `${API_BASE}/api/empresas/?search=${encodeURIComponent(email)}`, label: 'Empresa' },
    ];
    for (const ep of endpoints) {
      const res = await fetchWithAuth(ep.url, { headers: { 'Content-Type': 'application/json' } });
      if (!res.ok) continue;
      const data = await res.json();
      const items = Array.isArray(data) ? data : (data.results || []);
      if (items.length > 0) {
        role = ep.label;
        break;
      }
    }
  } catch (err) {
    console.error('Erro detectando papel:', err);
  }
  const titleEl = document.getElementById('roleTitle');
  if (titleEl) titleEl.textContent = 'Sou ' + role;
}

function renderProjects(items) {
  const container = document.getElementById('projectsList');
  if (!items || items.length === 0) {
    container.innerHTML = `<div class="col-12">Nenhum projeto encontrado.</div>`;
    return;
  }
  container.innerHTML = items.map(p => (
    `<div class="col-md-6">
      <div class="card">
        <div class="card-body">
          <h5 class="card-title">${escapeHtml(p.titulo)}</h5>
          <p class="card-text">${escapeHtml(p.descricao || '')}</p>
          <p class="text-muted small">Status: ${escapeHtml(p.status || '')} • Progresso: ${p.progresso || 0}%</p>
        </div>
      </div>
    </div>`
  )).join('');
}

function escapeHtml(unsafe) {
  return unsafe
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}

// logout
const logoutBtn = document.getElementById('logoutBtn');
if (logoutBtn) {
  logoutBtn.addEventListener('click', () => {
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
    window.location.href = 'index.html';
  });
}

// inicializa automaticamente somente se window.skipAutoFetchProjects não estiver setada
// (usado por professor.js e outras páginas especializadas para controlar inicialização)
if (!window.skipAutoFetchProjects) {
  fetchProjects();
}
