const API_BASE = 'http://127.0.0.1:8000';

function getAuthHeader() {
  const access = localStorage.getItem('access');
  return access ? { 'Authorization': `Bearer ${access}` } : {};
}

let currentPropostaId = null;
let assignModal = null;

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
      options.headers['Authorization'] = `Bearer ${localStorage.getItem('access')}`;
      return fetch(url, options);
    }
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
    window.location.href = 'index.html';
    return res;
  }
  return res;
}

async function fetchProfessores() {
  const headers = { 'Content-Type': 'application/json' };
  const res = await fetchWithAuth(`${API_BASE}/api/professores/`, { headers });
  if (!res.ok) return [];
  const data = await res.json();
  const items = Array.isArray(data) ? data : (data.results || []);
  return items;
}

// Garante que o usuário atual é Coordenador; senão redireciona
async function ensureIsCoordinator() {
  const role = localStorage.getItem('user_role');
  const email = localStorage.getItem('user_email');
  if (role === 'Coordenador') return true; // atalho
  // valida via API
  if (!email) {
    window.location.href = 'index.html';
    return false;
  }
  try {
    const res = await fetchWithAuth(`${API_BASE}/api/coordenadores/?search=${encodeURIComponent(email)}`, { headers: { 'Content-Type': 'application/json' } });
    if (!res.ok) {
      window.location.href = 'projects.html';
      return false;
    }
    const data = await res.json();
    const items = Array.isArray(data) ? data : (data.results || []);
    if (items.length === 0) {
      // não é coordenador
      window.location.href = 'projects.html';
      return false;
    }
    // seta role para acelerar próximas verificações
    localStorage.setItem('user_role', 'Coordenador');
    return true;
  } catch (err) {
    console.error('Erro validando coordenador', err);
    window.location.href = 'index.html';
    return false;
  }
}

async function getCurrentCoordenadorId() {
  const email = localStorage.getItem('user_email');
  if (!email) return null;
  const headers = { 'Content-Type': 'application/json', ...getAuthHeader() };
  const res = await fetch(`${API_BASE}/api/coordenadores/?search=${encodeURIComponent(email)}`, { headers });
  if (!res.ok) return null;
  const data = await res.json();
  const items = Array.isArray(data) ? data : (data.results || []);
  return items.length ? items[0].id : null;
}

async function fetchPropostas() {
  const headers = { 'Content-Type': 'application/json' };
  const res = await fetchWithAuth(`${API_BASE}/api/propostas/em_analise/`, { headers });
  if (res.status === 401) {
    alert('Token inválido ou expirado. Faça login novamente.');
    window.location.href = 'index.html';
    return;
  }
  if (!res.ok) {
    document.getElementById('projectsList').innerHTML = `<div class="col-12 text-danger">Erro ao buscar propostas</div>`;
    return;
  }
  const data = await res.json();
  const items = Array.isArray(data) ? data : (data.results || []);
  renderPropostas(items);
}

