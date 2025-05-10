from django.test import TestCase
import unittest

class TDDTest(TestCase):
    @unittest.skip("Ignorar até implementação final")
    def test_criacao_empresa(self):
        empresa = Empresa()
        empresa.nome = "Tech Solutions"
        empresa.cnpj = 12345678901234
        empresa.email = "contato@tech.com"

        self.assertEqual(empresa.nome, "Tech Solutions")
        self.assertEqual(empresa.cnpj, 12345678901234)
        self.assertIn("@", empresa.email)

    @unittest.skip("Ignorar até implementação final")
    def test_adicionar_filial(self):
        empresa = Empresa()
        filial = Filial("Filial SP")
        empresa.filas.append(filial)

        self.assertEqual(len(empresa.filas), 1)
        self.assertEqual(empresa.filas[0].nome, "Filial SP")

    @unittest.skip("Ignorar até implementação final")
    def test_criacao_veiculo(self):
        veiculo = Veiculo.create(nome="Caminhão")
        self.assertEqual(veiculo.nome, "Caminhão")

    @unittest.skip("Ignorar até implementação final")
    def test_utilitario_com_funcao(self):
        util = Utilitario()
        util.descricao = "Chave de Fenda"
        util.funcao = "Apertar parafusos"

        self.assertEqual(util.funcao, "Apertar parafusos")
        self.assertIn("Fenda", util.descricao)

    @unittest.skip("Ignorar até implementação final")
    def test_imovel_com_area_positiva(self):
        imovel = Imobiliario()
        imovel.area = 250.5
        imovel.tipo = "Comercial"

        self.assertGreater(imovel.area, 0)
        self.assertEqual(imovel.tipo, "Comercial")

    @unittest.skip("Ignorar até implementação final")
    def test_listagem_patrimonios(self):
        empresa = Empresa()
        empresa.fillWithSomeData()
        patrimonios = empresa.listarTodosPatrimonios()

        self.assertIsInstance(patrimonios, list)
        self.assertGreater(len(patrimonios), 0)

    @unittest.skip("Ignorar até implementação final")
    def test_getNomesPatrimonios_retorna_lista_strings(self):
        filial = Filial()
        filial.patrimonios = [Veiculo(nome="Caminhão"), Utilitario(nome="Furadeira")]
        nomes = filial.getNomesPatrimonios()
        
        self.assertIsInstance(nomes, list)
        self.assertIn("Caminhão", nomes)
        
    @unittest.skip("Ignorar até implementação final")
    def test_veiculo_herda_item_patrimonio(veiculo):
        assert isinstance(veiculo, Veiculo)
        assert hasattr(veiculo, 'valor')
        assert hasattr(veiculo, 'cor') 
