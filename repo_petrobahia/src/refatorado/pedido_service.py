"""Módulo de serviço para processamento de pedidos e aplicação de regras de negócio."""
from typing import Dict, Optional, Union

from refatorado.preco_calculadora import PrecoCalculadora


# pylint: disable=R0903
class PedidoService:
    """
    Serviço responsável pela orquestração do pedido, aplicação de
    cupons e regras de arredondamento.
    """

    def __init__(self) -> None:
        self.calculadora = PrecoCalculadora()

    def processar_pedido(self, pedido: Dict[str, Union[str, int, None]]) -> float:
        """
        Processa o pedido (calcula preço base + descontos de cupom + arredondamento)
        e retorna o valor final.
        """
        produto = pedido.get("produto")
        quantidade = pedido.get("qtd", 0)
        cupom = pedido.get("cupom")
        cliente_nome = pedido.get("cliente")

        if not produto or quantidade <= 0:
            # O cliente_nome pode ser None/Opcional no pedido.
            log_cliente = f"de {cliente_nome}" if cliente_nome else ""
            print(f"[ERRO] Pedido inválido {log_cliente}: quantidade 0 ou produto ausente.")
            return 0.0

        # 1. Preço com descontos de quantidade
        preco = self.calculadora.calcular_preco(produto, quantidade)

        # 2. Aplicação de cupom
        preco = self._aplicar_cupom(preco, cupom, produto)

        # 3. Arredondamento final
        preco = self._arredondar_valor(preco, produto)

        print(f"Pedido OK: {cliente_nome} | {produto} x{quantidade} => R${preco:.2f}")
        return preco

    @staticmethod
    def _aplicar_cupom(preco: float, cupom: Optional[str], produto: str) -> float:
        """
        Aplica descontos de cupom percentuais ou fixos, se o cupom for conhecido.
        """
        if not cupom:
            return preco

        descontos = {
            "MEGA10": lambda p: p * 0.9,
            "NOVO5": lambda p: p * 0.95,
            # LUB2 é um desconto fixo de 2.00, mas SÓ para lubrificante
            "LUB2": lambda p: p - 2.0 if produto == "lubrificante" else p,
        }

        # Retorna a função de desconto do dicionário, ou uma função que retorna o preço
        # original se o cupom não for encontrado.
        return descontos.get(cupom, lambda p: p)(preco)

    @staticmethod
    def _arredondar_valor(preco: float, produto: str) -> float:
        """
        Arredonda o valor final conforme o tipo de produto, aplicando regras específicas.
        """
        match produto:
            case "diesel":
                return round(preco, 0)
            case "gasolina":
                return round(preco, 2)
            case _:
                # Implementação de truncamento:
                # Multiplica por 100, pega a parte inteira, e divide por 100
                return float(int(preco * 100) / 100.0)