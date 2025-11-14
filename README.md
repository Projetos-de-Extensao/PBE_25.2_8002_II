# 🎓 CadPro - Sistema de Gestão de Projetos Acadêmicos

**Código da Disciplina**: IBM8936

## 📋 Sobre 

Plataforma web completa para gestão de projetos acadêmicos, permitindo:
- **Empresas**: Criar e acompanhar propostas de projetos
- **Coordenadores**: Aprovar/rejeitar propostas, atribuir professores e gerenciar projetos
- **Professores**: Editar e acompanhar seus projetos

Sistema com autenticação JWT, controle de permissões baseado em papéis e interface web responsiva.

## 🛠️ Tecnologias

**Backend:**
- Python 3.11+
- Django 5.2.7
- Django REST Framework
- djangorestframework-simplejwt (JWT)
- drf-spectacular (OpenAPI/Swagger)
- django-cors-headers
- django-filter
- SQLite (banco de dados)

**Frontend:**
- HTML5 + CSS3
- JavaScript (Vanilla ES6+)
- Bootstrap 5.3.2
- Fetch API para comunicação com backend

## 👥 Integrantes do Grupo

- Murilo Piatigorsky - 202202448605
- Joao Marcio - 202208385001
- Enzo Zambrotti - 202407095917
- Nicholas Victorino - 202203813021

## 🚀 Instalação e Configuração

### 1. Clone o Repositório
```bash
git clone https://github.com/Projetos-de-Extensao/PBE_25.2_8002_II.git
cd PBE_25.2_8002_II
```

### 2. Configure o Ambiente Virtual (Backend)
```powershell
# Criar ambiente virtual
python -m venv .venv

# Ativar (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Ativar (Linux/Mac)
source .venv/bin/activate
```

### 3. Instale as Dependências
```bash
pip install -r requirements.txt
```

### 4. Configure o Banco de Dados
```bash
cd src
python manage.py migrate
```

### 5. (Opcional) Crie um Superusuário
```bash
python manage.py createsuperuser
```

### 6. Inicie o Servidor Backend
```bash
python manage.py runserver
```
O backend estará disponível em: http://127.0.0.1:8000

### 7. Inicie o Frontend
Em outro terminal, vá até a pasta `frontend`:
```bash
cd frontend
python -m http.server 3000
```
O frontend estará disponível em: http://localhost:3000

## 🎯 Funcionalidades por Papel

### 👔 Empresa
- ✅ Criar propostas de projeto
- ✅ Visualizar próprias propostas e seus status
- ✅ Acompanhar propostas: Em análise, Aprovada, Rejeitada, Transformada em projeto

### 👨‍💼 Coordenador
- ✅ Visualizar propostas em análise
- ✅ Aprovar propostas (atribuindo professor automaticamente)
- ✅ Rejeitar propostas
- ✅ Editar qualquer projeto
- ✅ Atribuir/reatribuir professores aos projetos
- ✅ Marcar projetos como concluídos
- ✅ Acesso completo a todos os projetos

### 👨‍🏫 Professor
- ✅ Visualizar projetos sob sua responsabilidade
- ✅ Editar projetos próprios:
  - Título e descrição
  - Progresso (0-100%)
  - Status (Em andamento, Concluído, Pausado, Cancelado)
  - Lista de alunos
  - Anexos
- ✅ Marcar projetos como concluídos

## 🔐 Autenticação e Segurança

### Sistema JWT Customizado
- **Login por email** (não username)
- **Auto-hash de senhas**: Senhas em texto plano são automaticamente convertidas em hash no primeiro login (⚠️ recurso de desenvolvimento)
- **Tokens com tipo de usuário**: JWT inclui campo `user_type` (professor/coordenador/empresa/usuario)
- **Refresh token**: Renovação automática de tokens expirados

### Permissões Implementadas

| Permissão | Descrição |
|-----------|-----------|
| `IsCoordenador` | Permite acesso apenas a coordenadores |
| `IsProfessorOrCoordenadorOrReadOnly` | Leitura pública, escrita apenas para professor responsável ou coordenador. **Bloqueia empresas explicitamente** |
| `IsEmpresaOrCoordenador` | Permite acesso a empresas e coordenadores (usado para criar propostas) |

### Fluxo de Autenticação
1. **Registro**: POST `/api/register/` com `role` (Professor/Coordenador/Empresa)
2. **Login**: POST `/api/token/` retorna `access` e `refresh` tokens
3. **Detecção de papel**: Frontend busca em professores/coordenadores/empresas pelo email
4. **Redirecionamento**: Usuário é redirecionado para interface apropriada
5. **Token refresh**: Frontend renova automaticamente tokens expirados

## 📂 Estrutura do Projeto

