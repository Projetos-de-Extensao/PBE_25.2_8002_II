# API EchoAPI - Documentação

API REST para gerenciamento de projetos de extensão, desenvolvida com Django REST Framework.

## 🚀 Como Usar

### Iniciar o servidor
```bash
cd src
python manage.py runserver
```

A API estará disponível em: `http://127.0.0.1:8000/api/`

## 📋 Endpoints Disponíveis

### 1️⃣ **Usuários**
- **GET** `/api/usuarios/` - Lista todos os usuários
- **POST** `/api/usuarios/` - Cria um novo usuário
- **GET** `/api/usuarios/{id}/` - Detalha um usuário específico
- **PUT** `/api/usuarios/{id}/` - Atualiza um usuário
- **PATCH** `/api/usuarios/{id}/` - Atualiza parcialmente um usuário
- **DELETE** `/api/usuarios/{id}/` - Remove um usuário

### 2️⃣ **Professores**
- **GET** `/api/professores/` - Lista todos os professores
- **POST** `/api/professores/` - Cria um novo professor
- **GET** `/api/professores/{id}/` - Detalha um professor
- **GET** `/api/professores/{id}/projetos/` - Lista projetos do professor
- **PUT/PATCH** `/api/professores/{id}/` - Atualiza professor
- **DELETE** `/api/professores/{id}/` - Remove professor

### 3️⃣ **Coordenadores**
- **GET** `/api/coordenadores/` - Lista todos os coordenadores
- **POST** `/api/coordenadores/` - Cria um novo coordenador
- **GET** `/api/coordenadores/{id}/` - Detalha um coordenador
- **GET** `/api/coordenadores/{id}/projetos_aprovados/` - Lista projetos aprovados
- **PUT/PATCH** `/api/coordenadores/{id}/` - Atualiza coordenador
- **DELETE** `/api/coordenadores/{id}/` - Remove coordenador

### 4️⃣ **Empresas**
- **GET** `/api/empresas/` - Lista todas as empresas
- **POST** `/api/empresas/` - Cria uma nova empresa
- **GET** `/api/empresas/{id}/` - Detalha uma empresa
- **GET** `/api/empresas/{id}/propostas/` - Lista propostas da empresa
- **GET** `/api/empresas/{id}/projetos/` - Lista projetos da empresa
- **PUT/PATCH** `/api/empresas/{id}/` - Atualiza empresa
- **DELETE** `/api/empresas/{id}/` - Remove empresa

### 5️⃣ **Propostas**
- **GET** `/api/propostas/` - Lista todas as propostas
- **GET** `/api/propostas/em_analise/` - Lista propostas em análise
- **POST** `/api/propostas/` - Cria uma nova proposta
- **GET** `/api/propostas/{id}/` - Detalha uma proposta
- **PUT/PATCH** `/api/propostas/{id}/` - Atualiza proposta
- **DELETE** `/api/propostas/{id}/` - Remove proposta

**Filtros disponíveis:**
- `?status=Em análise`
- `?empresa=1`

### 6️⃣ **Projetos**
- **GET** `/api/projetos/` - Lista todos os projetos
- **POST** `/api/projetos/` - Cria um novo projeto
- **GET** `/api/projetos/{id}/` - Detalha um projeto
- **PATCH** `/api/projetos/{id}/atualizar_progresso/` - Atualiza progresso
- **PUT/PATCH** `/api/projetos/{id}/` - Atualiza projeto
- **DELETE** `/api/projetos/{id}/` - Remove projeto

**Filtros disponíveis:**
- `?status=Em andamento`
- `?professor_responsavel=1`
- `?empresa_associada=2`
- `?aprovado_por=1`

### 7️⃣ **Grupos**
- **GET** `/api/grupos/` - Lista todos os grupos
- **POST** `/api/grupos/` - Cria um novo grupo
- **GET** `/api/grupos/{id}/` - Detalha um grupo
- **GET** `/api/grupos/{id}/projetos/` - Lista projetos do grupo
- **PUT/PATCH** `/api/grupos/{id}/` - Atualiza grupo
- **DELETE** `/api/grupos/{id}/` - Remove grupo

