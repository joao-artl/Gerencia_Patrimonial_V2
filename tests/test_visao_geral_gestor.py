import pytest
import requests
import os
import random


@pytest.fixture(scope="session")
def api_url():
    """Fornece a URL base da API."""
    api_host = os.getenv("API_HOST", "localhost")
    return f"http://{api_host}:8000/api"


@pytest.fixture
def cenario_gestor_com_empresa_populada(api_url):
    """
    Fixture que cria um cenário completo:
    - 1 Gestor logado
    - 1 Empresa
    - Filial A com 1 Veículo e 1 Utilitário
    - Filial B com 1 Utilitário
    - 1 Funcionário na Filial A
    """

    random_id_gestor = random.randint(10000, 99999)
    gestor_data = {
        "cpf": f"999{random_id_gestor}",
        "email": f"gestor.l5.{random_id_gestor}@empresa.com",
        "nome": "Gestor L5", "senha": "senha123", "tipo_usuario": "GESTOR"
    }
    create_user_response = requests.post(f"{api_url}/usuarios/", json=gestor_data)
    assert create_user_response.status_code == 201, (
        f"Setup falhou: não criou gestor. "
        f"Resposta: {create_user_response.text}"
    )

    login_response = requests.post(f"{api_url}/token/", json={
        "email": gestor_data['email'],
        "senha": gestor_data['senha']
        }
    )
    assert login_response.status_code == 200, (
        f"Setup falhou: não logou gestor. "
        f"Resposta: {login_response.text}"
    )
    token_gestor = login_response.json()['access']
    headers_gestor = {'Authorization': f'Bearer {token_gestor}'}

    random_id_empresa = random.randint(10000, 99999)
    empresa_data = {
        "cnpj": f"777{random_id_empresa}", "nome": "Holding de Teste L5",
        "email": f"contato{random_id_empresa}@l5.com",
        "telefone": f"119777{random_id_empresa}",
        "senha": "senha-empresa",
        "endereco": {
            "cep": "05050000", "estado": "SP", "cidade": "SP",
            "bairro": "Perdizes", "logradouro": "Rua A",
            "numero": "1"
        }
    }
    empresa_response = requests.post(
        f"{api_url}/empresas/",
        headers=headers_gestor,
        json=empresa_data
    )
    assert empresa_response.status_code == 201, (
        f"Setup falhou: não criou empresa. "
        f"Resposta: {empresa_response.text}"
    )
    id_empresa = empresa_response.json()['id']

    filial_a_data = {
        "cnpj": f"888{random.randint(10000000,99999999)}",
        "nome": "Filial A", "senha": "senha-a",
        "email": f"filiala{random.randint(1000,9999)}@a.com",
        "telefone": f"1198888{random.randint(1000,9999)}",
        "endereco": {
            "cep": "1", "estado": "a", "cidade": "b",
            "bairro": "c", "logradouro": "d", "numero": "e"
            }
        }
    filial_a_response = requests.post(f"{api_url}/empresas/{id_empresa}/filiais/",
                                      headers=headers_gestor, json=filial_a_data)
    assert filial_a_response.status_code == 201, (
        f"Setup falhou: não criou a Filial A. "
        f"Resposta: {filial_a_response.text}"
    )
    id_filial_a = filial_a_response.json()['id']

    veiculo_a_data = {
        "nome": "Carro de Serviço",
        "valor": "80000.00", "quantidade": 1,
        "cor": "Branco", "modelo": "Fiorino",
        "fabricante": "Fiat"
    }
    r_veiculo_a = requests.post(
        f"{api_url}/empresas/{id_empresa}/filiais/{id_filial_a}/veiculos/",
        headers=headers_gestor, json=veiculo_a_data
    )
    assert r_veiculo_a.status_code == 201, (
        f"Setup falhou: não criou Veículo na Filial A. "
        f"Resposta: {r_veiculo_a.text}"
    )

    utilitario_a_data = {"nome": "Mesa de Escritório",
                         "valor": "750.00", "quantidade": 5,
                         "descricao": "Mesa de trabalho",
                         "funcao": "Mobiliário"}
    r_utilitario_a = requests.post(
        f"{api_url}/empresas/{id_empresa}/filiais/{id_filial_a}/utilitarios/",
        headers=headers_gestor, json=utilitario_a_data
        )
    assert r_utilitario_a.status_code == 201, (
        f"Setup falhou: não criou Utilitário na Filial A. "
        f"Resposta: {r_utilitario_a.text}"
    )

    filial_b_data = {
        "cnpj": f"999{random.randint(10000000,99999999)}",
        "nome": "Filial B",
        "senha": "senha-b",
        "email": f"filialb{random.randint(1000,9999)}@b.com",
        "telefone": f"1199999{random.randint(1000,9999)}",
        "endereco": {
            "cep": "2",
            "estado": "b",
            "cidade": "c",
            "bairro": "d",
            "logradouro": "e",
            "numero": "f"
        }
    }
    filial_b_response = requests.post(f"{api_url}/empresas/{id_empresa}/filiais/",
                                      headers=headers_gestor, json=filial_b_data)
    assert filial_b_response.status_code == 201, (
        f"Setup falhou: não criou a Filial B."
        f"Resposta: {filial_b_response.text}"
    )
    id_filial_b = filial_b_response.json()['id']

    utilitario_b_data = {"nome": "Notebook Dell",
                         "valor": "5000.00", "quantidade": 10,
                         "descricao": "Notebook i7 para desenvolvimento",
                         "funcao": "Computador"}
    r_utilitario_b = requests.post(
        f"{api_url}/empresas/{id_empresa}/filiais/{id_filial_b}/utilitarios/",
        headers=headers_gestor, json=utilitario_b_data
    )
    assert r_utilitario_b.status_code == 201, (
        f"Setup falhou: não criou Utilitário na Filial B. "
        f"Resposta: {r_utilitario_b.text}"
    )

    func_data = {"cpf": f"121{random.randint(10000,99999)}",
                 "email": f"func.l5.{random.randint(1000,9999)}@empresa.com",
                 "nome": "Funcionario L5", "senha": "senhaDoFuncionario",
                 "tipo_usuario": "FUNCIONARIO", "filial_associada": id_filial_a,
                 "senha_da_filial": "senha-a"}
    response_func = requests.post(f"{api_url}/usuarios/",
                                  headers=headers_gestor, json=func_data)
    assert response_func.status_code == 201, (
        f"Setup falhou: não criou o funcionário. "
        f"Resposta: {response_func.text}"
    )

    return {"token_gestor": token_gestor, "id_empresa": id_empresa}


