from django.contrib import admin
from .models import (
	Usuario,
	Diretor,
	Professor,
	Empresa,
	Coordenacao,
	Projeto,
	Grupo,
	HallOfFame,
)


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
	list_display = ('id', 'nome', 'email')
	search_fields = ('nome', 'email')


@admin.register(Diretor)
class DiretorAdmin(admin.ModelAdmin):
	list_display = ('id', 'user')


@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
	list_display = ('id', 'user')


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
	list_display = ('id', 'nome', 'contato')


@admin.register(Coordenacao)
class CoordenacaoAdmin(admin.ModelAdmin):
	list_display = ('id', 'nome', 'email')


@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
	list_display = ('id', 'titulo', 'status', 'professor_responsavel')
	search_fields = ('titulo', 'descricao')
	list_filter = ('status',)


@admin.register(Grupo)
class GrupoAdmin(admin.ModelAdmin):
	list_display = ('id', 'tipo')


@admin.register(HallOfFame)
class HallOfFameAdmin(admin.ModelAdmin):
	list_display = ('id', 'projeto', 'destaque')

