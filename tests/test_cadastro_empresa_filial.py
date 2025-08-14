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
def gestor_autenticado(api_url):
    """Cria um novo GESTOR e faz o login, retornando seu token e dados."""
    random_id = random.randint(10000, 99999)
    user_data = {
        "cpf": f"7788899{random_id}",
        "email": f"gestor.fixture.{random_id}@empresa.com",
        "nome": "Gestor de Teste Nível 2",
        "senha": "senhaFixture123",
        "tipo_usuario": "GESTOR"
    }
    create_response = requests.post(f"{api_url}/usuarios/", json=user_data)
    assert create_response.status_code == 201, (
        f"Setup falhou: não criou gestor. "
        f"Resposta: {create_response.text}"
    )

    login_data = {"email": user_data['email'], "senha": user_data['senha']}
    login_response = requests.post(f"{api_url}/token/", json=login_data)
    assert login_response.status_code == 200, (
        f"Setup falhou: não logou gestor. "
        f"Resposta: {login_response.text}"
    )

    return {"token": login_response.json()['access']}


@pytest.fixture
def empresa_criada_pelo_gestor(api_url, gestor_autenticado):
    """
    Usa um gestor autenticado para criar uma empresa e retorna o token
    do gestor e os dados da empresa criada.
    """

    url = f"{api_url}/empresas/"
    headers = {'Authorization': f'Bearer {gestor_autenticado["token"]}'}
    random_id = random.randint(10000, 99999)

    empresa_data = {
        "cnpj": f"33444555{random_id}",
        "nome": "Empresa de Teste 2",
        "email": f"contato{random_id}@empresa-2.com",
        "telefone": f"119555{str(random_id)}",
        "senha": "senha-da-empresa-2",
        "endereco": {
            "cep": "01001000", "estado": "SP",
            "cidade": "São Paulo", "bairro": "Sé",
            "logradouro": "Praça da Sé", "numero": "1"
        }
    }
    response = requests.post(url, headers=headers, json=empresa_data)
    assert response.status_code == 201, (
        f"A fixture 'empresa_criada_pelo_gestor' falhou."
        f"Resposta: {response.text}"
    )
    return {"token": gestor_autenticado["token"], "dados_empresa": response.json()}


def test_gestor_cria_empresa_com_sucesso(empresa_criada_pelo_gestor):
    """Garante que um gestor autenticado pode criar uma nova empresa"""
    """(validado atráves da Fixture)"""

    assert "id" in empresa_criada_pelo_gestor["dados_empresa"]


def test_gestor_cria_empresa_sem_endereco_falha(api_url, gestor_autenticado):
    """Garante que a API rejeita a criação de empresa sem endereço."""

    url = f"{api_url}/empresas/"
    headers = {'Authorization': f'Bearer {gestor_autenticado["token"]}'}
    empresa_data_incompleta = {
        "cnpj": "44555666000188", "nome": "Empresa Incompleta",
        "email": "contato@incompleta.com",
        "telefone": "11944443333",
        "senha": "senha-incompleta"
    }
    response = requests.post(url, headers=headers, json=empresa_data_incompleta)

    assert response.status_code == 400
    assert "endereco" in response.json()


def test_gestor_cria_filial_com_sucesso(api_url, empresa_criada_pelo_gestor):
    """Garante que um gestor pode criar uma filial para ela."""

    setup_data = empresa_criada_pelo_gestor
    id_empresa = setup_data['dados_empresa']['id']
    token_gestor = setup_data['token']
    headers = {'Authorization': f'Bearer {token_gestor}'}

    url = f"{api_url}/empresas/{id_empresa}/filiais/"
    random_id = random.randint(10000, 99999)
    filial_data = {
        "cnpj": f"66777888{random_id}",
        "nome": "Filial de Teste",
        "email": f"contato{random_id}@filial-teste.com",
        "telefone": f"1192222{str(random_id)[-4:]}",
        "senha": "senha-da-filial-teste",
        "endereco": {
            "cep": "02020020", "estado": "SP", "cidade": "São Paulo",
            "bairro": "Santana", "logradouro": "Rua Voluntários",
            "numero": "2000"
        }
    }

    response = requests.post(url, headers=headers, json=filial_data)

    assert response.status_code == 201, f"Erro ao criar filial: {response.text}"
    response_data = response.json()
    assert response_data['nome'] == filial_data['nome']
    assert int(response_data['empresa_matriz']) == id_empresa
