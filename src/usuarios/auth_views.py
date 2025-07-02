from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, serializers
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['nome'] = user.nome
        token['tipo_usuario'] = user.tipo_usuario
        return token

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField()
        self.fields['password'] = serializers.CharField(
            style={'input_type': 'password'},
            trim_whitespace=False
        )
    @property
    def username_field(self):
        return 'email'

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer