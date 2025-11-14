---
id: diagrama_classes_implementacao
title: Diagrama de Classes - Implementação Django
---

# Diagrama de Classes - Implementação Django

@startuml
!define ENTITY class
skinparam classAttributeIconSize 0
skinparam shadowing false

ENTITY Usuario {
  +id: Integer
  +nome: String
  +email: String
  +senha: String
  --
  +__str__(): String
}

ENTITY Diretor {
  +id: Integer
  +user: OneToOne(Usuario)
  --
  +__str__(): String
}

ENTITY Professor {
  +id: Integer
  +user: OneToOne(Usuario)
  --
  +__str__(): String
}

ENTITY Empresa {
  +id: Integer
  +nome: String
  +contato: String
  --
  +__str__(): String
}

ENTITY Coordenacao {
  +id: Integer
  +nome: String
  +email: String
  --
  +__str__(): String
}

ENTITY Projeto {
  +id: Integer
  +titulo: String
  +descricao: Text
  +status: String
  +progresso: String
  +curso_turma: String
  +alunos: Text
  +data_inicio: Date
  +data_final: Date
  +etapa_atual: Integer
  +etapa_final: Integer
  +etapa_total: Integer
  +anexos: Text
  +professor_responsavel: ForeignKey(Professor)
  +empresa_associada: ForeignKey(Empresa)
  +aprovado_por: ForeignKey(Coordenacao)
  +projetos_vinculados: ManyToMany(Projeto)
  --
  +__str__(): String
}

ENTITY Grupo {
  +id: Integer
  +tipo: String
  +projetos: ManyToMany(Projeto)
  --
  +__str__(): String
}

ENTITY HallOfFame {
  +id: Integer
  +projeto: ForeignKey(Projeto)
  +destaque: Integer
  --
  +__str__(): String
}

ENTITY Token {
  +key: String (primary)
  +user: OneToOne(User)
  +created: DateTime
}

' Relacionamentos
Usuario "1" -- "0..1" Diretor : user
Usuario "1" -- "0..1" Professor : user
Professor "1" -- "0..*" Projeto : professor_responsavel
Empresa "1" -- "0..*" Projeto : empresa_associada
Coordenacao "1" -- "0..*" Projeto : aprovado_por
Projeto "0..*" -- "0..*" Projeto : projetos_vinculados
Projeto "0..*" -- "0..*" Grupo : projetos
Projeto "1" -- "0..*" HallOfFame : projeto
User "1" -- "0..1" Token : token
@enduml