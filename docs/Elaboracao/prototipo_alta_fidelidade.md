# O Prototipo 
Ele foi dividido em duas partes, uma pro professor e outra pro diretor.


0) Login (professor/diretor)
```
+----------------------------------------------+
|  Plataforma de Gestão de Projetos Acadêmicos |
+----------------------------------------------+
|  [ Email institucional................. ]    |
|  [ Senha............................... ]    |
|                                              |
|  [ Entrar ]   [ Esqueci a senha ]            |
+----------------------------------------------+
|  Dica: use seu e-mail @ibmec.edu.br          |
+----------------------------------------------+
```

1) Direção — Lista de Projetos
```
+--------------------------------------------------------------+
| Projetos em andamento                                        |
+--------------------------------------------------------------+
| Filtro: [ Todos v ]  Buscar: [___________]  [ Buscar ]       |
+--------------------------------------------------------------+
| Projeto 1        | Em revisão           | [Detalhes]      [⋮]|
| Projeto 2        | 20/22 passos prontos    | [Detalhes]   [⋮]|
| Projeto 3        | 13/13passos prontos    | [Detalhes]   [⋮] |
--------------------------------------------------------------+
| [ Novo Projeto ]                                              |
+--------------------------------------------------------------+
Legenda [⋮]: Ações rápidas (Editar, Enviar p/ análise, Excluir)
Vazios: mostrar estado "Nenhum projeto ainda. Crie o primeiro!"
```

2) Direção — Novo / Editar Projeto
```
+--------------------------------------------------------------+
| Direção · Novo/Editar Projeto                                |
+--------------------------------------------------------------+
| Nome:        [__________________________________________]    |
| Descrição:   [__________________________________________]    |
|              [__________________________________________]    |
| Datas:       Início [__/__/____]  Fim [__/__/____]           |
| Curso/Turma: [____________________]  Diretor: [__________]   |
|                                                  (auto)      |
| Anexos:      [ + Adicionar arquivo ]                         |
+--------------------------------------------------------------+
| [ Cancelar ]  [ Salvar rascunho ]  [ Enviar para análise ]   |
+--------------------------------------------------------------+
Validações: Nome obrigatório; Início ≤ Fim; Status “Concluído” exige Fim.
```

3) Direção — Detalhes do Projeto
```
+--------------------------------------------------------------+
| Direção · Detalhes do Projeto                                |
+--------------------------------------------------------------+
| Nome: Projeto 1                          Status: Em andamento|
| Curso/Turma: Eng. Comp · 7º período                          |
| Professor responsável: (a definir)                           |
| Alunos: (a definir)                                          |
| Datas: 01/09/2025  —  --                                     |
| Descrição: Sistema de controle de tarefas                    |
+--------------------------------------------------------------+
| [ Editar ]  [ Enviar para análise ]  [ Excluir ]  [ Voltar ] |
+--------------------------------------------------------------+
| Histórico                                                    |
| - 01/09/2025 10:30 · Criado pelo Diretor                     |
| - 05/09/2025 09:05 · Descrição atualizada                    |
+--------------------------------------------------------------+
```

4) Direção — Enviar para Análise (modal)
```
+----------------------------------------------+
| Enviar para análise do professor             |
+----------------------------------------------+
| Professor destino: [ Professor X v ]         |
| Mensagem (opcional):                         |
| [__________________________________________] |
| [__________________________________________] |
+----------------------------------------------+
| [ Cancelar ]                 [ Confirmar ]   |
+----------------------------------------------+
Feedback: “Projeto enviado para Professor X.”
```

5) Direção — Ações rápidas no menu ⋮
```
Ao clicar em [⋮] na lista:
--------------------------------
Editar
Enviar para análise
Duplicar
Excluir
--------------------------------
```

6) Direção — Confirmação de Exclusão (modal)
```
+----------------------------------------------+
| Excluir Projeto                              |
+----------------------------------------------+
| Tem certeza que deseja excluir este projeto? |
| Esta ação não pode ser desfeita.             |
+----------------------------------------------+
| [ Cancelar ]                 [ Confirmar ]   |
+----------------------------------------------+
```

7) Estados & mensagens
```
• Sucesso (banner verde): "Projeto salvo com sucesso."
• Erro   (banner vermelho): "Preencha o campo Nome."
• Vazio: "Nenhum projeto. Clique em [Novo Projeto] para começar."
• Carregando: "[…] Carregando projetos..."
```

-----------------------------------------------------------------
===================== FIM DO FLUXO DIREÇÃO =======================
-----------------------------------------------------------------

