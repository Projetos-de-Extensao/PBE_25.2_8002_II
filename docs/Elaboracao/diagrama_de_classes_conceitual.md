# Diagrama de Classes Conceitual

> Adicione aqui o diagrama de classes conceitual do sistema.

Se desejar, insira uma imagem:

![Diagrama de Classes Conceitual](classes_conceitual.png)

Ou utilize uma ferramenta como draw.io, Lucidchart, ou exporte do StarUML e adicione o arquivo de imagem na pasta.


@startuml DiagramaClassesConceitual

class Projeto {
  +id: int
  +titulo: string
  +descricao: string
  +status: string
  +progresso: string
}

class Professor {
  +id: int
  +nome: string
  +email: string
}

class Empresa {
  +id: int
  +nome: string
  +contato: string
}

class Coordenacao {
  +id: int
  +nome: string
  +email: string
}

class Grupo {
  +id: int
  +tipo: string // Grupo I ou Grupo II
}

class HallOfFame {
  +id: int
  +projeto: Projeto
}

Projeto "1" -- "1" Professor : professorResponsavel
Projeto "1" -- "1" Empresa : empresaAssociada
Projeto "1" -- "1" Coordenacao : aprovadoPor
Projeto "1" -- "N" Grupo : gruposVinculados
Grupo "N" -- "1" Projeto : projetoVinculado
HallOfFame "N" -- "1" Projeto : destaque

@enduml