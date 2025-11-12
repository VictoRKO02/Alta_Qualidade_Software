from refatorado.pedido_service import PedidoService
from refatorado.cliente_service import ClienteService


def main():
    pedidos = [
        {"cliente": "TransLog", "produto": "diesel", "qtd": 1200, "cupom": "MEGA10"},
        {"cliente": "MoveMais", "produto": "gasolina", "qtd": 300, "cupom": None},
        {"cliente": "EcoFrota", "produto": "etanol", "qtd": 50, "cupom": "NOVO5"},
        {"cliente": "PetroPark", "produto": "lubrificante", "qtd": 12, "cupom": "LUB2"},
    ]

    clientes = [
        {"nome": "Ana Paula", "email": "ana@@petrobahia", "cnpj": "123"},
        {"nome": "Carlos", "email": "carlos@petrobahia.com", "cnpj": "456"},
    ]

    print("==== Início do processamento PetroBahia ====")

    cliente_service = ClienteService()
    pedido_service = PedidoService()

    for cliente in clientes:
        if cliente_service.cadastrar_cliente(cliente):
            print(f"Cliente OK: {cliente['nome']}")
        else:
            print(f"Cliente com problema: {cliente}")

    valores = [pedido_service.processar_pedido(pedido) for pedido in pedidos]

    print(f"TOTAL = {sum(valores):.2f}")
    print("==== Fim do processamento PetroBahia ====")


if __name__ == "__main__":
    main()
