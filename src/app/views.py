from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from .models import (
    Usuario,
    Professor,
    Coordenador,
    Empresa,
    Proposta,
    Projeto,
    Grupo,
    HallOfFame,
)
from .serializers import (
    UsuarioSerializer,
    ProfessorSerializer,
    CoordenadorSerializer,
    EmpresaSerializer,
    PropostaSerializer,
    ProjetoSerializer,
    GrupoSerializer,
    HallOfFameSerializer,
)


@extend_schema_view(
    list=extend_schema(
        summary="Listar todos os usuários",
        description="Retorna uma lista paginada de todos os usuários cadastrados no sistema.",
        tags=["Usuários"]
    ),
    create=extend_schema(
        summary="Criar novo usuário",
        description="Cria um novo usuário no sistema.",
        tags=["Usuários"]
    ),
    retrieve=extend_schema(
        summary="Detalhar usuário",
        description="Retorna os detalhes de um usuário específico.",
        tags=["Usuários"]
    ),
    update=extend_schema(
        summary="Atualizar usuário",
        description="Atualiza completamente os dados de um usuário.",
        tags=["Usuários"]
    ),
    partial_update=extend_schema(
        summary="Atualizar parcialmente usuário",
        description="Atualiza parcialmente os dados de um usuário.",
        tags=["Usuários"]
    ),
    destroy=extend_schema(
        summary="Remover usuário",
        description="Remove um usuário do sistema.",
        tags=["Usuários"]
    ),
)
class UsuarioViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar usuários.
    
    Permite operações CRUD completas sobre usuários.
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome', 'email']
    ordering_fields = ['id', 'nome', 'email']


