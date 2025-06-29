from rest_framework import serializers
from .models import Endereco, Empresa, Filial
from django.contrib.auth.hashers import make_password

class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = '__all__'

class FilialSerializer(serializers.ModelSerializer):

    endereco = EnderecoSerializer()
    empresa_matriz = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Filial
        fields = ['id', 'cnpj', 'nome', 'email', 'telefone', 'senha', 'endereco', 'empresa_matriz']
        extra_kwargs = {
            'senha': {'write_only': True}
        }

    def create(self, validated_data):
        endereco_data = validated_data.pop('endereco')
        validated_data['senha'] = make_password(validated_data['senha'])
        endereco = Endereco.objects.create(**endereco_data)
        filial = Filial.objects.create(endereco=endereco, **validated_data)
        return filial

    def update(self, instance, validated_data):
        if 'endereco' in validated_data:
            endereco_data = validated_data.pop('endereco')
            endereco_instance = instance.endereco
            for attr, value in endereco_data.items():
                setattr(endereco_instance, attr, value)
            endereco_instance.save()
            
        if 'senha' in validated_data:
            validated_data['senha'] = make_password(validated_data['senha'])
            
        return super().update(instance, validated_data)

class EmpresaSerializer(serializers.ModelSerializer):
    endereco = EnderecoSerializer()
    
    class FilialInfoSerializer(serializers.ModelSerializer):
        class Meta:
            model = Filial
            fields = ['id', 'nome', 'email', 'telefone'] 
            
    filiais = FilialInfoSerializer(many=True, read_only=True)

    class Meta:
        model = Empresa
        fields = ['id', 'cnpj', 'nome', 'email', 'telefone', 'senha', 'endereco', 'filiais']
        extra_kwargs = {
            'senha': {'write_only': True}
        }

    def create(self, validated_data):
        endereco_data = validated_data.pop('endereco')
        validated_data.pop('filiais', None)
        validated_data['senha'] = make_password(validated_data['senha'])
        endereco = Endereco.objects.create(**endereco_data)
        empresa = Empresa.objects.create(endereco=endereco, **validated_data)
        return empresa

    def update(self, instance, validated_data):
        validated_data.pop('filiais', None) 
        if 'endereco' in validated_data:
            endereco_data = validated_data.pop('endereco')
            endereco_instance = instance.endereco
            for attr, value in endereco_data.items():
                setattr(endereco_instance, attr, value)
            endereco_instance.save()
            
        if 'senha' in validated_data:
            validated_data['senha'] = make_password(validated_data['senha'])
            
        return super().update(instance, validated_data)