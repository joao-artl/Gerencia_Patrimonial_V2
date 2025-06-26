from django.db import models


class Endereco(models.Model):
    cep = models.CharField(max_length=8, verbose_name="CEP")
    estado = models.CharField(max_length=2, verbose_name="Estado")
    cidade = models.CharField(max_length=30, verbose_name="Cidade")
    bairro = models.CharField(max_length=20, verbose_name="Bairro")
    logradouro = models.CharField(max_length=120, verbose_name="Logradouro")
    complemento = models.CharField(max_length=60, blank=True, null=True, verbose_name="Complemento")
    numero = models.CharField(max_length=10, blank=True, null=True, verbose_name="Número")

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