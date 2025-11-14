# 🔐 Autenticação JWT - EchoAPI

## Visão Geral

A API utiliza autenticação baseada em **JWT (JSON Web Tokens)** para proteger os endpoints. Este documento descreve como obter e usar tokens de autenticação.

---

## 📋 Endpoints de Autenticação

### 1. **Registrar Novo Usuário**
```http
POST /api/register/
```

**Permissão:** Público (não requer autenticação)

**Request Body:**
```json
{
  "nome": "João Silva",
  "email": "joao@example.com",
  "password": "senha_segura_123",
  "password2": "senha_segura_123"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "nome": "João Silva",
  "email": "joao@example.com"
}
```

---

### 2. **Obter Token de Acesso**
```http
POST /api/token/
```

**Permissão:** Público (não requer autenticação)

**Request Body:**
```json
{
  "email": "joao@example.com",
  "password": "senha_segura_123"
}
```

**Response (200 OK):**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

- **refresh:** Token para renovar o access token (válido por 1 dia)
- **access:** Token para autenticação nas requisições (válido por 5 horas)

---

### 3. **Renovar Token de Acesso**
```http
POST /api/token/refresh/
```

**Permissão:** Público (não requer autenticação)

**Request Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response (200 OK):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

### 4. **Verificar Token**
```http
POST /api/token/verify/
```

**Permissão:** Público (não requer autenticação)

**Request Body:**
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response (200 OK):**
```json
{}
```
*Se o token for inválido, retorna erro 401*

---

## 🔑 Como Usar Tokens

### No Header da Requisição

Para acessar endpoints protegidos, inclua o token de acesso no header `Authorization`:

```http
GET /api/projetos/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

### Exemplo com cURL:
```bash
curl -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..." \
     http://127.0.0.1:8000/api/projetos/
```

### Exemplo com Python (requests):
```python
import requests

# Obter token
response = requests.post('http://127.0.0.1:8000/api/token/', json={
    'email': 'joao@example.com',
    'password': 'senha_segura_123'
})
tokens = response.json()
refresh_token = tokens['refresh']
access_token = tokens['access']

# Usar token em requisição protegida
headers = {'Authorization': f'Bearer {access_token}'}
response = requests.get('http://127.0.0.1:8000/api/projetos/', headers=headers)
projetos = response.json()
```

### Exemplo com JavaScript (fetch):
```javascript
// Obter token
const loginResponse = await fetch('http://127.0.0.1:8000/api/token/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'joao@example.com',
    password: 'senha_segura_123'
  })
});
const { refresh, access } = await loginResponse.json();

// Usar token em requisição protegida
const projetosResponse = await fetch('http://127.0.0.1:8000/api/projetos/', {
  headers: { 'Authorization': `Bearer ${access}` }
});
const projetos = await projetosResponse.json();
```

---

## 🛡️ Configuração de Segurança

### Política de Permissões

A API está configurada com `IsAuthenticatedOrReadOnly`, o que significa:

- ✅ **Leitura (GET):** Qualquer pessoa pode visualizar dados (endpoints públicos)
- 🔒 **Escrita (POST, PUT, PATCH, DELETE):** Apenas usuários autenticados

### Validade dos Tokens

| Token | Validade | Descrição |
|-------|----------|-----------|
| `refresh` | 1 dia | Token para renovar o access token |
| `access` | 5 horas | Token para autenticação nas requisições |

**Observação:** O token retornado usa `email` para login (não `username`), pois nosso modelo Usuario utiliza email como identificador único.

## 🎭 Sistema de Autenticação por Papel (Role-Based)

### Registro com Papel

O sistema suporta registro diferenciado por papel (role). Use o campo `role` no registro:

```http
POST /api/register/
```

**Request Body:**
```json
{
  "nome": "João Professor",
  "email": "prof@example.com",
  "password": "senha123",
  "password2": "senha123",
  "role": "Professor"
}
```

**Papéis Disponíveis:**
- `Professor` - Cria registro na tabela Professor (herda de Usuario)
- `Coordenador` - Cria registro na tabela Coordenador (herda de Usuario)
- `Empresa` - Cria registro na tabela Empresa (modelo separado)

**Campo Adicional para Empresas:**
```json
{
  "nome": "Tech Corp",
  "email": "contato@techcorp.com",
  "password": "senha123",
  "password2": "senha123",
  "role": "Empresa",
  "contato": "11999999999"
}
```

### Token JWT com Tipo de Usuário

Os tokens JWT incluem o campo `user_type` no payload:

```json
{
  "token_type": "access",
  "exp": 1699999999,
  "iat": 1699999999,
  "jti": "abc123...",
  "user_id": 1,
  "email": "prof@example.com",
  "nome": "João Professor",
  "user_type": "professor"
}
```

**Valores de `user_type`:**
- `professor` - Usuário é um Professor
- `coordenador` - Usuário é um Coordenador
- `empresa` - Usuário é uma Empresa
- `usuario` - Usuário base (sem papel específico)

### Autenticação Customizada

O sistema usa `CustomJWTAuthentication` que:
1. Extrai o token do header `Authorization: Bearer <token>`
2. Decodifica e obtém `user_type` do payload
3. Busca o usuário na tabela apropriada (Professor/Coordenador/Empresa/Usuario)
4. Retorna um `UsuarioWrapper` com propriedade `user_type`

### Auto-Hash de Senhas (Desenvolvimento)

⚠️ **Recurso de Desenvolvimento**: O sistema possui um fallback de auto-hash para facilitar testes.

**Como funciona:**
1. Ao fazer login, tenta validar com `check_password()`
2. Se falhar, verifica se a senha em texto plano corresponde
3. Se sim, aplica `make_password()` e salva o hash
4. Próximo login já usa o hash normalmente

**Exemplo:**
```python
# Primeira tentativa de login com senha em texto plano "abc123"
POST /api/token/
{
  "email": "user@test.com",
  "password": "abc123"
}

