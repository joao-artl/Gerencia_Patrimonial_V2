from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from django.db.models import Q
from .models import Empresa, Filial, Gerencia 
from .serializers import EmpresaSerializer, FilialSerializer, JoinEmpresaSerializer, JoinByEmailSerializer 
from patrimonio.models import Veiculo, Utilitario, Imobiliario
from patrimonio.serializers import VeiculoSerializer, UtilitarioSerializer, ImobiliarioSerializer
from usuarios.permissions import IsGestor, IsManagerOfParentCompany
from usuarios.models import Usuario
from usuarios.serializers import UsuarioSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes


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
        
        search_term = request.query_params.get('search', None)

        for filial in filiais_da_empresa:
            veiculos = Veiculo.objects.filter(filial_associada=filial)
            utilitarios = Utilitario.objects.filter(filial_associada=filial)
            imobiliarios = Imobiliario.objects.filter(filial_associada=filial)

            if search_term:
                veiculos = veiculos.filter(
                    Q(nome__icontains=search_term) |
                    Q(modelo__icontains=search_term) |
                    Q(fabricante__icontains=search_term)
                )
                utilitarios = utilitarios.filter(
                    Q(nome__icontains=search_term) |
                    Q(descricao__icontains=search_term)
                )
                imobiliarios = imobiliarios.filter(
                    Q(nome__icontains=search_term) |
                    Q(tipo__icontains=search_term) |
                    Q(endereco__cidade__icontains=search_term) |
                    Q(endereco__logradouro__icontains=search_term)
                )

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
    

    @action(detail=False, methods=['post'], url_path='join-by-email', permission_classes=[IsAuthenticated, IsGestor])
    def join_by_email(self, request):

        serializer = JoinByEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email_empresa = serializer.validated_data['email']
        senha_submetida = serializer.validated_data['senha']
        gestor = request.user

        try:
            empresa = Empresa.objects.get(email=email_empresa)
        except Empresa.DoesNotExist:
            return Response({'error': 'Nenhuma empresa encontrada com este email.'}, status=status.HTTP_404_NOT_FOUND)

        if not check_password(senha_submetida, empresa.password):
            return Response({'error': 'A senha da empresa está incorreta.'}, status=status.HTTP_400_BAD_REQUEST)

        if Gerencia.objects.filter(empresa=empresa, usuario=gestor).exists():
            return Response({'message': 'Você já é um gestor desta empresa.'}, status=status.HTTP_200_OK)

        Gerencia.objects.create(empresa=empresa, usuario=gestor)

        return Response(
            {'message': f'Você foi adicionado com sucesso como gestor da empresa {empresa.nome}.'},
            status=status.HTTP_200_OK
        )

@extend_schema(
    parameters=[
        OpenApiParameter(name='empresa_pk', description='ID da Empresa mãe', required=True, type=OpenApiTypes.INT, location=OpenApiParameter.PATH),
        OpenApiParameter(name='pk', description='ID da Filial', required=True, type=OpenApiTypes.INT, location=OpenApiParameter.PATH),
    ]
)

class FilialViewSet(viewsets.ModelViewSet):
    serializer_class = FilialSerializer
    permission_classes = [IsAuthenticated, IsManagerOfParentCompany]

    def get_queryset(self):
        return Filial.objects.filter(empresa_matriz_id=self.kwargs['empresa_pk'])

    def perform_create(self, serializer):
        serializer.save(empresa_matriz_id=self.kwargs['empresa_pk'])