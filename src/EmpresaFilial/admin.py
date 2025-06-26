from django.contrib import admin
from .models import Endereco, Empresa, Filial

admin.site.register(Endereco)
admin.site.register(Empresa)
admin.site.register(Filial)