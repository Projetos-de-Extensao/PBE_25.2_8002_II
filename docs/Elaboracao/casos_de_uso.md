---
id: casos_de_uso
title: Casos de Uso
---

## Casos de Uso do Sistema

### Módulos:

- **Autenticação**: Registro, Login JWT, Renovação de Token
- **Propostas**: Cadastro, Listagem, Filtros, Avaliação
- **Projetos**: Cadastro, Atualização de Progresso, Vínculos
- **Grupos**: Cadastro (Tipo I/II), Vinculação com Projetos
- **Hall of Fame**: Destaques, Top 10

---

## UC01 - Registro de Usuário

**Ator:** Usuário

**Fluxo:**
1. Usuário fornece nome, email e senha via `/api/register/`
2. Sistema valida e criptografa senha
3. Sistema cria usuário e retorna dados

---

## UC02 - Login com JWT

**Ator:** Usuário

**Fluxo:**
1. Usuário fornece email e senha via `/api/token/`
2. Sistema valida credenciais
3. Sistema retorna tokens JWT (access e refresh)

---

## UC03 - Cadastrar Proposta

**Ator:** Empresa

**Pré-condição:** Empresa autenticada

**Fluxo:**
1. Empresa fornece título, descrição e anexos via `/api/propostas/`
2. Sistema vincula proposta à empresa
3. Sistema registra data de envio e retorna proposta

---

## UC04 - Avaliar Proposta

**Ator:** Coordenador

**Pré-condição:** Coordenador autenticado

**Fluxo:**
1. Coordenador atualiza status da proposta (Aprovada/Rejeitada)
2. Sistema atualiza e retorna proposta

---

## UC05 - Criar Projeto

**Ator:** Coordenador/Professor

**Pré-condição:** Proposta aprovada existe

**Fluxo:**
1. Usuário fornece dados do projeto e vincula a proposta (OneToOne)
2. Sistema valida e cria projeto
3. Sistema retorna projeto criado

---

## UC06 - Atualizar Progresso

**Ator:** Professor/Coordenador

**Fluxo:**
1. Usuário fornece progresso (0-100%) via `/api/projetos/{id}/atualizar_progresso/`
2. Sistema atualiza e retorna projeto

---

## UC07 - Adicionar ao Hall of Fame

**Ator:** Coordenador

**Fluxo:**
1. Coordenador fornece projeto e prioridade via `/api/halloffame/`
2. Sistema cria entrada e retorna dados

---

## UC08 - Ver Top 10 Destaques

**Ator:** Qualquer usuário

**Fluxo:**
1. Usuário acessa `/api/halloffame/destaques/`
2. Sistema retorna 10 projetos ordenados por prioridade
