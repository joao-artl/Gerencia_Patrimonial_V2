from django.shortcuts import render, get_object_or_404
from .models import Empresa, Filial
from django.apps import apps

def listar_filiais(request, empresa_id):
    empresa = get_object_or_404(Empresa, id=empresa_id)
    filiais = empresa.filiais.all()
    return render(request, 'listar_filiais.html', {'empresa': empresa, 'filiais': filiais})

def listar_gestores(request, empresa_id):
    empresa = get_object_or_404(Empresa, id=empresa_id)
    gestores = empresa.gestores.all()
    return render(request, 'listar_gestores.html', {'empresa': empresa, 'gestores': gestores})

def listar_patrimonios_empresa(request, empresa_id):
    empresa = get_object_or_404(Empresa, id=empresa_id)

    Imobiliario = apps.get_model('Patrimonio', 'Imobiliario')
    Utilitario = apps.get_model('Patrimonio', 'Utilitario')
    Veiculo = apps.get_model('Patrimonio', 'Veiculo')

    resultado = []
    for filial in empresa.filiais.all(): 
        imobiliarios = Imobiliario.objects.filter(filial=filial)
        utilitarios = Utilitario.objects.filter(filial=filial)
        veiculos = Veiculo.objects.filter(filial=filial)

        patrimonios = [
            {'nome': i.nome, 'tipo': 'Imobiliário'} for i in imobiliarios
        ] + [
            {'nome': u.nome, 'tipo': 'Utilitário'} for u in utilitarios
        ] + [
            {'nome': v.nome, 'tipo': 'Veículo'} for v in veiculos
        ]

        resultado.append({
            'filial': filial,
            'patrimonios': patrimonios
        })

    return render(request, 'listar_patrimonios_empresa.html', {
        'empresa': empresa,
        'filiais_com_patrimonios': resultado
    })

def listar_funcionarios(request, filial_id):
    filial = get_object_or_404(Filial, id=filial_id)
    funcionarios = filial.funcionarios.all()
    return render(request, 'listar_filiais.html', {'filial': filial, 'funcionarios': funcionarios})

def listar_patrimonios_filial(request, filial_id):
    filial = get_object_or_404(Filial, id=filial_id)

    Imobiliario = apps.get_model('Patrimonio', 'Imobiliario')
    Utilitario = apps.get_model('Patrimonio', 'Utilitario')
    Veiculo = apps.get_model('Patrimonio', 'Veiculo')

    imobiliario_patrimonio = Imobiliario.objects.filter(filial=filial)
    utilitario_patrimonio = Utilitario.objects.filter(filial=filial)
    veiculo_patrimonio = Veiculo.objects.filter(filial=filial)

    tipo_patrimonio = [
        {'nome': i.nome, 'tipo': 'Imobiliário'} for i in imobiliario_patrimonio
    ] + [
        {'nome': u.nome, 'tipo': 'Utilitário'} for u in utilitario_patrimonio
    ] + [
        {'nome': v.nome, 'tipo': 'Veículo'} for v in veiculo_patrimonio
    ]

    return render(request, 'listar_patrimonios_filial.html', {
        'filial': filial,
        'patrimonios': tipo_patrimonio
    })

