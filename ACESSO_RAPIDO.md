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

✅ Paginação (10 itens por página)
✅ Busca por texto
✅ Filtros por campos
✅ Ordenação customizada
✅ Endpoints customizados
✅ Documentação completa no Swagger

---

## 📚 Documentação Completa

- **API_README.md** - Guia completo da API
- **SWAGGER_README.md** - Detalhes da implementação Swagger
- **Este arquivo** - Guia rápido de acesso

---

## 🎯 Próximos Passos

1. ✅ Acesse o Swagger: http://127.0.0.1:8000/api/docs/
2. ✅ Explore os endpoints
3. ✅ Teste criar alguns dados
4. ✅ Veja a documentação interativa

**Divirta-se explorando a API! 🚀**
