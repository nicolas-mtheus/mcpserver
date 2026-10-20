import unittest

from helpdesk_chat import parse_command


class ChatCommandTests(unittest.TestCase):
    def test_list_commands_map_to_list_tool(self):
        self.assertEqual(
            parse_command("Quais chamados estão abertos?"),
            ("listar_chamados", {"status": "aberto"}),
        )
        self.assertEqual(parse_command("listar chamados"), ("listar_chamados", {}))

    def test_history_command_extracts_client_id(self):
        self.assertEqual(
            parse_command("histórico do cliente cli-001"),
            ("buscar_historico_cliente", {"cliente_id": "cli-001"}),
        )

    def test_update_command_maps_numeric_ticket_and_status(self):
        self.assertEqual(
            parse_command("alterar chamado 3 para fechado"),
            (
                "atualizar_status",
                {
                    "chamado_id": "HD-1003",
                    "novo_status": "fechado",
                    "observacao": "Status atualizado pelo cliente Streamlit.",
                },
            ),
        )

    def test_update_command_accepts_full_ticket_id_and_note(self):
        self.assertEqual(
            parse_command(
                "atualizar chamado HD-1001 para em andamento observacao revisar acesso"
            ),
            (
                "atualizar_status",
                {
                    "chamado_id": "HD-1001",
                    "novo_status": "em_andamento",
                    "observacao": "revisar acesso",
                },
            ),
        )

    def test_unknown_command_is_rejected(self):
        self.assertIsNone(parse_command("faça algo inesperado"))


if __name__ == "__main__":
    unittest.main()