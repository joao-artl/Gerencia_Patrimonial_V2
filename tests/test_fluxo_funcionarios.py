import pytest
import requests
import os
import random


@pytest.fixture(scope="session")
def api_url():
    api_host = os.getenv("API_HOST", "localhost")
    return f"http://{api_host}:8000/api"

@pytest.fixture
def cenario_com_funcionario(api_url):

    gestor_data = {"email": f"gestor.l4.{random.randint(1000,9999)}@empresa.com", "senha": "123", "cpf": f"111{random.randint(10000,99999)}", "nome": "G", "tipo_usuario": "GESTOR"}
    requests.post(f"{api_url}/usuarios/", json=gestor_data)
    login_response = requests.post(f"{api_url}/token/", json={"email": gestor_data['email'], "senha": gestor_data['senha']})
    token_gestor = login_response.json()['access']
    headers_gestor = {'Authorization': f'Bearer {token_gestor}'}
    
    empresa_data = {
        "cnpj": f"111{random.randint(10000000,99999999)}", "nome": "Empresa L4", "email": f"contato{random.randint(1000,9999)}@l4.com",
        "telefone": f"1191111{random.randint(1000,9999)}", "senha": "senha-empresa",
        "endereco": {"cep": "01010000", "estado": "SP", "cidade": "SP", "bairro": "Centro", "logradouro": "Rua X", "numero": "1"}
    }
    empresa_response = requests.post(f"{api_url}/empresas/", headers=headers_gestor, json=empresa_data)
    id_empresa = empresa_response.json()['id']

    filial_a_data = {
        "cnpj": f"222{random.randint(10000000,99999999)}", "nome": "Filial A", "email": f"contato{random.randint(1000,9999)}@fa.com",
        "telefone": f"1192222{random.randint(1000,9999)}", "senha": "senha-filial-a",
        "endereco": {"cep": "02020000", "estado": "SP", "cidade": "SP", "bairro": "Norte", "logradouro": "Rua Y", "numero": "2"}
    }
    filial_a_response = requests.post(f"{api_url}/empresas/{id_empresa}/filiais/", headers=headers_gestor, json=filial_a_data)
    id_filial_a = filial_a_response.json()['id']

    filial_b_data = {
        "cnpj": f"333{random.randint(10000000,99999999)}", "nome": "Filial B", "email": f"contato{random.randint(1000,9999)}@fb.com",
        "telefone": f"1193333{random.randint(1000,9999)}", "senha": "senha-filial-b",
        "endereco": {"cep": "03030000", "estado": "SP", "cidade": "SP", "bairro": "Leste", "logradouro": "Rua Z", "numero": "3"}
    }
    filial_b_response = requests.post(f"{api_url}/empresas/{id_empresa}/filiais/", headers=headers_gestor, json=filial_b_data)
    id_filial_b = filial_b_response.json()['id']

    funcionario_data = {
        "cpf": f"444{random.randint(10000,99999)}", "email": f"func.l4.{random.randint(1000,9999)}@empresa.com",
        "nome": "Funcionario L4", "senha": "senhaDoFuncionario", "tipo_usuario": "FUNCIONARIO",
        "filial_associada_id": id_filial_a, "senha_da_filial": "senha-filial-a"
    }
    requests.post(f"{api_url}/usuarios/", headers=headers_gestor, json=funcionario_data)

    login_func_response = requests.post(f"{api_url}/token/", json={"email": funcionario_data['email'], "senha": funcionario_data['senha']})
    token_funcionario = login_func_response.json()['access']
    
    return {
        "token_funcionario": token_funcionario,
        "id_empresa": id_empresa,
        "id_filial_correta": id_filial_a,
        "id_filial_errada": id_filial_b
    }


def test_funcionario_acessa_recursos_permitidos(api_url, cenario_com_funcionario):

    setup = cenario_com_funcionario
    url = f"{api_url}/empresas/{setup['id_empresa']}/filiais/{setup['id_filial_correta']}/patrimonios/"
    headers = {'Authorization': f'Bearer {setup["token_funcionario"]}'}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200

def test_funcionario_cria_veiculo_com_sucesso(api_url, cenario_com_funcionario):

    setup = cenario_com_funcionario
    url = f"{api_url}/empresas/{setup['id_empresa']}/filiais/{setup['id_filial_correta']}/veiculos/"
    headers = {'Authorization': f'Bearer {setup["token_funcionario"]}'}
    veiculo_data = { "nome": "Veículo de Teste do Funcionário", "valor": "75000.00", "quantidade": 1, "cor": "Prata", "modelo": "Onix", "fabricante": "Chevrolet" }
    response = requests.post(url, headers=headers, json=veiculo_data)
    assert response.status_code == 201

def test_funcionario_cria_utilitario_com_sucesso(api_url, cenario_com_funcionario):

    setup = cenario_com_funcionario
    url = f"{api_url}/empresas/{setup['id_empresa']}/filiais/{setup['id_filial_correta']}/utilitarios/"
    headers = {'Authorization': f'Bearer {setup["token_funcionario"]}'}
    utilitario_data = { "nome": "Notebook Dell i7", "valor": "5500.00", "quantidade": 10, "descricao": "Notebook para equipe de vendas", "funcao": "Trabalho" }
    response = requests.post(url, headers=headers, json=utilitario_data)
    assert response.status_code == 201

