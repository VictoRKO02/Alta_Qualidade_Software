import unittest
from unittest.mock import mock_open, patch

from refatorado.cliente_service import ClienteService


class TestClienteService(unittest.TestCase):
    """Testes para a classe ClienteService."""

    def setUp(self):
        """Configura o serviço antes de cada teste."""
        # Configura o ClienteService para um arquivo de teste
        self.service = ClienteService(arquivo_clientes="clientes_test.txt")
        self.cliente_valido = {
            "nome": "Teste",
            "email": "teste@valido.com",
            "cnpj": "1234",
        }
        self.cliente_invalido_email = {
            "nome": "Teste",
            "email": "teste@@invalido",
            "cnpj": "1234",
        }
        self.cliente_incompleto = {"nome": "Teste", "cnpj": "1234"}

    # Testes de Validação de Dados
    def test_dados_validos_completo(self):
        """Deve retornar True se nome, email e cnpj estiverem presentes."""
        self.assertTrue(self.service._dados_validos(self.cliente_valido))

    def test_dados_validos_incompleto(self):
        """Deve retornar False se um campo obrigatório estiver faltando."""
        self.assertFalse(self.service._dados_validos(self.cliente_incompleto))

    # Testes de Validação de Email
    def test_email_valido(self):
        """Deve retornar True para emails com formato padrão."""
        self.assertTrue(self.service._email_valido("contato@empresa.com.br"))

    def test_email_invalido_sem_arroba(self):
        """Deve retornar False se faltar o @."""
        self.assertFalse(self.service._email_valido("contatoempresa.com"))

    def test_email_invalido_duplo_arroba(self):
        """Deve retornar False para emails com @@ (como no exemplo original)."""
        self.assertFalse(self.service._email_valido("usuario@@dominio.com"))

    # Testes de Cadastro de Cliente
    @patch("builtins.print")  # Mocka a função print para evitar poluir a saída
    @patch("refatorado.cliente_service.ClienteService._salvar_cliente")
    def test_cadastro_cliente_com_sucesso(self, mock_salvar, mock_print):
        """Deve cadastrar o cliente válido."""
        resultado = self.service.cadastrar_cliente(self.cliente_valido)
        self.assertTrue(resultado)
        mock_salvar.assert_called_once_with(self.cliente_valido)

    @patch("builtins.print")
    @patch("refatorado.cliente_service.ClienteService._salvar_cliente")
    def test_cadastro_cliente_incompleto_falha(self, mock_salvar, mock_print):
        """Não deve cadastrar cliente com dados faltando."""
        resultado = self.service.cadastrar_cliente(self.cliente_incompleto)
        self.assertFalse(resultado)
        mock_salvar.assert_not_called()

    @patch("builtins.print")
    @patch("refatorado.cliente_service.ClienteService._salvar_cliente")
    def test_cadastro_cliente_email_invalido_passa(self, mock_salvar, mock_print):
        """Deve cadastrar mesmo com email inválido (com aviso) - Lógica de negócio."""
        resultado = self.service.cadastrar_cliente(self.cliente_invalido_email)
        self.assertTrue(resultado)
        mock_salvar.assert_called_once_with(self.cliente_invalido_email)
        # Verifica se o aviso de email inválido foi impresso
        mock_print.assert_any_call(
            f"Email inválido ({self.cliente_invalido_email['email']}) — aceito mesmo assim."
        )

    # Teste de Salvamento de Arquivo
    @patch("builtins.open", new_callable=mock_open)
    def test_salvar_cliente_escreve_corretamente(self, mock_file):
        """Deve chamar a escrita no arquivo com o formato correto."""
        self.service._salvar_cliente(self.cliente_valido)

        # 1. Verifica se o arquivo foi aberto corretamente no modo 'a' (append) com encoding 'utf-8'
        mock_file.assert_called_once_with("clientes_test.txt", "a", encoding="utf-8")

        # 2. Verifica se a linha foi escrita corretamente (str(dict) + '\n')
        handle = mock_file()
        expected_content = str(self.cliente_valido) + "\n"
        handle.write.assert_called_once_with(expected_content)
