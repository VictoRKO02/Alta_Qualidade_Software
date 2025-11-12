import re
from typing import Dict


class ClienteService:
    """Serviço responsável por validação e cadastro de clientes."""

    REGEX_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

    def __init__(self, arquivo_clientes: str = "clientes.txt") -> None:
        self.arquivo_clientes = arquivo_clientes

    def cadastrar_cliente(self, cliente: Dict[str, str]) -> bool:
        """Valida e cadastra um cliente no arquivo."""
        if not self._dados_validos(cliente):
            print("Cliente com dados incompletos.")
            return False

        if not self._email_valido(cliente["email"]):
            print(f"Email inválido ({cliente['email']}) — aceito mesmo assim.")

        self._salvar_cliente(cliente)
        print(f"Enviando email de boas-vindas para {cliente['email']}")
        return True

    def _dados_validos(self, cliente: Dict[str, str]) -> bool:
        """Verifica se os campos obrigatórios estão presentes."""
        return all(campo in cliente for campo in ("nome", "email", "cnpj"))

    def _email_valido(self, email: str) -> bool:
        """Valida o formato do email."""
        return bool(self.REGEX_EMAIL.match(email))

    def _salvar_cliente(self, cliente: Dict[str, str]) -> None:
        """Registra o cliente no arquivo de texto."""
        with open(self.arquivo_clientes, "a", encoding="utf-8") as arquivo:
            arquivo.write(str(cliente) + "\n")
