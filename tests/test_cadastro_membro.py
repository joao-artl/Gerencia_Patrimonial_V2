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
        "filial_associada_id": setup_data['id_filial'],
        "senha_da_filial": setup_data['senha_da_filial']
    }
    response = requests.post(url, headers=headers, json=funcionario_data)

    assert response.status_code == 201, f"Erro ao criar funcionário: {response.text}"

def test_gestor_adiciona_outro_gestor_com_sucesso(api_url, gestor_fundador_com_empresa_e_filial, gestor_independente):
    """
    Garante que um gestor pode adicionar outro gestor à sua empresa
    """

    setup_fundador = gestor_fundador_com_empresa_e_filial
    token_do_ator = setup_fundador['token_gestor']
    id_da_empresa_alvo = setup_fundador['id_empresa']
    senha_da_empresa_alvo = setup_fundador['senha_da_empresa']
    dados_gestor_a_adicionar = gestor_independente
    email_a_adicionar = dados_gestor_a_adicionar['email']

    url = f"{api_url}/empresas/{id_da_empresa_alvo}/gestores/"
    headers = {'Authorization': f'Bearer {token_do_ator}'}
    
    data = {
        "usuario_email": email_a_adicionar,
        "senha_da_empresa": senha_da_empresa_alvo
    }

    response = requests.post(url, headers=headers, json=data)
    assert response.status_code == 201, f"Erro ao adicionar gestor: {response.text}"
    response_data = response.json()
    assert response_data['usuario']['email'] == email_a_adicionar

def test_gestor_independente_se_conecta_por_email(api_url):
    """
    Garante que um gestor pode se conectar a uma empresa usando o email e a senha da empresa.
    """

    empresa_data = {
        "cnpj": f"12121212{random.randint(10000,99999)}", "nome": "Empresa Alvo Para Join", 
        "email": f"contato.alvo.{random.randint(1000,9999)}@empresa.com", "telefone": f"1191212{random.randint(1000,9999)}",
        "senha": "senha-secreta-da-empresa-alvo",
        "endereco": {"cep": "3", "estado": "c", "cidade": "d", "bairro": "e", "logradouro": "f", "numero": "g"}
    }

    gestor_temporario_data = {"email": f"temp.{random.randint(1000,9999)}@temp.com", "senha": "123", "cpf": f"131{random.randint(10000,99999)}", "nome":"T", "tipo_usuario":"GESTOR"}
    requests.post(f"{api_url}/usuarios/", json=gestor_temporario_data)
    login_temp_res = requests.post(f"{api_url}/token/", json={"email": gestor_temporario_data['email'], "senha": gestor_temporario_data['senha']})
    headers_temp = {'Authorization': f'Bearer {login_temp_res.json()["access"]}'}
    requests.post(f"{api_url}/empresas/", headers=headers_temp, json=empresa_data)

    gestor_join_data = {
        "cpf": f"30405060{random.randint(10000,99999)}",
        "email": f"gestor.join.{random.randint(1000,9999)}@empresa.com",
        "nome": "Gestor que quer entrar", "senha": "senhaDoJoin", "tipo_usuario": "GESTOR"
    }
    requests.post(f"{api_url}/usuarios/", json=gestor_join_data)
    
    login_join_res = requests.post(f"{api_url}/token/", json={"email": gestor_join_data['email'], "senha": gestor_join_data['senha']})
    token_gestor_join = login_join_res.json()['access']
    headers_join = {'Authorization': f'Bearer {token_gestor_join}'}

    url = f"{api_url}/empresas/join-by-email/"
    data = {
        "email": empresa_data['email'],
        "senha": empresa_data['senha']
    }
    response = requests.post(url, headers=headers_join, json=data)

    assert response.status_code == 200, f"Erro ao tentar se conectar à empresa: {response.text}"
    assert "adicionado com sucesso" in response.json()['message']