function renderPropostas(items) {
  const container = document.getElementById('projectsList');
  if (!items || items.length === 0) {
    container.innerHTML = `<div class="col-12">Nenhuma proposta em análise.</div>`;
    return;
  }
  container.innerHTML = items.map(p => (
    `<div class="col-md-6" data-id="${p.id}">
      <div class="card">
        <div class="card-body">
          <h5 class="card-title">${escapeHtml(p.titulo)}</h5>
          <p class="card-text">${escapeHtml(p.descricao || '')}</p>
          <p class="text-muted small">Empresa: ${escapeHtml(p.empresa?.nome || (p.empresa || ''))}</p>
          <div class="d-flex gap-2 mt-2">
            <button class="btn btn-sm btn-success btn-approve" data-id="${p.id}">Aprovar</button>
            <button class="btn btn-sm btn-danger btn-reject" data-id="${p.id}">Rejeitar</button>
          </div>
        </div>
      </div>
    </div>`
  )).join('');

  // Attach handlers
  document.querySelectorAll('.btn-approve').forEach(b => b.addEventListener('click', onApprove));
  document.querySelectorAll('.btn-reject').forEach(b => b.addEventListener('click', onReject));
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

async function onApprove(evt) {
  // Ao invés de aprovar diretamente, abrimos o modal para escolher o professor
  // e transformar a proposta em projeto.
  const id = evt.currentTarget.dataset.id;
  currentPropostaId = id;
  // Prepara modal: carrega professores
  const profs = await fetchProfessores();
  const select = document.getElementById('profSelect');
  select.innerHTML = profs.map(p => `<option value="${p.id}">${escapeHtml(p.nome)} (${escapeHtml(p.email)})</option>`).join('');
  // Abre modal
  if (!assignModal) assignModal = new bootstrap.Modal(document.getElementById('assignModal'));
  assignModal.show();
}

async function onReject(evt) {
  const id = evt.currentTarget.dataset.id;
  if (!confirm('Confirma rejeitar esta proposta?')) return;
  const headers = { 'Content-Type': 'application/json', ...getAuthHeader() };
    const res = await fetchWithAuth(`${API_BASE}/api/propostas/${id}/rejeitar/`, { method: 'POST', headers });
  if (!res.ok) {
    alert('Erro ao rejeitar proposta');
    return;
  }
  await fetchPropostas();
}

// Confirmar atribuição e inicialização
document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('confirmAssign');
  if (btn) btn.addEventListener('click', async () => {
    const select = document.getElementById('profSelect');
    const profId = select.value;
    if (!profId) {
      alert('Escolha um professor');
      return;
    }
    const coordId = await getCurrentCoordenadorId();
    const headers = { 'Content-Type': 'application/json' };
    const res = await fetchWithAuth(`${API_BASE}/api/propostas/${currentPropostaId}/ajeitar/`, {
      method: 'POST',
      headers,
      body: JSON.stringify({ professor_id: Number(profId), coordenador_id: coordId })
    });
    if (!res.ok) {
      const txt = await res.text();
      alert('Erro ao transformar proposta em projeto: ' + txt);
      return;
    }
    assignModal.hide();
    alert('Proposta transformada em projeto com sucesso');
    await fetchPropostas();
  });

  // logout
  const logoutBtn = document.getElementById('logoutBtn');
  if (logoutBtn) logoutBtn.addEventListener('click', () => {
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
    window.location.href = 'index.html';
  });

  // Listeners do modal de edição
  const saveBtn = document.getElementById('saveEdit');
  if (saveBtn) saveBtn.addEventListener('click', saveProjectEdits);
  
  const doneBtn = document.getElementById('markDone');
  if (doneBtn) doneBtn.addEventListener('click', markProjectDone);

  // carrega propostas
  fetchPropostas();
  // carrega todos os projetos na aba Projetos
  fetchAllProjects();
});

async function fetchAllProjects() {
  const headers = { 'Content-Type': 'application/json' };
  const res = await fetchWithAuth(`${API_BASE}/api/projetos/`, { headers });
  if (!res.ok) {
    document.getElementById('allProjectsList').innerHTML = `<div class="col-12 text-danger">Erro ao buscar projetos</div>`;
    return;
  }
  const data = await res.json();
  const items = Array.isArray(data) ? data : (data.results || []);
  renderAllProjects(items);
}

function renderAllProjects(items) {
  const container = document.getElementById('allProjectsList');
  if (!items || items.length === 0) {
    container.innerHTML = `<div class="col-12">Nenhum projeto encontrado.</div>`;
    return;
  }
  container.innerHTML = items.map(p => {
    const hasProf = p.professor_responsavel || p.professor_responsavel === 0 ? true : false;
    const professorName = p.professor_nome || '';
    return (`<div class="col-md-6" data-id="${p.id}">
      <div class="card">
        <div class="card-body">
          <h5 class="card-title">${escapeHtml(p.titulo)}</h5>
          <p class="card-text">${escapeHtml(p.descricao || '')}</p>
          <p class="text-muted small">Status: ${escapeHtml(p.status || '')} • Professor: ${escapeHtml(professorName)}</p>
          <div class="d-flex gap-2 mt-2 align-items-center">
            <button class="btn btn-sm btn-warning btn-edit-project" data-project-id="${p.id}">Editar</button>
            ${hasProf ? '' : `<select class="form-select form-select-sm assign-prof-select" data-project-id="${p.id}"><option value="">Carregando...</option></select><button class="btn btn-sm btn-primary btn-assign-prof" data-project-id="${p.id}">Atribuir</button>`}
          </div>
        </div>
      </div>
    </div>`);
  }).join('');

  // Carrega professores para cada select e attach handlers
  document.querySelectorAll('.assign-prof-select').forEach(async (sel) => {
    const profs = await fetchProfessores();
    sel.innerHTML = profs.map(p => `<option value="${p.id}">${escapeHtml(p.nome)} (${escapeHtml(p.email)})</option>`).join('');
  });
  document.querySelectorAll('.btn-assign-prof').forEach(b => b.addEventListener('click', onAssignProfessorClick));
  document.querySelectorAll('.btn-edit-project').forEach(b => b.addEventListener('click', onEditProjectClick));
}

