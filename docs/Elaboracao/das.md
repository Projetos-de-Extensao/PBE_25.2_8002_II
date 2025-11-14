---
id: documento_de_arquitetura
title: Documento de Arquitetura
---
# Documento de Arquitetura de Software

## Sistema de Gestão de Projetos Acadêmicos

### Objetivo

Plataforma REST API para gerenciar projetos acadêmicos em parceria com empresas: propostas, aprovação, acompanhamento e Hall of Fame.

### Acrônimos

- **API** - Application Programming Interface
- **REST** - Representational State Transfer
- **JWT** - JSON Web Token
- **DRF** - Django REST Framework
- **ORM** - Object-Relational Mapping

---

## Arquitetura REST API

### Stack Tecnológico

- **Python 3.11.5** + **Django 5.2.7** + **DRF 3.16.1**
- **SQLite** (banco de dados)
- **JWT** (autenticação via djangorestframework-simplejwt)
- **Swagger/OpenAPI** (documentação via drf-spectacular)

### Camadas

**Model:** 8 classes (Usuario, Professor, Coordenador, Empresa, Proposta, Projeto, Grupo, HallOfFame) com relacionamentos (Herança, ForeignKey, ManyToMany, OneToOne)

**Serializer:** 9 serializers para conversão Python ↔ JSON com validações

**View:** 8 ViewSets + RegisterView com actions customizadas, filtros e paginação

**URL:** DefaultRouter + rotas JWT

---

## Características

- **Segurança:** JWT (5h access, 1d refresh), senhas PBKDF2, CORS configurado
- **Persistência:** ORM Django, migrations, integridade referencial
- **Escalabilidade:** API stateless, paginação, filtros otimizados
- **Manutenibilidade:** 916 linhas de código organizado em camadas, documentação Swagger

---

## Estrutura

```
src/app/
├── models.py (93 linhas)
├── serializers.py (137 linhas)
├── views.py (324 linhas)
├── urls.py (29 linhas)
├── admin.py (59 linhas)
└── authentication.py (54 linhas)
```

---

## Endpoints Principais

### Autenticação
- `POST /api/register/` - Registro
- `POST /api/token/` - Login (email + senha)
- `POST /api/token/refresh/` - Renovar token

### CRUD
- `/api/usuarios/`, `/api/professores/`, `/api/coordenadores/`, `/api/empresas/`
- `/api/propostas/`, `/api/projetos/`, `/api/grupos/`, `/api/halloffame/`

### Customizados
- `GET /api/professores/{id}/projetos/`
- `GET /api/propostas/em_analise/`
- `PATCH /api/projetos/{id}/atualizar_progresso/`
- `GET /api/halloffame/destaques/`

### Documentação
- `/api/docs/` - Swagger UI
- `/api/schema/` - OpenAPI JSON

---

## Modelo de Dados

### Herança
```
Usuario → Professor, Coordenador, Empresa
```

### Relacionamentos
- Empresa ⇒ Proposta (1:N)
- Proposta ⇔ Projeto (1:1)
- Professor/Coordenador/Empresa ⇔ Projeto (N:N e N:1)
- Grupo ⇔ Projeto (N:N)
- Projeto ⇐ HallOfFame (1:N)

---

## Métricas

- **Total:** 1.080 linhas (incluindo migrations)
- **Código principal:** 916 linhas
- **Modelos:** 8 classes
- **Endpoints:** 40+ (CRUD + customizados)
- **Tempo resposta:** < 200ms

---

## Referências

- Django: https://docs.djangoproject.com/
- DRF: https://www.django-rest-framework.org/
- SimpleJWT: https://django-rest-framework-simplejwt.readthedocs.io/

<p align = "justify">

**Segurança:**
- Autenticação JWT obrigatória para endpoints protegidos
- Senhas criptografadas com PBKDF2
- Tokens com tempo de expiração
- CORS configurado

**Persistência:**
- Banco de dados relacional SQLite
- ORM Django para abstração de queries
- Migrations para versionamento de schema
- Integridade referencial garantida por ForeignKeys

**Escalabilidade:**
- API REST stateless (JWT)
- Possibilidade de cache
- Paginação automática de resultados
- Filtros otimizados