0) Login do Professor
```
+--------------------------------------------------+
| Plataforma de Gestão de Projetos Acadêmicos      |
+--------------------------------------------------+
|  [ Email institucional (@ibmec.edu.br)..... ]    |
|  [ Senha................................... ]    |
|                                                  |
|  [ Entrar ]   [ Esqueci a senha ]                |
+--------------------------------------------------+
```

1) Professor · Lista de Projetos
```
+------------------------------------------------------------------+
| Professor · Projetos                                             |
+------------------------------------------------------------------+
| Projeto 1 | Etapa atual: 2/5  | [Ver Detalhes]   [⋮]              |
| Projeto 2 | Etapa atual: 5/5  | [Ver Detalhes]   [⋮]              |
| Projeto 3 | Etapa atual: 1/3  | [Ver Detalhes]   [⋮]              |
+------------------------------------------------------------------+
| Filtro: [Todos v]  Buscar: [___________]  [Buscar]                |
+------------------------------------------------------------------+
Legenda [⋮]: ações rápidas (Avançar/Recuar etapa, Editar etapas, Editar turma/alunos)
```

2) Professor · Detalhes do Projeto
```
+------------------------------------------------------------------+
| Detalhes do Projeto                                              |
+------------------------------------------------------------------+
| Nome: Projeto 1                                                  |
| Etapas totais: 5                                                 |
| Etapa atual: 2/5 (Em revisão)                                    |
| Curso/Turma: Eng. Comp · 7º período                              |
| Alunos: João, Maria, Pedro                                       |
| Datas: 01/09/2025 — --                                           |
| Descrição: Sistema de controle de tarefas                        |
+------------------------------------------------------------------+
| [ Avançar etapa ]  [ Recuar etapa ]  [ Editar etapas ]           |
| [ Atribuir turma/alunos ]  [ Voltar ]                            |
+------------------------------------------------------------------+
| Histórico                                                        |
| - 05/09/2025: Etapa 1 concluída                                  |
| - 06/09/2025: Etapa 2 iniciada                                   |
+------------------------------------------------------------------+
```

3) Professor · Configuração de Etapas
```
+------------------------------------------------------------------+
| Configurar Etapas do Projeto                                     |
+------------------------------------------------------------------+
| Número de etapas: [ 5 ]                                          |
|                                                                  |
| 1. Definição do escopo        [ Editar ] [ Remover ]             |
| 2. Levantamento de requisitos [ Editar ] [ Remover ]             |
| 3. Desenvolvimento inicial    [ Editar ] [ Remover ]             |
| 4. Testes e ajustes           [ Editar ] [ Remover ]             |
| 5. Entrega final              [ Editar ] [ Remover ]             |
+------------------------------------------------------------------+
| [ + Adicionar etapa ]                                            |
+------------------------------------------------------------------+
| [ Cancelar ]                                    [ Salvar etapas ]|
+------------------------------------------------------------------+
Validações:
- Número de etapas ≥ 1
- Etapas devem ter nomes únicos
```

4) Professor · Avançar/Recuar Etapa (modal de confirmação)
```
+----------------------------------------------+
| Alterar etapa                                |
+----------------------------------------------+
| Projeto: Projeto 1                            |
| Etapa atual: 2/5                              |
|                                              |
| Confirmar avanço para etapa 3/5?             |
+----------------------------------------------+
| [ Cancelar ]                 [ Confirmar ]   |
+----------------------------------------------+
```

(similar para recuar, só mudando a mensagem)

5) Professor · Atribuir Turma e Alunos
```
+------------------------------------------------------------------+
| Atribuir Turma e Alunos                                          |
+------------------------------------------------------------------+
| Selecionar turma: [ Turma 7º período Eng. Comp ▾ ]               |
|                                                                  |
| Alunos no projeto:                                               |
| - João Silva   [Remover]                                         |
| - Maria Souza  [Remover]                                         |
| - Pedro Lima   [Remover]                                         |
|                                                                  |
| [ + Adicionar aluno ]                                            |
+------------------------------------------------------------------+
| [ Cancelar ]                                    [ Salvar ]       |
+------------------------------------------------------------------+
```

6) Professor · Ações rápidas no menu ⋮
```
Ao clicar em [⋮] na lista de projetos:
--------------------------------------------
Avançar etapa
Recuar etapa
Editar etapas
Atribuir turma/alunos
Ver detalhes
--------------------------------------------
```

7) Estados & mensagens
```
• Sucesso (verde): "Etapa avançada com sucesso."
• Sucesso (verde): "Configuração de etapas salva."
• Erro   (vermelho): "Número de etapas inválido."
• Aviso  (amarelo): "Nenhum aluno atribuído a este projeto."
```


