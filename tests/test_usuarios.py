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
def dados_novo_gestor():
    """Gera dados únicos para um novo gestor."""
    random_id = random.randint(10000, 99999)
    return {
        "cpf": f"11122233{random_id}",
        "email": f"gestor.teste.{random_id}@empresa.com",
        "nome": "Gestor de Teste 1",
        "senha": "senhaForte123",
        "tipo_usuario": "GESTOR"
    }


def test_criar_gestor_publicamente_com_sucesso(api_url, dados_novo_gestor):
    """Garante que um usuário anônimo PODE criar uma conta de GESTOR."""

    url = f"{api_url}/usuarios/"
    response = requests.post(url, json=dados_novo_gestor)

    assert response.status_code == 201, f"Erro! Resposta: {response.text}"
    response_data = response.json()
    assert response_data['email'] == dados_novo_gestor['email']


def test_criar_funcionario_publicamente_falha(api_url):
    """Garante que um usuário anônimo NÃO PODE criar uma conta de FUNCIONARIO."""

    url = f"{api_url}/usuarios/"
    data = {
        "cpf": "22233344455",
        "email": "funcionario.falha@empresa.com",
        "nome": "Funcionário com Falha",
        "senha": "senha123",
        "tipo_usuario": "FUNCIONARIO",
        "filial_associada": 99,
        "senha_da_filial": "senhaqualquer"
    }
    response = requests.post(url, json=data)
    assert response.status_code == 401


def test_login_com_sucesso(api_url, dados_novo_gestor):
    """Garante que um usuário existente consegue fazer login."""

    requests.post(f"{api_url}/usuarios/", json=dados_novo_gestor)

    login_url = f"{api_url}/token/"
    login_data = {
        "email": dados_novo_gestor['email'],
        "senha": dados_novo_gestor['senha']
    }
    login_response = requests.post(login_url, json=login_data)

    assert login_response.status_code == 200, f"Erro no login: {login_response.text}"
    response_data = login_response.json()
    assert 'access' in response_data