# Sistema detecta texto plano, converte para hash e salva
# Próximo login já usa o hash
```

**⚠️ Remover em Produção:**
- Este fallback deve ser removido do arquivo `src/app/jwt_views.py`
- Garantir que todas as senhas no banco estejam hasheadas
- Implementar política de senhas fortes

---

## 📝 Fluxo de Autenticação Completo

```mermaid
sequenceDiagram
    participant Cliente
    participant API
    
    Cliente->>API: POST /api/register/ (registro)
    API-->>Cliente: 201 Created (usuário criado)
    
    Cliente->>API: POST /api/token/ (email + senha)
    API-->>Cliente: 200 OK (access + refresh tokens)
    
    Cliente->>API: GET /api/projetos/ (com access token)
    API-->>Cliente: 200 OK (dados dos projetos)
    
    Note over Cliente,API: Após 5 horas, access token expira
    
    Cliente->>API: POST /api/token/refresh/ (refresh token)
    API-->>Cliente: 200 OK (novo access token)
    
    Cliente->>API: GET /api/projetos/ (com novo access token)
    API-->>Cliente: 200 OK (dados dos projetos)
```

---

## 🧪 Testando no Swagger

1. Acesse a documentação Swagger: http://127.0.0.1:8000/api/docs/

2. **Registre um usuário:**
   - Use o endpoint `POST /api/register/`
   - Preencha nome, email e senhas

3. **Obtenha um token:**
   - Use o endpoint `POST /api/token/`
   - Preencha email e senha
   - Copie o `access` token da resposta

4. **Autentique no Swagger:**
   - Clique no botão **"Authorize"** (cadeado) no topo da página
   - No campo **"jwtAuth (http, Bearer)"**, cole apenas o token (SEM a palavra "Bearer")
   - Clique em "Authorize" e depois "Close"

5. **Teste endpoints protegidos:**
   - Agora você pode testar endpoints POST/PUT/DELETE
   - Todos usarão automaticamente seu token

---

## ❌ Tratamento de Erros

### Token Inválido ou Expirado
```json
{
  "detail": "Given token not valid for any token type",
  "code": "token_not_valid",
  "messages": [
    {
      "token_class": "AccessToken",
      "token_type": "access",
      "message": "Token is invalid or expired"
    }
  ]
}
```
**Solução:** Use o refresh token para obter um novo access token.

### Token Não Fornecido
```json
{
  "detail": "Authentication credentials were not provided."
}
```
**Solução:** Inclua o header `Authorization: Bearer <token>` na requisição.

### Credenciais Inválidas
```json
{
  "detail": "No active account found with the given credentials"
}
```
**Solução:** Verifique se o email e senha estão corretos.

---

## 🔧 Configurações Avançadas

### Customizar Tempo de Expiração

Edite `src/CadPro/settings.py`:

```python
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=5),  # Altere aqui
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),  # Altere aqui
    # ...
}
```

### Modelo de Usuário Customizado

A API usa o modelo `Usuario` da aplicação `app`. Se precisar customizar:

```python
# settings.py
AUTH_USER_MODEL = 'app.Usuario'  # Se necessário
```

---

## 📚 Referências

- [Django REST Framework Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/)
- [JWT.io](https://jwt.io/) - Decodificador de tokens
- [drf-spectacular](https://drf-spectacular.readthedocs.io/) - Documentação OpenAPI

---

## ⚡ Início Rápido

**1. Registre-se:**
```bash
curl -X POST http://127.0.0.1:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"nome":"Test User","email":"test@test.com","password":"test123456","password2":"test123456"}'
```

**2. Obtenha token:**
```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"test123456"}'
```

**3. Use a API:**
```bash
curl -H "Authorization: Bearer SEU_ACCESS_TOKEN" \
     http://127.0.0.1:8000/api/projetos/
```

---

**✅ Autenticação JWT implementada com sucesso!** 🎉