@extend_schema_view(
    list=extend_schema(summary="Listar professores", tags=["Professores"]),
    create=extend_schema(summary="Criar professor", tags=["Professores"]),
    retrieve=extend_schema(summary="Detalhar professor", tags=["Professores"]),
    update=extend_schema(summary="Atualizar professor", tags=["Professores"]),
    partial_update=extend_schema(summary="Atualizar parcialmente professor", tags=["Professores"]),
    destroy=extend_schema(summary="Remover professor", tags=["Professores"]),
)
class ProfessorViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar professores.
    
    Professores são usuários que podem ser responsáveis por projetos.
    """
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome', 'email']
    ordering_fields = ['id', 'nome']
    
    @extend_schema(
        summary="Listar projetos do professor",
        description="Retorna todos os projetos associados ao professor.",
        tags=["Professores"],
        responses={200: ProjetoSerializer(many=True)}
    )
    @action(detail=True, methods=['get'])
    def projetos(self, request, pk=None):
        """Endpoint customizado para listar projetos de um professor"""
        professor = self.get_object()
        projetos = professor.projetos.all()
        serializer = ProjetoSerializer(projetos, many=True)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(summary="Listar coordenadores", tags=["Coordenadores"]),
    create=extend_schema(summary="Criar coordenador", tags=["Coordenadores"]),
    retrieve=extend_schema(summary="Detalhar coordenador", tags=["Coordenadores"]),
    update=extend_schema(summary="Atualizar coordenador", tags=["Coordenadores"]),
    partial_update=extend_schema(summary="Atualizar parcialmente coordenador", tags=["Coordenadores"]),
    destroy=extend_schema(summary="Remover coordenador", tags=["Coordenadores"]),
)
class CoordenadorViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar coordenadores.
    
    Coordenadores são usuários que podem aprovar projetos.
    """
    queryset = Coordenador.objects.all()
    serializer_class = CoordenadorSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome', 'email']
    ordering_fields = ['id', 'nome']
    
    @extend_schema(
        summary="Listar projetos aprovados",
        description="Retorna todos os projetos aprovados por este coordenador.",
        tags=["Coordenadores"],
        responses={200: ProjetoSerializer(many=True)}
    )
    @action(detail=True, methods=['get'])
    def projetos_aprovados(self, request, pk=None):
        """Endpoint customizado para listar projetos aprovados por um coordenador"""
        coordenador = self.get_object()
        projetos = coordenador.projetos.all()
        serializer = ProjetoSerializer(projetos, many=True)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(summary="Listar empresas", tags=["Empresas"]),
    create=extend_schema(summary="Criar empresa", tags=["Empresas"]),
    retrieve=extend_schema(summary="Detalhar empresa", tags=["Empresas"]),
    update=extend_schema(summary="Atualizar empresa", tags=["Empresas"]),
    partial_update=extend_schema(summary="Atualizar parcialmente empresa", tags=["Empresas"]),
    destroy=extend_schema(summary="Remover empresa", tags=["Empresas"]),
)
class EmpresaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar empresas parceiras.
    """
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome', 'email', 'contato']
    ordering_fields = ['id', 'nome']
    
    @extend_schema(
        summary="Listar propostas da empresa",
        tags=["Empresas"],
        responses={200: PropostaSerializer(many=True)}
    )
    @action(detail=True, methods=['get'])
    def propostas(self, request, pk=None):
        """Endpoint customizado para listar propostas de uma empresa"""
        empresa = self.get_object()
        propostas = empresa.propostas.all()
        serializer = PropostaSerializer(propostas, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        summary="Listar projetos da empresa",
        tags=["Empresas"],
        responses={200: ProjetoSerializer(many=True)}
    )
    @action(detail=True, methods=['get'])
    def projetos(self, request, pk=None):
        """Endpoint customizado para listar projetos de uma empresa"""
        empresa = self.get_object()
        projetos = empresa.projetos_associados.all()
        serializer = ProjetoSerializer(projetos, many=True)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(summary="Listar propostas", tags=["Propostas"]),
    create=extend_schema(summary="Criar proposta", tags=["Propostas"]),
    retrieve=extend_schema(summary="Detalhar proposta", tags=["Propostas"]),
    update=extend_schema(summary="Atualizar proposta", tags=["Propostas"]),
    partial_update=extend_schema(summary="Atualizar parcialmente proposta", tags=["Propostas"]),
    destroy=extend_schema(summary="Remover proposta", tags=["Propostas"]),
)
class PropostaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar propostas de projetos.
    """
    queryset = Proposta.objects.all()
    serializer_class = PropostaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'empresa']
    search_fields = ['titulo', 'descricao']
    ordering_fields = ['id', 'titulo', 'data_envio', 'status']
    ordering = ['-data_envio']  # Ordenação padrão
    
    @extend_schema(
        summary="Listar propostas em análise",
        description="Retorna apenas as propostas que estão com status 'Em análise'.",
        tags=["Propostas"],
        responses={200: PropostaSerializer(many=True)}
    )
    @action(detail=False, methods=['get'])
    def em_analise(self, request):
        """Endpoint customizado para listar propostas em análise"""
        propostas = self.queryset.filter(status='Em análise')
        serializer = self.get_serializer(propostas, many=True)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(summary="Listar projetos", tags=["Projetos"]),
    create=extend_schema(summary="Criar projeto", tags=["Projetos"]),
    retrieve=extend_schema(summary="Detalhar projeto", tags=["Projetos"]),
    update=extend_schema(summary="Atualizar projeto", tags=["Projetos"]),
    partial_update=extend_schema(summary="Atualizar parcialmente projeto", tags=["Projetos"]),
    destroy=extend_schema(summary="Remover projeto", tags=["Projetos"]),
)
class ProjetoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar projetos de extensão.
    """
    queryset = Projeto.objects.all()
    serializer_class = ProjetoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'professor_responsavel', 'empresa_associada', 'aprovado_por']
    search_fields = ['titulo', 'descricao', 'curso_turma', 'alunos']
    ordering_fields = ['id', 'titulo', 'status', 'progresso', 'data_inicio']
    ordering = ['-id']
    
    @extend_schema(
        summary="Atualizar progresso do projeto",
        description="Atualiza apenas o campo de progresso do projeto (em %).",
        tags=["Projetos"],
        request={"application/json": {"type": "object", "properties": {"progresso": {"type": "number"}}}},
        responses={200: ProjetoSerializer}
    )
    @action(detail=True, methods=['patch'])
    def atualizar_progresso(self, request, pk=None):
        """Endpoint customizado para atualizar apenas o progresso do projeto"""
        projeto = self.get_object()
        progresso = request.data.get('progresso')
        if progresso is not None:
            projeto.progresso = progresso
            projeto.save()
            serializer = self.get_serializer(projeto)
            return Response(serializer.data)
        return Response({'error': 'Progresso não informado'}, status=400)


@extend_schema_view(
    list=extend_schema(summary="Listar grupos", tags=["Grupos"]),
    create=extend_schema(summary="Criar grupo", tags=["Grupos"]),
    retrieve=extend_schema(summary="Detalhar grupo", tags=["Grupos"]),
    update=extend_schema(summary="Atualizar grupo", tags=["Grupos"]),
    partial_update=extend_schema(summary="Atualizar parcialmente grupo", tags=["Grupos"]),
    destroy=extend_schema(summary="Remover grupo", tags=["Grupos"]),
)
class GrupoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar grupos de projetos (Grupo I e Grupo II).
    """
    queryset = Grupo.objects.all()
    serializer_class = GrupoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tipo']
    ordering_fields = ['id', 'tipo']
    
    @extend_schema(
        summary="Listar projetos do grupo",
        tags=["Grupos"],
        responses={200: ProjetoSerializer(many=True)}
    )
    @action(detail=True, methods=['get'])
    def projetos(self, request, pk=None):
        """Endpoint customizado para listar projetos de um grupo"""
        grupo = self.get_object()
        projetos = grupo.projetos.all()
        serializer = ProjetoSerializer(projetos, many=True)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(summary="Listar Hall of Fame", tags=["Hall of Fame"]),
    create=extend_schema(summary="Adicionar ao Hall of Fame", tags=["Hall of Fame"]),
    retrieve=extend_schema(summary="Detalhar entrada do Hall of Fame", tags=["Hall of Fame"]),
    update=extend_schema(summary="Atualizar entrada do Hall of Fame", tags=["Hall of Fame"]),
    partial_update=extend_schema(summary="Atualizar parcialmente entrada", tags=["Hall of Fame"]),
    destroy=extend_schema(summary="Remover do Hall of Fame", tags=["Hall of Fame"]),
)
class HallOfFameViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar o Hall of Fame de projetos em destaque.
    """
    queryset = HallOfFame.objects.all()
    serializer_class = HallOfFameSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['destaque']
    ordering_fields = ['id', 'destaque']
    ordering = ['destaque']  # Ordenação por prioridade
    
    @extend_schema(
        summary="Top 10 destaques",
        description="Retorna os 10 projetos mais destacados do Hall of Fame.",
        tags=["Hall of Fame"],
        responses={200: HallOfFameSerializer(many=True)}
    )
    @action(detail=False, methods=['get'])
    def destaques(self, request):
        """Endpoint customizado para listar apenas os projetos em destaque (top 10)"""
        destaques = self.queryset.order_by('destaque')[:10]
        serializer = self.get_serializer(destaques, many=True)
        return Response(serializer.data)
