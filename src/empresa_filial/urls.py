from django.urls import path, include
from rest_framework_nested import routers
from .views import EmpresaViewSet, FilialViewSet

router = routers.DefaultRouter()
router.register(r'empresas', EmpresaViewSet, basename='empresa')

filiais_router = routers.NestedDefaultRouter(router, r'empresas', lookup='empresa')
filiais_router.register(r'filiais', FilialViewSet, basename='empresa-filiais')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(filiais_router.urls)),
]