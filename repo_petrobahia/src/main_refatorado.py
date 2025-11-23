"""
Ponto de entrada principal para o processamento de pedidos e clientes
da PetroBahia. Orquestra os serviços e exibe o resultado final.
"""
# isort: organiza as importações em ordem alfabética e por tipo
from refatorado.cliente_service import ClienteService
from refatorado.pedido_service import PedidoService


def main():
    """Orquestra o cadastro de clientes e o processamento de pedidos."""
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

    # Processamento de Clientes
    for cliente in clientes:
        print("Registrando cliente...")
        if cliente_service.cadastrar_cliente(cliente):
            # O serviço já imprime o OK e o email
            pass
        else:
            print(f"Cliente com problema: {cliente}")

    # Processamento de Pedidos
    valores = [pedido_service.processar_pedido(pedido) for pedido in pedidos]

    print(f"TOTAL = {sum(valores):.2f}")
    print("==== Fim do processamento PetroBahia ====")


if __name__ == "__main__":
    main()
