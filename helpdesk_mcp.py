"""Local MCP helpdesk backed by a demonstrative SQLite database."""

from __future__ import annotations

import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastmcp import FastMCP


STATUSES = ("aberto", "em_andamento", "resolvido", "fechado")
DB_PATH = Path(
    os.environ.get("HELPDESK_DB_PATH", Path(__file__).with_name("helpdesk.db"))
)
mcp = FastMCP("Helpdesk MCP")


def _connect(db_path: Path | None = None) -> sqlite3.Connection:
    path = db_path or DB_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database(db_path: Path | None = None) -> None:
    """Create the schema and seed fictitious records when the database is empty."""
    with _connect(db_path) as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS clients (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            );
            CREATE TABLE IF NOT EXISTS tickets (
                id TEXT PRIMARY KEY,
                client_id TEXT NOT NULL REFERENCES clients(id),
                subject TEXT NOT NULL,
                description TEXT NOT NULL,
                status TEXT NOT NULL CHECK (status IN (
                    'aberto', 'em_andamento', 'resolvido', 'fechado'
                )),
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS ticket_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id TEXT NOT NULL REFERENCES tickets(id),
                old_status TEXT,
                new_status TEXT NOT NULL,
                note TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            """
        )
        if connection.execute("SELECT COUNT(*) FROM tickets").fetchone()[0] == 0:
            now = datetime.now(timezone.utc).isoformat()
            connection.executemany(
                "INSERT OR IGNORE INTO clients (id, name, email) VALUES (?, ?, ?)",
                [
                    ("cli-001", "Ana Souza", "ana@example.test"),
                    ("cli-002", "Bruno Lima", "bruno@example.test"),
                    ("cli-003", "Carla Mendes", "carla@example.test"),
                ],
            )
            connection.executemany(
                """INSERT OR IGNORE INTO tickets
                (id, client_id, subject, description, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)""",
                [
                    (
                        "HD-1001", "cli-001", "Acesso bloqueado",
                        "Cliente nao consegue acessar a conta.", "aberto", now, now,
                    ),
                    (
                        "HD-1002", "cli-001", "Atualizacao de cadastro",
                        "Solicitada correcao do telefone de contato.",
                        "resolvido", now, now,
                    ),
                    (
                        "HD-1003", "cli-002", "Erro no relatorio",
                        "Relatorio mensal apresenta dados incompletos.",
                        "em_andamento", now, now,
                    ),
                ],
            )
            connection.executemany(
                """INSERT INTO ticket_history
                (ticket_id, old_status, new_status, note, created_at)
                VALUES (?, ?, ?, ?, ?)""",
                [
                    ("HD-1001", None, "aberto", "Chamado criado.", now),
                    ("HD-1002", None, "aberto", "Chamado criado.", now),
                    ("HD-1002", "aberto", "resolvido", "Cadastro corrigido.", now),
                    ("HD-1003", None, "aberto", "Chamado criado.", now),
                    ("HD-1003", "aberto", "em_andamento", "Analise iniciada.", now),
                ],
            )


def listar_chamados(status: str | None = None) -> list[dict[str, Any]]:
    """List all tickets, optionally filtering by a valid status."""
    if status is not None and status not in STATUSES:
        raise ValueError(f"Status invalido. Use um destes: {', '.join(STATUSES)}.")

    query = """SELECT t.id, t.client_id, c.name AS client_name, t.subject,
               t.description, t.status, t.created_at, t.updated_at
               FROM tickets AS t JOIN clients AS c ON c.id = t.client_id"""
    parameters: tuple[str, ...] = ()
    if status:
        query += " WHERE t.status = ?"
        parameters = (status,)
    query += " ORDER BY t.created_at, t.id"

    with _connect() as connection:
        rows = connection.execute(query, parameters).fetchall()
    return [dict(row) for row in rows]


def buscar_historico_cliente(cliente_id: str) -> dict[str, Any]:
    """Return a client's details, tickets, and chronological ticket history."""
    with _connect() as connection:
        client = connection.execute(
            "SELECT id, name, email FROM clients WHERE id = ?", (cliente_id,)
        ).fetchone()
        if client is None:
            raise ValueError(f"Cliente '{cliente_id}' nao encontrado.")

        tickets = connection.execute(
            """SELECT id, subject, description, status, created_at, updated_at
               FROM tickets WHERE client_id = ? ORDER BY created_at, id""",
            (cliente_id,),
        ).fetchall()
        history = connection.execute(
            """SELECT h.ticket_id, t.subject, h.old_status, h.new_status,
                      h.note, h.created_at
               FROM ticket_history AS h
               JOIN tickets AS t ON t.id = h.ticket_id
               WHERE t.client_id = ?
               ORDER BY h.created_at, h.id""",
            (cliente_id,),
        ).fetchall()
    return {
        "cliente": dict(client),
        "chamados": [dict(row) for row in tickets],
        "historico": [dict(row) for row in history],
    }


def atualizar_status(
    chamado_id: str, novo_status: str, observacao: str = "Status atualizado."
) -> dict[str, Any]:
    """Change a ticket's status and append a history event atomically."""
    if novo_status not in STATUSES:
        raise ValueError(f"Status invalido. Use um destes: {', '.join(STATUSES)}.")

    with _connect() as connection:
        ticket = connection.execute(
            "SELECT status FROM tickets WHERE id = ?", (chamado_id,)
        ).fetchone()
        if ticket is None:
            raise ValueError(f"Chamado '{chamado_id}' nao encontrado.")

        status_anterior = ticket["status"]
        if status_anterior == novo_status:
            return {
                "chamado_id": chamado_id,
                "status_anterior": status_anterior,
                "status_atual": novo_status,
                "alterado": False,
            }

        now = datetime.now(timezone.utc).isoformat()
        connection.execute(
            "UPDATE tickets SET status = ?, updated_at = ? WHERE id = ?",
            (novo_status, now, chamado_id),
        )
        connection.execute(
            """INSERT INTO ticket_history
               (ticket_id, old_status, new_status, note, created_at)
               VALUES (?, ?, ?, ?, ?)""",
            (chamado_id, status_anterior, novo_status, observacao, now),
        )
    return {
        "chamado_id": chamado_id,
        "status_anterior": status_anterior,
        "status_atual": novo_status,
        "alterado": True,
    }


mcp.tool()(listar_chamados)
mcp.tool()(buscar_historico_cliente)
mcp.tool()(atualizar_status)


if __name__ == "__main__":
    initialize_database()
    mcp.run(transport="stdio", show_banner=False)