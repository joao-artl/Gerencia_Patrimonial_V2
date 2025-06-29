from rest_framework import viewsets
from .models import Usuario
from empresa_filial.models import Gerencia
from .serializers import UsuarioSerializer, GerenciaSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer


class FuncionarioViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UsuarioSerializer
    
    def get_queryset(self):
        return Usuario.objects.filter(
            tipo_usuario='FUNCIONARIO',
            filial_associada_id=self.kwargs['filial_pk']
        )


class GerenciaViewSet(viewsets.ModelViewSet):
    serializer_class = GerenciaSerializer

    def get_queryset(self):
        return Gerencia.objects.filter(empresa_id=self.kwargs['empresa_pk'])

    def perform_create(self, serializer):
        serializer.save(empresa_id=self.kwargs['empresa_pk'])