async function onAssignProfessorClick(evt) {
  const projectId = evt.currentTarget.dataset.projectId;
  const select = document.querySelector(`.assign-prof-select[data-project-id='${projectId}']`);
  if (!select) return alert('Selecione um professor');
  const profId = select.value;
  if (!profId) return alert('Escolha um professor');
  if (!confirm('Confirma atribuir este professor ao projeto?')) return;
  const coordId = await getCurrentCoordenadorId();
  const headers = { 'Content-Type': 'application/json' };
  const res = await fetchWithAuth(`${API_BASE}/api/projetos/${projectId}/assign_professor/`, {
    method: 'POST', headers, body: JSON.stringify({ professor_id: Number(profId), coordenador_id: coordId })
  });
  if (!res.ok) {
    const txt = await res.text();
    alert('Erro ao atribuir professor: ' + txt);
    return;
  }
  alert('Professor atribuído com sucesso');
  await fetchAllProjects();
}

// Edição de projetos
let editModal = null;
let currentEditProjectId = null;

async function onEditProjectClick(evt) {
  const projectId = evt.currentTarget.dataset.projectId;
  currentEditProjectId = projectId;
  
  // Busca dados do projeto
  const headers = { 'Content-Type': 'application/json' };
  const res = await fetchWithAuth(`${API_BASE}/api/projetos/${projectId}/`, { headers });
  if (!res.ok) {
    alert('Erro ao carregar projeto');
    return;
  }
  const project = await res.json();
  
  // Preenche modal
  document.getElementById('editTitulo').value = project.titulo || '';
  document.getElementById('editDescricao').value = project.descricao || '';
  document.getElementById('editProgresso').value = project.progresso || 0;
  document.getElementById('editStatus').value = project.status || 'Em andamento';
  document.getElementById('editAlunos').value = project.alunos || '';
  document.getElementById('editAnexos').value = project.anexos || '';
  
  // Abre modal
  if (!editModal) editModal = new bootstrap.Modal(document.getElementById('editModal'));
  editModal.show();
}

async function saveProjectEdits() {
  const titulo = document.getElementById('editTitulo').value;
  const descricao = document.getElementById('editDescricao').value;
  const progresso = parseInt(document.getElementById('editProgresso').value) || 0;
  const status = document.getElementById('editStatus').value;
  const alunos = document.getElementById('editAlunos').value;
  const anexos = document.getElementById('editAnexos').value;
  
  const body = { titulo, descricao, progresso, status, alunos, anexos };
  const headers = { 'Content-Type': 'application/json' };
  const res = await fetchWithAuth(`${API_BASE}/api/projetos/${currentEditProjectId}/`, {
    method: 'PATCH',
    headers,
    body: JSON.stringify(body)
  });
  
  if (!res.ok) {
    const txt = await res.text();
    alert('Erro ao salvar projeto: ' + txt);
    return;
  }
  
  editModal.hide();
  alert('Projeto atualizado com sucesso');
  await fetchAllProjects();
}

async function markProjectDone() {
  if (!confirm('Marcar este projeto como concluído?')) return;
  
  const body = { status: 'Concluído', progresso: 100 };
  const headers = { 'Content-Type': 'application/json' };
  const res = await fetchWithAuth(`${API_BASE}/api/projetos/${currentEditProjectId}/`, {
    method: 'PATCH',
    headers,
    body: JSON.stringify(body)
  });
  
  if (!res.ok) {
    const txt = await res.text();
    alert('Erro ao marcar projeto como concluído: ' + txt);
    return;
  }
  
  editModal.hide();
  alert('Projeto marcado como concluído');
  await fetchAllProjects();
}
