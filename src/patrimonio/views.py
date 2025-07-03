from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from usuarios.permissions import IsEmployeeOfThisBranchOrManager 
from .models import Imobiliario, Utilitario, Veiculo
from .serializers import ImobiliarioSerializer, UtilitarioSerializer, VeiculoSerializer
from itertools import chain

class BasePatrimonioViewSet(viewsets.ModelViewSet):
    
    permission_classes = [IsAuthenticated, IsEmployeeOfThisBranchOrManager]
    
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

class PatrimonioDaFilialListView(APIView):
    permission_classes = [IsAuthenticated, IsEmployeeOfThisBranchOrManager]

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