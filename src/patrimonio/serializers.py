from rest_framework import serializers
from .models import Imobiliario, Utilitario, Veiculo

class ImobiliarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imobiliario
        fields = '__all__'

class UtilitarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilitario
        fields = '__all__'

class VeiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Veiculo
        fields = '__all__'
