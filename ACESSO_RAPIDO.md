# 🚀 Guia Rápido - Acesso à API e Swagger

## ✅ Servidor Django Rodando!

O servidor está ativo em: **http://127.0.0.1:8000**

---

## 📍 URLs Principais

### 🎯 Swagger UI (DOCUMENTAÇÃO INTERATIVA) ⭐
**http://127.0.0.1:8000/api/docs/**

👉 **COMECE POR AQUI!** Interface completa para explorar e testar todos os endpoints.

### 📖 ReDoc (Documentação Limpa)
**http://127.0.0.1:8000/api/redoc/**

### 📊 API Root (Navegador de Endpoints)
**http://127.0.0.1:8000/api/**

### 🔧 Admin Django
**http://127.0.0.1:8000/admin/**
- Usuário: admin
- Senha: (a que você definiu)

---

## 🔐 Autenticação JWT

### 🆕 Endpoints de Autenticação

- `/api/register/` - Registrar novo usuário (público)
- `/api/token/` - Obter tokens de acesso (login)
- `/api/token/refresh/` - Renovar token de acesso
- `/api/token/verify/` - Verificar se token é válido

### ⚡ Início Rápido - Autenticação

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

### 🧪 Autenticação no Swagger

1. Acesse http://127.0.0.1:8000/api/docs/
2. Use `POST /api/token/` para obter um token
3. Clique no botão **"Authorize"** (cadeado) no topo
4. Digite: `Bearer SEU_TOKEN_AQUI`
5. Clique em "Authorize" → "Close"
6. Agora pode testar todos os endpoints! 🎉

📖 **Documentação completa:** `AUTH_README.md`

---

## 📋 Endpoints da API

### Base URL: `http://127.0.0.1:8000/api/`

- `/usuarios/` - Gerenciar usuários
- `/professores/` - Gerenciar professores
- `/coordenadores/` - Gerenciar coordenadores
- `/empresas/` - Gerenciar empresas
- `/propostas/` - Gerenciar propostas
- `/projetos/` - Gerenciar projetos
- `/grupos/` - Gerenciar grupos
- `/hall-of-fame/` - Hall da fama

---

## 🎨 Como Usar o Swagger

1. **Acesse:** http://127.0.0.1:8000/api/docs/

2. **Explore os endpoints:**
   - Use os filtros por tag (Usuários, Professores, Empresas, etc.)
   - Clique em qualquer endpoint para expandir

3. **Teste uma requisição:**
   - Clique em "Try it out"
   - Preencha os parâmetros
   - Clique em "Execute"
   - Veja a resposta

4. **Veja os schemas:**
   - Role até o final
   - Seção "Schemas" mostra estrutura dos dados

---

## 📝 Exemplo: Criar um Usuário

**Via Swagger:**
1. Vá em `/api/docs/`
2. Encontre "Usuários" → POST `/api/usuarios/`
3. Clique em "Try it out"
4. Preencha o JSON:
```json
{
  "nome": "João Silva",
  "email": "joao@example.com",
  "senha": "senha123"
}
```
5. Clique em "Execute"

**Via cURL:**
```bash
curl -X POST http://127.0.0.1:8000/api/usuarios/ \
  -H "Content-Type: application/json" \
  -d '{"nome":"João Silva","email":"joao@example.com","senha":"senha123"}'
```

---

## 🔍 Recursos Disponíveis

✅ **Autenticação JWT com tokens**
✅ Paginação (10 itens por página)
✅ Busca por texto
✅ Filtros por campos
✅ Ordenação customizada
✅ Endpoints customizados
✅ Documentação completa no Swagger

---

## 📚 Documentação Completa

- **AUTH_README.md** - 🔐 Guia completo de autenticação JWT
- **API_README.md** - Guia completo da API
- **SWAGGER_README.md** - Detalhes da implementação Swagger
- **Este arquivo** - Guia rápido de acesso

---

## 🎯 Próximos Passos

1. ✅ Acesse o Swagger: http://127.0.0.1:8000/api/docs/
2. ✅ Registre um usuário: `POST /api/register/`
3. ✅ Obtenha um token: `POST /api/token/`
4. ✅ Autentique no Swagger com o token
5. ✅ Explore e teste os endpoints

**Divirta-se explorando a API! 🚀**
