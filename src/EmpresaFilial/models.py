from django.db import models
from django.core.exceptions import ValidationError
from django.apps import apps


class Endereco(models.Model):
    cep = models.CharField(max_length=8, verbose_name="CEP")
    estado = models.CharField(max_length=2, verbose_name="Estado")
    cidade = models.CharField(max_length=30, verbose_name="Cidade")
    bairro = models.CharField(max_length=20, verbose_name="Bairro")
    logradouro = models.CharField(max_length=120, verbose_name="Logradouro")
    complemento = models.CharField(max_length=60, blank=True, null=True, verbose_name="Complemento (Opcional)")
    numero = models.CharField(max_length=10, blank=True, null=True, verbose_name="Número (Opcional)")

    class Meta:
        unique_together = (('logradouro', 'numero', 'complemento', 'bairro', 'cidade', 'estado', 'cep'),)
        verbose_name="Endereço"
        verbose_name_plural="Endereços"

    def __str__(self):
        primeira_parte_elementos = []
        primeira_parte_elementos.append(self.logradouro)
        if self.numero:
            primeira_parte_elementos.append(self.numero)
        if self.complemento:
            primeira_parte_elementos.append(self.complemento)
        primeira_parte_str = ", ".join(primeira_parte_elementos)
        endereco_completo_elementos = [primeira_parte_str]
        endereco_completo_elementos.append(self.bairro)
        endereco_completo_elementos.append(f"{self.cidade}/{self.estado}")
        endereco_completo_elementos.append(self.cep)
        return ", ".join(filter(None, endereco_completo_elementos))

class Empresa(models.Model):
    cnpj = models.CharField(max_length=14, unique=True, verbose_name="CNPJ")
    nome = models.CharField(max_length=255, verbose_name="Nome")
    senha = models.CharField(max_length=128, verbose_name="Senha")
    email = models.EmailField(max_length=255, unique=True, verbose_name="E-mail")
    telefone = models.CharField(max_length=11, unique=True, verbose_name="Telefone")
    endereco = models.OneToOneField(Endereco, on_delete=models.CASCADE, verbose_name="Endereço")
    gestores = models.ManyToManyField('Usuarios.Usuario', through='Gerencia', related_name='empresa_administrada')

    def clean(self):
        if self.endereco:
            Imobiliario = apps.get_model('Patrimonio', 'Imobiliario')
            filial_usa = Filial.objects.filter(endereco=self.endereco).exists()
            imobiliario_usa = Imobiliario.objects.filter(endereco=self.endereco).exists()
            
            if filial_usa or imobiliario_usa:
                raise ValidationError({
                    'endereco': 'Este endereço já está em uso por uma Filial ou Imobiliário.'
                })
        super().clean()

    class Meta:
        verbose_name="Empresa"
        verbose_name_plural="Empresas"
    
    def __str__(self):
        return self.nome
    

class Gerencia(models.Model):
    usuario = models.ForeignKey('Usuarios.Usuario', on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE) 

    class Meta:
        unique_together = ('usuario', 'empresa')

    def __str__(self):
        return f"{self.usuario.nome} na empresa {self.empresa.nome}"

class Filial(models.Model):
    cnpj = models.CharField(max_length=14, unique=True, verbose_name="CNPJ")
    nome = models.CharField(max_length=255, verbose_name="Nome")
    senha = models.CharField(max_length=128, verbose_name="Senha")
    email = models.EmailField(max_length=255, unique=True, verbose_name="E-mail")
    telefone = models.CharField(max_length=11, unique=True, verbose_name="Telefone")
    endereco = models.OneToOneField(Endereco, on_delete=models.CASCADE, verbose_name="Endereço")
    empresa_matriz = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='filiais')

    def clean(self):
        if self.endereco:
            Imobiliario = apps.get_model('Patrimonio', 'Imobiliario')
            empresa_usa = Empresa.objects.filter(endereco=self.endereco).exists()
            imobiliario_usa = Imobiliario.objects.filter(endereco=self.endereco).exists()

            if empresa_usa or imobiliario_usa:
                raise ValidationError({
                    'endereco': 'Este endereço já está em uso por uma Empresa ou Imobiliário.'
                })
        super().clean()

    class Meta:
        verbose_name="Filial"
        verbose_name_plural="Filiais"
    
    def __str__(self):
        return self.nome