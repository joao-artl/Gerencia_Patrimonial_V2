from rest_framework import viewsets
from .models import Empresa, Filial
from .serializers import EmpresaSerializer, FilialSerializer

class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.prefetch_related('filiais', 'endereco').all()
    serializer_class = EmpresaSerializer

class FilialViewSet(viewsets.ModelViewSet):
    serializer_class = FilialSerializer

    def get_queryset(self):
        return Filial.objects.filter(empresa_matriz_id=self.kwargs['empresa_pk'])

    def perform_create(self, serializer):
        serializer.save(empresa_matriz_id=self.kwargs['empresa_pk'])