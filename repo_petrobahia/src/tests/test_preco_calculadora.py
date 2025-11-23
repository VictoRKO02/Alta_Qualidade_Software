import unittest

from refatorado.preco_calculadora import PrecoCalculadora


class TestPrecoCalculadora(unittest.TestCase):
    """Testes para a classe PrecoCalculadora."""

    def setUp(self):
        """Configura a calculadora antes de cada teste."""
        self.calc = PrecoCalculadora()

    # Testes de Preços Base e Produtos Desconhecidos
    def test_produto_desconhecido(self):
        """Deve retornar 0.0 para um produto não listado."""
        self.assertEqual(self.calc.calcular_preco("agua", 10), 0.0)

    def test_preco_base_lubrificante(self):
        """Deve calcular o preço base corretamente sem descontos."""
        # Preço base: 25.00 * 10 = 250.00
        self.assertEqual(self.calc.calcular_preco("lubrificante", 10), 250.00)

    # Testes de Desconto para Diesel
    def test_desconto_diesel_baixo(self):
        """Sem desconto para qtd <= 500."""
        # Preço base: 3.99 * 500 = 1995.00
        self.assertEqual(self.calc.calcular_preco("diesel", 500), 1995.00)

    def test_desconto_diesel_medio(self):
        """Desconto de 5% para 500 < qtd <= 1000."""
        # Preço base: 3.99 * 800 = 3192.00
        # Desconto: 3192.00 * 0.95 = 3032.40
        self.assertAlmostEqual(self.calc.calcular_preco("diesel", 800), 3032.40, 2)

    def test_desconto_diesel_alto(self):
        """Desconto de 10% para qtd > 1000."""
        # Preço base: 3.99 * 1200 = 4788.00
        # Desconto: 4788.00 * 0.9 = 4309.20
        self.assertAlmostEqual(self.calc.calcular_preco("diesel", 1200), 4309.20, 2)

    # Testes de Desconto para Gasolina
    def test_desconto_gasolina_baixo(self):
        """Sem desconto para qtd <= 200."""
        # Preço base: 5.19 * 200 = 1038.00
        self.assertAlmostEqual(self.calc.calcular_preco("gasolina", 200), 1038.00, 2)

    def test_desconto_gasolina_alto(self):
        """Desconto fixo de R$100.00 para qtd > 200."""
        # Preço base: 5.19 * 300 = 1557.00
        # Desconto: 1557.00 - 100.00 = 1457.00
        self.assertAlmostEqual(self.calc.calcular_preco("gasolina", 300), 1457.00, 2)

    # Testes de Desconto para Etanol
    def test_desconto_etanol_baixo(self):
        """Sem desconto para qtd <= 80."""
        # Preço base: 3.59 * 50 = 179.50
        self.assertAlmostEqual(self.calc.calcular_preco("etanol", 50), 179.50, 2)

    def test_desconto_etanol_alto(self):
        """Desconto de 3% para qtd > 80."""
        # Preço base: 3.59 * 100 = 359.00
        # Desconto: 359.00 * 0.97 = 348.23
        self.assertAlmostEqual(self.calc.calcular_preco("etanol", 100), 348.23, 2)