```
PBE_25.2_8002_II/
├── src/
│   ├── manage.py
│   ├── CadPro/
│   │   ├── settings.py          # Configurações Django + CORS + JWT
│   │   ├── urls.py               # Rotas principais
│   │   └── ...
│   └── app/
│       ├── models.py             # Usuario, Professor, Coordenador, Empresa, Proposta, Projeto
│       ├── serializers.py        # Serializadores DRF
│       ├── views.py              # ViewSets da API
│       ├── jwt_views.py          # Autenticação JWT customizada
│       ├── authentication.py     # CustomJWTAuthentication + UsuarioWrapper
│       ├── permissions.py        # Permissões customizadas
│       └── urls.py               # Rotas da API
├── frontend/
│   ├── index.html                # Tela de login
│   ├── register.html             # Cadastro com seleção de papel
│   ├── professor.html            # Interface do professor
│   ├── coordenador.html          # Interface do coordenador
│   ├── empresa.html              # Interface da empresa
│   └── js/
│       ├── auth.js               # Lógica de login e detecção de papel
│       ├── register.js           # Lógica de cadastro
│       ├── projects.js           # Funções compartilhadas (fetchWithAuth)
│       ├── professor.js          # Lógica específica do professor
│       ├── coordenador.js        # Lógica específica do coordenador
│       └── empresa.js            # Lógica específica da empresa
├── requirements.txt              # Dependências Python
└── README.md
```

## 📚 Documentação

| Documento | Descrição |
|-----------|-----------|
| [API README](API_README.md) | Documentação completa da API REST |
| [AUTH README](AUTH_README.md) | Guia de autenticação JWT |
| [SWAGGER README](SWAGGER_README.md) | Como usar a interface Swagger |
| [Frontend README](frontend/README.md) | Instruções do frontend |

### Swagger/OpenAPI
Acesse a documentação interativa da API em: http://127.0.0.1:8000/api/docs/

## ⚠️ Notas Importantes de Segurança

### 🔧 Auto-Hash de Senhas (Desenvolvimento)
O sistema possui um **fallback de auto-hash** que converte senhas em texto plano para hash no primeiro login. 

**⚠️ Isso é um recurso de DESENVOLVIMENTO para facilitar testes.**

**Como funciona:**
1. Se `check_password()` falhar, o sistema verifica se a senha em texto plano corresponde
2. Se sim, aplica `make_password()` e salva o hash
3. Próximo login já usa o hash normalmente

**🚨 Antes de produção:**
- Remover o fallback de auto-hash em `jwt_views.py`
- Garantir que todas as senhas no banco estejam hasheadas
- Implementar política de senhas fortes
- Habilitar validações de senha (atualmente desabilitadas em `RegisterSerializer`)

### 🔒 Outras Considerações
- **CORS**: `CORS_ALLOW_ALL_ORIGINS = True` está habilitado para desenvolvimento. Configurar whitelist em produção.
- **SECRET_KEY**: Alterar antes de deploy
- **DEBUG**: Desabilitar em produção
- **Tokens em localStorage**: Para produção, considerar httpOnly cookies
- **Coordenador registration**: Implementar convite/código de acesso para evitar registros não autorizados

## 🧪 Testando o Sistema

### 1. Criar Usuários de Teste
```bash
# Via interface de cadastro em http://localhost:3000/register.html
# Ou via API:

# Professor
curl -X POST http://127.0.0.1:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"nome":"Prof. João","email":"prof@test.com","password":"123","password2":"123","role":"Professor"}'

# Coordenador
curl -X POST http://127.0.0.1:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"nome":"Coord. Maria","email":"coord@test.com","password":"123","password2":"123","role":"Coordenador"}'

# Empresa
curl -X POST http://127.0.0.1:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"nome":"Tech Corp","email":"empresa@test.com","password":"123","password2":"123","role":"Empresa","contato":"11999999999"}'
```

### 2. Login e Testes
1. Acesse http://localhost:3000
2. Faça login com um dos usuários criados
3. O sistema redirecionará automaticamente para a interface apropriada
4. Teste as funcionalidades específicas de cada papel

### 3. Teste via API (Opcional)
```bash
# Obter token
TOKEN=$(curl -s -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"email":"empresa@test.com","password":"123"}' \
  | jq -r .access)

# Criar proposta (como empresa)
curl -X POST http://127.0.0.1:8000/api/propostas/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"titulo":"Novo Projeto","descricao":"Descrição do projeto","anexos":"link1.pdf, link2.pdf"}'
```

## 🐛 Troubleshooting

### Erro: "Authentication credentials were not provided"
- Verifique se o token está no header: `Authorization: Bearer <token>`
- Token pode ter expirado, faça login novamente

### Erro: "CORS policy"
- Backend deve estar rodando em `http://127.0.0.1:8000`
- Frontend deve estar em servidor HTTP (não `file://`)
- Verifique `CORS_ALLOWED_ORIGINS` em `settings.py`

### Empresa não consegue criar proposta
- Verifique se o token tem `user_type: 'empresa'`
- Endpoint correto: POST `/api/propostas/` (não `/api/propostas/em_analise/`)

### Professor não vê botão de editar
- Certifique-se de estar logado como professor responsável pelo projeto
- Verifique se `professor.js` está carregado após `projects.js`

## 📞 Suporte

Para dúvidas ou problemas, entre em contato com a equipe:
- Murilo: muripp@gmail.com
- Issues: https://github.com/Projetos-de-Extensao/PBE_25.2_8002_II/issues

## 📄 Licença

Este projeto é parte da disciplina IBM8936 e está licenciado para fins acadêmicos.

---

**✅ Sistema completo e funcional!** 🎉


