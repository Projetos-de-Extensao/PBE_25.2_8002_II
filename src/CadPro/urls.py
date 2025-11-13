"""
URL configuration for CadPro project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)
from drf_spectacular.utils import extend_schema
from app.authentication import CustomTokenObtainPairView

# Customiza as views do SimpleJWT para adicionar documentação Swagger
@extend_schema(
    tags=["Autenticação"],
    summary="Renovar token de acesso",
    description="Obtém um novo token de acesso fornecendo um refresh token válido."
)
class CustomTokenRefreshView(TokenRefreshView):
    pass

@extend_schema(
    tags=["Autenticação"],
    summary="Verificar token",
    description="Verifica se um token é válido."
)
class CustomTokenVerifyView(TokenVerifyView):
    pass

urlpatterns = [
    # Redireciona a raiz para o admin
    path('', RedirectView.as_view(url='/admin/', permanent=False)),
    
    path('admin/', admin.site.urls),
    path('api/', include('app.urls')),  # Rotas da API
    
    # Autenticação JWT
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', CustomTokenVerifyView.as_view(), name='token_verify'),
    
    # Documentação da API
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
