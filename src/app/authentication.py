from django.contrib.auth.hashers import check_password, make_password
from drf_spectacular.utils import extend_schema
from .models import Usuario
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings
from django.contrib.auth import get_user_model


class UsuarioWrapper:
    """Wrapper leve para expor o objeto Usuario como um 'user' autenticado.

    Fornece is_authenticated = True e delega atributos ao modelo `Usuario`.
    Armazena o tipo de usuário (professor/coordenador/empresa/usuario) para
    facilitar verificações de permissão.
    """
    def __init__(self, usuario, user_type=None):
        self._usuario = usuario
        self._user_type = user_type  # 'professor', 'coordenador', 'empresa', 'usuario'

    @property
    def is_authenticated(self):
        return True
    
    @property
    def user_type(self):
        return self._user_type

    def __getattr__(self, name):
        return getattr(self._usuario, name)


class CustomJWTAuthentication(JWTAuthentication):
    """Extensão que suporta tokens emitidos para o modelo `Usuario` do app.

    Primeiro tenta resolver para o modelo de usuário padrão; se falhar, tenta
    buscar no modelo apropriado (Professor, Coordenador, Empresa, Usuario) baseado
    no campo `user_type` presente no token, e retorna um `UsuarioWrapper`.
    """
    def get_user(self, validated_token):
        from .models import Professor, Coordenador, Empresa
        
        # Pega claim configurado (por padrão 'user_id')
        id_claim = settings.SIMPLE_JWT.get('USER_ID_CLAIM', 'user_id')
        user_id = validated_token.get(id_claim)
        if user_id is None:
            return None

        # Tenta buscar no modelo padrão Django
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except Exception:
            pass

        # Fallback: usa user_type do token para buscar no modelo correto
        user_type = validated_token.get('user_type', 'usuario')
        
        try:
            if user_type == 'professor':
                usuario = Professor.objects.get(pk=user_id)
            elif user_type == 'coordenador':
                usuario = Coordenador.objects.get(pk=user_id)
            elif user_type == 'empresa':
                usuario = Empresa.objects.get(pk=user_id)
            else:
                # fallback genérico
                usuario = Usuario.objects.get(pk=user_id)
            
            return UsuarioWrapper(usuario, user_type=user_type)
        except Exception:
            from rest_framework_simplejwt.exceptions import AuthenticationFailed
            raise AuthenticationFailed('User not found')


# Note: Token obtain serializer/view are defined in app/jwt_views.py to avoid
# circular imports during settings import (they import rest_framework modules).
