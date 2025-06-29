from rest_framework import viewsets
from .models import Imobiliario, Utilitario, Veiculo
from .serializers import ImobiliarioSerializer, UtilitarioSerializer, VeiculoSerializer


class ImobiliarioViewSet(viewsets.ModelViewSet):
    queryset = Imobiliario.objects.all().order_by('-valor')
    serializer_class = ImobiliarioSerializer

class UtilitarioViewSet(viewsets.ModelViewSet):
    queryset = Utilitario.objects.all().order_by('-valor')
    serializer_class = UtilitarioSerializer

class VeiculoViewSet(viewsets.ModelViewSet):
    queryset = Veiculo.objects.all().order_by('-valor')
    serializer_class = VeiculoSerializer