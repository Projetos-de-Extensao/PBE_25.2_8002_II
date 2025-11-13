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
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

- **access:** Token para autenticação nas requisições (válido por 5 horas)
- **refresh:** Token para renovar o access token (válido por 1 dia)

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
const { access } = await loginResponse.json();

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
| `access` | 5 horas | Token para autenticação nas requisições |
| `refresh` | 1 dia | Token para renovar o access token |

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
   - No campo "**jwtAuth (http, Bearer)**", insira: `Bearer SEU_TOKEN_AQUI`
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
