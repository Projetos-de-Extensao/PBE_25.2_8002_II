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

    // Registro OK — não faz login automático.
    // Em vez disso, informa o usuário de sucesso e redireciona para a tela de login.
  console.log('Registro realizado com sucesso — redirecionando para login');
  localStorage.setItem('registered_msg', 'Conta criada com sucesso. Faça login.');
  // use replace para evitar que o botão Voltar leve de volta para a página de registro
  window.location.replace('index.html');
  return;

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
