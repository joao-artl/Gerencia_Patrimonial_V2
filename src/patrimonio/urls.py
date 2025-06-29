from django.urls import path, include
from rest_framework_nested import routers
from empresa_filial.views import EmpresaViewSet, FilialViewSet 
from .views import ImobiliarioViewSet, UtilitarioViewSet, VeiculoViewSet

router = routers.SimpleRouter()
router.register(r'empresas', EmpresaViewSet, basename='empresa')
filiais_router = routers.NestedSimpleRouter(router, r'empresas', lookup='empresa')
filiais_router.register(r'filiais', FilialViewSet, basename='filial')

imobiliarios_router = routers.NestedSimpleRouter(filiais_router, r'filiais', lookup='filial')
imobiliarios_router.register(r'imobiliarios', ImobiliarioViewSet, basename='filial-imobiliarios')

utilitarios_router = routers.NestedSimpleRouter(filiais_router, r'filiais', lookup='filial')
utilitarios_router.register(r'utilitarios', UtilitarioViewSet, basename='filial-utilitarios')

veiculos_router = routers.NestedSimpleRouter(filiais_router, r'filiais', lookup='filial')
veiculos_router.register(r'veiculos', VeiculoViewSet, basename='filial-veiculos')


urlpatterns = [
    path('', include(imobiliarios_router.urls)),
    path('', include(utilitarios_router.urls)),
    path('', include(veiculos_router.urls)),
]