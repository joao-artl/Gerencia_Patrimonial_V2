from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, serializers
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['email'] = self.fields.pop(self.username_field)
        self.fields['senha'] = self.fields.pop('password')
        self.fields['senha'].style = {'input_type': 'password'}
        self.fields['senha'].trim_whitespace = False

    def validate(self, attrs):
        
        attrs['password'] = attrs.pop('senha')
        
        data = super().validate(attrs)
        data.update({
            'nome': self.user.nome,
            'tipo_usuario': self.user.tipo_usuario
        })

        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer