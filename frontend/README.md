# 🎨 Frontend CadPro

Interface web para o sistema de gestão de projetos acadêmicos, com três interfaces distintas baseadas em papéis: Empresa, Coordenador e Professor.

## 🚀 Como Usar (Desenvolvimento Local)

### 1. Inicie o Backend
Certifique-se de que o Django esteja rodando:
```bash
cd src
python manage.py runserver
```
Backend disponível em: http://127.0.0.1:8000

### 2. Inicie o Frontend
Sirva os arquivos estáticos localmente para evitar problemas de CORS e `file://`:

```powershell
# A partir da pasta frontend
python -m http.server 3000
```

### 3. Acesse no Navegador
Abra: http://localhost:3000

## 📱 Páginas e Funcionalidades

### 🔐 index.html - Login
- Campo de email e senha
- Autenticação via POST `/api/token/`
- Armazena tokens JWT em `localStorage`
- **Detecção automática de papel**: busca o usuário em `/api/coordenadores/`, `/api/professores/` e `/api/empresas/`
- **Redirecionamento inteligente**: leva para a interface apropriada

### 📝 register.html - Cadastro
- Formulário com nome, email, senha
- **Seleção de papel**: Professor, Coordenador ou Empresa
- Campo "Contato" aparece dinamicamente para Empresas
- Registro via POST `/api/register/`
- **Auto-login**: após cadastro, faz login automaticamente e redireciona

### 👨‍🏫 professor.html - Interface do Professor
**Lista de Projetos:**
- Mostra apenas projetos sob responsabilidade do professor
- Cards com título, descrição e status

**Modal de Edição:**
- Título
- Descrição
- Progresso (0-100%)
- Status (Em andamento, Concluído, Pausado, Cancelado)
- Lista de alunos
- Anexos
- Botão "Marcar como Concluído"

**Ações:**
- ✏️ Editar projetos próprios (PATCH `/api/projetos/{id}/`)
- ✅ Marcar como concluído

### 👨‍💼 coordenador.html - Interface do Coordenador
**Aba "Propostas":**
- Lista propostas em análise
- Cada proposta mostra: título, descrição, empresa
- Botões:
  - **Aprovar**: Abre modal para selecionar professor → transforma em projeto automaticamente
  - **Rejeitar**: Rejeita diretamente

**Aba "Projetos":**
- Lista todos os projetos do sistema
- Cada projeto tem:
  - **Botão Editar**: Abre modal com todos os campos editáveis
  - **Dropdown de Professor**: Para projetos sem professor atribuído

**Modal de Edição:**
- Igual ao do professor, mas coordenador pode editar **qualquer projeto**

**Ações:**
- ✅ Aprovar propostas (com atribuição de professor)
- ❌ Rejeitar propostas
- ✏️ Editar qualquer projeto
- 👤 Atribuir/reatribuir professores
- ✅ Marcar projetos como concluídos

### 🏢 empresa.html - Interface da Empresa
**Formulário de Criação:**
- Título
- Descrição
- Anexos (texto livre)
- Criação via POST `/api/propostas/`
- Empresa é automaticamente associada no backend

**Lista de Propostas:**
- Mostra apenas propostas da empresa logada
- Badges coloridos de status:
  - 🟡 **Em análise** (amarelo)
  - 🟢 **Aprovada** (verde)
  - 🔴 **Rejeitada** (vermelho)
  - 🔵 **Transformada em projeto** (azul)

**Ações:**
- ➕ Criar novas propostas
- 👁️ Visualizar status das propostas

## 🗂️ Estrutura de Arquivos

```
frontend/
├── index.html              # Tela de login
├── register.html           # Cadastro com seleção de papel
├── professor.html          # Interface do professor
├── coordenador.html        # Interface do coordenador
├── empresa.html            # Interface da empresa
├── projects.html           # [LEGACY] Não usado mais
└── js/
    ├── auth.js             # Login e detecção de papel
    ├── register.js         # Lógica de cadastro
    ├── projects.js         # Utilidades compartilhadas (fetchWithAuth, refresh token)
    ├── professor.js        # Lógica específica do professor
    ├── coordenador.js      # Lógica específica do coordenador
    └── empresa.js          # Lógica específica da empresa
```

## 🔧 Arquitetura JavaScript

### projects.js - Utilidades Compartilhadas

**`fetchWithAuth(url, options, tryRefresh=true)`**
- Wrapper do fetch que adiciona token automaticamente
- **Renovação automática**: Em 401, tenta refresh token e re-faz a requisição
- Redireciona para login se refresh falhar
- Usado por todas as páginas

**`detectRoleAndSetTitle()`**
- Detecta papel do usuário via APIs
- Atualiza título da página ("Sou Professor", etc.)

**`fetchProjects()`**
- Lista projetos via GET `/api/projetos/`
- Pode ser sobrescrita por scripts específicos

**`skipAutoFetchProjects`**
- Flag para evitar race conditions
- Scripts específicos setam `true` e chamam `fetchProjects()` manualmente

### auth.js - Autenticação
- Login via POST `/api/token/`
- Salva tokens em `localStorage`
- **Detecção de papel**: busca email em professores → coordenadores → empresas
- Redireciona para página apropriada
- Salva email e role em `localStorage`

