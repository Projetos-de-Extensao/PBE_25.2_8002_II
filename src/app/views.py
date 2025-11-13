from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

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


class UsuarioViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar usuários.
    Endpoints:
    - GET /api/usuarios/ - Lista todos os usuários
    - POST /api/usuarios/ - Cria um novo usuário
    - GET /api/usuarios/{id}/ - Detalha um usuário específico
    - PUT /api/usuarios/{id}/ - Atualiza um usuário
    - DELETE /api/usuarios/{id}/ - Remove um usuário
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome', 'email']
    ordering_fields = ['id', 'nome', 'email']


class ProfessorViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar professores.
    """
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome', 'email']
    ordering_fields = ['id', 'nome']
    
    @action(detail=True, methods=['get'])
    def projetos(self, request, pk=None):
        """Endpoint customizado para listar projetos de um professor"""
        professor = self.get_object()
        projetos = professor.projetos.all()
        serializer = ProjetoSerializer(projetos, many=True)
        return Response(serializer.data)


class CoordenadorViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar coordenadores.
    """
    queryset = Coordenador.objects.all()
    serializer_class = CoordenadorSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome', 'email']
    ordering_fields = ['id', 'nome']
    
    @action(detail=True, methods=['get'])
    def projetos_aprovados(self, request, pk=None):
        """Endpoint customizado para listar projetos aprovados por um coordenador"""
        coordenador = self.get_object()
        projetos = coordenador.projetos.all()
        serializer = ProjetoSerializer(projetos, many=True)
        return Response(serializer.data)


class EmpresaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar empresas.
    """
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome', 'email', 'contato']
    ordering_fields = ['id', 'nome']
    
    @action(detail=True, methods=['get'])
    def propostas(self, request, pk=None):
        """Endpoint customizado para listar propostas de uma empresa"""
        empresa = self.get_object()
        propostas = empresa.propostas.all()
        serializer = PropostaSerializer(propostas, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def projetos(self, request, pk=None):
        """Endpoint customizado para listar projetos de uma empresa"""
        empresa = self.get_object()
        projetos = empresa.projetos_associados.all()
        serializer = ProjetoSerializer(projetos, many=True)
        return Response(serializer.data)


class PropostaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar propostas.
    """
    queryset = Proposta.objects.all()
    serializer_class = PropostaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'empresa']
    search_fields = ['titulo', 'descricao']
    ordering_fields = ['id', 'titulo', 'data_envio', 'status']
    ordering = ['-data_envio']  # Ordenação padrão
    
    @action(detail=False, methods=['get'])
    def em_analise(self, request):
        """Endpoint customizado para listar propostas em análise"""
        propostas = self.queryset.filter(status='Em análise')
        serializer = self.get_serializer(propostas, many=True)
        return Response(serializer.data)


class ProjetoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar projetos.
    """
    queryset = Projeto.objects.all()
    serializer_class = ProjetoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'professor_responsavel', 'empresa_associada', 'aprovado_por']
    search_fields = ['titulo', 'descricao', 'curso_turma', 'alunos']
    ordering_fields = ['id', 'titulo', 'status', 'progresso', 'data_inicio']
    ordering = ['-id']
    
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


class GrupoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar grupos.
    """
    queryset = Grupo.objects.all()
    serializer_class = GrupoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tipo']
    ordering_fields = ['id', 'tipo']
    
    @action(detail=True, methods=['get'])
    def projetos(self, request, pk=None):
        """Endpoint customizado para listar projetos de um grupo"""
        grupo = self.get_object()
        projetos = grupo.projetos.all()
        serializer = ProjetoSerializer(projetos, many=True)
        return Response(serializer.data)


class HallOfFameViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar o Hall of Fame.
    """
    queryset = HallOfFame.objects.all()
    serializer_class = HallOfFameSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['destaque']
    ordering_fields = ['id', 'destaque']
    ordering = ['destaque']  # Ordenação por prioridade
    
    @action(detail=False, methods=['get'])
    def destaques(self, request):
        """Endpoint customizado para listar apenas os projetos em destaque (top 10)"""
        destaques = self.queryset.order_by('destaque')[:10]
        serializer = self.get_serializer(destaques, many=True)
        return Response(serializer.data)