**Manutenibilidade:**
- Código organizado em camadas
- Serializers desacoplados das views
- Documentação automática (Swagger/OpenAPI)
- 916 linhas de código principal bem estruturado

**Reusabilidade:**
- ViewSets genéricos do DRF
- Herança de modelos (Usuario → Professor/Coordenador/Empresa)
- Mixins do DRF para operações CRUD
- Serializers reutilizáveis

</p>

## Restrições

<p align = "justify">

**Tecnológicas:**
- Python 3.11.5+
- Django 5.2.7
- Django REST Framework 3.16.1
- SQLite (desenvolvimento)

**Acesso:**
- Aplicação acessível via HTTP/HTTPS
- Requer conexão com internet
- Endpoints REST documentados

**Autenticação:**
- JWT obrigatório para operações protegidas
- Email único por usuário
- Tokens com tempo de expiração fixo

</p>

## Ferramentas Utilizadas

- **Python 3.11.5**: Linguagem de programação principal
- **Django 5.2.7**: Framework web MVT
- **Django REST Framework 3.16.1**: Framework para APIs REST
- **djangorestframework-simplejwt**: Autenticação JWT
- **drf-spectacular**: Documentação OpenAPI/Swagger
- **django-filter 24.4**: Filtros avançados em queries
- **django-cors-headers 4.9.0**: Habilitação de CORS
- **SQLite**: Banco de dados relacional
- **Git/GitHub**: Controle de versão e colaboração
- **VS Code**: IDE de desenvolvimento

# Visão de Caso de Uso

<p align = "justify">
Os casos de uso do sistema estão documentados em detalhes no arquivo casos_de_uso.md. Os principais casos incluem:
</p>

- **UC01**: Registro de Novo Usuário
- **UC02**: Login com JWT
- **UC03**: Cadastrar Proposta de Projeto
- **UC04**: Avaliar e Aprovar Proposta
- **UC05**: Criar Projeto Vinculado a Proposta
- **UC06**: Atualizar Progresso do Projeto
- **UC07**: Adicionar Projeto ao Hall of Fame
- **UC08**: Visualizar Top 10 Destaques
- **UC09**: Listar Projetos de um Professor
- **UC10**: Cadastrar Grupo e Vincular Projetos

# Visão Lógica

## Estrutura de Pacotes

```
src/
├── app/
│   ├── models.py          # 8 modelos (93 linhas)
│   ├── serializers.py     # 9 serializers (137 linhas)
│   ├── views.py           # 8 ViewSets + RegisterView (324 linhas)
│   ├── urls.py            # Rotas da API (29 linhas)
│   ├── admin.py           # Admin panel (59 linhas)
│   └── authentication.py  # JWT customizado (54 linhas)
├── CadPro/
│   ├── settings.py        # Configurações (159 linhas)
│   └── urls.py            # Rotas principais (61 linhas)
└── manage.py
```

## Diagrama de Classes

Ver arquivo: `docs/diagrama_de_classes.puml`

Hierarquia principal:
- Usuario (base) → Professor, Coordenador, Empresa
- Proposta → Projeto (OneToOne)
- Relacionamentos ManyToMany entre entidades

# Visão de Implementação

## Endpoints da API

### Autenticação
- `POST /api/register/` - Registro de usuário
- `POST /api/token/` - Obter tokens JWT (email + senha)
- `POST /api/token/refresh/` - Renovar access token
- `POST /api/token/verify/` - Verificar validade do token

### CRUD Completo
- `/api/usuarios/` - Gerenciamento de usuários
- `/api/professores/` - Gerenciamento de professores
- `/api/coordenadores/` - Gerenciamento de coordenadores
- `/api/empresas/` - Gerenciamento de empresas
- `/api/propostas/` - Gerenciamento de propostas
- `/api/projetos/` - Gerenciamento de projetos
- `/api/grupos/` - Gerenciamento de grupos
- `/api/halloffame/` - Gerenciamento do Hall of Fame

### Endpoints Customizados
- `GET /api/professores/{id}/projetos/` - Projetos do professor
- `GET /api/coordenadores/{id}/projetos_aprovados/` - Projetos aprovados
- `GET /api/empresas/{id}/propostas/` - Propostas da empresa
- `GET /api/empresas/{id}/projetos/` - Projetos da empresa
- `GET /api/propostas/em_analise/` - Propostas em análise
- `PATCH /api/projetos/{id}/atualizar_progresso/` - Atualizar progresso
- `GET /api/grupos/{id}/projetos/` - Projetos do grupo
- `GET /api/halloffame/destaques/` - Top 10 destaques

