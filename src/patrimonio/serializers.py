from rest_framework import serializers
from .models import Imobiliario, Utilitario, Veiculo
from empresa_filial.serializers import EnderecoSerializer 
from empresa_filial.models import Endereco

class VeiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Veiculo
        exclude = ('filial_associada',)

class UtilitarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilitario
        exclude = ('filial_associada',)

class ImobiliarioSerializer(serializers.ModelSerializer):
    endereco = EnderecoSerializer()

    class Meta:
        model = Imobiliario
        exclude = ('filial_associada',)
        read_only_fields = ('quantidade',)

    def create(self, validated_data):
        endereco_data = validated_data.pop('endereco')
        endereco = Endereco.objects.create(**endereco_data)
        imobiliario = Imobiliario.objects.create(endereco=endereco, **validated_data)
        return imobiliario

    def update(self, instance, validated_data):
        if 'endereco' in validated_data:
            endereco_data = validated_data.pop('endereco')
            endereco_instance = instance.endereco
            for attr, value in endereco_data.items():
                setattr(endereco_instance, attr, value)
            endereco_instance.save()
            
        return super().update(instance, validated_data)