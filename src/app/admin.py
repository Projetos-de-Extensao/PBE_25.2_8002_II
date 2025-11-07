from django.contrib import admin
from .models import (
    Usuario,
    Coordenador,
    Professor,
    Empresa,
    Proposta,
    Projeto,
    Grupo,
    HallOfFame,
)


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'email')
    search_fields = ('nome', 'email')


@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'email')  # herda direto de Usuario
    search_fields = ('nome', 'email')
    filter_horizontal = ('projetos',)


@admin.register(Coordenador)
class CoordenadorAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'email')  # herda direto de Usuario
    search_fields = ('nome', 'email')
    filter_horizontal = ('projetos',)

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'email', 'contato')
    search_fields = ('nome', 'nome_cliente', 'email')
    filter_horizontal = ('projetos_associados',)


@admin.register(Proposta)
class PropostaAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'empresa', 'status', 'data_envio')
    search_fields = ('titulo', 'descricao', 'empresa__nome')
    list_filter = ('status', 'empresa')
    autocomplete_fields = ('empresa',)


@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'titulo',
        'status',
        'progresso',
        'professor_responsavel',
        'empresa_associada',
        'aprovado_por',
        'proposta',
    )
    search_fields = ('titulo', 'descricao', 'curso_turma', 'alunos')
    list_filter = ('status', 'empresa_associada', 'aprovado_por')
    autocomplete_fields = ('professor_responsavel', 'empresa_associada', 'aprovado_por', 'proposta')


@admin.register(Grupo)
class GrupoAdmin(admin.ModelAdmin):
    list_display = ('id', 'tipo')
    filter_horizontal = ('projetos',)


@admin.register(HallOfFame)
class HallOfFameAdmin(admin.ModelAdmin):
    list_display = ('id', 'projeto', 'destaque')
    list_filter = ('destaque',)
