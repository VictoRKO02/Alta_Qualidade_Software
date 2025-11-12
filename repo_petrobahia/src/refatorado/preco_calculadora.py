from typing import Dict


class PrecoCalculadora:
    """Responsável por calcular o preço de produtos."""

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
                pass  # sem desconto

        return round(preco_total, 2)

    @staticmethod
    def _aplicar_desconto_diesel(preco_total: float, qtd: int) -> float:
        if qtd > 1000:
            return preco_total * 0.9
        if qtd > 500:
            return preco_total * 0.95
        return preco_total

    @staticmethod
    def _aplicar_desconto_gasolina(preco_total: float, qtd: int) -> float:
        if qtd > 200:
            return preco_total - 100
        return preco_total

    @staticmethod
    def _aplicar_desconto_etanol(preco_total: float, qtd: int) -> float:
        if qtd > 80:
            return preco_total * 0.97
        return preco_total
