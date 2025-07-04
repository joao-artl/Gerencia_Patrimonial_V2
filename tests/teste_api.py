import unittest
import requests
import json
import os
import random

class TestCriacaoDeUsuarios(unittest.TestCase):

    def setUp(self):
        """
        Método que roda antes de cada teste. Usado para configurar o ambiente.
        """
        api_host = os.getenv("API_HOST", "localhost")
        self.base_url = f"http://{api_host}:8000/api"

    def test_1_1_criar_gestor_com_sucesso(self):
        """
        TESTE 1.1: Garante que um usuário anônimo PODE criar uma conta do tipo GESTOR.
        """
        print("\nExecutando Teste 1.1: Criar Gestor com Sucesso...")
        
        url = f"{self.base_url}/usuarios/"
        random_id = random.randint(10000, 99999)
        data = {
            "cpf": f"22233344{random_id}",
            "email": f"gestor.unittest.{random_id}@empresa.com",
            "nome": "Gestor de Teste Unitário",
            "senha": "senhaForte123",
            "tipo_usuario": "GESTOR"
        }

        response = requests.post(url, json=data)
        
        self.assertEqual(response.status_code, 201, f"Erro! A API retornou {response.status_code} em vez de 201. Resposta: {response.text}")
        
        response_data = response.json()
        self.assertEqual(response_data['email'], data['email'])
        self.assertEqual(response_data['tipo_usuario'], 'GESTOR')
        print("Teste 1.1 passou corretamente.")

if __name__ == '__main__':
    unittest.main()