**Filtros disponíveis:**
- `?tipo=I` ou `?tipo=II`

### 8️⃣ **Hall of Fame**
- **GET** `/api/hall-of-fame/` - Lista todos os destaques
- **GET** `/api/hall-of-fame/destaques/` - Lista top 10 destaques
- **POST** `/api/hall-of-fame/` - Adiciona ao hall of fame
- **GET** `/api/hall-of-fame/{id}/` - Detalha entrada
- **PUT/PATCH** `/api/hall-of-fame/{id}/` - Atualiza entrada
- **DELETE** `/api/hall-of-fame/{id}/` - Remove do hall of fame

## 🔍 Funcionalidades da API

### Paginação
Por padrão, a API retorna 10 itens por página. Para navegar:
- `?page=1` - Primeira página
- `?page=2` - Segunda página

### Busca
Use o parâmetro `search`:
- `/api/usuarios/?search=João` - Busca usuários com "João" no nome ou email
- `/api/projetos/?search=mobile` - Busca projetos com "mobile" no título ou descrição

### Ordenação
Use o parâmetro `ordering`:
- `/api/projetos/?ordering=titulo` - Ordena por título (A-Z)
- `/api/projetos/?ordering=-titulo` - Ordena por título (Z-A)
- `/api/propostas/?ordering=-data_envio` - Mais recentes primeiro

## 📝 Exemplos de Uso

### Criar um novo usuário
```bash
POST /api/usuarios/
Content-Type: application/json

{
  "nome": "João Silva",
  "email": "joao@example.com",
  "senha": "senha123"
}
```

### Criar uma proposta
```bash
POST /api/propostas/
Content-Type: application/json

{
  "titulo": "Sistema de Gestão",
  "descricao": "Sistema para gerenciar projetos",
  "status": "Em análise",
  "empresa": 1
}
```

### Atualizar progresso de um projeto
```bash
PATCH /api/projetos/1/atualizar_progresso/
Content-Type: application/json

{
  "progresso": 75.5
}
```

### Buscar propostas em análise
```bash
GET /api/propostas/em_analise/
```

### Listar projetos de uma empresa
```bash
GET /api/empresas/1/projetos/
```

## 🌐 Interface Web

O Django REST Framework fornece uma interface web interativa para testar a API:
- Acesse: `http://127.0.0.1:8000/api/`
- Navegue pelos endpoints
- Teste requisições diretamente no navegador

## 📊 Estrutura de Dados

### Relacionamentos
- **Professor** → pode ter múltiplos **Projetos**
- **Coordenador** → pode aprovar múltiplos **Projetos**
- **Empresa** → pode ter múltiplas **Propostas** e **Projetos**
- **Proposta** → tem um **Projeto** associado
- **Grupo** → pode ter múltiplos **Projetos**
- **HallOfFame** → destaca **Projetos** específicos

## ✨ Recursos Especiais

### Campos Calculados
Alguns serializers incluem campos calculados automaticamente:
- `total_projetos` - Total de projetos associados
- `total_propostas` - Total de propostas de uma empresa
- `professor_nome`, `empresa_nome`, etc. - Nomes dos relacionamentos

### Endpoints Customizados
- `/api/professores/{id}/projetos/` - Projetos de um professor
- `/api/coordenadores/{id}/projetos_aprovados/` - Projetos aprovados
- `/api/empresas/{id}/propostas/` - Propostas de uma empresa
- `/api/empresas/{id}/projetos/` - Projetos de uma empresa
- `/api/propostas/em_analise/` - Propostas aguardando análise
- `/api/projetos/{id}/atualizar_progresso/` - Atualiza apenas progresso
- `/api/grupos/{id}/projetos/` - Projetos de um grupo
- `/api/hall-of-fame/destaques/` - Top 10 destaques

## 🛠️ Tecnologias

- Django 5.2.7
- Django REST Framework 3.16.1
- django-filter (para filtros avançados)
- SQLite (banco de dados)
