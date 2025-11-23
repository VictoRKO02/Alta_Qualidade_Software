"""Módulo de serviço para gerenciamento e cadastro de clientes."""
import re
from typing import Dict


# pylint: disable=R0903
class ClienteService:
    """
    Serviço responsável por validação e cadastro de clientes,
    seguindo o Princípio da Responsabilidade Única (SRP).
    """

    # Pylint: o 'r' no início da string de regex garante que a string é tratada como raw (bruta).
    REGEX_EMAIL = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")

    def __init__(self, arquivo_clientes: str = "clientes.txt") -> None:
        self.arquivo_clientes = arquivo_clientes

    def cadastrar_cliente(self, cliente: Dict[str, str]) -> bool:
        """Valida e cadastra um cliente no arquivo, e simula envio de email."""
        if not self._dados_validos(cliente):
            print("Cliente com dados incompletos. Cadastro não realizado.")
            return False

        if not self._email_valido(cliente["email"]):
            # Lógica de negócio: aceitar email inválido com aviso
            print(f"Email inválido ({cliente['email']}) — aceito mesmo assim.")

        self._salvar_cliente(cliente)
        print(f"Enviando email de boas-vindas para {cliente['email']}")
        return True

    def _dados_validos(self, cliente: Dict[str, str]) -> bool:
        """Verifica se os campos obrigatórios ('nome', 'email', 'cnpj') estão presentes."""
        return all(campo in cliente for campo in ("nome", "email", "cnpj"))

    def _email_valido(self, email: str) -> bool:
        """Valida o formato básico do email (usa regex para garantir um '@' e um '.')."""
        return bool(self.REGEX_EMAIL.match(email))

    def _salvar_cliente(self, cliente: Dict[str, str]) -> None:
        """Registra o cliente no arquivo de texto 'clientes.txt' no modo append."""
        with open(self.arquivo_clientes, "a", encoding="utf-8") as arquivo:
            arquivo.write(str(cliente) + "\n")