def test_gestor_lista_filiais_da_empresa(api_url, cenario_gestor_com_empresa_populada):
    """Garante que um gestor pode listar todas as filiais de sua empresa."""

    setup = cenario_gestor_com_empresa_populada
    url = f"{api_url}/empresas/{setup['id_empresa']}/filiais/"
    headers = {'Authorization': f'Bearer {setup["token_gestor"]}'}

    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_gestor_lista_funcionarios_da_empresa(api_url, cenario_gestor_com_empresa_populada):
    """Garante que um gestor pode listar todos os funcionários de sua empresa."""

    setup = cenario_gestor_com_empresa_populada
    url = f"{api_url}/empresas/{setup['id_empresa']}/funcionarios/"
    headers = {'Authorization': f'Bearer {setup["token_gestor"]}'}

    response = requests.get(url, headers=headers)
    assert response.status_code == 200

    assert len(response.json()) == 1
    assert response.json()[0]['nome'] == "Funcionario L5"


def test_gestor_lista_patrimonios_da_empresa(api_url, cenario_gestor_com_empresa_populada):
    """Garante que um gestor pode listar todos os patrimônios de todas as suas filiais."""

    setup = cenario_gestor_com_empresa_populada
    url = f"{api_url}/empresas/{setup['id_empresa']}/patrimonios/"
    headers = {'Authorization': f'Bearer {setup["token_gestor"]}'}

    response = requests.get(url, headers=headers)
    assert response.status_code == 200

    response_data = response.json()
    assert len(response_data) == 2
    assert len(response_data[next(iter(response_data))]['veiculos']) == 1


def test_gestor_busca_patrimonio_na_empresa(api_url, cenario_gestor_com_empresa_populada):
    """Garante que a busca consolidada de patrimônios funciona."""

    setup = cenario_gestor_com_empresa_populada
    termo_busca = "Notebook"
    url = f"{api_url}/empresas/{setup['id_empresa']}/patrimonios/?search={termo_busca}"
    headers = {'Authorization': f'Bearer {setup["token_gestor"]}'}

    response = requests.get(url, headers=headers)
    assert response.status_code == 200

    response_data = response.json()
    filial_a_key = next(k for k in response_data if "Filial A" in k)
    filial_b_key = next(k for k in response_data if "Filial B" in k)

    assert len(response_data[filial_a_key]['utilitarios']) == 0
    assert len(response_data[filial_b_key]['utilitarios']) == 1
    assert response_data[filial_b_key]['utilitarios'][0]['nome'] == "Notebook Dell"
