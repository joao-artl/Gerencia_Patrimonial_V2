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

    senha = serializers.CharField(
        source='password',
        write_only=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = Filial
        fields = ['id',
                  'cnpj',
                  'nome',
                  'email',
                  'telefone',
                  'senha',
                  'endereco',
                  'empresa_matriz']

    def create(self, validated_data):
        endereco_data = validated_data.pop('endereco')

        validated_data['password'] = make_password(validated_data['password'])

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

        if 'password' in validated_data:
            password_data = validated_data.pop('password')
            instance.password = make_password(password_data)

        return super().update(instance, validated_data)


class EmpresaSerializer(serializers.ModelSerializer):
    endereco = EnderecoSerializer()

    class FilialInfoSerializer(serializers.ModelSerializer):
        class Meta:
            model = Filial
            fields = ['id', 'nome', 'email', 'telefone']

    filiais = FilialInfoSerializer(many=True, read_only=True)

    senha = serializers.CharField(
        source='password',
        write_only=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = Empresa
        fields = ['id', 'cnpj', 'nome', 'email', 'telefone', 'senha', 'endereco', 'filiais']

    def create(self, validated_data):
        endereco_data = validated_data.pop('endereco')
        validated_data.pop('filiais', None)

        validated_data['password'] = make_password(validated_data['password'])

        endereco = Endereco.objects.create(**endereco_data)
        empresa = Empresa.objects.create(endereco=endereco, **validated_data)
        return empresa

    def update(self, instance, validated_data):
        if 'endereco' in validated_data:
            endereco_data = validated_data.pop('endereco')
            endereco_serializer = EnderecoSerializer(instance.endereco,
                                                     data=endereco_data,
                                                     partial=True)
            if endereco_serializer.is_valid(raise_exception=True):
                endereco_serializer.save()

        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance, validated_data)


class JoinEmpresaSerializer(serializers.Serializer):
    senha_da_empresa = serializers.CharField(write_only=True)

    class Meta:
        fields = ['senha_da_empresa']


class JoinByEmailSerializer(serializers.Serializer):

    email = serializers.EmailField()
    senha = serializers.CharField(write_only=True)

    class Meta:
        fields = ['email', 'senha']
