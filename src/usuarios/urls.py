from django.urls import path, include
from rest_framework_nested import routers
from empresa_filial.views import EmpresaViewSet, FilialViewSet 
from .views import UsuarioViewSet, FuncionarioViewSet, GerenciaViewSet


router = routers.DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuario')
router.register(r'empresas', EmpresaViewSet, basename='empresa') 

gestores_router = routers.NestedSimpleRouter(router, r'empresas', lookup='empresa')
gestores_router.register(r'gestores', GerenciaViewSet, basename='empresa-gestores')

filiais_router = routers.NestedSimpleRouter(router, r'empresas', lookup='empresa')
filiais_router.register(r'filiais', FilialViewSet, basename='empresa-filiais')

funcionarios_router = routers.NestedSimpleRouter(filiais_router, r'filiais', lookup='filial')
funcionarios_router.register(r'funcionarios', FuncionarioViewSet, basename='filial-funcionarios')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(gestores_router.urls)),
    path('', include(filiais_router.urls)),
    path('', include(funcionarios_router.urls)),
]