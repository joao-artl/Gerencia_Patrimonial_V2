from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairSerializer(serializers.Serializer):

    email = serializers.EmailField()
    senha = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True 
    )

    def validate(self, attrs):

        email = attrs.get('email')
        password = attrs.get('senha') 

        if not email or not password:
            raise serializers.ValidationError('Por favor, forneça email e senha.', code='authorization')

        request = self.context.get('request')
        user = authenticate(request=request, username=email, password=password)

        if not user:
            raise serializers.ValidationError('Nenhuma conta ativa encontrada com as credenciais fornecidas.', code='authorization')

        refresh = RefreshToken.for_user(user)
        refresh.access_token['nome'] = user.nome
        refresh.access_token['tipo_usuario'] = user.tipo_usuario
        
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'usuario': {
                'id': user.id,
                'email': user.email,
                'nome': user.nome,
                'tipo_usuario': user.tipo_usuario
            }
        }
        
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer