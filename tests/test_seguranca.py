import pytest
import requests
import os
import random


@pytest.fixture(scope="module")
def api_url():
    """Fornece a URL base da API."""
    api_host = os.getenv("API_HOST", "localhost")
    return f"http://{api_host}:8000/api"


@pytest.fixture
def cenario_com_funcionario_logado(api_url):
    """
    Cria um cenário com um funcionário logado em uma empresa/filial.
    """

    gestor_data = {"email": f"gestor.l6.{random.randint(1000,9999)}@empresa.com",
                   "senha": "123", "cpf": f"111{random.randint(10000,99999)}",
                   "nome": "G", "tipo_usuario": "GESTOR"}
    requests.post(f"{api_url}/usuarios/", json=gestor_data)
    login_response = requests.post(f"{api_url}/token/",
                                   json={
                                       "email": gestor_data['email'],
                                       "senha": gestor_data['senha']})
    token_gestor = login_response.json()['access']
    headers_gestor = {'Authorization': f'Bearer {token_gestor}'}

    empresa_data = {
        "cnpj": f"111{random.randint(10000000,99999999)}",
        "nome": "Empresa L6",
        "email": f"contato{random.randint(1000,9999)}@l6.com",
        "telefone": f"1191111{random.randint(1000,9999)}",
        "senha": "senha-empresa",
        "endereco": {
            "cep": "1",
            "estado": "a",
            "cidade": "b",
            "bairro": "c",
            "logradouro": "d",
            "numero": "e"
        }
    }
    empresa_response = requests.post(f"{api_url}/empresas/",
                                     headers=headers_gestor,
                                     json=empresa_data)
    id_empresa = empresa_response.json()['id']

    filial_data = {
        "cnpj": f"222{random.randint(10000000,99999999)}",
        "nome": "Filial Segura",
        "senha": "senha-filial",
        "email": f"contato{random.randint(1000,9999)}@fs.com",
        "telefone": f"1192222{random.randint(1000,9999)}",
        "endereco": {
            "cep": "2",
            "estado": "b",
            "cidade": "c",
            "bairro": "d",
            "logradouro": "e",
            "numero": "f"
        }
    }
    filial_response = requests.post(f"{api_url}/empresas/{id_empresa}/filiais/",
                                    headers=headers_gestor,
                                    json=filial_data)
    id_filial = filial_response.json()['id']
    funcionario_data = {
        "cpf": f"444{random.randint(10000,99999)}",
        "email": f"func.l6.{random.randint(1000,9999)}@empresa.com",
        "nome": "Funcionario L6",
        "senha": "senhaDoFuncionario",
        "tipo_usuario": "FUNCIONARIO",
        "filial_associada": id_filial,
        "senha_da_filial": "senha-filial"
    }
    requests.post(f"{api_url}/usuarios/", headers=headers_gestor, json=funcionario_data)

    login_func_response = requests.post(f"{api_url}/token/",
                                        json={"email": funcionario_data['email'],
                                              "senha": funcionario_data['senha']})
    token_funcionario = login_func_response.json()['access']

    return {"token_funcionario": token_funcionario, "id_empresa": id_empresa}


@pytest.fixture
def cenario_duas_empresas(api_url):
    """
    Cria um cenário com duas empresas independentes (A e B).
    - Empresa A tem Gestor A.
    - Empresa B tem Gestor B, uma filial e um funcionário.
    """

    gestor_a_data = {"email": f"gestor.a.{random.randint(1000,9999)}@empresa.com",
                     "senha": "123", "cpf": f"333{random.randint(10000,99999)}",
                     "nome": "GA", "tipo_usuario": "GESTOR"}
    requests.post(f"{api_url}/usuarios/", json=gestor_a_data)
    login_a_response = requests.post(f"{api_url}/token/",
                                     json={"email": gestor_a_data['email'],
                                           "senha": gestor_a_data['senha']})
    token_gestor_a = login_a_response.json()['access']
    headers_gestor_a = {'Authorization': f'Bearer {token_gestor_a}'}
    empresa_a_data = {
        "cnpj": f"333{random.randint(10000000,99999999)}",
        "nome": "Empresa A",
        "email": f"contato{random.randint(1000,9999)}@a.com",
        "telefone": f"1193333{random.randint(1000,9999)}",
        "senha": "s",
        "endereco": {
            "cep": "3",
            "estado": "c",
            "cidade": "d",
            "bairro": "e",
            "logradouro": "f",
            "numero": "g"
        }
    }
    requests.post(f"{api_url}/empresas/", headers=headers_gestor_a, json=empresa_a_data)

    gestor_b_data = {"email": f"gestor.b.{random.randint(1000,9999)}@empresa.com",
                     "senha": "123", "cpf": f"444{random.randint(10000,99999)}",
                     "nome": "GB", "tipo_usuario": "GESTOR"}
    requests.post(f"{api_url}/usuarios/", json=gestor_b_data)
    login_b_response = requests.post(f"{api_url}/token/",
                                     json={"email": gestor_b_data['email'],
                                           "senha": gestor_b_data['senha']})
    token_gestor_b = login_b_response.json()['access']
    headers_gestor_b = {'Authorization': f'Bearer {token_gestor_b}'}
    empresa_b_data = {
        "cnpj": f"444{random.randint(10000000,99999999)}",
        "nome": "Empresa B",
        "email": f"contato{random.randint(1000,9999)}@b.com",
        "telefone": f"1194444{random.randint(1000,9999)}",
        "senha": "s",
        "endereco": {
            "cep": "4",
            "estado": "d",
            "cidade": "e",
            "bairro": "f",
            "logradouro": "g",
            "numero": "h"
        }
    }

    empresa_b_response = requests.post(f"{api_url}/empresas/",
                                       headers=headers_gestor_b,
                                       json=empresa_b_data)
    id_empresa_b = empresa_b_response.json()['id']
    filial_b_data = {
        "cnpj": f"555{random.randint(10000000,99999999)}",
        "nome": "Filial B",
        "senha": "s",
        "email": f"b{random.randint(1000,9999)}@b.com",
        "telefone": f"1195555{random.randint(1000,9999)}",
        "endereco": {
            "cep": "5",
            "estado": "e",
            "cidade": "f",
            "bairro": "g",
            "logradouro": "h",
            "numero": "i"
        }
    }
    filial_b_response = requests.post(
        f"{api_url}/empresas/"
        f"{id_empresa_b}/filiais/",
        headers=headers_gestor_b,
        json=filial_b_data
        )
    id_filial_b = filial_b_response.json()['id']
    func_b_data = {"cpf": f"555{random.randint(10000,99999)}",
                   "email": f"func.b.{random.randint(1000,9999)}@empresa.com",
                   "nome": "Func B", "senha": "123",
                   "tipo_usuario": "FUNCIONARIO",
                   "filial_associada": id_filial_b,
                   "senha_da_filial": "s"
                   }
    requests.post(f"{api_url}/usuarios/", headers=headers_gestor_b, json=func_b_data)

    return {"token_gestor_a": token_gestor_a, "id_empresa_b": id_empresa_b}


def test_funcionario_nao_pode_criar_filial(api_url, cenario_com_funcionario_logado):
    """ Garante que um funcionário, mesmo autenticado, não pode criar uma filial."""

    setup = cenario_com_funcionario_logado
    url = f"{api_url}/empresas/{setup['id_empresa']}/filiais/"
    headers = {'Authorization': f'Bearer {setup["token_funcionario"]}'}
    nova_filial_data = {"cnpj": "666777888000199",
                        "nome": "Filial Ilegal",
                        "senha": "s",
                        "email": "i@i.com",
                        "telefone": "1",
                        "endereco": {"cep": "6",
                                     "estado": "f",
                                     "cidade": "g",
                                     "bairro": "h",
                                     "logradouro": "i",
                                     "numero": "j"
                                     }
                        }

    response = requests.post(url, headers=headers, json=nova_filial_data)

    assert response.status_code == 403


def test_gestor_nao_pode_listar_patrimonios_de_outra_empresa(api_url, cenario_duas_empresas):
    """ Garante que um gestor da Empresa A não pode ver os patrimônios da Empresa B."""

    setup = cenario_duas_empresas

    url = f"{api_url}/empresas/{setup['id_empresa_b']}/patrimonios/"
    headers = {'Authorization': f'Bearer {setup["token_gestor_a"]}'}

    response = requests.get(url, headers=headers)

    assert response.status_code == 403


def test_gestor_nao_pode_listar_funcionarios_de_outra_empresa(api_url, cenario_duas_empresas):
    """ Garante que um gestor da Empresa A não pode ver os funcionários da Empresa B."""

    setup = cenario_duas_empresas

    url = f"{api_url}/empresas/{setup['id_empresa_b']}/funcionarios/"
    headers = {'Authorization': f'Bearer {setup["token_gestor_a"]}'}

    response = requests.get(url, headers=headers)

    assert response.status_code == 403
