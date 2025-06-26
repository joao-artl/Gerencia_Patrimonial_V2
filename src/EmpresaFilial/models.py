from django.db import models


class Endereco(models.Model):
    cep = models.CharField(max_length=8, verbose_name="CEP")
    estado = models.CharField(max_length=2, verbose_name="Estado")
    cidade = models.CharField(max_length=30, verbose_name="Cidade")
    bairro = models.CharField(max_length=20, verbose_name="Bairro")
    complemento = models.CharField(max_length=20, verbose_name="Complemento")
    numero = models.CharField(max_length=7, verbose_name="Número")

    def __str__(self):
        return f"{self.numero}, {self.bairro}, {self.cidade}/{self.estado} - {self.cep}"