import pytest
import requests
import os
import random


@pytest.fixture(scope="module")
def api_url():
    """Fornece a URL base da API para todos os testes neste arquivo."""

    api_host = os.getenv("API_HOST", "localhost")
    return f"http://{api_host}:8000/api"

@pytest.fixture
def gestor_fundador_com_empresa_e_filial(api_url):
    """
    Cria um gestor, loga, cria uma empresa e uma filial.
    """

    random_id = random.randint(10000, 99999)
    gestor_data = {
        "cpf": f"88899900{random_id}",
        "email": f"gestor.fundador.3.{random_id}@empresa.com",
        "nome": "Gestor Fundador 3", "senha": "senha123", "tipo_usuario": "GESTOR"
    }
    create_user_response = requests.post(f"{api_url}/usuarios/", json=gestor_data)
    assert create_user_response.status_code == 201, f"Setup falhou: não criou gestor. Resposta: {create_user_response.text}"
    
    login_data = {"email": gestor_data['email'], "senha": gestor_data['senha']}
    login_response = requests.post(f"{api_url}/token/", json=login_data)
    assert login_response.status_code == 200, f"Setup falhou: não logou gestor. Resposta: {login_response.text}"
    token = login_response.json()['access']
    headers = {'Authorization': f'Bearer {token}'}
    
    empresa_data = {
        "cnpj": f"44555666{random_id}", "nome": "Empresa para Contratação",
        "email": f"contato{random_id}@empresa-3.com", "telefone": f"1194444{str(random_id)[-4:]}",
        "senha": "senha-da-empresa-3",
        "endereco": {"cep": "01010000", "estado": "SP", "cidade": "São Paulo", "bairro": "Centro", "logradouro": "Rua Teste", "numero": "123"}
    }
    empresa_response = requests.post(f"{api_url}/empresas/", headers=headers, json=empresa_data)
    assert empresa_response.status_code == 201, f"Setup falhou: não criou empresa. Resposta: {empresa_response.text}"
    id_empresa = empresa_response.json()['id']

    filial_data = {
        "cnpj": f"55666777{random_id}", "nome": "Filial para Contratação",
        "email": f"contato{random_id}@filial-3.com", "telefone": f"1193333{str(random_id)[-4:]}",
        "senha": "senha-da-filial-3",
        "endereco": {"cep": "02020000", "estado": "SP", "cidade": "São Paulo", "bairro": "Santana", "logradouro": "Rua Teste 2", "numero": "456"}
    }
    filial_response = requests.post(f"{api_url}/empresas/{id_empresa}/filiais/", headers=headers, json=filial_data)
    assert filial_response.status_code == 201, f"Setup falhou: não criou filial. Resposta: {filial_response.text}"
    id_filial = filial_response.json()['id']

    return {
        "token_gestor": token,
        "id_empresa": id_empresa,
        "senha_da_empresa": empresa_data['senha'],
        "id_filial": id_filial,
        "senha_da_filial": filial_data['senha']
    }

@pytest.fixture
def gestor_independente(api_url):
    """Cria um gestor 'independente' para ser adicionado a uma empresa."""

    random_id = random.randint(10000, 99999)
    gestor_data = {
        "cpf": f"10203040{random_id}",
        "email": f"gestor.independente.{random_id}@email.com",
        "nome": "Gestor Independente", "senha": "senhaIndependente456", "tipo_usuario": "GESTOR"
    }
    response = requests.post(f"{api_url}/usuarios/", json=gestor_data)
    assert response.status_code == 201
    return response.json()


def test_gestor_adiciona_funcionario_com_sucesso(api_url, gestor_fundador_com_empresa_e_filial):
    """
    Garante que um gestor logado pode criar um novo funcionário para sua filial.
    """
    
    setup_data = gestor_fundador_com_empresa_e_filial
    headers = {'Authorization': f'Bearer {setup_data["token_gestor"]}'}
    
    url = f"{api_url}/usuarios/"
    random_id = random.randint(10000, 99999)
    funcionario_data = {
        "cpf": f"66677788{random_id}",
        "email": f"funcionario.contratado.{random_id}@empresa.com",
        "nome": "Funcionario Contratado",
        "senha": "senhaDoFuncionario",
        "tipo_usuario": "FUNCIONARIO",
        "filial_associada": setup_data['id_filial'],
        "senha_da_filial": setup_data['senha_da_filial']
    }
    response = requests.post(url, headers=headers, json=funcionario_data)

    assert response.status_code == 201, f"Erro ao criar funcionário: {response.text}"

def test_gestor_adiciona_outro_gestor_com_sucesso(api_url, gestor_fundador_com_empresa_e_filial, gestor_independente):
    """
    Garante que um gestor pode adicionar outro gestor à sua empresa.
    """
    
    setup_data = gestor_fundador_com_empresa_e_filial
    id_empresa = setup_data['id_empresa']
    token_fundador = setup_data['token_gestor']
    senha_empresa = setup_data['senha_da_empresa']
    
    id_gestor_a_adicionar = gestor_independente['id']

    url = f"{api_url}/empresas/{id_empresa}/gestores/"
    headers = {'Authorization': f'Bearer {token_fundador}'}
    data = {
        "usuario_id": id_gestor_a_adicionar,
        "senha_da_empresa": senha_empresa
    }
    response = requests.post(url, headers=headers, json=data)

    assert response.status_code == 201, f"Erro ao adicionar gestor: {response.text}"
    assert response.json()['usuario']['id'] == id_gestor_a_adicionar