import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import helpdesk_mcp


class HelpdeskToolsTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test-helpdesk.db"
        patcher = patch.object(helpdesk_mcp, "DB_PATH", self.db_path)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.addCleanup(self.temp_dir.cleanup)
        helpdesk_mcp.initialize_database()

    def test_database_is_seeded_and_status_filter_works(self):
        tickets = helpdesk_mcp.listar_chamados()
        open_tickets = helpdesk_mcp.listar_chamados("aberto")

        self.assertEqual(len(tickets), 3)
        self.assertEqual([ticket["status"] for ticket in open_tickets], ["aberto"])

    def test_invalid_status_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Status invalido"):
            helpdesk_mcp.listar_chamados("pendente")

    def test_customer_history_includes_tickets_and_events(self):
        result = helpdesk_mcp.buscar_historico_cliente("cli-001")

        self.assertEqual(len(result["chamados"]), 2)
        self.assertEqual(len(result["historico"]), 3)
        self.assertEqual(
            [event["new_status"] for event in result["historico"]],
            ["aberto", "aberto", "resolvido"],
        )
        self.assertEqual(
            {event["ticket_id"] for event in result["historico"]},
            {ticket["id"] for ticket in result["chamados"]},
        )

    def test_customer_without_tickets_returns_empty_lists(self):
        result = helpdesk_mcp.buscar_historico_cliente("cli-003")

        self.assertEqual(result["cliente"]["id"], "cli-003")
        self.assertEqual(result["chamados"], [])
        self.assertEqual(result["historico"], [])

    def test_unknown_customer_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "nao encontrado"):
            helpdesk_mcp.buscar_historico_cliente("missing")

    def test_status_change_persists_and_records_history(self):
        result = helpdesk_mcp.atualizar_status(
            "HD-1001", "em_andamento", "Agente iniciou a analise."
        )

        self.assertTrue(result["alterado"])
        self.assertEqual(helpdesk_mcp.listar_chamados("em_andamento")[0]["id"], "HD-1001")
        history = helpdesk_mcp.buscar_historico_cliente("cli-001")["historico"]
        self.assertEqual(history[-1]["note"], "Agente iniciou a analise.")

    def test_repeating_status_does_not_add_history_event(self):
        before = len(helpdesk_mcp.buscar_historico_cliente("cli-001")["historico"])

        result = helpdesk_mcp.atualizar_status("HD-1001", "aberto")
        after = len(helpdesk_mcp.buscar_historico_cliente("cli-001")["historico"])

        self.assertFalse(result["alterado"])
        self.assertEqual(after, before)

    def test_unknown_ticket_and_status_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "nao encontrado"):
            helpdesk_mcp.atualizar_status("missing", "aberto")
        with self.assertRaisesRegex(ValueError, "Status invalido"):
            helpdesk_mcp.atualizar_status("HD-1001", "pendente")


if __name__ == "__main__":
    unittest.main()