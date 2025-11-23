"""Módulo de serviço para cálculo do preço base de produtos e descontos por quantidade."""
from typing import Dict


# pylint: disable=R0903
class PrecoCalculadora:
    """
    Responsável por calcular o preço de produtos aplicando descontos por quantidade.
    Seguindo o Princípio da Responsabilidade Única (SRP).
    """

    BASES: Dict[str, float] = {
        "diesel": 3.99,
        "gasolina": 5.19,
        "etanol": 3.59,
        "lubrificante": 25.00,
    }

    def calcular_preco(self, produto: str, quantidade: int) -> float:
        """Calcula o preço total de acordo com produto e quantidade."""
        if produto not in self.BASES:
            print(f"Produto '{produto}' desconhecido. Retornando 0.")
            return 0.0

        preco_base = self.BASES[produto]
        preco_total = preco_base * quantidade

        match produto:
            case "diesel":
                preco_total = self._aplicar_desconto_diesel(preco_total, quantidade)
            case "gasolina":
                preco_total = self._aplicar_desconto_gasolina(preco_total, quantidade)
            case "etanol":
                preco_total = self._aplicar_desconto_etanol(preco_total, quantidade)
            case "lubrificante":
                pass  # sem desconto por quantidade

        return round(preco_total, 2)

    @staticmethod
    def _aplicar_desconto_diesel(preco_total: float, qtd: int) -> float:
        """Aplica desconto de 5% ou 10% para diesel dependendo da quantidade."""
        if qtd > 1000:
            return preco_total * 0.9  # 10% de desconto
        if qtd > 500:
            return preco_total * 0.95  # 5% de desconto
        return preco_total

    @staticmethod
    def _aplicar_desconto_gasolina(preco_total: float, qtd: int) -> float:
        """Aplica desconto fixo de R$100.00 para gasolina acima de 200."""
        if qtd > 200:
            return preco_total - 100.0
        return preco_total

    @staticmethod
    def _aplicar_desconto_etanol(preco_total: float, qtd: int) -> float:
        """Aplica desconto de 3% para etanol acima de 80."""
        if qtd > 80:
            return preco_total * 0.97
        return preco_total