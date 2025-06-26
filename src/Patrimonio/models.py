from django.db import models
from django.core.exceptions import ValidationError


class ItemDePatrimonio(models.Model):
    nome = models.CharField(max_length=40,verbose_name="Nome")
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor")
    quantidade = models.IntegerField(verbose_name="Quantidade")
    filial_associada = models.ForeignKey('EmpresaFilial.Filial', on_delete=models.CASCADE, related_name='%(class)s_associado')

    class Meta:
        abstract = True

    def __str__(self):
        return self.nome
    
class Imobiliario(ItemDePatrimonio):
    area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Área")
    tipo = models.CharField(max_length=15,verbose_name="Tipo")
    endereco = models.OneToOneField('EmpresaFilial.Endereco', on_delete=models.CASCADE, verbose_name="Endereço")
    quantidade = models.IntegerField(default=1) # Define 1 como padrão para quantidade do Imobiliario

    class Meta:
        verbose_name="Imobiliario"
        verbose_name_plural="Imobiliarios"

    def clean(self):
        if self.quantidade != 1:
            raise ValidationError({'quantidade': 'A quantidade para um imóvel deve ser sempre 1.'})

    def save(self, *args, **kwargs):
        self.full_clean() 
        super().save(*args, **kwargs)

class Utilitario(ItemDePatrimonio):
    descricao = models.CharField(max_length=50,verbose_name="Descrição")
    funcao = models.CharField(max_length=20,verbose_name="Função")

    class Meta:
        verbose_name="Utilitario"
        verbose_name_plural="Utilitarios"
    

class Veiculo(ItemDePatrimonio):
    cor = models.CharField(max_length=15,verbose_name="Cor")
    modelo = models.CharField(max_length=25,verbose_name="Modelo")
    fabricante = models.CharField(max_length=25,verbose_name="Fabricante")

    class Meta:
        verbose_name="Veiculo"
        verbose_name_plural="Veiculos"