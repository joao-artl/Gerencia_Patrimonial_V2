from django.shortcuts import render, get_object_or_404
from .models import Usuario

def listar_empresa(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    empresa_administrada = usuario.empresa_administrada.all()
    return render(request, 'listar_empresa_administrada.html', {'usuario': usuario, 'empresa_administrada': empresa_administrada})
