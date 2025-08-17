from rest_framework import serializers
from django.contrib.auth.hashers import check_password
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

    senha = serializers.CharField(
        source='password',
        write_only=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = Usuario
        fields = ['id',
                  'cpf',
                  'email',
                  'nome',
                  'senha',
                  'tipo_usuario',
                  'filial_associada',
                  'senha_da_filial']

    def validate(self, data):
        tipo_usuario = data.get('tipo_usuario')
        filial_associada_obj = data.get('filial_associada')

        if tipo_usuario == 'FUNCIONARIO':
            if not filial_associada_obj:
                raise serializers.ValidationError(
                    {
                        "filial_associada": (
                            "Para criar um 'Funcionário', "
                            "a filial associada é obrigatória."
                        )
                    }
                )

            senha_filial_submetida = data.get('senha_da_filial')
            if not senha_filial_submetida:
                raise serializers.ValidationError({
                    "senha_da_filial": (
                        "A senha da filial é obrigatória para cadastrar um funcionário."
                    )
                })

            if not check_password(senha_filial_submetida, filial_associada_obj.password):
                raise serializers.ValidationError({
                    "senha_da_filial": (
                        "A senha da filial está incorreta."
                    )
                })

        if tipo_usuario == 'GESTOR' and filial_associada_obj:
            raise serializers.ValidationError(
                {
                    "filial_associada": (
                        "Para o tipo 'Gestor', a filial associada deve ser nula."
                    )
                }
            )

        data.pop('senha_da_filial', None)
        return data

    def create(self, validated_data):
        return Usuario.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance, validated_data)


class GerenciaSerializer(serializers.ModelSerializer):

    usuario_email = serializers.EmailField(write_only=True)
    senha_da_empresa = serializers.CharField(write_only=True)
    usuario = UsuarioSerializer(read_only=True)

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
        if not check_password(senha_empresa_submetida, empresa.password):
            raise serializers.ValidationError({"senha_da_empresa":
                                               "A senha da empresa está incorreta."})

        try:
            Usuario.objects.get(email=data['usuario_email'], tipo_usuario='GESTOR')
        except Usuario.DoesNotExist:
            raise serializers.ValidationError({"usuario_email":
                                               "Nenhum gestor encontrado com este email."})

        data.pop('senha_da_empresa')
        return data

    def create(self, validated_data):

        usuario_obj = Usuario.objects.get(email=validated_data['usuario_email'])
        empresa_id_da_url = validated_data['empresa_id']
        gerencia = Gerencia.objects.create(
            usuario=usuario_obj,
            empresa_id=empresa_id_da_url
        )
        return gerencia
