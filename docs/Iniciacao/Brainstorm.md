
 

## Introdução
<p align = "justify">
O brainstorm é uma técnica de elicitação de requisitos que consiste em reunir a equipe e discutir sobre diversos tópicos do projeto. O diálogo é incentivado e críticas são evitadas para permitir que todos colaborem com suas próprias ideias.
</p>

## Metodologia
<p align = "justify">
Definimos 6 perguntas norteadoras para a sessão de brainstorming. Cada membro respondeu individualmente e, em seguida, consolidamos as ideias para definir os requisitos do sistema de gestão de projetos acadêmicos.
</p>

## Brainstorm

## Versão 1.0

## Perguntas

### 1. Qual o objetivo principal da aplicação?

<p align = "justify">
<b>Murilo</b> - O objetivo é criar uma plataforma para gerenciar projetos acadêmicos, facilitando o cadastro, acompanhamento e aprovação por empresas, professores e coordenação.
</p>
<p align = "justify">
<b>Joao</b> - Centralizar todas as informações dos projetos, tornando o processo de seleção e acompanhamento mais transparente e eficiente.
</p>
<p align = "justify">
<b>Enzo</b> - Permitir que professores e grupos adotem projetos aprovados e acompanhem o progresso de forma simples.
</p>
<p align = "justify">
<b>Nicholas</b> - Garantir que o histórico dos melhores projetos fique registrado e acessível (Hall of Fame).
</p>

---

### 2. Como será o processo para cadastrar um novo usuário (empresa, professor, coordenação, grupo)?

<p align = "justify">
<b>Murilo</b> - O usuário acessa o sistema, escolhe o tipo de cadastro e preenche um formulário com dados básicos. A coordenação valida o cadastro antes de liberar o acesso.
</p>
<p align = "justify">
<b>Joao</b> - O cadastro deve ser simples, com campos obrigatórios e validação automática. Após o envio, o sistema notifica a coordenação para análise.
</p>
<p align = "justify">
<b>Enzo</b> - O usuário pode anexar documentos ou informações adicionais para facilitar a análise.
</p>
<p align = "justify">
<b>Nicholas</b> - Todo cadastro fica registrado no histórico, garantindo rastreabilidade.
</p>

---

### 3. Como será a forma de cadastrar e aprovar projetos?

<p align = "justify">
<b>Murilo</b> - Empresas ou professores cadastram projetos preenchendo um formulário detalhado. O projeto passa por etapas: Recebido, Em avaliação, Pendência e Aprovado.
</p>
<p align = "justify">
<b>Joao</b> - A coordenação avalia os projetos e pode solicitar ajustes antes da aprovação.
</p>
<p align = "justify">
<b>Enzo</b> - O status do projeto é atualizado automaticamente e notifica os envolvidos.
</p>
<p align = "justify">
<b>Nicholas</b> - Após aprovado, o projeto fica disponível para adoção por professores e grupos.
</p>

---

### 4. Como será o acompanhamento dos projetos e entregas?

<p align = "justify">
<b>Murilo</b> - Professores e grupos podem atualizar o status das entregas e anexar documentos.
</p>
<p align = "justify">
<b>Joao</b> - O sistema exibe um painel com todos os projetos em andamento, aprovados e finalizados.
</p>
<p align = "justify">
<b>Enzo</b> - A coordenação pode acompanhar o progresso e dar feedbacks em cada etapa.
</p>
<p align = "justify">
<b>Nicholas</b> - O Hall of Fame mostra os projetos de destaque e suas principais entregas.
</p>

---

### 5. O que o dashboard deve mostrar para cada perfil?

<p align = "justify">
<b>Murilo</b> - Para a coordenação: estatísticas gerais, status dos projetos, entregas pendentes e aprovadas.
</p>
<p align = "justify">
<b>Joao</b> - Para professores: lista de projetos disponíveis para adoção, status dos projetos adotados e entregas dos grupos.
</p>
<p align = "justify">
<b>Enzo</b> - Para empresas: status dos projetos submetidos, feedbacks e histórico de parcerias.
</p>
<p align = "justify">
<b>Nicholas</b> - Para grupos: projetos disponíveis, status das entregas e feedbacks recebidos.
</p>

---

### 6. Quais informações seriam interessantes para os usuários?

<p align = "justify">
<b>Murilo</b> - Status do projeto, prazos, responsáveis e histórico de alterações.
</p>
<p align = "justify">
<b>Joao</b> - Documentos, feedbacks e avaliações recebidas.
</p>
<p align = "justify">
<b>Enzo</b> - Painel com projetos aprovados, em andamento e finalizados.
</p>
<p align = "justify">
<b>Nicholas</b> - Gráficos de desempenho e Hall of Fame com os melhores projetos.
</p>

---

## Requisitos elicitados

Após a sessão de brainstorming, o grupo consolidou os seguintes requisitos essenciais para o sistema de gestão de projetos acadêmicos:

### Requisitos Funcionais (RF)

**RF01:** O sistema deve permitir o cadastro de projetos, empresas, coordenação, professores e grupos.
**RF02:** O sistema deve gerenciar o processo de seleção dos projetos (Recebido, Em avaliação, Pendência, Aprovado).
**RF03:** Professores podem adotar projetos aprovados e vinculá-los a grupos.
**RF04:** O sistema deve registrar todas as entregas dos grupos, com anexos e descrições.
**RF05:** Usuários podem visualizar o histórico de projetos (Hall of Fame) e projetos em andamento.
**RF06:** O sistema envia notificações sobre prazos e atualizações importantes.
**RF07:** É possível filtrar projetos por área, status, empresa ou localização.
**RF08:** O sistema permite anexar documentos e feedbacks em cada etapa do projeto.
**RF09:** Professores e grupos podem atualizar o status das entregas.
**RF10:** A coordenação pode aprovar ou reprovar projetos e entregas.
**RF11:** O sistema mantém um histórico completo de todas as ações realizadas.
**RF12:** Usuários recebem alertas sobre eventos e prazos relevantes.
**RF13:** O painel exibe gráficos de desempenho dos projetos.
**RF14:** O sistema permite exportar relatórios de acompanhamento.
**RF15:** O usuário pode acessar feedbacks e avaliações recebidas em cada projeto.

### Requisitos Não Funcionais (RNF)

**RNF01 (Usabilidade):** A interface do sistema deve ser intuitiva, clara e de fácil utilização para todos os perfis de usuário.
**RNF02 (Desempenho):** As páginas e respostas a ações do usuário devem carregar rapidamente.
**RNF03 (Compatibilidade):** O sistema deve ser compatível com os principais navegadores web.

## Conclusão
<p align = "justify">
A técnica de brainstorming permitiu elicitar requisitos fundamentais para o desenvolvimento do sistema, garantindo que as necessidades dos diferentes perfis de usuários fossem consideradas.
</p>

## Autor(es)
| Data | Versão | Descrição | Autor(es) |
| 26/09/2025 | 1.0 | Criação do documento | Murilo Piatigorsky, Joao Marcio, Enzo Zambrotti, Nicholas Victorino |
