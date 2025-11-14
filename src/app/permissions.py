from rest_framework.permissions import BasePermission
from .models import Coordenador


class IsCoordenador(BasePermission):
    """Permissão que permite apenas coordenadores (ou staff/superuser) acessarem.

    - Se o usuário for um Django User (is_staff/is_superuser), permite.
    - Se o usuário for do modelo `app.Coordenador` (busca por email), permite.
    """
    def has_permission(self, request, view):
        user = request.user
        # Requer autenticação
        if not getattr(user, 'is_authenticated', False):
            return False

        # Django built-in staff/superuser
        if getattr(user, 'is_staff', False) or getattr(user, 'is_superuser', False):
            return True

        # Para o caso do modelo app.Usuario (ou UsuarioWrapper) procuramos um Coordenador
        email = getattr(user, 'email', None)
        if email:
            return Coordenador.objects.filter(email=email).exists()

        return False


from rest_framework.permissions import SAFE_METHODS
from .models import Professor, Empresa


class IsEmpresaOrCoordenador(BasePermission):
    """Permissão que permite acesso apenas para Empresas ou Coordenadores.
    
    Usada para ações como criar propostas, onde empresas podem criar suas próprias
    propostas e coordenadores podem criar/gerenciar qualquer proposta.
    """
    def has_permission(self, request, view):
        if not getattr(request.user, 'is_authenticated', False):
            return False
        
        # Coordenador / staff tem acesso
        if IsCoordenador().has_permission(request, view):
            return True
        
        # Empresa tem acesso
        user_type = getattr(request.user, 'user_type', None)
        if user_type == 'empresa':
            return True
        
        # Verifica se existe registro de Empresa com o email do usuário
        email = getattr(request.user, 'email', None)
        if email and Empresa.objects.filter(email=email).exists():
            return True
        
        return False


class IsProfessorOrCoordenadorOrReadOnly(BasePermission):
    """Permissão que permite:
    - métodos seguros (GET, HEAD, OPTIONS) para usuários autenticados;
    - métodos de escrita (POST/PUT/PATCH/DELETE) apenas se o usuário for o
      professor responsável pelo objeto `Projeto` ou for um Coordenador/staff.
    - NEGA acesso de escrita para Empresas (mesmo que tenham token válido).

    Usada em `ProjetoViewSet` para permitir que professores editem seus projetos
    sem abrir edição para qualquer outro professor ou empresas.
    """
    def has_permission(self, request, view):
        # permitir leitura para qualquer (pode ajustar para exigir autenticação se desejado)
        if request.method in SAFE_METHODS:
            return True
        # para operações de escrita, requer autenticação; object-level check fará o resto
        return getattr(request.user, 'is_authenticated', False)

    def has_object_permission(self, request, view, obj):
        # Leitura: permitido
        if request.method in SAFE_METHODS:
            return True

        # Bloqueia Empresas explicitamente de editar projetos
        user_type = getattr(request.user, 'user_type', None)
        if user_type == 'empresa':
            return False

        # Coordenador / staff tem acesso total
        if IsCoordenador().has_permission(request, view):
            return True

        # Verifica se o usuário é o professor responsável pelo projeto
        email = getattr(request.user, 'email', None)
        if not email:
            return False

        try:
            prof = getattr(obj, 'professor_responsavel', None)
            if prof and getattr(prof, 'email', None) == email:
                return True
        except Exception:
            return False

        return False
