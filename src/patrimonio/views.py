from rest_framework import viewsets
from .models import Imobiliario, Utilitario, Veiculo
from .serializers import ImobiliarioSerializer, UtilitarioSerializer, VeiculoSerializer

class BasePatrimonioViewSet(viewsets.ModelViewSet):
    
    def get_queryset(self):
        return self.queryset.filter(filial_associada_id=self.kwargs['filial_pk'])

    def perform_create(self, serializer):
        serializer.save(filial_associada_id=self.kwargs['filial_pk'])

class VeiculoViewSet(BasePatrimonioViewSet):
    queryset = Veiculo.objects.all()
    serializer_class = VeiculoSerializer

class UtilitarioViewSet(BasePatrimonioViewSet):
    queryset = Utilitario.objects.all()
    serializer_class = UtilitarioSerializer

class ImobiliarioViewSet(BasePatrimonioViewSet):
    queryset = Imobiliario.objects.all()
    serializer_class = ImobiliarioSerializer