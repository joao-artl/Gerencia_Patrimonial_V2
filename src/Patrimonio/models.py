from django.db import models
from EmpresaFilial.models import Endereco



class ItemDePatrimonio(models.Model):
    nome = models.CharField(max_length=40,verbose_name="Nome")
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor")
    quantidade = models.IntegerField(verbose_name="Quantidade")

    class Meta:
        abstract = True

    def __str__(self):
        return self.nome
    
class Imobiliario(ItemDePatrimonio):
    area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Área")
    tipo = models.CharField(max_length=15,verbose_name="Tipo")
    endereco = models.OneToOneField(Endereco, on_delete=models.CASCADE, verbose_name="Endereço")

class Utilitario(ItemDePatrimonio):
    descricao = models.CharField(max_length=50,verbose_name="Descrição")
    funcao = models.CharField(max_length=20,verbose_name="Função")

class Veiculo(ItemDePatrimonio):
    cor = models.CharField(max_length=15,verbose_name="Cor")
    modelo = models.CharField(max_length=25,verbose_name="Modelo")
    fabricante = models.CharField(max_length=25,verbose_name="Fabricante")