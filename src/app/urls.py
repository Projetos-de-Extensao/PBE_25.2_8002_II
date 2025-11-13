from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView,
    UsuarioViewSet,
    ProfessorViewSet,
    CoordenadorViewSet,
    EmpresaViewSet,
    PropostaViewSet,
    ProjetoViewSet,
    GrupoViewSet,
    HallOfFameViewSet,
)

# Cria o router do Django REST Framework
router = DefaultRouter()

# Registra os ViewSets com suas rotas
router.register(r'usuarios', UsuarioViewSet, basename='usuario')
router.register(r'professores', ProfessorViewSet, basename='professor')
router.register(r'coordenadores', CoordenadorViewSet, basename='coordenador')
router.register(r'empresas', EmpresaViewSet, basename='empresa')
router.register(r'propostas', PropostaViewSet, basename='proposta')
router.register(r'projetos', ProjetoViewSet, basename='projeto')
router.register(r'grupos', GrupoViewSet, basename='grupo')
router.register(r'hall-of-fame', HallOfFameViewSet, basename='halloffame')

# URLs da aplicação
urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
]