def test_funcionario_cria_imobiliario_com_sucesso(api_url, cenario_com_funcionario):

    setup = cenario_com_funcionario
    url = f"{api_url}/empresas/{setup['id_empresa']}/filiais/{setup['id_filial_correta']}/imobiliarios/"
    headers = {'Authorization': f'Bearer {setup["token_funcionario"]}'}
    imobiliario_data = { "nome": "Sala Comercial 101", "valor": "250000.00", "area": "45.50", "tipo": "Escritório", "endereco": { "cep": "04543000", "estado": "SP", "cidade": "São Paulo", "bairro": "Vila Olímpia", "logradouro": "Rua Olimpíadas", "numero": "205" }}
    response = requests.post(url, headers=headers, json=imobiliario_data)
    assert response.status_code == 201

def test_funcionario_nao_acessa_outra_filial(api_url, cenario_com_funcionario):

    setup = cenario_com_funcionario
    url = f"{api_url}/empresas/{setup['id_empresa']}/filiais/{setup['id_filial_errada']}/patrimonios/"
    headers = {'Authorization': f'Bearer {setup["token_funcionario"]}'}
    response = requests.get(url, headers=headers)
    assert response.status_code == 403

def test_funcionario_busca_patrimonio(api_url, cenario_com_funcionario):

    setup = cenario_com_funcionario
    headers = {'Authorization': f'Bearer {setup["token_funcionario"]}'}
    url_criacao = f"{api_url}/empresas/{setup['id_empresa']}/filiais/{setup['id_filial_correta']}/veiculos/"
    
    nome_unico_veiculo = f"Kwid Laranja Teste {random.randint(1000, 9999)}"
    veiculo_para_buscar = {
        "nome": nome_unico_veiculo, "valor": "65000.00", "quantidade": 1,
        "cor": "Laranja", "modelo": "Kwid", "fabricante": "Renault"
    }

    create_response = requests.post(url_criacao, headers=headers, json=veiculo_para_buscar)
    assert create_response.status_code == 201, "Setup do teste 4.4 falhou: não conseguiu criar o veículo para a busca."
    url_busca = f"{url_criacao}?search={nome_unico_veiculo}"
    response = requests.get(url_busca, headers=headers)
    assert response.status_code == 200, f"A busca falhou com status {response.status_code}. Resposta: {response.text}"
    
    response_data = response.json()
    assert len(response_data) == 1, "A busca retornou mais ou menos de 1 resultado."
    assert response_data[0]['nome'] == nome_unico_veiculo, "O item encontrado na busca não é o correto."
    
def test_funcionario_lista_patrimonios_da_filial(api_url, cenario_com_funcionario):

    setup = cenario_com_funcionario
    headers = {'Authorization': f'Bearer {setup["token_funcionario"]}'}
    base_url = f"{api_url}/empresas/{setup['id_empresa']}/filiais/{setup['id_filial_correta']}"

    veiculo_data = {"nome": "Veiculo da Lista", "valor": "50000.00", "quantidade": 1, "cor": "Branco", "modelo": "Strada", "fabricante": "Fiat"}
    response_veiculo = requests.post(f"{base_url}/veiculos/", headers=headers, json=veiculo_data)
    assert response_veiculo.status_code == 201, f"Setup falhou ao criar Veículo: {response_veiculo.text}"

    utilitario_data = {"nome": "Utilitario da Lista", "valor": "1200.00", "quantidade": 5, "descricao": "Cadeira de escritório", "funcao": "Mobiliário"}
    response_utilitario = requests.post(f"{base_url}/utilitarios/", headers=headers, json=utilitario_data)
    assert response_utilitario.status_code == 201, f"Setup falhou ao criar Utilitário: {response_utilitario.text}"

    imobiliario_data = {"nome": "Imobiliario da Lista", "valor": "300000.00", "area": "50.0", "tipo": "Sala", "endereco": {"cep":"12345000", "estado":"RJ", "cidade":"Rio", "bairro":"Centro", "logradouro":"Av Central", "numero":"100"}}
    response_imobiliario = requests.post(f"{base_url}/imobiliarios/", headers=headers, json=imobiliario_data)
    assert response_imobiliario.status_code == 201, f"Setup falhou ao criar Imobiliário: {response_imobiliario.text}"

    url_listagem = f"{base_url}/patrimonios/"
    response = requests.get(url_listagem, headers=headers)

    assert response.status_code == 200, f"Erro ao listar patrimônios consolidados. Resposta: {response.text}"
    
    response_data = response.json()
    
    assert "veiculos" in response_data
    assert "utilitarios" in response_data
    assert "imobiliarios" in response_data
    
    assert len(response_data['veiculos']) >= 1
    assert len(response_data['utilitarios']) >= 1
    assert len(response_data['imobiliarios']) >= 1

    assert response_data['veiculos'][0]['nome'] == "Veiculo da Lista"