### register.js - Cadastro
- Validação de senha (match)
- Mostra/oculta campo "contato" para Empresas
- POST `/api/register/` com role
- Auto-login após sucesso

### professor.js
- Busca ID do professor via email
- **Override de `renderProjects()`**: adiciona botão "Editar" apenas nos projetos próprios
- Modal de edição com PATCH `/api/projetos/{id}/`
- Validação de permissão no backend

### coordenador.js
- Lista propostas em análise via GET `/api/propostas/em_analise/`
- Modal para selecionar professor ao aprovar
- Aprovar: POST `/api/propostas/{id}/ajeitar/` (transforma em projeto)
- Rejeitar: POST `/api/propostas/{id}/rejeitar/`
- Lista todos projetos via GET `/api/projetos/`
- Edição de qualquer projeto via PATCH
- Atribuir professor: POST `/api/projetos/{id}/assign_professor/`

### empresa.js
- Busca ID da empresa via email
- Criação de proposta: POST `/api/propostas/`
- Lista propostas da empresa: GET `/api/propostas/?empresa={id}`
- Renderização com badges coloridos de status

## 🔐 Segurança

### Tokens JWT
- **Access token**: Armazenado em `localStorage.access`
- **Refresh token**: Armazenado em `localStorage.refresh`
- **Auto-refresh**: `fetchWithAuth()` renova automaticamente tokens expirados

⚠️ **Nota de Produção**: 
- Em produção, considere usar httpOnly cookies ao invés de localStorage
- Tokens em localStorage são vulneráveis a XSS

### CORS
- Backend configurado com `CORS_ALLOW_ALL_ORIGINS = True` para desenvolvimento
- **Antes de produção**: configurar whitelist em `settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    "https://seudominio.com",
]
```

## 🎨 Estilo e UX

### Bootstrap 5.3.2
- Framework CSS usado em todas as páginas
- Layout responsivo
- Modais para edição e aprovação
- Cards para listagem de projetos/propostas

### Badges de Status
| Status | Cor | Classe |
|--------|-----|--------|
| Em análise | Amarelo | `badge bg-warning` |
| Aprovada | Verde | `badge bg-success` |
| Rejeitada | Vermelho | `badge bg-danger` |
| Transformada em projeto | Azul | `badge bg-info` |
| Em andamento | Azul | `badge bg-primary` |
| Concluído | Verde | `badge bg-success` |

### Interatividade
- Confirmações com `confirm()` para ações destrutivas
- Alerts com `alert()` para feedback
- Modals do Bootstrap para formulários
- Loading implícito (botões desabilitados durante fetch)

## 🐛 Troubleshooting

### Erro: "Authentication credentials were not provided"
**Causa**: Token não está no header ou expirou

**Solução**:
1. Limpe localStorage: `localStorage.clear()`
2. Faça login novamente
3. Verifique se o backend está rodando

### Botão "Editar" não aparece (professor)
**Causa**: Race condition entre `projects.js` e `professor.js`

**Solução**: Já implementado com `skipAutoFetchProjects`
- `professor.js` sobrescreve `renderProjects()` e chama manualmente

### CORS Error
**Causa**: Frontend acessado via `file://` ou backend não está rodando

**Solução**:
1. Use servidor HTTP: `python -m http.server 3000`
2. Acesse via `http://localhost:3000` (não `file://`)
3. Backend deve estar em `http://127.0.0.1:8000`

### Token não renova automaticamente
**Causa**: `fetchWithAuth()` não está sendo usado

**Solução**: Use sempre `fetchWithAuth()` ao invés de `fetch()`:
```javascript
// ❌ Errado
const res = await fetch(url, { headers: { Authorization: ... } });

// ✅ Correto
const res = await fetchWithAuth(url, options);
```

### Redirecionamento errado após login
**Causa**: Usuário não encontrado em nenhum endpoint de papel

**Solução**:
1. Verifique se o registro foi feito com `role` correto
2. Confirme que existe registro em Professor/Coordenador/Empresa com o email
3. Veja console do navegador para erros

## 🚀 Melhorias Futuras (Opcionais)

### UX
- [ ] Substituir `alert()` por toasts do Bootstrap
- [ ] Loading spinners durante requisições
- [ ] Desabilitar botões durante processamento
- [ ] Validação de formulários no frontend

### Funcionalidades
- [ ] Empresa editar/deletar propostas (apenas em "Em análise")
- [ ] Upload real de arquivos (atualmente é campo de texto)
- [ ] Notificações quando status muda
- [ ] Filtros e busca de projetos
- [ ] Paginação (backend já suporta)

### Segurança
- [ ] Migrar tokens para httpOnly cookies
- [ ] Implementar CSP (Content Security Policy)
- [ ] Rate limiting no frontend
- [ ] Logout em todas as abas (broadcast channel)

## 📞 Suporte

Para problemas relacionados ao frontend:
1. Verifique console do navegador (F12)
2. Verifique network tab para erros de API
3. Confirme que backend está rodando
4. Veja logs do terminal do backend

---

**✅ Frontend completo e responsivo!** 🎉
