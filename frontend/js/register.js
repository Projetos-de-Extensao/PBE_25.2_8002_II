const API_BASE = 'http://127.0.0.1:8000';

const form = document.getElementById('registerForm');
const msg = document.getElementById('msg');

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  msg.style.display = 'none';
  const nome = document.getElementById('nome').value;
  const email = document.getElementById('email').value;
    const role = document.getElementById('role').value;
  const password = document.getElementById('password').value;
  const password2 = document.getElementById('password2').value;
    const contato = document.getElementById('contato') ? document.getElementById('contato').value : '';

  if (password !== password2) {
    msg.textContent = 'As senhas não coincidem.';
    msg.style.display = 'block';
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/api/register/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ nome, email, password, password2, role, contato })
    });

    if (!res.ok) {
      const j = await res.json().catch(() => ({}));
      msg.textContent = j.detail || (j.password ? (Array.isArray(j.password) ? j.password.join('; ') : j.password) : 'Erro ao registrar');
      msg.style.display = 'block';
      return;
    }

    // Registro OK — agora realiza login automático para obter tokens e redirecionar
    const tokenRes = await fetch(`${API_BASE}/api/token/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    if (!tokenRes.ok) {
      // Registro funcionou, mas login automático falhou. Mostrar mensagem e voltar ao login.
      msg.textContent = 'Conta criada, mas falha no login automático. Faça login manualmente.';
      msg.style.display = 'block';
      return;
    }

    const data = await tokenRes.json();
    localStorage.setItem('access', data.access);
    localStorage.setItem('refresh', data.refresh);
    localStorage.setItem('user_email', email);

    // Redireciona conforme papel (reutiliza lógica simples)
    const headers = { 'Content-Type': 'application/json', 'Authorization': `Bearer ${data.access}` };
    const check = async (url) => {
      const r = await fetch(url, { headers });
      if (!r.ok) return [];
      const j = await r.json();
      return Array.isArray(j) ? j : (j.results || []);
    };

    const isCoord = await check(`${API_BASE}/api/coordenadores/?search=${encodeURIComponent(email)}`);
    console.debug('role-check coordenadores:', isCoord);
    if (isCoord.length) {
      localStorage.setItem('user_role', 'Coordenador');
      return window.location.href = 'coordenador.html';
    }

    const isProf = await check(`${API_BASE}/api/professores/?search=${encodeURIComponent(email)}`);
    console.debug('role-check professores:', isProf);
    if (isProf.length) {
      localStorage.setItem('user_role', 'Professor');
      return window.location.href = 'professor.html';
    }

    const isEmp = await check(`${API_BASE}/api/empresas/?search=${encodeURIComponent(email)}`);
    console.debug('role-check empresas:', isEmp);
    if (isEmp.length) {
      localStorage.setItem('user_role', 'Empresa');
      return window.location.href = 'empresa.html';
    }

    localStorage.setItem('user_role', 'Usuário');
    window.location.href = 'projects.html';

  } catch (err) {
    console.error(err);
    msg.textContent = 'Erro de conexão';
    msg.style.display = 'block';
  }
});

// mostra/oculta campo de contato quando empresa selecionada
document.addEventListener('DOMContentLoaded', () => {
  const roleSel = document.getElementById('role');
  const contatoGroup = document.getElementById('contatoGroup');
  if (roleSel) {
    const toggle = () => {
      if (roleSel.value === 'empresa') contatoGroup.style.display = '';
      else contatoGroup.style.display = 'none';
    };
    roleSel.addEventListener('change', toggle);
    toggle();
  }
});
