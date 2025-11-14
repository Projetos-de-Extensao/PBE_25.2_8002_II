# Diagrama de Classes

Estrutura do sistema de gestão de projetos acadêmicos.

## Arquivo do Diagrama

**PlantUML:** `docs/diagrama_de_classes.puml`

## Classes

### Usuario (Base)
- id, nome, email, senha
- **Subclasses:** Professor, Coordenador, Empresa

### Professor (herda Usuario)
- projetos: String
- Relacionamentos: ManyToMany com Projeto

### Coordenador (herda Usuario)
- Relacionamentos: ManyToMany com Projeto

### Empresa (herda Usuario)
- contato, projetos: String
- Relacionamentos: 1:N com Proposta, N:N com Projeto

### Proposta
- titulo, descricao, data_envio, status, anexos
- Relacionamentos: N:1 com Empresa, 1:1 com Projeto

### Projeto (Central)
- titulo, descricao, status, progresso, curso_turma, alunos, datas, anexos
- Relacionamentos: 1:1 com Proposta, N:1 com Professor/Empresa/Coordenador, N:N com Grupo

### Grupo
- tipo ("I" ou "II"), alunos
- Relacionamentos: N:N com Projeto

### HallOfFame
- destaque (prioridade)
- Relacionamentos: N:1 com Projeto

## Hierarquia

```
Usuario → Professor, Coordenador, Empresa
```

## Relacionamentos Principais

- Empresa → Proposta (1:N)
- Proposta → Projeto (1:1)
- Projeto → Professor/Coordenador/Empresa (N:1 e N:N)
- Grupo → Projeto (N:N)
- Projeto → HallOfFame (1:N)
