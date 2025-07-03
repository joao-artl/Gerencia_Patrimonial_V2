from rest_framework import viewsets, permissions
from .models import Usuario
from empresa_filial.models import Gerencia
from .serializers import UsuarioSerializer, GerenciaSerializer
from .permissions import IsOwner, UserCreationPermission, IsEmployeeOfThisBranchOrManager, IsGestor

class UsuarioViewSet(viewsets.ModelViewSet):

    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    
    def get_permissions(self):

        if self.action == 'create':
            permission_classes = [UserCreationPermission]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, IsOwner]
        else: 
            permission_classes = [permissions.IsAdminUser]
            
        return [permission() for permission in permission_classes]


class FuncionarioViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmployeeOfThisBranchOrManager]
    
    def get_queryset(self):
        return Usuario.objects.filter(
            tipo_usuario='FUNCIONARIO',
            filial_associada_id=self.kwargs['filial_pk']
        )


class GerenciaViewSet(viewsets.ModelViewSet):
    serializer_class = GerenciaSerializer
    permission_classes = [permissions.IsAuthenticated, IsGestor]

    def get_queryset(self):
        return Gerencia.objects.filter(empresa_id=self.kwargs['empresa_pk'])

    def perform_create(self, serializer):
        serializer.save(empresa_id=self.kwargs['empresa_pk'])