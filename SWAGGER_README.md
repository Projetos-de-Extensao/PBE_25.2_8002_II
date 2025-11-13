# 📚 Documentação Swagger - EchoAPI

## ✅ Swagger Implementado com Sucesso!

A documentação Swagger foi implementada usando **drf-spectacular**, a biblioteca mais moderna para OpenAPI 3.0 no Django REST Framework.

## 🌐 URLs de Acesso

Com o servidor rodando (`python manage.py runserver`), acesse:

### 1️⃣ Swagger UI (Recomendado)
**URL:** http://127.0.0.1:8000/api/docs/

Interface interativa completa onde você pode:
- Explorar todos os endpoints da API
- Testar requisições diretamente no navegador
- Ver exemplos de request e response
- Visualizar schemas de dados
- Filtrar por tags (Usuários, Professores, Empresas, etc.)

### 2️⃣ ReDoc
**URL:** http://127.0.0.1:8000/api/redoc/

Documentação alternativa com visual mais limpo:
- Ideal para leitura e referência
- Estrutura clara e organizada
- Busca integrada
- Exemplos de código

### 3️⃣ Schema OpenAPI (JSON)
**URL:** http://127.0.0.1:8000/api/schema/

Retorna o schema OpenAPI 3.0 completo em formato JSON. Útil para:
- Importar em ferramentas como Postman
- Gerar código cliente automaticamente
- Integração com outras ferramentas

## 📋 Recursos Implementados

### Tags Organizadas
Os endpoints estão organizados por categorias:
- 👥 **Usuários** - Gerenciamento de usuários base
- 👨‍🏫 **Professores** - Professores e seus projetos
- 👔 **Coordenadores** - Coordenadores e aprovações
- 🏢 **Empresas** - Empresas parceiras
- 📝 **Propostas** - Propostas de projetos
- 📁 **Projetos** - Projetos de extensão
- 👥 **Grupos** - Grupos I e II
- 🏆 **Hall of Fame** - Projetos em destaque

### Documentação Detalhada
Cada endpoint possui:
- ✅ Título descritivo
- ✅ Descrição completa
- ✅ Parâmetros de entrada
- ✅ Exemplos de request
- ✅ Estrutura de response
- ✅ Códigos de status HTTP

### Funcionalidades Especiais Documentadas
- 🔍 **Filtros** - Filtrar por status, empresa, professor, etc.
- 🔎 **Busca** - Buscar por texto em múltiplos campos
- 📊 **Ordenação** - Ordenar resultados
- 📄 **Paginação** - Navegação por páginas
- ⚡ **Endpoints customizados** - Ações especiais documentadas

## 🎯 Endpoints Customizados Documentados

### Professores
- `GET /api/professores/{id}/projetos/` - Lista projetos do professor

### Coordenadores
- `GET /api/coordenadores/{id}/projetos_aprovados/` - Projetos aprovados

### Empresas
- `GET /api/empresas/{id}/propostas/` - Propostas da empresa
- `GET /api/empresas/{id}/projetos/` - Projetos da empresa

### Propostas
- `GET /api/propostas/em_analise/` - Propostas em análise

### Projetos
- `PATCH /api/projetos/{id}/atualizar_progresso/` - Atualiza progresso

### Grupos
- `GET /api/grupos/{id}/projetos/` - Projetos do grupo

### Hall of Fame
- `GET /api/hall-of-fame/destaques/` - Top 10 destaques

## 🛠️ Configuração Técnica

### Biblioteca Usada
**drf-spectacular** - OpenAPI 3.0 schema generation for Django REST Framework

### Configurações no settings.py
```python
INSTALLED_APPS = [
    # ...
    'drf_spectacular',
]

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    # ...
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'EchoAPI - API de Projetos de Extensão',
    'DESCRIPTION': 'API REST para gerenciamento de projetos...',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'SCHEMA_PATH_PREFIX': '/api/',
    # ...
}
```

### URLs Configuradas
```python
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
```

## 📝 Decoradores Usados

### @extend_schema_view
Documenta operações padrão do ViewSet (list, create, retrieve, update, etc.)

```python
@extend_schema_view(
    list=extend_schema(summary="Listar usuários", tags=["Usuários"]),
    create=extend_schema(summary="Criar usuário", tags=["Usuários"]),
)
class UsuarioViewSet(viewsets.ModelViewSet):
    ...
```

### @extend_schema
Documenta actions customizadas

```python
@extend_schema(
    summary="Listar projetos do professor",
    description="Retorna todos os projetos associados ao professor.",
    tags=["Professores"],
    responses={200: ProjetoSerializer(many=True)}
)
@action(detail=True, methods=['get'])
def projetos(self, request, pk=None):
    ...
```

## 🎨 Features do Swagger UI

### Try it out
- Teste qualquer endpoint diretamente
- Preencha parâmetros e body
- Veja a resposta em tempo real

### Schemas
- Visualize a estrutura de todos os modelos
- Veja campos obrigatórios e opcionais
- Tipos de dados claramente definidos

### Filtros e Parâmetros
- Query params documentados
- Filtros por campo
- Parâmetros de ordenação e busca

### Authentication (Futuro)
- Placeholder para autenticação JWT/Token
- Persistência de autorização entre requisições

## 🚀 Como Usar o Swagger

1. **Inicie o servidor**
   ```bash
   cd src
   python manage.py runserver
   ```

2. **Acesse o Swagger UI**
   - Abra: http://127.0.0.1:8000/api/docs/

3. **Explore os endpoints**
   - Clique em qualquer endpoint para expandir
   - Use os filtros por tag no topo

4. **Teste uma requisição**
   - Clique em "Try it out"
   - Preencha os parâmetros necessários
   - Clique em "Execute"
   - Veja a resposta abaixo

5. **Veja os schemas**
   - Role até o final da página
   - Seção "Schemas" mostra todos os modelos

## 📦 Exportar para outras ferramentas

### Postman
1. Acesse http://127.0.0.1:8000/api/schema/
2. Copie o JSON
3. No Postman: Import → Raw text → Cole o JSON

### Outras ferramentas
O schema OpenAPI 3.0 é compatível com:
- Insomnia
- Paw
- HTTPie
- Geradores de código cliente (openapi-generator)

## ✨ Próximos Passos (Sugestões)

- [ ] Adicionar autenticação JWT
- [ ] Implementar permissões por role
- [ ] Adicionar exemplos de response nos schemas
- [ ] Documentar códigos de erro específicos
- [ ] Adicionar rate limiting

## 🎓 Referências

- [drf-spectacular Documentation](https://drf-spectacular.readthedocs.io/)
- [OpenAPI Specification](https://swagger.io/specification/)
- [Django REST Framework](https://www.django-rest-framework.org/)
