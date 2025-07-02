from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from .models import Usuario
from empresa_filial.models import Gerencia, Filial, Empresa


class UsuarioSerializer(serializers.ModelSerializer):
    filial_associada = serializers.PrimaryKeyRelatedField(
        queryset=Filial.objects.all(),
        required=False, 
        allow_null=True,
        label="ID da Filial Associada"
    )

    senha_da_filial = serializers.CharField(
        write_only=True,
        required=False,
        label="Senha da Filial"
    )

    class Meta:
        model = Usuario
        fields = ['id', 'cpf', 'email', 'nome', 'senha', 'tipo_usuario', 'filial_associada', 'senha_da_filial']
        extra_kwargs = {
            'senha': {'write_only': True}
        }

    def validate(self, data):
        tipo_usuario = data.get('tipo_usuario')
        filial_associada_obj = data.get('filial_associada')

        if tipo_usuario == 'FUNCIONARIO':
            if not filial_associada_obj:
                raise serializers.ValidationError({
                    "filial_associada": "Para o tipo 'Funcionário', a filial associada é obrigatória."
                })
            
            senha_filial_submetida = data.get('senha_da_filial')
            if not senha_filial_submetida:
                raise serializers.ValidationError({
                    "senha_da_filial": "A senha da filial é obrigatória para cadastrar um funcionário."
                })

            if not check_password(senha_filial_submetida, filial_associada_obj.senha):
                raise serializers.ValidationError({
                    "senha_da_filial": "A senha da filial está incorreta."
                })

        if tipo_usuario == 'GESTOR' and filial_associada_obj:
            raise serializers.ValidationError({
                "filial_associada": "Para o tipo 'Gestor', a filial associada deve ser nula."
            })
        
        data.pop('senha_da_filial', None)
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
    usuario_email = serializers.PrimaryKeyRelatedField(
        queryset=Usuario.objects.filter(tipo_usuario='GESTOR'),
        source='usuario',
        write_only=True,
        label="Email do Gestor"
    )
    
    senha_da_empresa = serializers.CharField(
        write_only=True,
        label="Senha da Empresa"
    )

    class Meta:
        model = Gerencia
        fields = ['id', 'usuario', 'empresa', 'usuario_email', 'senha_da_empresa']
        read_only_fields = ('empresa',)

    def validate(self, data):
        view = self.context.get('view')
        empresa_pk = view.kwargs.get('empresa_pk')
        try:
            empresa = Empresa.objects.get(pk=empresa_pk)
        except Empresa.DoesNotExist:
            raise serializers.ValidationError("A empresa especificada não existe.")

        senha_empresa_submetida = data.get('senha_da_empresa')

        if not check_password(senha_empresa_submetida, empresa.senha):
            raise serializers.ValidationError({
                "senha_da_empresa": "A senha da empresa está incorreta."
            })
        
        data.pop('senha_da_empresa')

        return data



