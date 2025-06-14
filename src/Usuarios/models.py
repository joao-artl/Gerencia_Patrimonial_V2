from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


TIPO_USUARIO_CHOICES = [
    ('GESTOR', 'Gestor'),
    ('FUNCIONARIO', 'Funcionário'),
]

class Usuario(models.Model):
    cpf = models.CharField(max_length=14, unique=True, verbose_name="CPF")
    email = models.EmailField(max_length=255, verbose_name="E-mail")
    nome = models.CharField(max_length=255, verbose_name="Nome Completo")
    senha = models.CharField(max_length=128, verbose_name="Senha")
    tipo_usuario = models.CharField(
        max_length=20,
        choices=TIPO_USUARIO_CHOICES,
        verbose_name="Tipo de Usuário"
    )
    def __str__(self):
        return self.nome