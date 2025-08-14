from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Usuario
from empresa_filial.models import Gerencia, Filial
from .serializers import UsuarioSerializer, GerenciaSerializer
from empresa_filial.serializers import EmpresaSerializer, FilialSerializer
from .permissions import (
    IsOwner, 
    UserCreationPermission, 
    IsEmployeeOfThisBranchOrManager, 
    IsGestor, 
    IsOwnerOrManagerOfSameCompany
)
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

class UsuarioViewSet(viewsets.ModelViewSet):

    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    
    def get_permissions(self):
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, IsOwnerOrManagerOfSameCompany]
        elif self.action in ['empresas_gerenciadas', 'filiais_acessiveis']:
            permission_classes = [permissions.IsAuthenticated, IsOwner, IsGestor]
        elif self.action == 'create':
            permission_classes = [UserCreationPermission]
        else: 
            permission_classes = [permissions.IsAdminUser]
            
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['get'], url_path='empresas')
    def empresas_gerenciadas(self, request, pk=None):
        gestor = self.get_object()
        empresas = gestor.empresa_administrada.all()
        serializer = EmpresaSerializer(empresas, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='filiais')
    def filiais_acessiveis(self, request, pk=None):
        gestor = self.get_object()
        ids_empresas_gerenciadas = gestor.empresa_administrada.values_list('id', flat=True)
        filiais = Filial.objects.filter(empresa_matriz_id__in=ids_empresas_gerenciadas)
        serializer = FilialSerializer(filiais, many=True)
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        user_to_delete = self.get_object()
        password = request.data.get('senha')
        if not password:
            return Response(
                {'error': 'A senha é obrigatória para confirmar a exclusão.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not user_to_delete.check_password(password):
            return Response(
                {'error': 'A senha informada está incorreta.'},
                status=status.HTTP_403_FORBIDDEN
            )
        if user_to_delete.tipo_usuario == 'GESTOR':
            empresas_gerenciadas = user_to_delete.empresa_administrada.all()
            for empresa in empresas_gerenciadas:
                if empresa.gestores.count() == 1:
                    empresa.delete()
        self.perform_destroy(user_to_delete)
        return Response(status=status.HTTP_204_NO_CONTENT)

@extend_schema(
    parameters=[
        OpenApiParameter(name='empresa_pk', description='ID da Empresa', required=True, type=OpenApiTypes.INT, location=OpenApiParameter.PATH),
        OpenApiParameter(name='filial_pk', description='ID da Filial', required=True, type=OpenApiTypes.INT, location=OpenApiParameter.PATH),
        OpenApiParameter(name='pk', description='ID do Funcionário', required=True, type=OpenApiTypes.INT, location=OpenApiParameter.PATH),
    ]
)
class FuncionarioViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmployeeOfThisBranchOrManager]
    
    def get_queryset(self):
        return Usuario.objects.filter(
            tipo_usuario='FUNCIONARIO',
            filial_associada_id=self.kwargs['filial_pk']
        )

@extend_schema(
    parameters=[
        OpenApiParameter(name='empresa_pk', description='ID da Empresa', required=True, type=OpenApiTypes.INT, location=OpenApiParameter.PATH),
        OpenApiParameter(name='pk', description='ID da associação de Gerência', required=True, type=OpenApiTypes.INT, location=OpenApiParameter.PATH),
    ]
)
class GerenciaViewSet(viewsets.ModelViewSet):
    serializer_class = GerenciaSerializer
    permission_classes = [permissions.IsAuthenticated, IsGestor]

    def get_queryset(self):
        return Gerencia.objects.filter(empresa_id=self.kwargs['empresa_pk'])

    def perform_create(self, serializer):
        serializer.save(empresa_id=self.kwargs['empresa_pk'])