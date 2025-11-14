// professor.js — UI para professores editarem seus projetos
// Depende de: js/projects.js (fetchWithAuth, fetchProjects)

// Sinaliza ao projects.js para não inicializar automaticamente
window.skipAutoFetchProjects = true;

let currentProfessorIdCache = null;
let editModal = null;

async function getCurrentProfessorId() {
  if (currentProfessorIdCache) return currentProfessorIdCache;
  const email = localStorage.getItem('user_email');
  if (!email) return null;
  const res = await fetchWithAuth(`${API_BASE}/api/professores/?search=${encodeURIComponent(email)}`, { headers: { 'Content-Type': 'application/json' } });
  if (!res.ok) return null;
  const data = await res.json();
  const items = Array.isArray(data) ? data : (data.results || []);
  if (!items.length) return null;
  currentProfessorIdCache = items[0].id;
  return currentProfessorIdCache;
}

// Sobrescreve a renderização dos projetos para incluir botão Editar quando aplicável
function renderProjects(items) {
  const container = document.getElementById('projectsList');
  if (!items || items.length === 0) {
    container.innerHTML = `<div class="col-12">Nenhum projeto encontrado.</div>`;
    return;
  }

  const userRole = localStorage.getItem('user_role');
  const userEmail = localStorage.getItem('user_email');

  container.innerHTML = items.map(p => {
    const profId = p.professor_responsavel || null;
    const professorName = p.professor_nome || '';
    // Mostrar botão editar se: (a) usuário é coordenador; (b) usuário é professor responsável
    const showEdit = (userRole === 'Coordenador') ? true : (profId && profId === Number(localStorage.getItem('user_professor_id')));
    const editBtn = showEdit ? `<button class="btn btn-sm btn-outline-primary btn-edit" data-id="${p.id}">Editar</button>` : '';
    return (`<div class="col-md-6">
      <div class="card">
        <div class="card-body">
          <h5 class="card-title">${escapeHtml(p.titulo)}</h5>
          <p class="card-text">${escapeHtml(p.descricao || '')}</p>
          <p class="text-muted small">Status: ${escapeHtml(p.status || '')} • Progresso: ${p.progresso || 0}% • Professor: ${escapeHtml(professorName)}</p>
          <div class="d-flex gap-2 mt-2">${editBtn}</div>
        </div>
      </div>
    </div>`);
  }).join('');

  // attach handlers
  document.querySelectorAll('.btn-edit').forEach(b => b.addEventListener('click', async (evt) => {
    const id = evt.currentTarget.dataset.id;
    await openEditModal(id);
  }));
}

async function openEditModal(projectId) {
  // carrega dados do projeto
  const res = await fetchWithAuth(`${API_BASE}/api/projetos/${projectId}/`, { headers: { 'Content-Type': 'application/json' } });
  if (!res.ok) {
    alert('Erro ao carregar projeto');
    return;
  }
  const p = await res.json();
  document.getElementById('editProjectId').value = p.id;
  document.getElementById('editTitulo').value = p.titulo || '';
  document.getElementById('editDescricao').value = p.descricao || '';
  document.getElementById('editProgresso').value = p.progresso || 0;
  document.getElementById('editStatus').value = p.status || '';
  document.getElementById('editAlunos').value = p.alunos || '';
  document.getElementById('editAnexos').value = p.anexos || '';

  if (!editModal) editModal = new bootstrap.Modal(document.getElementById('editProjectModal'));
  editModal.show();
}

async function saveProjectEdits() {
  const id = document.getElementById('editProjectId').value;
  const payload = {};
  const titulo = document.getElementById('editTitulo').value;
  const descricao = document.getElementById('editDescricao').value;
  const progresso = document.getElementById('editProgresso').value;
  const status = document.getElementById('editStatus').value;
  const alunos = document.getElementById('editAlunos').value;
  const anexos = document.getElementById('editAnexos').value;
  if (titulo !== null) payload.titulo = titulo;
  if (descricao !== null) payload.descricao = descricao;
  if (progresso !== null && progresso !== '') payload.progresso = Number(progresso);
  if (status !== null) payload.status = status;
  if (alunos !== null) payload.alunos = alunos;
  if (anexos !== null) payload.anexos = anexos;

  const headers = { 'Content-Type': 'application/json' };
  const res = await fetchWithAuth(`${API_BASE}/api/projetos/${id}/`, { method: 'PATCH', headers, body: JSON.stringify(payload) });
  if (!res.ok) {
    const txt = await res.text().catch(() => 'erro');
    alert('Erro ao salvar projeto: ' + txt);
    return;
  }
  alert('Projeto atualizado com sucesso');
  editModal.hide();
  await fetchProjects();
}

async function markProjectDone() {
  const id = document.getElementById('editProjectId').value;
  const headers = { 'Content-Type': 'application/json' };
  const res = await fetchWithAuth(`${API_BASE}/api/projetos/${id}/`, { method: 'PATCH', headers, body: JSON.stringify({ status: 'Concluído', progresso: 100 }) });
  if (!res.ok) {
    const txt = await res.text().catch(() => 'erro');
    alert('Erro ao marcar concluído: ' + txt);
    return;
  }
  alert('Projeto marcado como concluído');
  editModal.hide();
  await fetchProjects();
}

// inicializa handlers
document.addEventListener('DOMContentLoaded', async () => {
  console.log('[professor.js] Inicializando...');
  // prefetch professor id and store locally for quick checks
  const profId = await getCurrentProfessorId();
  console.log('[professor.js] Professor ID:', profId);
  if (profId) localStorage.setItem('user_professor_id', String(profId));

  const btnSave = document.getElementById('btnSaveProject');
  const btnDone = document.getElementById('btnMarkDone');
  if (btnSave) btnSave.addEventListener('click', saveProjectEdits);
  if (btnDone) btnDone.addEventListener('click', markProjectDone);

  // carga inicial de projetos (agora que a função renderProjects foi sobrescrita)
  console.log('[professor.js] Carregando projetos...');
  await fetchProjects();
  console.log('[professor.js] Projetos carregados, botões devem estar visíveis se professor for responsável');
});
