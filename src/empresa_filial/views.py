from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from .models import Empresa, Filial, Gerencia
from .serializers import EmpresaSerializer, FilialSerializer, JoinEmpresaSerializer
from usuarios.permissions import IsGestor, IsManagerOfParentCompany


class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.prefetch_related('filiais', 'endereco').all()
    serializer_class = EmpresaSerializer
    permission_classes = [IsAuthenticated, IsGestor]

    def perform_create(self, serializer):
        empresa_criada = serializer.save()
        Gerencia.objects.create(
            usuario=self.request.user,
            empresa=empresa_criada
        )

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsGestor])
    def join(self, request, pk=None):
        empresa = self.get_object()
        gestor = request.user

        serializer = JoinEmpresaSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            senha_submetida = serializer.validated_data['senha_da_empresa']

            if not check_password(senha_submetida, empresa.password):
                return Response(
                    {'error': 'A senha da empresa está incorreta.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if Gerencia.objects.filter(empresa=empresa, usuario=gestor).exists():
                return Response(
                    {'message': 'Você já é um gestor desta empresa.'},
                    status=status.HTTP_200_OK
                )

            Gerencia.objects.create(empresa=empresa, usuario=gestor)

            return Response(
                {'message': f'Você foi adicionado com sucesso como gestor da empresa {empresa.nome}.'},
                status=status.HTTP_200_OK
            )

class FilialViewSet(viewsets.ModelViewSet):
    serializer_class = FilialSerializer
    permission_classes = [IsAuthenticated, IsManagerOfParentCompany]

    def get_queryset(self):
        return Filial.objects.filter(empresa_matriz_id=self.kwargs['empresa_pk'])

    def perform_create(self, serializer):
        serializer.save(empresa_matriz_id=self.kwargs['empresa_pk'])