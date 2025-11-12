from typing import Dict, Optional
from refatorado.preco_calculadora import PrecoCalculadora


class PedidoService:
    """Serviço responsável por processar pedidos."""

    def __init__(self) -> None:
        self.calculadora = PrecoCalculadora()

    def processar_pedido(self, pedido: Dict[str, Optional[str | int]]) -> float:
        """Processa o pedido e retorna o valor final."""
        produto = pedido.get("produto")
        quantidade = pedido.get("qtd", 0)
        cupom = pedido.get("cupom")
        cliente = pedido.get("cliente")

        if not produto or quantidade <= 0:
            print(f"[ERRO] Pedido inválido de {cliente}: quantidade 0.")
            return 0.0

        preco = self.calculadora.calcular_preco(produto, quantidade)
        preco = self._aplicar_cupom(preco, cupom, produto)
        preco = self._arredondar_valor(preco, produto)

        print(f"Pedido OK: {cliente} | {produto} x{quantidade} => R${preco:.2f}")
        return preco

    @staticmethod
    def _aplicar_cupom(preco: float, cupom: Optional[str], produto: str) -> float:
        """Aplica descontos de cupom, se existirem."""
        if not cupom:
            return preco

        descontos = {
            "MEGA10": lambda p: p * 0.9,
            "NOVO5": lambda p: p * 0.95,
            "LUB2": lambda p: p - 2 if produto == "lubrificante" else p,
        }

        return descontos.get(cupom, lambda p: p)(preco)

    @staticmethod
    def _arredondar_valor(preco: float, produto: str) -> float:
        """Arredonda o valor final conforme o tipo de produto."""
        match produto:
            case "diesel":
                return round(preco, 0)
            case "gasolina":
                return round(preco, 2)
            case _:
                return float(int(preco * 100) / 100.0)
