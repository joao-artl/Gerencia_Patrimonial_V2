from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Usuario
from empresa_filial.models import Gerencia, Filial


class UsuarioSerializer(serializers.ModelSerializer):
    filial_associada = serializers.PrimaryKeyRelatedField(
        queryset=Filial.objects.all(), 
        required=False, 
        allow_null=True,
        label="ID da Filial Associada"
    )

    class Meta:
        model = Usuario
        fields = ['id', 'cpf', 'email', 'nome', 'senha', 'tipo_usuario', 'filial_associada']
        extra_kwargs = {
            'senha': {'write_only': True} 
        }

    def validate(self, data):
        tipo_usuario = data.get('tipo_usuario')
        filial_associada = data.get('filial_associada')

        if tipo_usuario == 'FUNCIONARIO' and not filial_associada:
            raise serializers.ValidationError({
                "filial_associada": "Para o tipo 'Funcionário', a filial associada é obrigatória."
            })
        
        if tipo_usuario == 'GESTOR' and filial_associada:
            raise serializers.ValidationError({
                "filial_associada": "Para o tipo 'Gestor', a filial associada deve ser nula."
            })

        return data

    def create(self, validated_data):
        validated_data['senha'] = make_password(validated_data['senha'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'senha' in validated_data:
            validated_data['senha'] = make_password(validated_data['senha'])
        return super().update(instance, validated_data)


class GerenciaSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)
    usuario_id = serializers.PrimaryKeyRelatedField(
        queryset=Usuario.objects.filter(tipo_usuario='GESTOR'),
        source='usuario',
        write_only=True,
        label="E-mail do Gestor"
    )

    class Meta:
        model = Gerencia
        fields = ['id', 'usuario', 'empresa', 'usuario_id']
        read_only_fields = ('empresa',) 