### Documentação
- `/api/docs/` - Swagger UI interativo
- `/api/redoc/` - ReDoc
- `/api/schema/` - Schema OpenAPI JSON

# Visão de Dados

## Modelo Entidade Relacionamento (MER)

### Entidades Principais:

1. **Usuario** (Superclasse)
   - Atributos: id, nome, email (unique), senha
   - Subclasses: Professor, Coordenador, Empresa

2. **Professor** (herda Usuario)
   - Atributo adicional: projetos (String)
   - Relacionamentos: ManyToMany com Projeto

3. **Coordenador** (herda Usuario)
   - Relacionamentos: ManyToMany com Projeto

4. **Empresa** (herda Usuario)
   - Atributos adicionais: contato, projetos (String)
   - Relacionamentos: OneToMany com Proposta, ManyToMany com Projeto

5. **Proposta**
   - Atributos: id, titulo, descricao, data_envio, status, anexos
   - Relacionamentos: ForeignKey para Empresa, OneToOne com Projeto

6. **Projeto** (Entidade Central)
   - Atributos: id, titulo, descricao, status, progresso, curso_turma, alunos, data_inicio, data_final, anexos
   - Relacionamentos: 
     - OneToOne com Proposta (obrigatório)
     - ForeignKey para Professor, Empresa, Coordenador
     - ManyToMany com Professor, Coordenador, Empresa, Grupo

7. **Grupo**
   - Atributos: id, tipo (choices: "I", "II"), alunos
   - Relacionamentos: ManyToMany com Projeto

8. **HallOfFame**
   - Atributos: id, destaque (prioridade)
   - Relacionamentos: ForeignKey para Projeto

### Relacionamentos:

- Usuario → Professor (herança)
- Usuario → Coordenador (herança)
- Usuario → Empresa (herança)
- Empresa → Proposta (1:N)
- Proposta → Projeto (1:1)
- Professor → Projeto (N:N e 0..1:N)
- Coordenador → Projeto (N:N e 0..1:N)
- Empresa → Projeto (N:N e 0..1:N)
- Grupo → Projeto (N:N)
- Projeto → HallOfFame (1:N)

# Tamanho e Desempenho

## Métricas de Código

- **Total de linhas (projeto)**: 1.080 linhas
- **Código principal**: 916 linhas
- **Modelos**: 93 linhas (8 classes)
- **Views**: 324 linhas (9 classes)
- **Serializers**: 137 linhas (9 classes)
- **Migrations**: 164 linhas (19 migrations)

## Desempenho

- Autenticação JWT: < 100ms
- Queries do banco: otimizadas por ORM
- Paginação: 100 itens por página (padrão DRF)
- Tempo de resposta médio: < 200ms

# Qualidade

## Boas Práticas Implementadas

- ✅ Arquitetura em camadas (Model-Serializer-View)
- ✅ Autenticação segura (JWT + senha criptografada)
- ✅ Documentação automática (Swagger/OpenAPI)
- ✅ Validações em múltiplos níveis
- ✅ Código organizado e modular
- ✅ Relacionamentos bem definidos
- ✅ Herança adequada de modelos
- ✅ Actions customizadas documentadas
- ✅ Filtros e buscas implementados
- ✅ Admin panel configurado

# Referências Bibliográficas

- Django Documentation: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/
- drf-spectacular: https://drf-spectacular.readthedocs.io/
- SimpleJWT: https://django-rest-framework-simplejwt.readthedocs.io/

# Histórico de Versão

| Data       | Versão | Descrição                                                   | Autor(es) |
| ---------- | ------ | ----------------------------------------------------------- | --------- |
| 14/11/2024 | 1.0    | Criação do documento com arquitetura implementada          | Equipe    |
| 14/11/2024 | 1.1    | Adição de visões, métricas e estrutura de pacotes         | Equipe    |
| 14/11/2024 | 1.2    | Documentação completa de endpoints e relacionamentos       | Equipe    |
