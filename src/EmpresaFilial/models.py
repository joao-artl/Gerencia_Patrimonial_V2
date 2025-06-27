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
        if self.telefone:
            filial_telefone = Filial.objects.filter(telefone=self.telefone).exists()
            
            if filial_telefone:
                raise ValidationError({
                    'telefone': 'Este telefone já está em uso por uma Filial.'
                })
    
        if self.cnpj:
            filial_cnpj = Filial.objects.filter(cnpj=self.cnpj).exists()

            if filial_cnpj:
                raise ValidationError({
                    'cnpj': 'Este CNPJ já está em uso por uma Filial.'
                })
    
        if self.email:
            usuario = apps.get_model('Usuarios', 'Usuario')
            usuario_email = usuario.objects.filter(email=self.email).exists()
            filial_email = Filial.objects.filter(email=self.email).exists()
            
            if usuario_email or filial_email:
                raise ValidationError({
                    'email': 'Este email já está em uso por um Usuário ou Filial.'
                })
            
        if self.endereco:
            imobiliario = apps.get_model('Patrimonio', 'Imobiliario')
            filial_endereco = Filial.objects.filter(endereco=self.endereco).exists()
            imobiliario_endereco = imobiliario.objects.filter(endereco=self.endereco).exists()
            
            if filial_endereco or imobiliario_endereco:
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
        if self.telefone:
            empresa_telefone = Empresa.objects.filter(telefone=self.telefone).exists()
            
            if empresa_telefone:
                raise ValidationError({
                    'telefone': 'Este telefone já está em uso por uma Empresa.'
                })
    
        if self.cnpj:
            empresa_cnpj = Empresa.objects.filter(cnpj=self.cnpj).exists()
            
            if empresa_cnpj:
                raise ValidationError({
                    'cnpj': 'Este CNPJ já está em uso por uma Empresa.'
                })
    
        if self.email:
            usuario = apps.get_model('Usuarios', 'Usuario')
            usuario_email = usuario.objects.filter(email=self.email).exists()
            empresa_email = Empresa.objects.filter(email=self.email).exists()
            
            if usuario_email or empresa_email:
                raise ValidationError({
                    'email': 'Este email já está em uso por um Usuário ou Empresa.'
                })
            
        if self.endereco:
            imobiliario = apps.get_model('Patrimonio', 'Imobiliario')
            empresa_endereco = Empresa.objects.filter(endereco=self.endereco).exists()
            imobiliario_endereco = imobiliario.objects.filter(endereco=self.endereco).exists()

            if empresa_endereco or imobiliario_endereco:
                raise ValidationError({
                    'endereco': 'Este endereço já está em uso por uma Empresa ou Imobiliário.'
                })
            
        super().clean()

    class Meta:
        verbose_name="Filial"
        verbose_name_plural="Filiais"
    
    def __str__(self):
        return self.nome