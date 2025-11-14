const API_BASE = 'http://127.0.0.1:8000';

const form = document.getElementById('loginForm');
const msg = document.getElementById('msg');

// Se veio de registro bem-sucedido, mostra mensagem de sucesso e limpa o flag
const regMsg = localStorage.getItem('registered_msg');
if (regMsg) {
  msg.textContent = regMsg;
  msg.style.display = 'block';
  localStorage.removeItem('registered_msg');
}

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  msg.style.display = 'none';
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;

  try {
    const res = await fetch(`${API_BASE}/api/token/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });

    if (!res.ok) {
      const j = await res.json().catch(() => ({}));
      msg.textContent = j.detail || 'Erro ao autenticar';
      msg.style.display = 'block';
      return;
    }

    const data = await res.json();
    // salva tokens no localStorage (simples, não totalmente seguro)
    localStorage.setItem('access', data.access);
    localStorage.setItem('refresh', data.refresh);
    // salva email para identificar papel (role) no frontend
    localStorage.setItem('user_email', email);

    // Detecta papel e redireciona de acordo
    try {
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

      // Padrão
      localStorage.setItem('user_role', 'Usuário');
      window.location.href = 'projects.html';
    } catch (err) {
      // Se algo falhar na detecção, vai para a listagem padrão
      console.error('Erro detectando papel após login:', err);
      window.location.href = 'projects.html';
    }
  } catch (err) {
    console.error(err);
    msg.textContent = 'Erro de conexão';
    msg.style.display = 'block';
  }
});
