from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password, check_password
from .models import Usuario, Empresa


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Serializer customizado para usar email em vez de username"""
    username_field = 'email'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uname_field = getattr(self, 'username_field', 'username')
        if uname_field in self.fields and uname_field != 'email':
            self.fields['email'] = self.fields.pop(uname_field)

    @classmethod
    def get_token(cls, user):
        from .models import Professor, Coordenador, Empresa
        token = super().get_token(user)
        token['email'] = user.email
        token['nome'] = user.nome
        
        # Adiciona user_type ao token para permitir distinção no backend
        user_type = 'unknown'
        if isinstance(user, Professor):
            user_type = 'professor'
        elif isinstance(user, Coordenador):
            user_type = 'coordenador'
        elif isinstance(user, Empresa):
            user_type = 'empresa'
        elif isinstance(user, Usuario):
            # Usuario genérico (não Professor/Coordenador)
            user_type = 'usuario'
        token['user_type'] = user_type
        
        return token

    def validate(self, attrs):
        # Busca usuário por email
        email = attrs.get('email')
        password = attrs.get('password')

        user = None
        # Tenta primeiro Usuario
        try:
            user = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            # Se não existir, tenta Empresa (permitir que empresas façam login)
            try:
                user = Empresa.objects.get(email=email)
            except Empresa.DoesNotExist:
                from rest_framework_simplejwt.exceptions import AuthenticationFailed
                raise AuthenticationFailed('No active account found with the given credentials')

        # Verifica senha — tanto para Usuario quanto Empresa usamos o campo 'senha'
        if not check_password(password, user.senha):
            if user.senha == password:
                user.senha = make_password(password)
                user.save(update_fields=['senha'])
            else:
                from rest_framework_simplejwt.exceptions import AuthenticationFailed
                raise AuthenticationFailed('No active account found with the given credentials')

        refresh = self.get_token(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


@extend_schema(
    tags=["Autenticação"],
    summary="Obter token de acesso",
    description="Obtém um par de tokens (access e refresh) fornecendo email e senha válidos."
)
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
