from django.db import models
from django.core.exceptions import ValidationError
from django.apps import apps
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UsuarioManager(BaseUserManager):

    def create_user(self, email, nome, cpf, tipo_usuario, password=None, **extra_fields):
        if not email:
            raise ValueError('O campo de Email é obrigatório')

        email = self.normalize_email(email)
        user = self.model(email=email,
                          nome=nome,
                          cpf=cpf,
                          tipo_usuario=tipo_usuario,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, nome, cpf, tipo_usuario, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser deve ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser deve ter is_superuser=True.')

        return self.create_user(email, nome, cpf, tipo_usuario, password, **extra_fields)


TIPO_USUARIO_CHOICES = [
    ('GESTOR', 'Gestor'),
    ('FUNCIONARIO', 'Funcionário'),
]


class Usuario(AbstractBaseUser, PermissionsMixin):
    cpf = models.CharField(max_length=14, unique=True, verbose_name="CPF")
    email = models.EmailField(max_length=255, unique=True, verbose_name="E-mail")
    nome = models.CharField(max_length=255, verbose_name="Nome Completo")
    tipo_usuario = models.CharField(max_length=20,
                                    choices=TIPO_USUARIO_CHOICES,
                                    verbose_name="Tipo de Usuário")
    filial_associada = models.ForeignKey('empresa_filial.Filial',
                                         on_delete=models.CASCADE,
                                         null=True,
                                         blank=True,
                                         related_name='funcionarios')
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    is_staff = models.BooleanField(default=False, verbose_name="Membro da Equipe")
    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome', 'cpf', 'tipo_usuario']

    class Meta:

        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return self.email

    def clean(self):

        super().clean()
        if self.email:

            if (
                self.__class__._default_manager
                .filter(email=self.email)
                .exclude(pk=self.pk)
                .exists()
            ):
                pass

            empresa = apps.get_model('empresa_filial', 'Empresa')
            filial = apps.get_model('empresa_filial', 'Filial')
            empresa_email = empresa.objects.filter(email=self.email).exists()
            filial_email = filial.objects.filter(email=self.email).exists()

            if empresa_email or filial_email:
                raise ValidationError({
                    'email': 'Este email já está em uso por uma Empresa ou Filial.'
                })
