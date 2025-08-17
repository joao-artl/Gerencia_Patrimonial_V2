from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from usuarios.permissions import IsEmployeeOfThisBranchOrManager
from .models import Imobiliario, Utilitario, Veiculo
from .serializers import ImobiliarioSerializer, UtilitarioSerializer
from .serializers import VeiculoSerializer, PatrimonioConsolidadoSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes


@extend_schema(
    parameters=[
        OpenApiParameter(name='empresa_pk',
                         description='ID da Empresa',
                         required=True,
                         type=OpenApiTypes.INT,
                         location=OpenApiParameter.PATH),
        OpenApiParameter(name='filial_pk',
                         description='ID da Filial',
                         required=True,
                         type=OpenApiTypes.INT,
                         location=OpenApiParameter.PATH),
    ]
)
class BasePatrimonioViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsEmployeeOfThisBranchOrManager]
    filter_backends = [SearchFilter]

    def get_queryset(self):
        return self.queryset.filter(filial_associada_id=self.kwargs['filial_pk'])

    def perform_create(self, serializer):
        serializer.save(filial_associada_id=self.kwargs['filial_pk'])


class VeiculoViewSet(BasePatrimonioViewSet):

    queryset = Veiculo.objects.all()
    serializer_class = VeiculoSerializer

    search_fields = ['nome', 'modelo', 'fabricante', 'cor']


class UtilitarioViewSet(BasePatrimonioViewSet):

    queryset = Utilitario.objects.all()
    serializer_class = UtilitarioSerializer

    search_fields = ['nome', 'descricao', 'funcao']


class ImobiliarioViewSet(BasePatrimonioViewSet):

    queryset = Imobiliario.objects.all()
    serializer_class = ImobiliarioSerializer

    search_fields = [
        'nome',
        'tipo',
        'endereco__logradouro',
        'endereco__bairro',
        'endereco__cidade',
        'endereco__estado',
        'endereco__cep'
    ]


class PatrimonioDaFilialListView(APIView):
    permission_classes = [IsAuthenticated, IsEmployeeOfThisBranchOrManager]

    @extend_schema(responses=PatrimonioConsolidadoSerializer)
    def get(self, request, empresa_pk=None, filial_pk=None):
        veiculos = Veiculo.objects.filter(filial_associada_id=filial_pk)
        utilitarios = Utilitario.objects.filter(filial_associada_id=filial_pk)
        imobiliarios = Imobiliario.objects.filter(filial_associada_id=filial_pk)

        veiculos_data = VeiculoSerializer(veiculos, many=True).data
        utilitarios_data = UtilitarioSerializer(utilitarios, many=True).data
        imobiliarios_data = ImobiliarioSerializer(imobiliarios, many=True).data

        resposta_consolidada = {
            'veiculos': veiculos_data,
            'utilitarios': utilitarios_data,
            'imobiliarios': imobiliarios_data
        }

        return Response(resposta_consolidada)
