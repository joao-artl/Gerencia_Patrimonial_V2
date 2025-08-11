"""
URL configuration for gerencia_patrimonio project.

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
from rest_framework_nested import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from usuarios.auth_views import MyTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from empresa_filial.views import EmpresaViewSet, FilialViewSet
from usuarios.views import UsuarioViewSet, GerenciaViewSet, FuncionarioViewSet
from patrimonio.views import ImobiliarioViewSet, UtilitarioViewSet, VeiculoViewSet, PatrimonioDaFilialListView
from src.keep_alive import keep_alive_view


router = routers.DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuario')
router.register(r'empresas', EmpresaViewSet, basename='empresa') 

filiais_router = routers.NestedSimpleRouter(router, r'empresas', lookup='empresa')
filiais_router.register(r'filiais', FilialViewSet, basename='empresa-filiais')
gestores_router = routers.NestedSimpleRouter(router, r'empresas', lookup='empresa')
gestores_router.register(r'gestores', GerenciaViewSet, basename='empresa-gestores')

funcionarios_router = routers.NestedSimpleRouter(filiais_router, r'filiais', lookup='filial')
funcionarios_router.register(r'funcionarios', FuncionarioViewSet, basename='filial-funcionarios')
veiculos_router = routers.NestedSimpleRouter(filiais_router, r'filiais', lookup='filial')
veiculos_router.register(r'veiculos', VeiculoViewSet, basename='filial-veiculos')
utilitarios_router = routers.NestedSimpleRouter(filiais_router, r'filiais', lookup='filial')
utilitarios_router.register(r'utilitarios', UtilitarioViewSet, basename='filial-utilitarios')
imobiliarios_router = routers.NestedSimpleRouter(filiais_router, r'filiais', lookup='filial')
imobiliarios_router.register(r'imobiliarios', ImobiliarioViewSet, basename='filial-imobiliarios')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/keep-alive/', keep_alive_view, name='keep_alive'),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(), name='redoc'),
    path('api/', include(router.urls)), 
    path('api/', include(filiais_router.urls)),
    path('api/', include(gestores_router.urls)),
    path('api/', include(funcionarios_router.urls)),
    path('api/', include(veiculos_router.urls)),
    path('api/', include(utilitarios_router.urls)),
    path('api/', include(imobiliarios_router.urls)),
    path(
        'api/empresas/<int:empresa_pk>/filiais/<int:filial_pk>/patrimonios/', 
        PatrimonioDaFilialListView.as_view(), 
        name='filial-patrimonios-list'
    ),
]