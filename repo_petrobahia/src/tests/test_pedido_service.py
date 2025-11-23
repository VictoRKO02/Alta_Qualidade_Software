import unittest
from unittest.mock import MagicMock, patch

from refatorado.pedido_service import PedidoService


class TestPedidoService(unittest.TestCase):
    """Testes para a classe PedidoService."""

    def setUp(self):
        """Configura o serviço antes de cada teste."""
        # Mocka a calculadora para retornar valores fixos e testar apenas o PedidoService
        self.calc_mock = MagicMock()
        # Inicializa o PedidoService com o mock da calculadora
        with patch("refatorado.pedido_service.PrecoCalculadora") as MockCalc:
            MockCalc.return_value = self.calc_mock
            self.service = PedidoService()

    # Testes de Validação
    def test_pedido_invalido_sem_produto(self):
        """Deve retornar 0.0 para pedido sem produto."""
        pedido = {"cliente": "Teste", "qtd": 10}
        self.assertEqual(self.service.processar_pedido(pedido), 0.0)

    def test_pedido_invalido_qtd_zero(self):
        """Deve retornar 0.0 para quantidade zero."""
        pedido = {"cliente": "Teste", "produto": "diesel", "qtd": 0}
        self.assertEqual(self.service.processar_pedido(pedido), 0.0)

    # Testes de Cupom
    def test_aplicar_cupom_mega10(self):
        """Deve aplicar 10% de desconto (0.9)."""
        preco_inicial = 100.0
        preco_final = self.service._aplicar_cupom(preco_inicial, "MEGA10", "gasolina")
        self.assertAlmostEqual(preco_final, 90.0)

    def test_aplicar_cupom_novo5(self):
        """Deve aplicar 5% de desconto (0.95)."""
        preco_inicial = 100.0
        preco_final = self.service._aplicar_cupom(preco_inicial, "NOVO5", "gasolina")
        self.assertAlmostEqual(preco_final, 95.0)

    def test_aplicar_cupom_lub2_com_lubrificante(self):
        """Deve aplicar R$2.00 de desconto se for lubrificante."""
        preco_inicial = 50.0
        preco_final = self.service._aplicar_cupom(preco_inicial, "LUB2", "lubrificante")
        self.assertAlmostEqual(preco_final, 48.0)

    def test_aplicar_cupom_lub2_sem_lubrificante(self):
        """Não deve aplicar R$2.00 de desconto se não for lubrificante."""
        preco_inicial = 50.0
        preco_final = self.service._aplicar_cupom(preco_inicial, "LUB2", "diesel")
        self.assertAlmostEqual(preco_final, 50.0)

    def test_aplicar_cupom_desconhecido(self):
        """Não deve aplicar desconto para cupom desconhecido."""
        preco_inicial = 100.0
        preco_final = self.service._aplicar_cupom(
            preco_inicial, "DESCONTO100", "gasolina"
        )
        self.assertAlmostEqual(preco_final, 100.0)

    # Testes de Arredondamento
    def test_arredondar_diesel(self):
        """Deve arredondar para o inteiro mais próximo (0 casas decimais)."""
        self.assertAlmostEqual(
            self.service._arredondar_valor(3878.28, "diesel"), 3878.00
        )
        self.assertAlmostEqual(
            self.service._arredondar_valor(3878.51, "diesel"), 3879.00
        )

    def test_arredondar_gasolina(self):
        """Deve arredondar para 2 casas decimais."""
        self.assertAlmostEqual(
            self.service._arredondar_valor(1457.003, "gasolina"), 1457.00
        )
        self.assertAlmostEqual(
            self.service._arredondar_valor(1457.996, "gasolina"), 1458.00
        )

    def test_arredondar_outros(self):
        """Deve truncar para 2 casas decimais (float(int(preco * 100) / 100.0))."""
        # 170.525 * 100 = 17052.5 -> int(17052.5) = 17052 -> 17052 / 100.0 = 170.52
        self.assertAlmostEqual(
            self.service._arredondar_valor(170.525, "etanol"), 170.52
        )
        # 99.999 * 100 = 9999.9 -> int(9999.9) = 9999 -> 9999 / 100.0 = 99.99
        self.assertAlmostEqual(
            self.service._arredondar_valor(99.999, "lubrificante"), 99.99
        )

    # Teste de Orquestração
    def test_processamento_completo(self):
        """Testa um cenário de processamento de pedido de ponta a ponta (com mock)."""
        # Configura o mock da calculadora para retornar um valor simulado após descontos de quantidade
        self.calc_mock.calcular_preco.return_value = (
            100.0  # Valor após desconto de quantidade
        )

        pedido = {"cliente": "Teste", "produto": "etanol", "qtd": 100, "cupom": "NOVO5"}

        # 1. Calculadora retorna 100.0 (simulação de preço c/ desconto de quantidade)
        # 2. Aplicar cupom NOVO5: 100.0 * 0.95 = 95.0
        # 3. Arredondar (etanol - outros/truncar): 95.00

        preco_final = self.service.processar_pedido(pedido)
        self.assertAlmostEqual(preco_final, 95.00)
        self.calc_mock.calcular_preco.assert_called_once_with("etanol", 100)
