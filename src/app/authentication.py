from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema
from .models import Usuario


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Serializer customizado para usar email em vez de username"""
    username_field = 'email'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove o campo username e adiciona email e password
        self.fields['email'] = self.fields.pop('username')
        self.fields['password'] = self.fields['password']
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Adiciona informações customizadas ao token
        token['email'] = user.email
        token['nome'] = user.nome
        return token
    
    def validate(self, attrs):
        # Busca usuário por email
        email = attrs.get('email')
        password = attrs.get('password')
        
        try:
            user = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            from rest_framework_simplejwt.exceptions import AuthenticationFailed
            raise AuthenticationFailed('No active account found with the given credentials')
        
        # Verifica senha
        if not check_password(password, user.senha):
            from rest_framework_simplejwt.exceptions import AuthenticationFailed
            raise AuthenticationFailed('No active account found with the given credentials')
        
        # Cria token manualmente
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
    """View customizada para login com email"""
    serializer_class = CustomTokenObtainPairSerializer
