# Especificação de Requisitos

## Sistema: Plataforma de Gestão de Projetos Acadêmicos

### 1. Introdução

O presente documento descreve os requisitos do sistema de gestão de projetos acadêmicos. O sistema possibilita o cadastro, acompanhamento e avaliação de projetos em parceria com empresas, professores e coordenação, garantindo transparência no processo de seleção e execução.

### 2. Escopo

O sistema será utilizado por professores, empresas parceiras e coordenação acadêmica.
As principais funcionalidades são:

- Cadastro de entidades (Projetos, Empresas, Coordenação, Professores e Grupos).
- Processo de seleção de projetos (Recebido → Em Avaliação → Pendência → Aprovado).
- Listagem de projetos aprovados disponíveis.
- Acompanhamento de projetos em andamento.
- Visualização de histórico (Hall of Fame).

### 3. Requisitos Funcionais

RF01. O sistema deve permitir o cadastro de projetos com dados básicos (título, descrição, professor responsável, empresa associada).
RF02. O sistema deve permitir o cadastro de empresas parceiras.
**RF03.** O sistema deve permitir o cadastro de coordenação (usuários com perfil de coordenação).
**RF04.** O sistema deve gerenciar o processo de seleção dos projetos, com os seguintes status:
	- Recebido
	- Em Avaliação
	- Pendência
	- Aprovado
**RF05.** O sistema deve permitir o cadastro de professores.
**RF06.** O sistema deve disponibilizar a lista de projetos aprovados disponíveis.
**RF07.** O sistema deve gerar a lista de projetos do professor, com a possibilidade de adoção de projetos.
**RF08.** O sistema deve gerenciar a alocação de grupos de alunos a projetos, divididos em Grupo I e Grupo II.
**RF09.** O sistema deve permitir o acompanhamento dos projetos (status e progresso).
**RF10.** O sistema deve permitir a visualização de Hall of Fame (projetos concluídos de destaque) e dos projetos em andamento.
**RF11.** O sistema deve permitir o cadastro de grupos de alunos.

### 4. Requisitos Não Funcionais

**RNF01.** O sistema deve ser acessível via navegador web.
**RNF02.** O sistema deve possuir autenticação de usuários (Professor, Coordenação, Empresa).
**RNF03.** O banco de dados deve garantir integridade e consistência das informações.
**RNF04.** O sistema deve ser responsivo, acessível também em dispositivos móveis.
**RNF05.** O tempo de resposta não deve ultrapassar 2 segundos para operações de consulta.

### 5. Regras de Negócio

**RN01.** Apenas a Coordenação pode aprovar ou reprovar projetos.
**RN02.** Um projeto só pode ser atribuído a grupos após ser aprovado.
**RN03.** Cada grupo pode estar vinculado a apenas um projeto por vez.
**RN04.** Professores podem adotar projetos apenas da lista de aprovados.

### 6. Casos de Uso (resumidos)

**UC01 – Cadastrar Projeto**

Ator: Professor/Coordenação

Descrição: Permite cadastrar novo projeto com dados obrigatórios.

**UC02 – Avaliar Projeto**

Ator: Coordenação

Descrição: Define status do projeto (Recebido, Em Avaliação, Pendência ou Aprovado).

**UC03 – Adotar Projeto**

Ator: Professor

Descrição: Permite que o professor adote projeto aprovado, vinculando-o a grupo(s).

**UC04 – Acompanhar Projeto**

Ator: Coordenação/Professor

Descrição: Permite visualizar status, progresso e grupos vinculados ao projeto.
