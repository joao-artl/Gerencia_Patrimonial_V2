from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ImobiliarioViewSet, UtilitarioViewSet, VeiculoViewSet


router = DefaultRouter()
router.register(r'imobiliarios', ImobiliarioViewSet, basename='imobiliario')
router.register(r'utilitarios', UtilitarioViewSet, basename='utilitario')
router.register(r'veiculos', VeiculoViewSet, basename='veiculo')

urlpatterns = [
    path('', include(router.urls)),
]