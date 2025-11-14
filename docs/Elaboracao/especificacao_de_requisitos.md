# Especificação de Requisitos

## Sistema de Gestão de Projetos Acadêmicos

---

## 1. Introdução

Este documento descreve os requisitos do sistema de Gestão de Projetos Acadêmicos. A plataforma permite o cadastro, seleção, acompanhamento e avaliação de projetos desenvolvidos em parceria com empresas, professores e a coordenação acadêmica, proporcionando transparência e organização em todo o processo.

---

## 2. Escopo

### Usuários do Sistema

- **Professores**
- **Empresas parceiras**
- **Coordenação acadêmica**

### Principais Funcionalidades

- Cadastro de entidades (Projetos, Empresas, Professores, Coordenação e Grupos de alunos)
- Processo completo de seleção de projetos: **Recebido** → **Em Avaliação** → **Pendência** → **Aprovado**
- Listagem de projetos aprovados disponíveis para adoção
- Acompanhamento dos projetos em andamento
- Visualização de histórico de destaque (Hall of Fame)

---

## 3. Requisitos Funcionais

**RF01. Cadastro de Projetos**  
O sistema deve permitir o cadastro de projetos contendo título, descrição, professor responsável e empresa associada.

**RF02. Cadastro de Empresas**  
O sistema deve permitir que empresas parceiras sejam cadastradas com seus dados básicos.

**RF03. Cadastro de Usuários da Coordenação**  
O sistema deve permitir o cadastro de usuários com perfil de coordenação.

**RF04. Gerenciamento do Processo de Seleção**  
O sistema deve permitir alterar o status dos projetos entre as seguintes etapas:
- Recebido
- Em Avaliação
- Pendência
- Aprovado

**RF05. Cadastro de Professores**  
O sistema deve permitir o cadastro de professores e seus dados profissionais.

**RF06. Listagem de Projetos Aprovados**  
O sistema deve disponibilizar aos professores a lista de projetos já aprovados e aptos para adoção.

**RF07. Lista de Projetos do Professor**  
O sistema deve gerar a lista de projetos vinculados a cada professor, permitindo a adoção ou visualização de informações.

**RF08. Alocação de Grupos**  
O sistema deve gerenciar a alocação de grupos de alunos aos projetos, dividindo-os em Grupo I e Grupo II.

**RF09. Acompanhamento de Projetos**  
O sistema deve permitir o acompanhamento do status, progresso e informações gerais dos projetos em execução.

**RF10. Hall of Fame e Projetos Atuais**  
O sistema deve disponibilizar a visualização dos projetos em andamento e dos projetos concluídos de destaque (Hall of Fame).

**RF11. Cadastro de Grupos de Alunos**  
O sistema deve permitir o cadastro e gerenciamento de grupos de alunos participantes.

---

## 4. Requisitos Não Funcionais

**RNF01. Acesso via Navegador**  
O sistema deve ser acessível através de navegadores web modernos.

**RNF02. Autenticação**  
O sistema deve possuir autenticação para diferentes perfis: Professor, Coordenação e Empresa.

**RNF03. Integridade dos Dados**  
O banco de dados deve garantir a integridade, segurança e consistência das informações armazenadas.

**RNF04. Responsividade**  
O sistema deve ser responsivo e acessível em dispositivos móveis e tablets.

**RNF05. Desempenho**  
O tempo de resposta para operações de consulta não deve exceder 2 segundos.

---

## 5. Regras de Negócio

**RN01. Aprovação Exclusiva pela Coordenação**  
Somente usuários com perfil de coordenação podem aprovar, reprovar ou alterar o status de seleção dos projetos.

**RN02. Atribuição de Projeto a Grupos**  
Um projeto só pode ser alocado a grupos após ter sido aprovado.

**RN03. Vínculo Único por Grupo**  
Cada grupo de alunos pode estar vinculado a apenas um projeto por vez.

**RN04. Adoção de Projetos**  
Professores podem adotar apenas projetos que estejam na lista de aprovados.

---

## 6. Casos de Uso

**UC01 – Cadastrar Projeto**

- **Ator:** Professor / Coordenação
- **Descrição:** Permite cadastrar um novo projeto preenchendo os dados obrigatórios.

**UC02 – Avaliar Projeto**

- **Ator:** Coordenação
- **Descrição:** Permite definir ou alterar o status do projeto (Recebido, Em Avaliação, Pendência, Aprovado).

**UC03 – Adotar Projeto**

- **Ator:** Professor
- **Descrição:** Permite que o professor adote um projeto aprovado e vincule grupos de alunos.

**UC04 – Acompanhar Projeto**

- **Ator:** Professores / Coordenação
- **Descrição:** Permite visualizar o status do projeto, progresso e grupos vinculados.