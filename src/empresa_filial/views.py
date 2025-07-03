from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from .models import Empresa, Filial, Gerencia 
from .serializers import EmpresaSerializer, FilialSerializer, JoinEmpresaSerializer 
from patrimonio.models import Veiculo, Utilitario, Imobiliario
from patrimonio.serializers import VeiculoSerializer, UtilitarioSerializer, ImobiliarioSerializer
from usuarios.permissions import IsGestor, IsManagerOfParentCompany
from usuarios.models import Usuario
from usuarios.serializers import UsuarioSerializer


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
        serializer.is_valid(raise_exception=True)
        
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

    @action(detail=True, methods=['get'], url_path='patrimonios', permission_classes=[IsAuthenticated, IsManagerOfParentCompany])
    def listar_todos_patrimonios(self, request, pk=None):
        empresa = self.get_object()
        filiais_da_empresa = empresa.filiais.all()
        resposta_consolidada = {}

        for filial in filiais_da_empresa:
            veiculos = Veiculo.objects.filter(filial_associada=filial)
            utilitarios = Utilitario.objects.filter(filial_associada=filial)
            imobiliarios = Imobiliario.objects.filter(filial_associada=filial)

            resposta_consolidada[f"Filial: {filial.nome} (ID: {filial.id})"] = {
                'veiculos': VeiculoSerializer(veiculos, many=True).data,
                'utilitarios': UtilitarioSerializer(utilitarios, many=True).data,
                'imobiliarios': ImobiliarioSerializer(imobiliarios, many=True).data,
            }

        return Response(resposta_consolidada)
        
    @action(detail=True, methods=['get'], url_path='funcionarios', permission_classes=[IsAuthenticated, IsManagerOfParentCompany])
    def listar_todos_funcionarios(self, request, pk=None):
        empresa = self.get_object()

        funcionarios_da_empresa = Usuario.objects.filter(
            tipo_usuario='FUNCIONARIO',
            filial_associada__empresa_matriz=empresa
        )

        serializer = UsuarioSerializer(funcionarios_da_empresa, many=True)
        
        return Response(serializer.data)


class FilialViewSet(viewsets.ModelViewSet):
    serializer_class = FilialSerializer
    permission_classes = [IsAuthenticated, IsManagerOfParentCompany]

    def get_queryset(self):
        return Filial.objects.filter(empresa_matriz_id=self.kwargs['empresa_pk'])

    def perform_create(self, serializer):
        serializer.save(empresa_matriz_id=self.kwargs['empresa_pk'])